from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime
from src.core.security import validate_cpf, format_cpf

class ClientBase(BaseModel):
    cpf: str = Field(..., description="CPF do cliente")
    nome_completo: str = Field(..., min_length=3, max_length=255, description="Nome completo do cliente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    sexo: Optional[str] = Field(None, regex="^[MF]$", description="Sexo (M/F)")
    nome_mae: Optional[str] = Field(None, max_length=255, description="Nome da mãe")
    nome_pai: Optional[str] = Field(None, max_length=255, description="Nome do pai")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone fixo")
    celular: Optional[str] = Field(None, max_length=20, description="Celular")
    cep: Optional[str] = Field(None, max_length=9, description="CEP")
    endereco: Optional[str] = Field(None, max_length=255, description="Endereço")
    numero: Optional[str] = Field(None, max_length=10, description="Número")
    complemento: Optional[str] = Field(None, max_length=255, description="Complemento")
    bairro: Optional[str] = Field(None, max_length=100, description="Bairro")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")
    uf: Optional[str] = Field(None, regex="^[A-Z]{2}$", description="UF (estado)")
    ativo: bool = Field(True, description="Status do cliente")
    
    @validator('cpf')
    def validate_cpf_format(cls, v):
        if not validate_cpf(v):
            raise ValueError('CPF inválido')
        return format_cpf(v)
    
    @validator('uf')
    def uppercase_uf(cls, v):
        return v.upper() if v else v

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=255)
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = Field(None, regex="^[MF]$")
    nome_mae: Optional[str] = Field(None, max_length=255)
    nome_pai: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    cep: Optional[str] = Field(None, max_length=9)
    endereco: Optional[str] = Field(None, max_length=255)
    numero: Optional[str] = Field(None, max_length=10)
    complemento: Optional[str] = Field(None, max_length=255)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    uf: Optional[str] = Field(None, regex="^[A-Z]{2}$")
    ativo: Optional[bool] = None
    
    @validator('uf')
    def uppercase_uf(cls, v):
        return v.upper() if v else v

class ClientResponse(ClientBase):
    id_cliente: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ClientSearchFilters(BaseModel):
    cpf: Optional[str] = Field(None, description="CPF do cliente")
    nome: Optional[str] = Field(None, description="Nome ou parte do nome")
    cidade: Optional[str] = Field(None, description="Cidade")
    uf: Optional[str] = Field(None, description="UF (estado)")
    ativo: Optional[bool] = Field(None, description="Status do cliente")
    
    @validator('cpf')
    def format_cpf(cls, v):
        return v.replace('.', '').replace('-', '') if v else v
    
    @validator('uf')
    def uppercase_uf(cls, v):
        return v.upper() if v else v

class PaginatedResponse(BaseModel):
    items: List[ClientResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True

class ExportFormat(BaseModel):
    format: str = Field(..., regex="^(excel|pdf|csv)$", description="Formato de exportação")
    filters: ClientSearchFilters = Field(..., description="Filtros para exportação")
    fields: Optional[List[str]] = Field(None, description="Campos específicos para exportar")
