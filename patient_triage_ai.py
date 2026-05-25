import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.title("🏥 Triagem Inteligente de Pacientes")

patient = st.text_area(
    "Descreva sintomas e informações do paciente:"
)

if st.button("Realizar Triagem"):

    if not patient.strip():
        st.warning("Informe os dados do paciente.")
        st.stop()

    prompt = f"""
    Analise os dados clínicos abaixo e retorne APENAS um JSON válido com:

    - "nivel_risco": baixo, médio, alto ou crítico
    - "prioridade": 1 a 5
    - "possivel_area": especialidade médica provável
    - "sentimento_paciente": calmo, preocupado ou ansioso
    - "orientacao_inicial": orientação curta
    - "acoes_sugeridas": lista de próximos passos

    Paciente:
    {patient}
    """

    with st.spinner("Analisando paciente..."):

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um sistema de apoio "
                        "à triagem hospitalar. "
                        "Retorne apenas JSON válido."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        try:

            result = json.loads(
                resp.choices[0].message.content
            )

            st.json(result)

            st.subheader("📊 Resultado da Triagem")

            df = pd.DataFrame([result])

            st.dataframe(df)

            st.metric(
                "Prioridade Detectada",
                f"{result['prioridade']}/5"
            )

            st.info(
                "🩺 Orientação Inicial:\n" +
                result["orientacao_inicial"]
            )

        except Exception as e:

            st.error(
                f"Erro ao processar JSON: {e}"
            )