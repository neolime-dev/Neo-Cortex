import datetime
import re

# Palavras-chave que aumentam a prioridade
URGENT_KEYWORDS = ["urgent", "urgente", "asap", "critical", "critico", "deadline", "prazo", "hj", "hoje", "today", "now", "agora"]
ACTION_KEYWORDS = ["buy", "comprar", "pay", "pagar", "call", "ligar", "send", "enviar", "email"]

def calculate_priority(item_dict):
    """
    Analisa um dicionário de item e retorna (score, smart_category).
    item_dict deve ter: content, source, due_date (datetime), is_pinned (bool)
    """
    score = 0
    content = item_dict.get("content", "").lower()
    due_date = item_dict.get("due_date")
    source = item_dict.get("source", "")
    is_pinned = item_dict.get("is_pinned", False)
    now = datetime.datetime.now()

    # 1. Source Weight
    if source == "telegram":
        score += 20
    elif source == "reminder-cli":
        score += 15
    
    # 2. Pin Weight
    if is_pinned:
        score += 30

    # 3. Keyword Analysis
    for word in URGENT_KEYWORDS:
        if word in content:
            score += 40
            break # Apenas conta uma vez para não inflar
    
    for word in ACTION_KEYWORDS:
        if word in content:
            score += 10
            break

    # 4. Time Urgency (The most important factor)
    if due_date:
        # Se já venceu
        if due_date < now:
            # Vencido é sempre problema.
            score += 60
        else:
            time_to_due = due_date - now
            hours_to_due = time_to_due.total_seconds() / 3600

            if hours_to_due < 1: # Menos de 1h
                score += 50
            elif hours_to_due < 4: # Menos de 4h (turno da manhã/tarde)
                score += 30
            elif hours_to_due < 24: # É para hoje/amanhã cedo
                score += 20
            elif hours_to_due < 48:
                score += 10
    
    # --- Categorização ---
    category = "backlog"

    if score >= 80:
        category = "critical"
    elif due_date and score >= 40:
        category = "scheduled"
    elif "routine" in content or "rotina" in content:
        category = "routine"
    elif score >= 20:
        category = "do_now" # Coisas rápidas sem data marcada mas importantes
    
    # Limpa o score para ficar bonitinho (0-100+)
    return int(score), category
