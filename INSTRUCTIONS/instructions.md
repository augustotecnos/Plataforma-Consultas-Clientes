# PRD - Sistema de Gestão de Clientes

## 1. Visão Geral \& Propósito

**Objetivo**: Desenvolver um sistema completo de gestão de clientes com funcionalidades de pesquisa, visualização e exportação de dados, utilizando arquitetura distribuída com PostgreSQL como banco principal e Redis para otimização de consultas.

**Escopo**:

- Interface web responsiva para gestão de clientes
- APIs RESTful em Python para operações CRUD
- Sistema de autenticação e autorização
- Funcionalidades de pesquisa avançada e exportação
- Arquitetura distribuída para alta performance


## 2. Objetivos \& Métricas de Sucesso (KPIs)

| Objetivo | Indicador (KPI) | Meta (MVP) |
| :-- | :-- | :-- |
| Performance de consulta | Tempo de resposta de pesquisa | ≤ 300 ms |
| Disponibilidade do sistema | Uptime | ≥ 99,9% mensal |
| Facilidade de uso | Taxa de sucesso em pesquisas | ≥ 95% |
| Capacidade de exportação | Tempo de geração de relatórios | ≤ 5 s para até 10k registros |

## 3. Stakeholders \& Personas

| Stakeholder | Papel | Engajamento |
| :-- | :-- | :-- |
| Usuários Operacionais | Consultam e gerenciam dados de clientes | Daily users |
| Administradores | Gerenciam usuários e configurações do sistema | Weekly review |
| Gerentes | Analisam relatórios e métricas | Monthly reports |
| Equipe de TI | Mantém infraestrutura e realiza deploys | On-demand |

**Persona Principal**: Maria, Analista de Atendimento

- **Objetivos**: Encontrar rapidamente informações de clientes, gerar relatórios para análise
- **Dores**: Sistemas lentos, dificuldade para encontrar dados específicos
- **Necessidades**: Interface intuitiva, pesquisa rápida, exportação fácil


## 4. Requisitos Funcionais (RF)

| ID | Descrição |
| :-- | :-- |
| RF-001 | O sistema deve permitir autenticação via email e senha |
| RF-002 | O sistema deve exibir tela inicial com cards de navegação para diferentes funcionalidades |
| RF-003 | O sistema deve permitir pesquisa de clientes por CPF, nome, cidade e outros campos |
| RF-004 | O sistema deve exibir resultados de pesquisa organizados por categorias |
| RF-005 | O sistema deve permitir exportação de resultados em Excel, PDF e CSV |
| RF-006 | O sistema deve utilizar Redis para cache de consultas frequentes |
| RF-007 | O sistema deve sincronizar dados entre PostgreSQL e Redis automaticamente |
| RF-008 | O sistema deve permitir visualização detalhada de perfil do cliente |
| RF-009 | O sistema deve registrar logs de auditoria para todas as operações |
| RF-010 | O sistema deve suportar paginação de resultados |

## 5. Requisitos Não Funcionais (NFR)

| ID | Categoria | Descrição |
| :-- | :-- | :-- |
| NFR-001 | Performance | Consultas no Redis devem responder em ≤ 50 ms |
| NFR-002 | Escalabilidade | Sistema deve suportar até 1000 usuários simultâneos |
| NFR-003 | Segurança | Todas as comunicações devem usar HTTPS/TLS 1.2+ |
| NFR-004 | Confiabilidade | Sincronização PostgreSQL-Redis deve ter 99,9% de consistência |
| NFR-005 | Usabilidade | Interface deve ser responsiva para dispositivos mobile |
| NFR-006 | Manutenibilidade | Código Python deve seguir PEP 8 e ter cobertura de testes ≥ 80% |

## 6. Arquitetura do Sistema

### 6.1 Stack Tecnológica

**Back-end (Python)**:

- Framework: FastAPI ou Django REST Framework
- ORM: SQLAlchemy ou Django ORM
- Cache: Redis-py
- Autenticação: JWT + bcrypt
- Exportação: pandas + openpyxl/reportlab
- Validação: Pydantic

**Banco de Dados**:

- Principal: PostgreSQL 13+
- Cache: Redis 6+
- Sincronização: Celery + Redis broker

**Front-end**:

- Framework: React.js ou Vue.js
- UI Components: Material-UI ou Ant Design
- Estado: Redux ou Vuex
- HTTP Client: Axios


### 6.2 Estrutura de Módulos Python

```
src/
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── clients.py
│   │   └── reports.py
│   ├── models/
│   │   ├── client.py
│   │   ├── user.py
│   │   └── audit.py
│   ├── services/
│   │   ├── client_service.py
│   │   ├── search_service.py
│   │   ├── export_service.py
│   │   └── cache_service.py
│   ├── schemas/
│   │   ├── client_schemas.py
│   │   └── response_schemas.py
│   └── utils/
│       ├── database.py
│       ├── redis_client.py
│       └── validators.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── exceptions.py
├── tasks/
│   ├── sync_tasks.py
│   └── export_tasks.py
└── main.py
```


## 7. Especificações Técnicas

### 7.1 Modelo de Dados Principal

```python
# models/client.py
from sqlalchemy import Column, String, Integer, Date, Boolean, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True)
    cpf = Column(String(14), unique=True, nullable=False)
    nome_completo = Column(String(255), nullable=False)
    data_nascimento = Column(Date)
    sexo = Column(String(1))
    nome_mae = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Boolean, default=True)
```


### 7.2 API Endpoints Principais

```python
# routes/clients.py
from fastapi import APIRouter, Depends, Query
from typing import Optional, List

router = APIRouter(prefix="/api/v1/clients")

@router.get("/search")
async def search_clients(
    cpf: Optional[str] = Query(None),
    nome: Optional[str] = Query(None),
    cidade: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100)
):
    """Pesquisa clientes com múltiplos filtros"""
    pass

@router.get("/{client_id}")
async def get_client_details(client_id: int):
    """Retorna detalhes completos do cliente"""
    pass

@router.post("/export")
async def export_clients(
    format: str = Query(..., regex="^(excel|pdf|csv)$"),
    filters: dict = Body(...)
):
    """Exporta lista de clientes no formato especificado"""
    pass
```


### 7.3 Serviço de Cache Redis

```python
# services/cache_service.py
import redis
import json
from typing import Optional, Any

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    async def get_client_cache(self, cache_key: str) -> Optional[dict]:
        """Busca cliente no cache Redis"""
        cached_data = self.redis_client.get(cache_key)
        return json.loads(cached_data) if cached_data else None
    
    async def set_client_cache(self, cache_key: str, data: dict, ttl: int = 3600):
        """Armazena cliente no cache Redis"""
        self.redis_client.setex(
            cache_key, 
            ttl, 
            json.dumps(data, ensure_ascii=False)
        )
    
    def generate_search_key(self, **filters) -> str:
        """Gera chave única para consulta de pesquisa"""
        filter_str = "_".join([f"{k}:{v}" for k, v in sorted(filters.items()) if v])
        return f"search:{hash(filter_str)}"
```


## 8. Funcionalidades Detalhadas

### 8.1 Tela de Login

- **Campos**: Email, Senha
- **Validações**: Email formato válido, senha mínimo 8 caracteres
- **Segurança**: Hash bcrypt, limitação de tentativas
- **Token**: JWT com expiração de 24 horas


### 8.2 Tela Inicial (Dashboard)

- **Cards de Navegação**:
    - 🔍 Pesquisar Clientes
    - 📊 Relatórios
    - 👥 Gestão de Usuários (admin)
    - ⚙️ Configurações
- **Rodapé**: Versão do sistema, informações de contato
- **Header**: Logo, nome do usuário, logout


### 8.3 Tela de Pesquisa

- **Filtros Disponíveis**:
    - CPF (com máscara)
    - Nome completo (busca parcial)
    - Cidade/UF
    - Faixa etária
    - Status do cliente
- **Resultados**:
    - Tabela paginada
    - Ordenação por colunas
    - Preview de dados essenciais
    - Ação para ver detalhes completos


### 8.4 Exportação de Dados

- **Formatos**: Excel (.xlsx), PDF, CSV
- **Configurações**:
    - Seleção de campos para exportação
    - Aplicação de filtros atuais
    - Limite máximo: 50.000 registros por exportação
- **Processamento**: Assíncrono para grandes volumes


## 9. Critérios de Aceitação

### Login e Autenticação

- ✅ Usuário pode fazer login com credenciais válidas
- ✅ Sistema bloqueia após 5 tentativas inválidas
- ✅ Token JWT é renovado automaticamente


### Pesquisa de Clientes

- ✅ Pesquisa por CPF retorna resultado em ≤ 100ms (Redis)
- ✅ Pesquisa por nome suporta busca parcial
- ✅ Resultados são paginados corretamente
- ✅ Filtros podem ser combinados


### Exportação

- ✅ Excel gerado contém formatação adequada
- ✅ PDF mantém layout legível
- ✅ CSV utiliza encoding UTF-8
- ✅ Processo não bloqueia interface do usuário


### Performance

- ✅ Consultas frequentes são servidas pelo Redis
- ✅ Sincronização PostgreSQL-Redis é transparente
- ✅ Sistema suporta 100 usuários simultâneos sem degradação


## 10. Dependências \& Integrações

### Dependências Internas

- Módulo de Autenticação → Todas as funcionalidades
- Serviço de Cache → Pesquisa e relatórios
- Banco PostgreSQL → Fonte de verdade dos dados
- Redis → Cache e filas de processamento


### Dependências Externas

- Validação de CPF → Algoritmo interno
- Geração de relatórios → Bibliotecas Python (pandas, openpyxl)
- Monitoramento → Prometheus + Grafana (opcional)


### APIs Externas (Futuro)

- Validação de endereços → ViaCEP
- Verificação de CPF → Receita Federal
- Notificações → SendGrid ou similar


## 11. Plano de Implementação

### Fase 1 - MVP (4 semanas)

- [ ] Setup do ambiente Python + PostgreSQL + Redis
- [ ] Implementação das models e migrations
- [ ] APIs básicas de autenticação e pesquisa
- [ ] Interface web simples
- [ ] Testes unitários básicos


### Fase 2 - Funcionalidades Core (3 semanas)

- [ ] Sistema de cache Redis completo
- [ ] Exportação Excel/CSV/PDF
- [ ] Interface responsiva
- [ ] Logs de auditoria
- [ ] Testes de integração


### Fase 3 - Otimizações (2 semanas)

- [ ] Performance tuning
- [ ] Monitoramento e métricas
- [ ] Documentação completa
- [ ] Deploy em produção
- [ ] Testes de carga


## 12. Riscos \& Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
| :-- | :-- | :-- | :-- |
| Inconsistência PostgreSQL-Redis | Média | Alto | Implementar reconciliação automática + alertas |
| Performance degradada com volume alto | Baixa | Alto | Índices otimizados + cache inteligente |
| Falha na exportação de grandes volumes | Média | Médio | Processamento assíncrono + limites |
| Problemas de segurança | Baixa | Alto | Audit logs + testes de penetração |

## 13. Glossário

**CPF**: Cadastro de Pessoas Físicas - documento único brasileiro
**Cache Hit**: Consulta atendida pelo Redis sem acessar PostgreSQL
**TTL**: Time To Live - tempo de expiração do cache
**ORM**: Object-Relational Mapping - mapeamento objeto-relacional
**JWT**: JSON Web Token - padrão de autenticação stateless
**CRUD**: Create, Read, Update, Delete - operações básicas de dados

## 14. Métricas de Monitoramento

- **Performance**: Latência de APIs, hit rate do cache Redis
- **Negócio**: Número de pesquisas por dia, relatórios gerados
- **Sistema**: CPU, memória, conexões do banco, tamanho do cache
- **Usuário**: Sessões ativas, tempo médio de sessão, erros de login

***

Este PRD fornece a base completa para desenvolvimento do sistema de gestão de clientes em Python, seguindo as melhores práticas de arquitetura distribuída e priorizando performance através do uso inteligente de cache Redis.


