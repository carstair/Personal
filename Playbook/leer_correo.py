#!/usr/bin/env python3
from imap_tools import MailBox, AND # type: ignore
import re
import json
import os

# === CONFIGURA ESTO ===
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
FOLDER_NAME = "IOC"

def extraer_info(asunto, cuerpo):
    # Empresa entre corchetes [SAMSUNG]
    empresa = None
    match_empresa = re.search(r'\[([^\]]+)\]', asunto)
    if match_empresa:
        empresa = match_empresa.group(1)

    # Ticket en el formato #123456
    ticket = None
    match_ticket = re.search(r'#(\d+)', asunto)
    if match_ticket:
        ticket = match_ticket.group(1)

    # IoC desde campo Origin (attacker):
    ioc = None
    match_ioc = re.search(r'Origin \(attacker\):\s*([\d\.]+)', cuerpo)
    if match_ioc:
        ioc = match_ioc.group(1)

    return empresa, ticket, ioc

def main():
    try:
        print("🔐 Conectando al servidor IMAP...")
        with MailBox(IMAP_SERVER).login(IMAP_USER, IMAP_PASS) as mailbox:
            print(f"📂 Cambiando a carpeta: {FOLDER_NAME}")
            mailbox.folder.set(FOLDER_NAME)
            mensajes = mailbox.fetch(criteria=AND(seen=False), reverse=True, limit=1)

            for msg in mensajes:
                empresa, ticket, ioc = extraer_info(msg.subject, msg.text or msg.html or "")

                # Devuelve JSON siempre (incluso si algunos campos son None)
                print(json.dumps({
                    "Empresa": empresa or "Unknown",
                    "Ticket": ticket or "NO_TICKET",
                    "IOC": ioc or "NO_IOC",
                    "Asunto": msg.subject or "NO_ASUNTO",
                    "UID": msg.uid,
                    "From": msg.from_,
                    "status": "success"
                }))
                return

            # Si no hay mensajes
            print(json.dumps({"status": "no_unread_emails"}))

    except Exception as e:
        print(json.dumps({
            "status": "Error",
            "message": str(e)
        }))

if __name__ == "__main__":
    main()
