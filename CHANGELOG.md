# 📄 CHANGELOG

Todas as mudanças notáveis neste projeto serão documentadas aqui.


## 📦 v1.1.0 – Cobertura total e análise de qualidade
**Data:** 2025-07-03

### 📊 Qualidade e análise estática
- Integração com [SonarCloud](https://sonarcloud.io/) para análise de qualidade, cobertura e code smells.
- Configuração de projeto para reportar cobertura de testes via `pytest-cov`.
- Correção de todos os pontos críticos apontados pelo Sonar, incluindo duplicação de código, nomes não utilizados e práticas obsoletas.

### 🧪 Testes
- Implementação de novos testes unitários e de integração para atingir **100% de cobertura**.
- Testes para rotas de monitoramento (`/health/ready`) cobrindo falhas em MongoDB e RabbitMQ.
- Testes para logging de eventos assíncronos com validação de persistência no MongoDB.

### 🔧 Refatorações e ajustes técnicos
- Refatoração do serviço de logging (`logger.py`) para uso consistente de constantes de nível (`LogLevel`).
- Extração das instâncias de conexão com o MongoDB (`motor` e `pymongo`) para funções reutilizáveis em `app.db.mongo`.
- Substituição de acesso direto ao `MongoClient` por chamadas centralizadas via função (`get_sync_mongo_db`), melhorando testabilidade.
- Ajustes no `pytest.ini` para evitar warnings com `env_files` e migração de `Config` para `ConfigDict` no Pydantic v2.

### 🧼 Limpeza e manutenção
- Remoção de código redundante e proteção contra falhas silenciosas em exceções genéricas.
- Atualização das dependências com alerta para descontinuação de `crypt` no Python 3.13.
- Organização de imports e padronização de logs técnicos e mensagens de erro internas.


## 📦 v1.0.0 – Deploy na nuvem e CI/CD
**Data:** 2025-06-26

### 🚀 Features
- Versionamento do app com leitura de arquivo `VERSION`.
- Criação do endpoint `/info` com informações do app (versão e modo).
- Criação do endpoint `/summary`, retornando totais de tarefas por usuário (condicionado a feature flag).
- Adoção de feature flag via arquivo de configuração para controle de funcionalidades.

### 🔧 Ajustes técnicos
- Correção da estrutura de logging com configuração centralizada e formatação consistente.
- Worker Celery dummy adicionado para compatibilidade com plano gratuito do Render.

### ☁️ Deploy e Integração Contínua
- Configuração do projeto para deploy no [Render](https://render.com/) com suporte a MongoDB Atlas e CloudAMQP.
- Criação de pipeline no GitHub Actions:
  - Rodando `flake8` para lint.
  - Executando testes com `pytest` antes do deploy automático.


## 📦 v0.3.0 – Observabilidade e monitoramento
**Data:** 2025-06-20

### ✨ Novos recursos
- Integração com Prometheus para exportação de métricas da API.
- Dashboard base configurado no Grafana com visualização de dados operacionais.
- Endpoints de monitoramento:
  - `/metrics`: expõe métricas Prometheus.
  - `/health/live`: verificação de vida da API.
  - `/health/ready`: verificação de dependências externas (PostgreSQL, MongoDB, RabbitMQ).
- Logging estruturado em JSON para facilitar análise de logs e rastreamento.
- Contadores personalizados para Prometheus:
  - `task_created_total`
  - `user_login_total`

### 🧪 Testes
- Adição de testes automatizados para:
  - Autenticação
  - Tarefas
  - Healthcheck
- Estrutura de testes isolada com `pytest` e `httpx`.
- Ajustes na execução dos testes em ambiente Docker.

### 🛠️ Estrutura e documentação
- Comentários explicativos adicionados nos arquivos `schemas/`.
- Inclusão da ferramenta `pydeps` para visualização de dependências entre módulos.
- Criação de `docs/contracts.md` com contratos REST e payloads assíncronos via Celery.
- Refino nas rotas e agrupamento por tags na documentação Swagger.


## 📦 v0.2.0 – Autenticação e tarefas assíncronas
**Data:** 2025-06-13

### 🚀 Features
- Implementada autenticação com JWT: registro e login de usuários com geração de token.
- Restrições de acesso às tarefas: usuário só pode visualizar, editar e excluir suas próprias tasks.
- Logging de ações de usuário e tarefas utilizando MongoDB.
- Integração com Celery e RabbitMQ para logging assíncrono de eventos.

### 🛠 Infraestrutura
- Worker Celery configurado no `docker-compose.yml`.
- Registro explícito de tasks no `celery_app.py`.
- Conexão com MongoDB feita via `pymongo` no worker.
- Remoção de `task_routes` para compatibilidade com a fila padrão `celery`.

### 🔧 Outros
- Prints temporários incluídos para facilitar debug durante a execução das tasks.


## 📦 v0.1.0 – CRUD funcionando
**Data:** 2025-06-12

### 🚀 Features
- Implementado CRUD completo de tarefas com FastAPI.
- Endpoints REST integrados com PostgreSQL.
- Swagger UI ativo.

### 🛠 Infraestrutura
- Configuração inicial com Docker e Alembic.
- Estrutura modular: `models`, `schemas`, `routes`, `services`.

### 🔧 Outros
- Setup inicial de migrations e banco de dados.