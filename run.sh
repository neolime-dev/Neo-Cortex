#!/bin/bash

# Ativa o ambiente virtual
source .venv/bin/activate

# Inicia o servidor Uvicorn
# --host 0.0.0.0 permite acesso de qualquer IP (importante para o Pi)
# --port 8000 é a porta padrão, pode ser mudada
# --reload para desenvolvimento (reinicia o server ao detectar mudanças no código)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
