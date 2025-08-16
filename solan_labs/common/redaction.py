import re
PII_PATTERNS = [
    re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b"),                 # emails
    re.compile(r"\b(?:\+?\d{1,3})?[\s\-]?(?:\d{2,4}[\s\-]?){2,4}\d{2,4}\b"),  # phones (simple)
]
def redact(text: str) -> str:
    s = text or ""
    for pat in PII_PATTERNS:
        s = pat.sub("[REDACTED]", s)
    return s
