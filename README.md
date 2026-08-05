# Credit Default API

API para previsão de inadimplência de clientes de cartão de crédito, desenvolvida a partir do dataset **Default of Credit Card Clients** da UCI Machine Learning Repository.

O projeto percorre todo o fluxo de um problema de Machine Learning aplicado: entendimento e tratamento dos dados, pré-processamento, treinamento e comparação de modelos, otimização de hiperparâmetros, seleção do modelo final, ajuste de threshold, interpretação, criação de uma API REST, testes automatizados e containerização com Docker.

## Objetivo

O objetivo é desenvolver um modelo capaz de estimar a probabilidade de um cliente apresentar inadimplência no próximo mês e disponibilizar essa previsão através de uma API REST.

O problema é tratado como uma classificação binária:

* `0` → cliente adimplente
* `1` → cliente inadimplente

Além da classe prevista, a API retorna a probabilidade estimada de inadimplência e o threshold utilizado na decisão.

---

## Dataset

Foi utilizado o dataset **Default of Credit Card Clients**, disponibilizado pela UCI Machine Learning Repository.

O conjunto possui:

* **30.000 observações**
* **25 variáveis originalmente**
* **23 variáveis preditoras utilizadas após a remoção do identificador e da variável resposta**
* variável resposta: `default payment next month`

A distribuição da variável alvo é:

| Classe             | Quantidade | Proporção |
| ------------------ | ---------: | --------: |
| Adimplente (`0`)   |     23.364 |    77,88% |
| Inadimplente (`1`) |      6.636 |    22,12% |

Essa distribuição evidencia um problema de **desbalanceamento moderado**, tornando métricas como Precision, Recall, F1-score e ROC AUC importantes para a avaliação dos modelos.

---

## Fluxo do projeto

```text
Dataset
   │
   ▼
Entendimento dos dados
   │
   ▼
Tratamento e pré-processamento
   │
   ▼
Divisão treino / validação / teste
   │
   ▼
Modelagem
   │
   ├── Logistic Regression
   ├── Decision Tree
   ├── Random Forest
   └── XGBoost
   │
   ▼
Grid Search
   │
   ▼
Avaliação e seleção do modelo
   │
   ▼
Ajuste do threshold
   │
   ▼
XGBoost Tuned
   │
   ▼
FastAPI
   │
   ▼
Testes automatizados
   │
   ▼
Docker
```

---

## Pré-processamento

O pré-processamento foi implementado utilizando `scikit-learn` e organizado em uma pipeline para garantir que as mesmas transformações utilizadas durante o treinamento sejam aplicadas durante a inferência.

As variáveis numéricas são padronizadas utilizando `StandardScaler`.

As variáveis categóricas são transformadas utilizando `OneHotEncoder`.

As variáveis relacionadas ao histórico de pagamento (`PAY_0`, `PAY_2`, ..., `PAY_6`) foram mantidas em sua escala original.

A utilização de uma pipeline permite encapsular o pré-processamento junto ao modelo, reduzindo o risco de inconsistências entre treinamento e produção.

---

## Divisão dos dados

Foi utilizada divisão estratificada dos dados:

```text
Dataset
├── Treino: 80% (24.000)
│   ├── Treinamento do modelo: 19.200
│   └── Validação: 4.800
│
└── Teste: 20% (6.000)
```

A estratificação foi utilizada para preservar aproximadamente a mesma proporção das classes nos diferentes subconjuntos.

O conjunto de teste foi mantido separado para a avaliação final dos modelos.

---

# Modelagem

Foram avaliados quatro algoritmos de classificação:

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost

A comparação considerou não apenas Accuracy, mas também Precision, Recall, F1-score e ROC AUC.

Isso é especialmente importante neste problema, pois a classe inadimplente representa uma parcela menor das observações e os custos associados aos diferentes tipos de erro não são equivalentes.

---

## Logistic Regression

A Regressão Logística foi utilizada como modelo linear de referência.

### Baseline

| Métrica   | Resultado |
| --------- | --------: |
| Accuracy  |    0,8095 |
| Precision |    0,6966 |
| Recall    |    0,2457 |
| F1-score  |    0,3632 |
| ROC AUC   |    0,7100 |

O modelo apresentou boa Accuracy, porém baixo Recall para a classe inadimplente.

Foi posteriormente realizada otimização de hiperparâmetros utilizando Grid Search.

---

## Decision Tree

A árvore de decisão apresentou sinais claros de overfitting em sua configuração inicial.

No treinamento, o modelo atingiu aproximadamente:

* Accuracy: `0,9995`
* ROC AUC: `1,0000`

enquanto apresentou desempenho significativamente inferior no conjunto de teste.

Após a otimização dos hiperparâmetros, o modelo apresentou melhora de generalização, atingindo aproximadamente:

| Métrica  | Resultado |
| -------- | --------: |
| Accuracy |    0,8173 |
| ROC AUC  |    0,7477 |

---

## Random Forest

### Baseline

| Métrica  | Resultado |
| -------- | --------: |
| Accuracy |    0,8135 |
| ROC AUC  |    0,7546 |

O Random Forest apresentou desempenho superior ao modelo linear em ROC AUC e serviu como uma referência importante entre os modelos baseados em árvores.

Após Grid Search, o melhor resultado de validação cruzada alcançou:

```text
Best CV ROC AUC: 0,7827
```

Na avaliação final do modelo otimizado:

```text
Train Accuracy: 0,9143
Test Accuracy: 0,7867
Test ROC AUC:   0,7735
```

A diferença entre treino e teste indicou a existência de algum grau de overfitting.

---

# XGBoost

O XGBoost apresentou o melhor desempenho geral entre os modelos avaliados e foi selecionado como candidato principal para produção.

### Baseline

| Métrica   | Resultado |
| --------- | --------: |
| Accuracy  |    0,8183 |
| Precision |    0,6626 |
| Recall    |    0,3640 |
| F1-score  |    0,4698 |
| ROC AUC   |    0,7731 |

O modelo apresentou uma diferença relativamente pequena entre o desempenho de treinamento e teste, indicando boa capacidade de generalização.

---

## XGBoost com Grid Search

Foi realizada otimização dos hiperparâmetros utilizando Grid Search, avaliando **72 combinações**.

Os melhores hiperparâmetros encontrados foram:

```text
colsample_bytree = 0.8
learning_rate    = 0.05
max_depth        = 7
min_child_weight = 5
n_estimators     = 100
reg_lambda       = 5
subsample        = 0.8
```

O melhor resultado de validação cruzada foi:

```text
Best CV ROC AUC: 0.7853
```

---

# Ajuste do Threshold

O modelo fornece uma probabilidade de inadimplência, que normalmente seria convertida em uma classificação utilizando um threshold de `0.50`.

Entretanto, em problemas de classificação de crédito, o threshold não precisa necessariamente ser 0,50.

Como o objetivo envolve identificar uma parcela maior dos clientes inadimplentes, foi avaliado um threshold alternativo.

O threshold selecionado foi:

```text
0.24
```

A alteração aumenta a sensibilidade do modelo à classe inadimplente, permitindo identificar mais potenciais casos de default em troca de uma redução de Precision e Accuracy.

---

## Modelo final

Com o threshold de `0.24`, o XGBoost otimizado apresentou no conjunto de teste:

| Métrica   | Resultado |
| --------- | --------: |
| Accuracy  |    0,7733 |
| Precision |    0,4899 |
| Recall    |    0,6006 |
| F1-score  |    0,5396 |
| ROC AUC   |    0,7770 |

Matriz de confusão:

```text
                Predito
              0       1
Real  0      3843    830
      1       530    797
```

O modelo identifica **60,06% dos clientes inadimplentes** no conjunto de teste.

A escolha do threshold representa uma decisão orientada ao problema de negócio: aumentar a capacidade de identificação de potenciais inadimplentes, aceitando um aumento nos falsos positivos.

---

# Interpretabilidade

A interpretabilidade do modelo foi explorada utilizando **SHAP (SHapley Additive exPlanations)**.

Entre as variáveis com maior importância para o XGBoost otimizado destacam-se principalmente as variáveis relacionadas ao histórico de pagamentos, especialmente:

```text
PAY_0
PAY_2
PAY_3
...
```

A variável `PAY_0` apresentou a maior importância entre as features avaliadas.

Essa análise permite compreender quais características possuem maior influência nas previsões realizadas pelo modelo.

---

# API

O modelo final foi disponibilizado através de uma API REST desenvolvida com **FastAPI**.

Endpoint principal:

```text
POST /predict
```

A API recebe as características financeiras e cadastrais do cliente e retorna:

* probabilidade de inadimplência;
* threshold utilizado;
* classe prevista;
* classificação textual.

### Exemplo de requisição

```json
{
  "LIMIT_BAL": 20000,
  "SEX": 1,
  "EDUCATION": 2,
  "MARRIAGE": 1,
  "AGE": 24,
  "PAY_0": 2,
  "PAY_2": 2,
  "PAY_3": 0,
  "PAY_4": 0,
  "PAY_5": 0,
  "PAY_6": 0,
  "BILL_AMT1": 3913,
  "BILL_AMT2": 3102,
  "BILL_AMT3": 689,
  "BILL_AMT4": 0,
  "BILL_AMT5": 0,
  "BILL_AMT6": 0,
  "PAY_AMT1": 0,
  "PAY_AMT2": 689,
  "PAY_AMT3": 0,
  "PAY_AMT4": 0,
  "PAY_AMT5": 0,
  "PAY_AMT6": 0
}
```

### Exemplo de resposta

```json
{
  "probability": 0.3297,
  "threshold": 0.24,
  "prediction": 1,
  "classification": "inadimplente"
}
```

A documentação interativa da API é disponibilizada automaticamente pelo FastAPI em:

```text
http://127.0.0.1:8000/docs
```

---

# Validação da API

Foram implementados testes automatizados utilizando `pytest`.

Os testes verificam:

* entrada válida → HTTP `200`;
* entrada inválida, como `SEX = 7` → HTTP `422`.

Exemplo de execução:

```text
collected 2 items

tests/test_api.py ..                                      [100%]

2 passed
```

A validação também utiliza os recursos de validação do Pydantic definidos no schema da API.

---

# Docker

A aplicação foi containerizada utilizando Docker.

A imagem utiliza Python 3.13 e instala apenas as dependências necessárias para execução da API através do arquivo:

```text
requirements-api.txt
```

O container executa a aplicação utilizando Uvicorn:

```text
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Construção da imagem

Na raiz do projeto:

```bash
docker build -t credit-default-api .
```

### Execução

```bash
docker run -d --name credit-default-api-container -p 8000:8000 credit-default-api
```

A API ficará disponível em:

```text
http://localhost:8000
```

A documentação interativa estará disponível em:

```text
http://localhost:8000/docs
```

---

# Estrutura do projeto

```text
credit-default-api/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
│
├── data/
│   └── raw/
│
├── grafics/
│
├── models/
│   ├── decision_tree_baseline.pkl
│   ├── decision_tree_tuned.pkl
│   ├── logistic_regression_pipeline.pkl
│   ├── logistic_regression_tuned_pipeline.pkl
│   ├── random_forest_baseline.pkl
│   ├── random_forest_tuned_pipeline.pkl
│   ├── xgboost_baseline_pipeline.pkl
│   ├── xgboost_tuned_pipeline.pkl
│   ├── xgboost_tuned_feature_importance.csv
│   └── xgboost_tuned_threshold.pkl
│
├── notebooks/
│
├── src/
│   ├── data.py
│   ├── preprocessing.py
│   └── ingestion/
│
├── tests/
│   └── test_api.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements-api.txt
└── requirements.txt
```

---

# Tecnologias

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* SHAP
* Joblib
* FastAPI
* Pydantic
* Uvicorn
* Pytest
* Docker
* Git / GitHub

---

# Próximos passos

O projeto está sendo desenvolvido com foco em transformar o modelo de Machine Learning em uma aplicação utilizável.

As próximas etapas incluem:

* deploy da API;
* desenvolvimento de uma interface gráfica utilizando Streamlit;
* integração da interface com a API;
* disponibilização da aplicação para acesso externo;
* documentação final do projeto e dos resultados.
