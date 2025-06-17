
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))



DATA_FILE = os.path.join(BASE_DIR, "data.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    data = load_data()
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/api/jogos")
def get_jogos():
    data = load_data()
    return data.get("jogos", [])

@app.post("/api/add_jogo")
def add_jogo(jogo: dict):
    data = load_data()
    data["jogos"].append(jogo)
    save_data(data)
    return {"message": "Jogo adicionado com sucesso", "jogo": jogo}

@app.get("/api/classificacao")
def get_classificacao():
    data = load_data()
    return data.get("classificacao", {})

@app.post("/api/add_classificacao/{esporte}/{grupo}")
def add_classificacao(esporte: str, grupo: str, classificacao: list):
    data = load_data()
    if esporte not in data["classificacao"]:
        data["classificacao"][esporte] = {}
    data["classificacao"][esporte][grupo] = classificacao
    save_data(data)
    return {"message": "Classificação atualizada", "classificacao": classificacao}

@app.get("/api/estatisticas")
def get_estatisticas():
    data = load_data()
    return data.get("estatisticas", {})

@app.post("/api/add_estatistica/{esporte}")
def add_estatistica(esporte: str, estat: dict):
    data = load_data()
    if esporte not in data["estatisticas"]:
        data["estatisticas"][esporte] = {"gols": [], "assistencias": []}
    if "gols" in estat:
        data["estatisticas"][esporte]["gols"].append(estat["gols"])
    if "assistencias" in estat:
        data["estatisticas"][esporte]["assistencias"].append(estat["assistencias"])
    save_data(data)
    return {"message": "Estatística atualizada", "estatisticas": data["estatisticas"][esporte]}

@app.post("/api/save_json")
def save_json(request: Request, content: str = Form(...)):
    try:
        json_data = json.loads(content)
        save_data(json_data)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))