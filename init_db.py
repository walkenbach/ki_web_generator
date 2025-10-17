from database import engine, Base
from models import RequestLog

# Tabellen erstellen
Base.metadata.create_all(bind=engine)

print("Datenbank und Tabellen erstellt!")
