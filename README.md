# Tour Management Pro

A clean starter architecture for a tour management platform with:
- FastAPI backend
- SQLite database via SQLAlchemy
- Streamlit frontend
- PDF call sheet generation

## Structure

```text
app/
  api/          # FastAPI endpoints
  core/         # DB and config
  models/       # SQLAlchemy models
  schemas/      # Pydantic schemas
  services/     # Business logic
  frontend/     # Streamlit UI
```

## Install

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.api.main:app --reload
```

## Run the frontend

In a second terminal:

```bash
streamlit run app/frontend/streamlit_app.py
```

## Current features

- Create tours
- Log department finance entries
- View per-department summary
- View transactions per tour
- Generate a basic PDF call sheet

## Recommended next upgrades

- Add auth and real permissions
- Add a `shows` table and link finance rows to shows
- Add edit/delete endpoints
- Add merch inventory module
- Add VIP package module
- Add Excel export/import
- Swap SQLite to PostgreSQL when multi-user use starts
