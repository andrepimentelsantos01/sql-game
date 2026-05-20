# Backend do SQL Quest

## Rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_databases.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
```

API fixa: http://localhost:8002/api/health
