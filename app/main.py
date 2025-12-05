from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import datetime

from . import models, schemas
from .database import engine, init_db, get_db
from .services.priority_service import calculate_priority # Importar o serviço

# Cria as tabelas do banco de dados na inicialização
init_db()

app = FastAPI(
    title="Neo-Cortex API",
    description="Headless Intelligence Layer for NeoCognito",
    version="0.3.0", # Bump version
)

# --- Ingestão e Sincronização ---

@app.post("/ingest/", response_model=schemas.ItemInDB)
def ingest_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Smart Ingest: Cria ou Atualiza um item baseado no source_id.
    Calcula automaticamente Priority Score e Smart Category.
    """
    # 1. Calcular Inteligência
    # Converter Pydantic model para dict
    item_data = item.dict()
    score, category = calculate_priority(item_data)

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
            # Atualiza Inteligência
            existing_item.priority_score = score
            existing_item.smart_category = category
            
            db.commit()
            db.refresh(existing_item)
            return existing_item

    # Se não existe, cria novo
    db_item = models.Item(**item.dict())
    # Aplica Inteligência
    db_item.priority_score = score
    db_item.smart_category = category
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- Leitura para o Conky (Output) ---

@app.get("/dashboard/txt", response_class=PlainTextResponse)
def get_dashboard_txt(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna uma representação em texto puro formatada para o Conky.
    Agora muito mais inteligente: Agrupa por Categoria.
    """
    # Busca itens pendentes
    items = db.query(models.Item).filter(
        models.Item.status == "pending"
    ).order_by(
        models.Item.priority_score.desc(), # Mais importantes primeiro
        models.Item.due_date.asc()
    ).all() # Pegamos tudo para filtrar no python por categoria

    if not items:
        return "No active tasks. Brain is clear."

    # Agrupamento Manual
    critical = [i for i in items if i.smart_category == "critical"]
    scheduled = [i for i in items if i.smart_category == "scheduled"]
    inbox = [i for i in items if i.smart_category in ["do_now", "inbox", "backlog", "routine"]]
    
    output = []

    if critical:
        output.append("${color #FF4444}CRITICAL (Do First)${color}")
        for item in critical:
            time_str = item.due_date.strftime("%H:%M") if item.due_date else "NOW"
            output.append(f" [!] {time_str} {item.content}")
        output.append("") # Spacer

    if scheduled:
        output.append("${color #FFA500}SCHEDULED${color}")
        for item in scheduled[:5]: # Limita scheduled
            time_str = item.due_date.strftime("%H:%M") if item.due_date else "--:--"
            output.append(f"  •  {time_str} {item.content}")
        output.append("")

    if inbox:
        output.append("${color #00FF99}INBOX / BACKLOG${color}")
        for item in inbox[:7]: # Limita inbox
            output.append(f"  -  {item.content}")

    return "\n".join(output)

@app.get("/items/", response_model=list[schemas.ItemInDB])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items
