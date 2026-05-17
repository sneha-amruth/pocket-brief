"""
Sends the formatted bulletin to WhatsApp via Twilio.
"""

import os
from twilio.rest import Client


CHUNK_LIMIT = 1500


def _split_message(message: str) -> list[str]:
    """Split a long message at line boundaries, keeping each chunk under CHUNK_LIMIT."""
    chunks = []
    current = ""
    for line in message.splitlines(keepends=True):
        if current and len(current) + len(line) > CHUNK_LIMIT:
            chunks.append(current.rstrip())
            current = ""
        current += line
    if current.strip():
        chunks.append(current.rstrip())
    return chunks


def send_whatsapp(message: str) -> None:
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"],
    )
    from_ = os.environ["TWILIO_WHATSAPP_FROM"]
    to = os.environ["WHATSAPP_TO"]

    chunks = _split_message(message)
    for i, chunk in enumerate(chunks, 1):
        client.messages.create(from_=from_, to=to, body=chunk)
        print(f"[delivery] Sent part {i}/{len(chunks)}")

    print("[delivery] Bulletin sent successfully.")
