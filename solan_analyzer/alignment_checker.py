from typing import Dict
DEFAULT_VALUES = ["truth","freedom","wisdom","nature","courage"]

def alignment_score(model_claims: Dict[str,float], values = None) -> float:
    values = values or DEFAULT_VALUES
    if not model_claims: return 0.0
    # Verwacht keys als values-namen; gemiddelde als eenvoudige proxy:
    hits = [float(model_claims.get(v,0.0)) for v in values]
    if not hits: return 0.0
    s = sum(hits)/len(hits)
    return round(max(0.0, min(1.0, s)), 3)
