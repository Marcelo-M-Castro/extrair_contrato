# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Extrator de Contratos", layout="wide")

st.title("📄 Extrator de Contratos da Descrição")

st.write("Faça upload de uma planilha Excel contendo a coluna **description** e opcionalmente **contractid**.")

# Upload de arquivo
uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])

def extract_8_digit_numbers(text):
    if isinstance(text, str):
        return re.findall(r'\b\d{8}\b', text)
    return []

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Verificação das colunas obrigatórias
    if "description" not in df.columns:
        st.error("❌ O arquivo precisa conter a coluna 'description'.")
    else:
        st.success("✅ Arquivo carregado com sucesso!")

        # Extrai listas de números
        df["extracted_numbers"] = df["description"].apply(extract_8_digit_numbers)

        # Explode a lista em várias linhas
        df = df.explode("extracted_numbers")

        # Renomeia a coluna para clareza
        df = df.rename(columns={"extracted_numbers": "extracted_number"})

        # Converte para inteiro quando possível
        df["extracted_number"] = pd.to_numeric(df["extracted_number"], errors="coerce").astype("Int64")

        # Preenche com contractid se existir
        if "contractid" in df.columns:
            df["extracted_number"] = df["extracted_number"].fillna(df["contractid"])

        # Remove duplicados
        df = df.drop_duplicates(subset=["extracted_number"])

        st.subheader("📊 Resultado da Extração")
        st.dataframe(df)

        # Download do resultado
        output_file = "extracted_numbers.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Baixar Resultado em Excel",
                data=f,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
