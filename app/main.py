from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import datetime

from . import models, schemas
from .database import engine, init_db, get_db

# Cria as tabelas do banco de dados na inicialização
init_db()

app = FastAPI(
    title="Neo-Cortex API",
    description="Headless Intelligence Layer for NeoCognito",
    version="0.2.0",
)

# --- Ingestão e Sincronização ---

@app.post("/ingest/", response_model=schemas.ItemInDB)
def ingest_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Smart Ingest: Cria ou Atualiza um item baseado no source_id.
    """
    if item.source_id:
        existing_item = db.query(models.Item).filter(
            models.Item.source_id == item.source_id,
            models.Item.source == item.source
        ).first()

        if existing_item:
            # Atualiza campos se existirem mudanças
            existing_item.content = item.content
            existing_item.due_date = item.due_date
            existing_item.status = item.status
            existing_item.is_pinned = item.is_pinned
            # Recalcula prioridade aqui ou marca para reprocessamento
            db.commit()
            db.refresh(existing_item)
            return existing_item

    # Se não existe, cria novo
    db_item = models.Item(**item.dict())
    # Aqui virá a chamada para o algoritmo de priorização inicial
    # db_item.priority_score = calculate_priority(...) 
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- Leitura para o Conky (Output) ---

@app.get("/dashboard/txt", response_class=PlainTextResponse)
def get_dashboard_txt(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna uma representação em texto puro formatada para o Conky.
    """
    # Busca itens ordenados por score (descendente) e data
    items = db.query(models.Item).filter(
        models.Item.status == "pending"
    ).order_by(
        models.Item.priority_score.desc(),
        models.Item.due_date.asc()
    ).limit(limit).all()

    output = []
    for item in items:
        time_str = item.due_date.strftime("%H:%M") if item.due_date else "--:--"
        icon = "!" if item.is_pinned else "•"
        output.append(f"{icon} {time_str} - {item.content}")

    if not output:
        return "No active tasks."
        
    return "\n".join(output)

@app.get("/items/", response_model=list[schemas.ItemInDB])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items