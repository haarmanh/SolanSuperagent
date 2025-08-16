import json, hashlib, time, os
from typing import Optional

class ImmutableLogger:
    def __init__(self, path="logs/immutable_log.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._last = None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                last = None
                for line in f:
                    last = json.loads(line)
                self._last = last
        except FileNotFoundError:
            pass

    def _hash(self, payload: dict, prev_hash: Optional[str]):
        blob = json.dumps({"prev": prev_hash, "data": payload}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    def append(self, kind: str, data: dict):
        rec = {
            "ts": time.time(),
            "kind": kind,
            "data": data,
            "prev_hash": self._last["hash"] if self._last else None,
        }
        rec["hash"] = self._hash(rec, rec["prev_hash"])
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._last = rec
        return rec
