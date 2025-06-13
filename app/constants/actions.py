from enum import Enum

class LogAction(str, Enum):
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"