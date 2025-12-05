from pydantic import BaseModel
import datetime
from typing import Optional

class ItemBase(BaseModel):
    content: str
    source: str
    source_id: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    status: str = "pending"
    is_pinned: bool = False
    raw_data: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    # Permitir atualizar campos individuais
    content: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    status: Optional[str] = None
    is_pinned: Optional[bool] = None
    priority_score: Optional[int] = None
    smart_category: Optional[str] = None

class ItemInDB(ItemBase):
    id: int
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    priority_score: int
    smart_category: str

    class Config:
        from_attributes = True
