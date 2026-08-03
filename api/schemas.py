from typing import Literal

from pydantic import BaseModel, Field


class CreditDefaultRequest(BaseModel):
    """
    Dados de entrada para previsão de inadimplência.
    """

    LIMIT_BAL: int = Field(
        ...,
        description="Limite de crédito concedido"
    )

    SEX: Literal[1, 2] = Field(
        ...,
        description="Sexo do cliente"
    )

    EDUCATION: Literal[0, 1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Nível de escolaridade"
    )

    MARRIAGE: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Estado civil"
    )

    AGE: int = Field(
        ...,
        description="Idade do cliente"
    )

    PAY_0: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em setembro"
    )

    PAY_2: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em agosto"
    )

    PAY_3: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em julho"
    )

    PAY_4: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em junho"
    )

    PAY_5: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em maio"
    )

    PAY_6: Literal[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8] = Field(
        ...,
        description="Status de pagamento em abril"
    )

    BILL_AMT1: int = Field(
        ...,
        description="Valor da fatura em setembro"
    )

    BILL_AMT2: int = Field(
        ...,
        description="Valor da fatura em agosto"
    )

    BILL_AMT3: int = Field(
        ...,
        description="Valor da fatura em julho"
    )

    BILL_AMT4: int = Field(
        ...,
        description="Valor da fatura em junho"
    )

    BILL_AMT5: int = Field(
        ...,
        description="Valor da fatura em maio"
    )

    BILL_AMT6: int = Field(
        ...,
        description="Valor da fatura em abril"
    )

    PAY_AMT1: int = Field(
        ...,
        description="Valor pago em setembro"
    )

    PAY_AMT2: int = Field(
        ...,
        description="Valor pago em agosto"
    )

    PAY_AMT3: int = Field(
        ...,
        description="Valor pago em julho"
    )

    PAY_AMT4: int = Field(
        ...,
        description="Valor pago em junho"
    )

    PAY_AMT5: int = Field(
        ...,
        description="Valor pago em maio"
    )

    PAY_AMT6: int = Field(
        ...,
        description="Valor pago em abril"
    )