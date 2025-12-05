from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base
import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    target_time = Column(DateTime)
    status = Column(String, default="pending") # pending, done, missed, cancelled
    permanent = Column(Boolean, default=False)
    mute = Column(Boolean, default=False)
    repeat = Column(Integer, default=1)
    
    # Campos para o algoritmo inteligente
    priority = Column(Integer, default=0, index=True) # Ex: 0-100 (Eisenhower Matrix)
    category = Column(String, default="unassigned") # Ex: critical, scheduled, routine, backlog

    # Adicionar campo para ID do item original do reminder-cli
    original_id = Column(String, unique=True, index=True, nullable=True)
