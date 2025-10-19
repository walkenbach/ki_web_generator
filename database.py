# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------
# Datenbank-URL: entweder aus Umgebungsvariable (für PostgreSQL auf Render)
# oder lokale SQLite-Datei (für Test lokal)
# -------------------------
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./ki_api.db")

# -------------------------
# Engine erstellen
# -------------------------
if DATABASE_URL.startswith("sqlite"):
    # SQLite benötigt diesen Parameter
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL oder andere DBs
    engine = create_engine(DATABASE_URL)

# -------------------------
# Session und Base
# -------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()







