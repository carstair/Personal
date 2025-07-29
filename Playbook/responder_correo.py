#!/usr/bin/env python3
import smtplib
import os
from email.message import EmailMessage
import sys
import json

# Leer datos desde stdin (pasados por Ansible como input)
datos = json.loads(sys.stdin.read())

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("IMAP_USER")
SMTP_PASS = os.getenv("IMAP_PASS")

ioc = datos.get("IOC")
ticket = datos.get("Ticket")
destinatario = datos.get("From")
asunto_original = datos.get("Asunto")

msg = EmailMessage()
msg['Subject'] = f"Re: {asunto_original}"
msg['From'] = SMTP_USER
msg['To'] = destinatario
msg.set_content(f"""
Hola,

El siguiente IoC ha sido recibido y procesado:

Ticket: {ticket}
IoC: {ioc}

Gracias,
Ansible MSS
""")

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
        print(json.dumps({"status": "success", "message": "Correo enviado"}))
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))
