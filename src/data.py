"""
Funções para leitura e preparação dos dados.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def load_data():

    """
    Carrega o dataset bruto.
    """

    project_root = Path(__file__).resolve().parent.parent

    file_path = (
        project_root /
        "data" /
        "raw" /
        "default_of_credit_card_clients.xls"
    )

    df = pd.read_excel(
        file_path,
        header=1
    )

    return df


def split_data(
    df,
    test_size=0.20,
    random_state=42
):

    """
    Divide o dataset em treino e teste.
    """

    X = df.drop(
        columns=["default payment next month"]
    )

    y = df["default payment next month"]

    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )