#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header
import re
import json
import os

# === CONFIGURA ESTO ===
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
FOLDER_NAME = "IOC"

def extraer_info(asunto, cuerpo):
    empresa = None
    match_empresa = re.search(r'\[([^\]]+)\]', asunto)
    if match_empresa:
        empresa = match_empresa.group(1)

    ticket = None
    match_ticket = re.search(r'#(\d+)', asunto)
    if match_ticket:
        ticket = match_ticket.group(1)

    ioc = None
    match_ioc = re.search(r'Origin \(attacker\):\s*([\d\.]+)', cuerpo)
    if match_ioc:
        ioc = match_ioc.group(1)

    return empresa, ticket, ioc

def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
        for part, encoding in decoded
    )

def main():
    try:
        print("🔐 Conectando al servidor IMAP...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(IMAP_USER, IMAP_PASS)
        mail.select(FOLDER_NAME)

        result, data = mail.search(None, 'UNSEEN')
        if result != 'OK':
            raise Exception("No se pudo buscar mensajes.")

        email_ids = data[0].split()
        if not email_ids:
            print(json.dumps({"status": "no_unread_emails"}))
            return

        latest_email_id = email_ids[-1]

        result, data = mail.fetch(latest_email_id, '(RFC822)')
        if result != 'OK':
            raise Exception("No se pudo obtener el mensaje.")

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = decode_mime_words(msg.get("Subject", "NO_ASUNTO"))
        from_ = decode_mime_words(msg.get("From", ""))
        uid = latest_email_id.decode()

        # Marcar como leído
        mail.store(latest_email_id, '+FLAGS', '\\Seen')

        # Cuerpo del mensaje
        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    cuerpo = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    break
        else:
            cuerpo = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

        empresa, ticket, ioc = extraer_info(subject, cuerpo)

        print(json.dumps({
            "Empresa": empresa or "Unknown",
            "Ticket": ticket or "NO_TICKET",
            "IOC": ioc or "NO_IOC",
            "Asunto": subject or "NO_ASUNTO",
            "UID": uid,
            "From": from_,
            "status": "success"
        }))

    except Exception as e:
        print(json.dumps({
            "status": "Error",
            "message": str(e)
        }))

if __name__ == "__main__":
    main()
