import re
PATTERNS = {
    "confirmation_bias": re.compile(r"\b(only|always|never)\b.*\b(agree|support|believe)\b", re.I),
    "authority_bias": re.compile(r"\b(according to|as said by)\b", re.I),
}
def detect_bias(text: str):
    out = {}
    for name, pat in PATTERNS.items():
        m = pat.findall(text or "")
        if m:
            out[name] = len(m)
    return out
