import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logger import log, LogLevel


def send_reset_email(to_email: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    subject = "Recuperação de senha - TaskFlow"
    body = f"""
    Olá,<br><br>
    Você solicitou a redefinição de senha.<br><br>
    Clique no link abaixo para definir uma nova senha:<br>
    <a href="{reset_link}">{reset_link}</a><br><br>
    Se você não solicitou essa ação, apenas ignore este e-mail.<br><br>
    Atenciosamente,<br>
    Equipe TaskFlow
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        log(f"E-mail de redefinição enviado para {to_email}", level=LogLevel.INFO)
    except Exception as e:
        log(f"Erro ao enviar e-mail para {to_email}: {e}", level=LogLevel.ERROR)
        raise


def send_updated_email(to_email: str):
    subject = "Senha atualizada - TaskFlow"
    body = """
    Olá,<br><br>
    Informamos que a senha da sua conta TaskFlow foi atualizada com sucesso.<br><br>
    Se você realizou essa alteração, nenhuma ação adicional é necessária.<br><br>
    Caso **não tenha sido você**, por favor, entre em contato imediatamente com o suporte e atualize sua senha.<br><br>
    Atenciosamente,<br>
    Equipe TaskFlow
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        log(
            f"E-mail de confirmação de atualização de senha enviado para {to_email}",
            level=LogLevel.INFO,
        )
    except Exception as e:
        log(
            f"Erro ao enviar e-mail de confirmação para {to_email}: {e}",
            level=LogLevel.ERROR,
        )
        raise
