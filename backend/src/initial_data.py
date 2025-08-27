import asyncio
import os
from sqlalchemy.future import select
from src.core.config import settings
from src.core.security import get_password_hash
from src.api.models.client import User, Base
from src.utils.database import engine, AsyncSessionLocal

async def create_initial_user():
    """
    Cria o usuário administrador inicial se ele não existir.
    """
    # Adiciona uma pequena espera para garantir que o DB esteja pronto
    await asyncio.sleep(5)
    
    async with engine.begin() as conn:
        # Cria todas as tabelas (se não existirem)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        admin_email = settings.ADMIN_EMAIL
        result = await session.execute(select(User).filter(User.email == admin_email))
        user = result.scalars().first()

        if not user:
            print("Criando usuário administrador inicial...")
            admin_password = settings.ADMIN_PASSWORD
            hashed_password = get_password_hash(admin_password)
            
            admin_user = User(
                email=admin_email,
                hashed_password=hashed_password,
                full_name="Admin",
                is_active=True,
                is_admin=True
            )
            session.add(admin_user)
            await session.commit()
            print("Usuário administrador criado com sucesso.")
        else:
            print("Usuário administrador já existe.")

async def main():
    """
    Função principal para executar a inicialização.
    """
    print("Iniciando a verificação de dados iniciais...")
    await create_initial_user()
    print("Verificação de dados iniciais concluída.")

if __name__ == "__main__":
    asyncio.run(main())
