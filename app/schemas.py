from pydantic import BaseModel
import datetime
from typing import Optional

class ItemBase(BaseModel):
    message: str
    target_time: datetime.datetime
    status: str = "pending"
    permanent: bool = False
    mute: bool = False
    repeat: int = 1
    priority: int = 0
    category: str = "unassigned"
    original_id: Optional[str] = None # O ID do reminder-cli

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    status: Optional[str] = None
    priority: Optional[int] = None
    category: Optional[str] = None

class ItemInDB(ItemBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True # Habilita o modo ORM para ler dados do SQLAlchemy (Pydantic V2)