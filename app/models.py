from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from .database import Base
import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    
    # Core Data
    content = Column(String, index=True) # Mensagem do Reminder ou Texto do TODO
    source = Column(String, index=True) # "reminder-cli", "neocognito-vault", "telegram"
    source_id = Column(String, unique=True, index=True, nullable=True) # ID original (UUID do reminder ou Hash do Markdown)
    
    # Timing
    created_at = Column(DateTime, default=datetime.datetime.now)
    due_date = Column(DateTime, nullable=True) # target_time do reminder ou data extraída do TODO
    completed_at = Column(DateTime, nullable=True)
    
    # Status & Flags
    status = Column(String, default="pending") # pending, done, missed, archived
    is_pinned = Column(Boolean, default=False) # Permanent do reminder ou ! do TODO
    
    # Intelligent Layer (Calculado pelo Pi)
    priority_score = Column(Integer, default=0, index=True) 
    smart_category = Column(String, default="inbox") # inbox, do_now, schedule, delegate, backlog
    
    # Raw Metadata (Para guardar JSON bruto se precisar reprocessar)
    raw_data = Column(Text, nullable=True)