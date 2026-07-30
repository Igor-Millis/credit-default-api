import pandas as pd

df = pd.read_excel(
    "C:/Users/T-Gamer/Desktop/igor/credit-default-api/data/raw/default_of_credit_card_clients.xls",
    header=1)

print(df.columns.tolist())

# =====================================================
# Ajuste dos tipos das variáveis
# =====================================================

# Variáveis categóricas nominais
categoricas_nominais = [
    "SEX",
    "MARRIAGE",
    "default payment next month"
]

# Variáveis categóricas ordinais
categoricas_ordinais = [
    "EDUCATION"
]

# Conversão para category
df[categoricas_nominais] = df[categoricas_nominais].astype("category")
df[categoricas_ordinais] = df[categoricas_ordinais].astype("category")

from pandas.api.types import CategoricalDtype

education_order = CategoricalDtype(
    categories=[0, 1, 2, 3, 4, 5, 6],
    ordered=True
)

df["EDUCATION"] = df["EDUCATION"].astype(education_order)

print(df.info())











