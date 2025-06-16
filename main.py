from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "static", "backend", "data.json")

# Configurar templates e estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Função para carregar dados
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# Rotas principais
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/times", response_class=HTMLResponse)
async def read_times(request: Request):
    data = load_data()
    return templates.TemplateResponse("times.html", {"request": request, "data": data})


@app.get("/jogos", response_class=HTMLResponse)
async def read_jogos(request: Request):
    data = load_data()
    return templates.TemplateResponse("jogos.html", {"request": request, "data": data})


@app.get("/classificacao", response_class=HTMLResponse)
async def read_classificacao(request: Request):
    data = load_data()
    return templates.TemplateResponse("classificacao.html", {"request": request, "data": data})


@app.get("/estatisticas", response_class=HTMLResponse)
async def read_estatisticas(request: Request):
    data = load_data()
    return templates.TemplateResponse("estatisticas.html", {"request": request, "data": data})


@app.get("/individuais", response_class=HTMLResponse)
async def read_individuais(request: Request):
    data = load_data()
    return templates.TemplateResponse("individuais.html", {"request": request, "data": data})
