import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from fastapi.testclient import TestClient

from api.main import app

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


# ============================================================
# DADOS DE TESTE
# ============================================================

valid_payload = {
    "LIMIT_BAL": 290000,
    "SEX": 2,
    "EDUCATION": 1,
    "MARRIAGE": 2,
    "AGE": 25,
    "PAY_0": 0,
    "PAY_2": 0,
    "PAY_3": 0,
    "PAY_4": 0,
    "PAY_5": 0,
    "PAY_6": 0,
    "BILL_AMT1": 305823,
    "BILL_AMT2": 303701,
    "BILL_AMT3": 296384,
    "BILL_AMT4": 248801,
    "BILL_AMT5": 241983,
    "BILL_AMT6": 230925,
    "PAY_AMT1": 15000,
    "PAY_AMT2": 10500,
    "PAY_AMT3": 10000,
    "PAY_AMT4": 15000,
    "PAY_AMT5": 7844,
    "PAY_AMT6": 23333
}


# ============================================================
# TESTE 1 — ENTRADA VÁLIDA
# ============================================================

def test_predict_valid_input():

    response = client.post(
        "/predict",
        json=valid_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "probability" in data
    assert "threshold" in data
    assert "prediction" in data
    assert "classification" in data

    assert 0 <= data["probability"] <= 1
    assert 0 <= data["threshold"] <= 1
    assert data["prediction"] in [0, 1]

    assert data["classification"] in [
        "adimplente",
        "inadimplente"
    ]


# ============================================================
# TESTE 2 — ENTRADA INVÁLIDA
# ============================================================

def test_predict_invalid_sex():

    invalid_payload = valid_payload.copy()

    invalid_payload["SEX"] = 7

    response = client.post(
        "/predict",
        json=invalid_payload
    )

    assert response.status_code == 422