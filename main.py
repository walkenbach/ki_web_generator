from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import pickle
from io import BytesIO

# -------------------------
# URLs zu den GitHub-Modellen
# -------------------------
MODEL_URL = "https://raw.githubusercontent.com/walkenbach/ki_web_generator/main/model.pkl"
VECTORIZER_URL = "https://raw.githubusercontent.com/walkenbach/ki_web_generator/main/vectorizer.pkl"

# -------------------------
# Modelle laden
# -------------------------
def load_pickle_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return pickle.load(BytesIO(response.content))

model = load_pickle_from_url(MODEL_URL)
vectorizer = load_pickle_from_url(VECTORIZER_URL)

print("Modelle erfolgreich geladen!")

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="KI Web Generator API")

# -------------------------
# API-Key (sollte auf Render als Umgebungsvariable gesetzt werden)
# -------------------------
import os
API_KEY = os.environ.get("API_KEY", "rnd_qAPT86mEedXqRQrqijotOXe1G80g")  # Default für Test

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Ungültiger API-Key")

# -------------------------
# Request Body
# -------------------------
class InputText(BaseModel):
    text: str

# -------------------------
# Endpunkte
# -------------------------
@app.get("/")
def read_root():
    return {"message": "Willkommen bei der KI Web Generator API!"}

@app.post("/predict")
def predict(input_data: InputText, x_api_key: str = Header(...)):
    # API-Key prüfen
    verify_api_key(x_api_key)

    # Text in Vektor umwandeln
    X = vectorizer.transform([input_data.text])
    # Vorhersage mit Modell
    prediction = model.predict(X)
    return {"input": input_data.text, "prediction": prediction[0]}

# -------------------------
# Optional: zum lokalen Testen
# -------------------------
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)







