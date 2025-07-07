📄 Contratos de Integração – TaskFlow
Este documento descreve os contratos de integração usados entre APIs, serviços assíncronos e módulos internos do projeto.

🔐 Autenticação

POST /auth/register

Request:
{
"email": "user@example.com",
"password": "senha123"
}

Response:
{
"msg": "Usuário criado com sucesso"
}

POST /auth/login

Request:
{
"email": "user@example.com",
"password": "senha123"
}

Response:
{
"access_token": "jwt_token",
"token_type": "bearer"
}

📝 Tarefas

POST /tasks

Request:

{
"title": "Comprar leite",
"description": "Ir ao mercado à tarde"
}

Response:
{
"id": 1,
"title": "Comprar leite",
"description": "Ir ao mercado à tarde",
"owner_id": 5
}

GET /tasks

Response:
[
{
"id": 1,
"title": "Comprar leite",
"description": "Ir ao mercado à tarde",
"owner_id": 5
}
]

🌀 Celery – Log de eventos
Tarefa assíncrona: log_event.delay(user_id, action, data)
Exemplo de chamada:

log_event.delay("5", "TASK_CREATE", {"task_id": 1, "title": "Comprar leite"})

Estrutura salva no MongoDB:
{
"user_id": "5",
"action": "TASK_CREATE",
"timestamp": "2024-06-12T17:31:00Z",
"data": {
"task_id": 1,
"title": "Comprar leite"
}
}

📦 Observações
Todos os endpoints exigem autenticação JWT, exceto /auth/register e /auth/login.

Todos os retornos de erro seguem o padrão FastAPI:
{
"detail": "mensagem de erro"
}

O campo owner_id é extraído do token JWT, não do corpo da requisição.

📁 Referência de Schemas
Nome do schema	Local	Usado em
UserCreate	schemas/user.py	POST /auth/register
UserLogin	schemas/user.py	POST /auth/login
UserResponse	schemas/user.py	Resposta após login
TaskCreate	schemas/task.py	POST /tasks
TaskUpdate	schemas/task.py	PUT /tasks/{id}
TaskOut	schemas/task.py	GET, POST, PUT /tasks