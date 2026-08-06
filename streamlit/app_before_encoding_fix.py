import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/predict"
THRESHOLD = 0.24

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="ðŸ’³",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">ðŸ’³ Credit Default Prediction</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Sistema de previsÃ£o de inadimplÃªncia para clientes "
    "de cartÃ£o de crÃ©dito."
    "</div>",
    unsafe_allow_html=True,
)

st.info(
    "O sistema utiliza um modelo XGBoost treinado sobre dados "
    "histÃ³ricos de clientes de cartÃ£o de crÃ©dito. "
    "A previsÃ£o Ã© realizada atravÃ©s de uma API FastAPI."
)

with st.form("prediction_form"):

    st.subheader("ðŸ‘¤ InformaÃ§Ãµes do cliente")

    col1, col2, col3 = st.columns(3)

    with col1:
        limit_bal = st.number_input(
            "Limite de crÃ©dito (R$)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
        )

    with col2:
        age = st.number_input(
            "Idade",
            min_value=18,
            max_value=100,
            value=30,
        )

    with col3:
        sex = st.selectbox(
            "Sexo",
            options=[1, 2],
            format_func=lambda x: (
                "Masculino" if x == 1 else "Feminino"
            ),
        )

    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox(
            "NÃ­vel de educaÃ§Ã£o",
            options=[0, 1, 2, 3, 4, 5, 6],
            format_func=lambda x: {
                0: "Desconhecido",
                1: "PÃ³s-graduaÃ§Ã£o",
                2: "Universidade",
                3: "Ensino mÃ©dio",
                4: "Outros",
                5: "Outros",
                6: "Desconhecido",
            }[x],
        )

    with col2:
        marriage = st.selectbox(
            "Estado civil",
            options=[0, 1, 2, 3],
            format_func=lambda x: {
                0: "Desconhecido",
                1: "Casado",
                2: "Solteiro",
                3: "Outros",
            }[x],
        )

    st.divider()
    st.subheader("ðŸ“Š HistÃ³rico de pagamentos")

    st.caption(
        "Valores negativos indicam ausÃªncia de atraso ou "
        "situaÃ§Ãµes especÃ­ficas registradas no conjunto de dados."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        pay_0 = st.number_input(
            "Status de pagamento â€” mÃªs atual",
            min_value=-2,
            max_value=8,
            value=0,
        )

        pay_2 = st.number_input(
            "Status de pagamento â€” 2 meses atrÃ¡s",
            min_value=-2,
            max_value=8,
            value=0,
        )

    with col2:
        pay_3 = st.number_input(
            "Status de pagamento â€” 3 meses atrÃ¡s",
            min_value=-2,
            max_value=8,
            value=0,
        )

        pay_4 = st.number_input(
            "Status de pagamento â€” 4 meses atrÃ¡s",
            min_value=-2,
            max_value=8,
            value=0,
        )

    with col3:
        pay_5 = st.number_input(
            "Status de pagamento â€” 5 meses atrÃ¡s",
            min_value=-2,
            max_value=8,
            value=0,
        )

        pay_6 = st.number_input(
            "Status de pagamento â€” 6 meses atrÃ¡s",
            min_value=-2,
            max_value=8,
            value=0,
        )

    st.divider()
    st.subheader("ðŸ’° Valores das faturas")

    bill_cols = st.columns(3)

    with bill_cols[0]:
        bill_amt1 = st.number_input(
            "Fatura â€” mÃªs atual (R$)",
            value=0.0,
        )

        bill_amt2 = st.number_input(
            "Fatura â€” mÃªs anterior (R$)",
            value=0.0,
        )

    with bill_cols[1]:
        bill_amt3 = st.number_input(
            "Fatura â€” 3 meses atrÃ¡s (R$)",
            value=0.0,
        )

        bill_amt4 = st.number_input(
            "Fatura â€” 4 meses atrÃ¡s (R$)",
            value=0.0,
        )

    with bill_cols[2]:
        bill_amt5 = st.number_input(
            "Fatura â€” 5 meses atrÃ¡s (R$)",
            value=0.0,
        )

        bill_amt6 = st.number_input(
            "Fatura â€” 6 meses atrÃ¡s (R$)",
            value=0.0,
        )

    st.divider()
    st.subheader("ðŸ’µ Valores pagos")

    pay_cols = st.columns(3)

    with pay_cols[0]:
        pay_amt1 = st.number_input(
            "Pagamento â€” mÃªs atual (R$)",
            min_value=0.0,
            value=0.0,
        )

        pay_amt2 = st.number_input(
            "Pagamento â€” mÃªs anterior (R$)",
            min_value=0.0,
            value=0.0,
        )

    with pay_cols[1]:
        pay_amt3 = st.number_input(
            "Pagamento â€” 3 meses atrÃ¡s (R$)",
            min_value=0.0,
            value=0.0,
        )

        pay_amt4 = st.number_input(
            "Pagamento â€” 4 meses atrÃ¡s (R$)",
            min_value=0.0,
            value=0.0,
        )

    with pay_cols[2]:
        pay_amt5 = st.number_input(
            "Pagamento â€” 5 meses atrÃ¡s (R$)",
            min_value=0.0,
            value=0.0,
        )

        pay_amt6 = st.number_input(
            "Pagamento â€” 6 meses atrÃ¡s (R$)",
            min_value=0.0,
            value=0.0,
        )

    st.divider()

    submitted = st.form_submit_button(
        "ðŸ”Ž Realizar previsÃ£o",
        type="primary",
        use_container_width=True,
    )

if submitted:

    payload = {
        "LIMIT_BAL": limit_bal,
        "SEX": sex,
        "EDUCATION": education,
        "MARRIAGE": marriage,
        "AGE": age,
        "PAY_0": pay_0,
        "PAY_2": pay_2,
        "PAY_3": pay_3,
        "PAY_4": pay_4,
        "PAY_5": pay_5,
        "PAY_6": pay_6,
        "BILL_AMT1": bill_amt1,
        "BILL_AMT2": bill_amt2,
        "BILL_AMT3": bill_amt3,
        "BILL_AMT4": bill_amt4,
        "BILL_AMT5": bill_amt5,
        "BILL_AMT6": bill_amt6,
        "PAY_AMT1": pay_amt1,
        "PAY_AMT2": pay_amt2,
        "PAY_AMT3": pay_amt3,
        "PAY_AMT4": pay_amt4,
        "PAY_AMT5": pay_amt5,
        "PAY_AMT6": pay_amt6,
    }

    with st.spinner("Consultando o modelo..."):

        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=10,
            )

            if response.status_code == 200:

                result = response.json()

                probability = result["probability"]
                prediction = result["prediction"]

                st.divider()
                st.subheader("ðŸ“ˆ Resultado da previsÃ£o")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Probabilidade de inadimplÃªncia",
                        f"{probability:.2%}",
                    )

                with col2:
                    st.metric(
                        "Threshold",
                        f"{result['threshold']:.2f}",
                    )

                with col3:
                    status = (
                        "Inadimplente"
                        if prediction == 1
                        else "Adimplente"
                    )

                    st.metric(
                        "ClassificaÃ§Ã£o",
                        status,
                    )

                st.write("Probabilidade estimada")

                st.progress(
                    min(probability, 1.0),
                    text=f"{probability:.2%}",
                )

                if prediction == 1:
                    st.error(
                        "âš ï¸ O modelo classificou este cliente "
                        "como **inadimplente**."
                    )
                else:
                    st.success(
                        "âœ… O modelo classificou este cliente "
                        "como **adimplente**."
                    )

                with st.expander(
                    "â„¹ï¸ Como a classificaÃ§Ã£o Ã© determinada?"
                ):

                    st.write(
                        f"O modelo estima uma probabilidade de "
                        f"inadimplÃªncia de **{probability:.2%}**."
                    )

                    st.write(
                        f"A classificaÃ§Ã£o utiliza um threshold de "
                        f"**{THRESHOLD:.2f} ({THRESHOLD:.0%})**."
                    )

                    if probability >= THRESHOLD:
                        st.write(
                            "Como a probabilidade estimada estÃ¡ "
                            "acima do threshold, o cliente foi "
                            "classificado como inadimplente."
                        )
                    else:
                        st.write(
                            "Como a probabilidade estimada estÃ¡ "
                            "abaixo do threshold, o cliente foi "
                            "classificado como adimplente."
                        )

            else:
                st.error(
                    f"A API retornou um erro "
                    f"(HTTP {response.status_code})."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "âŒ NÃ£o foi possÃ­vel conectar Ã  API."
            )

            st.info(
                "Verifique se o container da FastAPI estÃ¡ "
                "em execuÃ§Ã£o na porta 8000."
            )

        except requests.exceptions.Timeout:
            st.error(
                "â±ï¸ A API demorou muito para responder."
            )

        except requests.exceptions.RequestException as error:
            st.error(
                f"Erro ao realizar a requisiÃ§Ã£o: {error}"
            )

st.divider()

st.caption(
    "Projeto de Machine Learning â€” Credit Default Prediction | "
    "XGBoost + FastAPI + Streamlit"
)
