# Guia de Configuração Docker

Este documento descreve como usar os arquivos Docker Compose criados para o sistema de gerenciamento de clientes.

## Estrutura de Arquivos

### Arquivos Individuais por Módulo

#### Backend
- `backend/docker-compose.yml` - Desenvolvimento com hot reload
- `backend/docker-compose.debug.yml` - Debug com portas de debugging expostas
- `backend/docker-compose.prod.yml` - Produção otimizada

#### Frontend
- `frontend/docker-compose.yml` - Desenvolvimento com hot reload
- `frontend/docker-compose.debug.yml` - Debug com portas de debugging expostas
- `frontend/docker-compose.prod.yml` - Produção otimizada com nginx

### Arquivos Unificados (Root)
- `docker-compose.yml` - Desenvolvimento completo (backend + frontend)
- `docker-compose.debug.yml` - Debug completo com portas de debugging
- `docker-compose.prod.yml` - Produção completa otimizada

## Como Usar

### Desenvolvimento Local (Ambos os módulos)
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

### Desenvolvimento Individual

#### Backend apenas
```bash
cd backend
docker-compose up -d
```

#### Frontend apenas
```bash
cd frontend
docker-compose up -d
```

### Debug Mode
```bash
# Debug completo (backend + frontend)
docker-compose -f docker-compose.debug.yml up -d

# Debug backend apenas
cd backend
docker-compose -f docker-compose.debug.yml up -d

# Debug frontend apenas
cd frontend
docker-compose -f docker-compose.debug.yml up -d
```

### Produção
```bash
# Produção completa
docker-compose -f docker-compose.prod.yml up -d

# Produção backend apenas
cd backend
docker-compose -f docker-compose.prod.yml up -d

# Produção frontend apenas
cd frontend
docker-compose -f docker-compose.prod.yml up -d
```

## Portas Utilizadas

### Desenvolvimento
- **Backend API**: 8000
- **Frontend**: 3000
- **PostgreSQL**: 5432
- **Redis**: 6379

### Debug
- **Backend API**: 8000
- **Backend Debug**: 5678 (Python debug)
- **Frontend**: 3000
- **Frontend Debug**: 9229 (Node.js debug)
- **PostgreSQL**: 5432
- **Redis**: 6379

### Produção
- **Backend API**: 8000
- **Frontend**: 80 (nginx)
- **PostgreSQL**: 5432 (não exposta externamente)
- **Redis**: 6379 (não exposta externamente)

## Configuração de Variáveis de Ambiente

### Backend (.env.prod)
- Configure `POSTGRES_PASSWORD` com uma senha segura
- Configure `SECRET_KEY` com uma chave secreta de pelo menos 32 caracteres

### Frontend (.env.prod)
- Configure `REACT_APP_API_URL` com a URL correta da API em produção

## Comandos Úteis

### Limpar todos os dados
```bash
# Desenvolvimento
docker-compose down -v

# Produção
docker-compose -f docker-compose.prod.yml down -v
```

### Rebuild sem cache
```bash
docker-compose build --no-cache
```

### Ver status dos serviços
```bash
docker-compose ps
```

### Executar comandos dentro dos containers
```bash
# Backend
docker-compose exec api python -m src.main

# Frontend
docker-compose exec frontend npm install
```

## Health Checks

Todos os serviços possuem health checks configurados:
- **PostgreSQL**: Verifica se o banco está respondendo
- **Redis**: Verifica se o cache está disponível
- **API**: Verifica se a API está respondendo
- **Frontend**: Verifica se o nginx está respondendo

## Segurança em Produção

1. **Senhas**: Sempre altere as senhas padrão em `.env.prod`
2. **Portas**: Em produção, PostgreSQL e Redis não são expostos externamente
3. **SSL**: Configure SSL/TLS no nginx para produção
4. **Firewall**: Configure firewall para permitir apenas portas necessárias
5. **Logs**: Monitore logs regularmente

## Troubleshooting

### Problemas comuns

1. **Portas já em uso**: Altere as portas no arquivo docker-compose correspondente
2. **Permissões**: Em Linux/macOS, use `sudo` se necessário
3. **Docker não encontrado**: Certifique-se de que Docker e Docker Compose estão instalados
4. **Build falhando**: Execute `docker-compose build --no-cache`

### Debug Python
Para debugar o backend Python, conecte-se à porta 5678 com seu IDE de preferência.

### Debug Node.js
Para debugar o frontend React, conecte-se à porta 9229 com seu navegador ou IDE.
