import os

import joblib
import pandas as pd
from fastapi import FastAPI

from api.schemas import CreditDefaultRequest


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "xgboost_tuned_pipeline.pkl"
)

THRESHOLD_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "xgboost_tuned_threshold.pkl"
)


# ============================================================
# CARREGAMENTO DO MODELO
# ============================================================

model = joblib.load(MODEL_PATH)

threshold = joblib.load(THRESHOLD_PATH)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Credit Default API",
    description=(
        "API para previsão de inadimplência "
        "de cartão de crédito."
    ),
    version="1.0.0"
)


# ============================================================
# ENDPOINT DE PREDIÇÃO
# ============================================================

@app.post("/predict")
def predict(request: CreditDefaultRequest):

    # --------------------------------------------------------
    # Conversão da entrada para DataFrame
    # --------------------------------------------------------

    data = request.model_dump()

    X = pd.DataFrame([data])

    # --------------------------------------------------------
    # Probabilidade de inadimplência
    # --------------------------------------------------------

    probability = model.predict_proba(X)[0, 1]

    # --------------------------------------------------------
    # Aplicação do threshold
    # --------------------------------------------------------

    prediction = int(
        probability >= threshold
    )

    # --------------------------------------------------------
    # Classificação
    # --------------------------------------------------------

    classification = (
        "inadimplente"
        if prediction == 1
        else "adimplente"
    )

    # --------------------------------------------------------
    # Resposta
    # --------------------------------------------------------

    return {
        "probability": round(
            float(probability),
            4
        ),
        "threshold": round(
            float(threshold),
            2
        ),
        "prediction": prediction,
        "classification": classification
    }