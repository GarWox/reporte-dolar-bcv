import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord(message: str):
   if not DISCORD_WEBHOOK_URL:
        raise ValueError("No se encontró DISCORD_WEBHOOK_URL en variables de entorno")
   
   payload = {"content": message}
   requests.post(DISCORD_WEBHOOK_URL, json=payload)


