import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", SMTP_USER)


def enviar_email(destino: str, assunto: str, corpo: str) -> bool:
    """Envia um e-mail de texto simples. Nunca derruba a API se falhar."""
    if not (SMTP_USER and SMTP_PASSWORD and destino):
        print("[email] SMTP não configurado ou sem destinatário; e-mail não enviado.")
        return False

    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = destino
    msg["Subject"] = assunto
    msg.set_content(corpo)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(SMTP_USER, SMTP_PASSWORD)
            servidor.send_message(msg)
        print(f"[email] enviado para {destino}")
        return True
    except Exception as exc:
        print(f"[email] falha ao enviar: {exc}")
        return False