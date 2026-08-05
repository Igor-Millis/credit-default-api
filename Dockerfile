FROM python:3.13-bookworm

WORKDIR /app

COPY requirements-api.txt .

RUN pip install --no-cache-dir -r requirements-api.txt

COPY api ./api
COPY src ./src

COPY models/xgboost_tuned_pipeline.pkl ./models/xgboost_tuned_pipeline.pkl
COPY models/xgboost_tuned_threshold.pkl ./models/xgboost_tuned_threshold.pkl

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]