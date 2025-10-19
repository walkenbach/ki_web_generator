import os
import pickle
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import RequestLog

# ----------------------------
# Basis-Pfad
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# FastAPI-App
# ----------------------------
app = FastAPI(title="KI Web Generator API")

# ----------------------------
# Token / API-Key für Schutz (optional)
# ----------------------------
API_KEY = os.environ.get("API_KEY")  # auf Render als Environment Variable setzen

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Ungültiger API-Key")

# ----------------------------
# Datenbank-Session
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# KI-Modelle laden
# ----------------------------
with open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

# ----------------------------
# Input-Daten
# ----------------------------
class InputData(BaseModel):
    text: str

# ----------------------------
# Endpunkte
# ----------------------------
@app.post("/predict", dependencies=[Depends(verify_api_key)])
def predict(data: InputData, db: Session = Depends(get_db)):
    X = vectorizer.transform([data.text])
    prediction = model.predict(X)[0]

    # Logging in DB
    log = RequestLog(input_text=data.text, output_text=prediction)
    db.add(log)
    db.commit()
    db.refresh(log)

    return {"input": data.text, "prediction": prediction}

@app.get("/")
def read_root():
    return {"message": "Willkommen bei der KI Web Generator API!"}

# ----------------------------
# Render-kompatibles Start-Skript
# ----------------------------
if __name__ == "__main__":
    import uvicorn

    # Render setzt automatisch PORT als Umgebungsvariable
    port_str = os.environ.get("PORT", "10000")
    try:
        port = int(port_str)
    except ValueError:
        print(f"Warnung: Ungültiger PORT-Wert '{port_str}', Default 10000 wird genutzt")
        port = 10000

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)






