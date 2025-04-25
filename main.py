from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "output": ""})

@app.post("/", response_class=HTMLResponse)
def generate_code(request: Request, prompt: str = Form(...)):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60
        )
        print("Risposta grezza:", response.text)  # 👈 AGGIUNGI QUESTO
        result = response.json()
        output = result.get("response", "Errore nella risposta.")
    except Exception as e:
        output = f"Errore durante la generazione: {e}"

    return templates.TemplateResponse("index.html", {"request": request, "output": output})
