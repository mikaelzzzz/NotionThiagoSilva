from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    nome = data.get('nome')
    email = data.get('email')
    whatsapp = data.get('whatsapp')

    if not nome or not email or not whatsapp:
        return {"error": "Nome, email ou WhatsApp faltando."}

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Nome": {
                "title": [
                    {
                        "text": {
                            "content": nome
                        }
                    }
                ]
            },
            "Email": {
                "email": email
            },
            "WhatsApp": {
                "rich_text": [
                    {
                        "text": {
                            "content": whatsapp
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return {"message": "Dados enviados para o Notion com sucesso."}
    else:
        return {"error": response.text}, response.status_code
