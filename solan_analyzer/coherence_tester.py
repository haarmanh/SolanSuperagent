from typing import List
def coherence_index(statements: List[str]) -> float:
    # Zeer eenvoudige placeholder: lange, consistente uitspraken → hogere score
    if not statements: return 0.0
    avg_len = sum(len(s or "") for s in statements)/len(statements)
    # knip op 280 chars (tweet) -> normaliseer
    return round(min(1.0, avg_len/280.0), 3)
