from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define o diretório 'instance' para o banco de dados
# Garante que o diretório 'instance' exista
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "instance")
os.makedirs(instance_path, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{instance_path}/neocortex.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obter a sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Método para criar todas as tabelas (será chamado no main.py)
def init_db():
    Base.metadata.create_all(bind=engine)
