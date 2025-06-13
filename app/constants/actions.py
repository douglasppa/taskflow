from enum import Enum

class LogAction(str, Enum):
    REGISTER = "register"
    LOGIN = "login"
    LOGOUT = "logout"
    TASK_CREATE = "create_task"
    TASK_UPDATE = "update_task"
    TASK_DELETE = "delete_task"