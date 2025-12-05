from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from . import models, schemas
from .database import engine, init_db, get_db

# Cria as tabelas do banco de dados na inicialização
init_db()

app = FastAPI(
    title="Neo-Cortex API",
    description="Central Brain for NeoCognito Ecosystem",
    version="0.1.0",
)

# Monta o diretório static para servir arquivos CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura o Jinja2 para templates HTML
templates = Jinja2Templates(directory="templates")

# --- CRUD Operations for Items ---

@app.post("/items/", response_model=schemas.ItemInDB)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.ItemInDB])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemInDB)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# --- Web Interface (The Wall) ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    # Lógica para obter os itens e categorizá-los para o "Wall"
    # Por enquanto, apenas busca todos os itens
    items = db.query(models.Item).order_by(models.Item.target_time).all()
    
    # Preparar dados para o template (substituir por lógica de categorização inteligente)
    critical_items = [item for item in items if item.category == "critical"]
    scheduled_items = [item for item in items if item.category == "scheduled"]
    routine_items = [item for item in items if item.category == "routine"]
    backlog_items = [item for item in items if item.category == "backlog"]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "critical_items": critical_items,
            "scheduled_items": scheduled_items,
            "routine_items": routine_items,
            "backlog_items": backlog_items,
        }
    )

