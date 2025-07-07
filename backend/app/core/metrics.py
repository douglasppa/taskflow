from prometheus_client import Counter

# Total de tarefas criadas com sucesso
task_created_total = Counter(
    "task_created_total", "Número total de tarefas criadas com sucesso"
)

# Total de logins realizados
user_login_total = Counter(
    "user_login_total", "Número total de logins realizados com sucesso"
)
