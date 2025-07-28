import pytest
from unittest.mock import patch, MagicMock
from app.services.email import send_reset_email, send_updated_email


# Testes para send_reset_email
def test_send_reset_email_success():
    with patch("smtplib.SMTP") as mock_smtp, patch(
        "app.services.email.log"
    ) as mock_log:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        send_reset_email("test@example.com", "dummy-token")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        mock_log.assert_called_with(
            "E-mail de redefinição enviado para test@example.com", level="INFO"
        )


def test_send_reset_email_failure():
    with patch("smtplib.SMTP", side_effect=Exception("SMTP error")), patch(
        "app.services.email.log"
    ) as mock_log:
        with pytest.raises(Exception) as e:
            send_reset_email("fail@example.com", "token")
        assert "SMTP error" in str(e.value)
        mock_log.assert_called()


# Testes para send_updated_email
def test_send_updated_email_success():
    with patch("smtplib.SMTP") as mock_smtp, patch(
        "app.services.email.log"
    ) as mock_log:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        send_updated_email("test@example.com")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        mock_log.assert_called_with(
            "E-mail de confirmação de atualização de senha enviado para test@example.com",
            level="INFO",
        )


def test_send_updated_email_failure():
    with patch("smtplib.SMTP", side_effect=Exception("SMTP error")), patch(
        "app.services.email.log"
    ) as mock_log:
        with pytest.raises(Exception) as e:
            send_updated_email("fail@example.com")
        assert "SMTP error" in str(e.value)
        mock_log.assert_called()
