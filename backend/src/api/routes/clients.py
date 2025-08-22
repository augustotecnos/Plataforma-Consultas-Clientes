from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import Optional, List
from src.api.models.client import Client
from src.api.schemas.client_schemas import (
    ClientCreate, 
    ClientUpdate, 
    ClientResponse, 
    ClientSearchFilters,
    PaginatedResponse
)
from src.api.services.cache_service import cache_service
from src.api.services.export_service import ExportService
from src.utils.database import get_db
from src.core.config import settings
from src.api.routes.auth import get_current_user
from src.api.models.client import User
from pydantic import BaseModel
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/clients", tags=["clients"])

class ExportRequest(BaseModel):
    format: str
    filters: dict = {}

@router.get("/search", response_model=PaginatedResponse)
async def search_clients(
    cpf: Optional[str] = Query(None, description="CPF do cliente"),
    nome: Optional[str] = Query(None, description="Nome ou parte do nome"),
    cidade: Optional[str] = Query(None, description="Cidade"),
    uf: Optional[str] = Query(None, description="UF (estado)"),
    ativo: Optional[bool] = Query(None, description="Status do cliente"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Tamanho da página"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Pesquisa clientes com múltiplos filtros"""
    
    # Generate cache key
    cache_key = cache_service.generate_search_key(
        cpf=cpf,
        nome=nome,
        cidade=cidade,
        uf=uf,
        ativo=ativo,
        page=page,
        size=size
    )
    
    # Try to get from cache
    cached_result = await cache_service.get(cache_key)
    if cached_result:
        return PaginatedResponse(**cached_result)
    
    # Build query
    query = select(Client)
    conditions = []
    
    if cpf:
        # Remove formatting for search
        cpf_clean = cpf.replace('.', '').replace('-', '')
        conditions.append(Client.cpf.contains(cpf_clean))
    
    if nome:
        conditions.append(Client.nome_completo.ilike(f"%{nome}%"))
    
    if cidade:
        conditions.append(Client.cidade.ilike(f"%{cidade}%"))
    
    if uf:
        conditions.append(Client.uf == uf.upper())
    
    if ativo is not None:
        conditions.append(Client.ativo == ativo)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Get total count
    count_query = select(func.count(Client.id_cliente))
    if conditions:
        count_query = count_query.where(and_(*conditions))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Calculate pagination
    offset = (page - 1) * size
    pages = (total + size - 1) // size
    
    # Get paginated results
    query = query.offset(offset).limit(size)
    result = await db.execute(query)
    clients = result.scalars().all()
    
    # Convert to response format
    items = [ClientResponse.from_orm(client) for client in clients]
    
    response_data = {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }
    
    # Cache the result
    await cache_service.set(cache_key, response_data, settings.SEARCH_CACHE_TTL)
    
    return PaginatedResponse(**response_data)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_details(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna detalhes completos do cliente"""
    
    # Try to get from cache
    cached_client = await cache_service.get_client(client_id)
    if cached_client:
        return ClientResponse(**cached_client)
    
    # Get from database
    result = await db.execute(select(Client).where(Client.id_cliente == client_id))
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Cache the result
    client_data = ClientResponse.from_orm(client).dict()
    await cache_service.set_client(client_id, client_data)
    
    return ClientResponse(**client_data)

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo cliente"""
    
    # Check if CPF already exists
    result = await db.execute(select(Client).where(Client.cpf == client_data.cpf))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF already registered"
        )
    
    # Create new client
    db_client = Client(**client_data.dict())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    
    # Invalidate search cache
    await cache_service.invalidate_search_cache()
    
    return ClientResponse.from_orm(db_client)

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza um cliente existente"""
    
    result = await db.execute(select(Client).where(Client.id_cliente == client_id))
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Update fields
    update_data = client_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    await db.commit()
    await db.refresh(client)
    
    # Invalidate caches
    await cache_service.invalidate_client(client_id)
    await cache_service.invalidate_search_cache()
    
    return ClientResponse.from_orm(client)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove um cliente (soft delete)"""
    
    result = await db.execute(select(Client).where(Client.id_cliente == client_id))
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    client.ativo = False
    await db.commit()
    
    # Invalidate caches
    await cache_service.invalidate_client(client_id)
    await cache_service.invalidate_search_cache()

@router.post("/export")
async def export_clients(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Exporta lista de clientes no formato especificado"""
    
    export_service = ExportService()
    
    # Build query based on filters
    query = select(Client)
    conditions = []
    
    filters = request.filters
    
    if filters.get('id_cliente'):
        conditions.append(Client.id_cliente == filters['id_cliente'])
    
    if filters.get('cpf'):
        cpf_clean = filters['cpf'].replace('.', '').replace('-', '')
        conditions.append(Client.cpf.contains(cpf_clean))
    
    if filters.get('nome'):
        conditions.append(Client.nome_completo.ilike(f"%{filters['nome']}%"))
    
    if filters.get('cidade'):
        conditions.append(Client.cidade.ilike(f"%{filters['cidade']}%"))
    
    if filters.get('uf'):
        conditions.append(Client.uf == filters['uf'].upper())
    
    if filters.get('ativo') is not None:
        conditions.append(Client.ativo == filters['ativo'])
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Get all matching clients
    result = await db.execute(query)
    clients = result.scalars().all()
    
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No clients found for export"
        )
    
    # Convert to response format
    client_data = [ClientResponse.from_orm(client).dict() for client in clients]
    
    # Generate export based on format
    if request.format.lower() == 'excel':
        file_content = export_service.export_to_excel(client_data)
        filename = "clientes_export.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif request.format.lower() == 'csv':
        file_content = export_service.export_to_csv(client_data)
        filename = "clientes_export.csv"
        media_type = "text/csv"
    elif request.format.lower() == 'pdf':
        file_content = export_service.export_to_pdf(client_data)
        filename = "clientes_export.pdf"
        media_type = "application/pdf"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid export format. Use 'excel', 'csv', or 'pdf'"
        )
    
    return StreamingResponse(
        BytesIO(file_content),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
