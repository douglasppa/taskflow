from enum import Enum

# Constantes para mensagens informativas
TASK_NOT_FOUND_MSG = "Task not found"
LOG_SEND_MSG = "Log sent successfully"


# Enum usada para registrar ações no log
class LogAction(str, Enum):
    REGISTER = "register"
    LOGIN = "login"
    LOGOUT = "logout"
    TASK_CREATE = "create_task"
    TASK_UPDATE = "update_task"
    TASK_DELETE = "delete_task"
