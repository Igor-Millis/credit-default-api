"""
Módulo responsável pelo pré-processamento dos dados.

Autor: Igor Millis
Projeto: Credit Default API
"""

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def create_preprocessor():

    """
    Cria o pipeline de pré-processamento utilizado
    por todos os modelos do projeto.

    Returns
    -------
    ColumnTransformer
        Pipeline de pré-processamento.
    """

    # ==========================
    # Variáveis
    # ==========================

    numeric_features = [
        "LIMIT_BAL",
        "AGE",
        "BILL_AMT1",
        "BILL_AMT2",
        "BILL_AMT3",
        "BILL_AMT4",
        "BILL_AMT5",
        "BILL_AMT6",
        "PAY_AMT1",
        "PAY_AMT2",
        "PAY_AMT3",
        "PAY_AMT4",
        "PAY_AMT5",
        "PAY_AMT6",
    ]

    categorical_features = [
        "SEX",
        "EDUCATION",
        "MARRIAGE",
    ]

    ordinal_features = [
        "PAY_0",
        "PAY_2",
        "PAY_3",
        "PAY_4",
        "PAY_5",
        "PAY_6",
    ]

    # ==========================
    # Transformações
    # ==========================

    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            )
        ]
    )

    # ==========================
    # ColumnTransformer
    # ==========================

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "num",
                numeric_transformer,
                numeric_features
            ),

            (
                "cat",
                categorical_transformer,
                categorical_features
            ),

            (
                "ord",
                "passthrough",
                ordinal_features
            ),

        ]

    )

    return preprocessor