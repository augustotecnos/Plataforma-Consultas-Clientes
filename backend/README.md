# Customer Management System - Backend

FastAPI-based backend for the Customer Management System with PostgreSQL and Redis.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access
- **Customer Management**: Full CRUD operations for customer data
- **Advanced Search**: Multi-field search with Redis caching
- **Data Export**: Excel, PDF, and CSV export capabilities
- **Performance**: Redis caching for frequently accessed data
- **Security**: Input validation, CPF validation, and secure password handling

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Cache**: Redis 7
- **Authentication**: JWT tokens with bcrypt
- **Validation**: Pydantic models
- **Export**: pandas, openpyxl, reportlab

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and setup**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start services**:
   ```bash
   # Using Docker Compose (recommended)
   docker-compose up -d

   # Or manually start PostgreSQL and Redis
   ```

4. **Run the application**:
   ```bash
   python -m src.main
   ```

### Docker Development

1. **Start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/login-json` - Login (JSON payload)
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

### Clients
- `GET /api/v1/clients/search` - Search clients with filters
- `GET /api/v1/clients/{client_id}` - Get client details
- `POST /api/v1/clients/` - Create new client
- `PUT /api/v1/clients/{client_id}` - Update client
- `DELETE /api/v1/clients/{client_id}` - Soft delete client

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_SERVER` | PostgreSQL host | localhost |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `POSTGRES_DB` | Database name | customer_db |
| `REDIS_HOST` | Redis host | localhost |
| `REDIS_PORT` | Redis port | 6379 |
| `SECRET_KEY` | JWT secret key | (required) |
| `DEBUG` | Debug mode | False |

## Database Schema

### Clients Table
- `id_cliente` (Primary Key)
- `cpf` (Unique, indexed)
- `nome_completo` (Indexed)
- `data_nascimento`
- `sexo`
- `nome_mae`
- `nome_pai`
- `email`
- `telefone`
- `celular`
- `cep`
- `endereco`
- `numero`
- `complemento`
- `bairro`
- `cidade` (Indexed)
- `uf`
- `ativo`
- `created_at`
- `updated_at`

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `hashed_password`
- `full_name`
- `is_active`
- `is_admin`
- `created_at`
- `updated_at`

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Performance Features

- **Redis Caching**: Automatic caching of search results and individual clients
- **Pagination**: Configurable page sizes (default: 50, max: 100)
- **Database Indexes**: Optimized for common search fields
- **Async Operations**: Full async support for better performance

## Security Features

- **JWT Authentication**: Stateless authentication with configurable expiration
- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Pydantic models with custom validators
- **CPF Validation**: Brazilian CPF format and check digit validation
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## Development

### Adding New Features

1. Create models in `src/api/models/`
2. Create schemas in `src/api/schemas/`
3. Create services in `src/api/services/`
4. Create routes in `src/api/routes/`
5. Update main.py to include new routes

### Database Migrations

For production, use Alembic:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### Common Issues

1. **Database connection failed**:
   - Check PostgreSQL is running
   - Verify credentials in .env
   - Check firewall settings

2. **Redis connection failed**:
   - Check Redis is running
   - Verify host/port in .env
   - Check Redis logs

3. **Import errors**:
   - Ensure all dependencies installed
   - Check Python path
   - Verify virtual environment

### Logs

- Application logs: Check console output
- Database logs: Check PostgreSQL logs
- Redis logs: Check Redis logs

## License

MIT License
