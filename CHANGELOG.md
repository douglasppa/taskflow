# 📄 CHANGELOG

Todas as mudanças notáveis neste projeto serão documentadas aqui.


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