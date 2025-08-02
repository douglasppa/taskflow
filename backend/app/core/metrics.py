from prometheus_client import Counter, Gauge

# Total de tarefas criadas com sucesso
task_created_total = Counter(
    "task_created_total", "Número total de tarefas criadas com sucesso"
)

# Total de logins realizados
user_login_total = Counter(
    "user_login_total", "Número total de logins realizados com sucesso"
)

frontend_lcp = Gauge(
    "frontend_lcp", "Largest Contentful Paint médio", ["route", "browser"]
)
frontend_ttfb = Gauge("frontend_ttfb", "Time to First Byte médio", ["route", "browser"])
frontend_cls = Gauge(
    "frontend_cls", "Cumulative Layout Shift médio", ["route", "browser"]
)
frontend_inp = Gauge(
    "frontend_inp", "Interaction to Next Paint médio", ["route", "browser"]
)
frontend_fcp = Gauge(
    "frontend_fcp", "First Contentful Paint médio", ["route", "browser"]
)
