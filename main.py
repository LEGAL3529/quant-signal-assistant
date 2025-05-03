from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
import xgboost as xgb
import numpy as np
import pickle

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="Quant Assistant", version="0.2")

class SignalInput(BaseModel):
    data: List[float]

@app.get("/")
def root():
    return {"message": "Quant Assistant with real model"}

@app.post("/predict")
def predict(input: SignalInput):
    X = np.array(input.data).reshape(1, -1)
    prediction = model.predict(X)[0]
    label = "BUY" if prediction == 1 else "SELL"
    return {"input": input.data, "prediction": label}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
