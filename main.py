import os
from dotenv import load_dotenv
from solan_labs.api.server import create_app

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Config via env vars:
    # SOLAN_API_KEYS='{"admin-key":"admin","analyst-key":"analyst"}'
    # RATE_LIMIT_PER_MIN=60
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
