"""Optional Meta WhatsApp Cloud API and SMTP email sending."""
import os
import smtplib
from email.message import EmailMessage
import httpx

async def send_whatsapp(to: str, message: str) -> dict:
    token, phone_id = os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip(), os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
    if not token or not phone_id: raise RuntimeError("WhatsApp is not configured. Add Meta Cloud API credentials to local .env.")
    if not to.strip() or not message.strip(): raise ValueError("Recipient and message are required.")
    payload = {"messaging_product":"whatsapp","to":to.strip(),"type":"text","text":{"body":message[:4096]}}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(f"https://graph.facebook.com/v22.0/{phone_id}/messages", json=payload, headers={"Authorization":f"Bearer {token}"})
        response.raise_for_status()
        return response.json()

def send_email(to: str, subject: str, body: str) -> None:
    host, user, password = (os.getenv(k, "").strip() for k in ("FRIDEY_SMTP_HOST","FRIDEY_SMTP_USERNAME","FRIDEY_SMTP_PASSWORD"))
    sender = os.getenv("FRIDEY_EMAIL_FROM", user).strip()
    port = int(os.getenv("FRIDEY_SMTP_PORT", "587"))
    if not all((host,user,password,sender)): raise RuntimeError("Email is not configured. Add SMTP settings to local .env.")
    if not to.strip() or not subject.strip() or not body.strip(): raise ValueError("Recipient, subject and body are required.")
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = sender, to.strip(), subject.strip()[:200]
    msg.set_content(body[:20000])
    with smtplib.SMTP(host,port,timeout=20) as server:
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
