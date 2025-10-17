from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle
import os
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
# Token / API-Key für Schutz
# ----------------------------
import os
API_KEY = os.environ.get("API_KEY")


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
# Laden des KI-Modells
# ----------------------------
with open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

# ----------------------------
# Input-Daten
# ----------------------------
class InputData(BaseModel):
    text: str  # kleinbuchstabig, wichtig für Swagger

# ----------------------------
# Predict-Endpunkt
# ----------------------------
@app.post("/predict", summary="Vorhersage von Text", dependencies=[Depends(verify_api_key)])
def predict(data: InputData, db: Session = Depends(get_db)):
    # Vorhersage
    X = vectorizer.transform([data.text])
    prediction = model.predict(X)[0]

    # In Datenbank speichern
    log = RequestLog(input_text=data.text, output_text=prediction)
    db.add(log)
    db.commit()
    db.refresh(log)

    # Antwort
    return {"input": data.text, "prediction": prediction}

