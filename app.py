import streamlit as st
import pandas as pd
import os
from book_faturamento import consolidar_planilhas

st.set_page_config(page_title="Consolidador de Planilhas", layout="centered")
st.title("📊 Consolidador de Planilhas")

# Criar diretório upload/ caso não exista
UPLOAD_DIR = "upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload
file1 = st.file_uploader("Upload da Planilha: Dados Cadastrais", type=["xlsx"])
file2 = st.file_uploader("Upload da Planilha: Férias", type=["xlsx"])
file3 = st.file_uploader("Upload da Planilha: Demitidos", type=["xlsx"])

if file1 and file2 and file3:
    if st.button("🔄 Consolidar planilhas"):
        try:
            # Salvar arquivos no diretório upload/
            path1 = os.path.join(UPLOAD_DIR, "dados_cadastrais.xlsx")
            path2 = os.path.join(UPLOAD_DIR, "ferias.xlsx")
            path3 = os.path.join(UPLOAD_DIR, "demitidos.xlsx")

            with open(path1, "wb") as f:
                f.write(file1.getbuffer())
            with open(path2, "wb") as f:
                f.write(file2.getbuffer())
            with open(path3, "wb") as f:
                f.write(file3.getbuffer())

            # Consolidar
            output_path = os.path.join(UPLOAD_DIR, "consolidacao.xlsx")
            df_final = consolidar_planilhas(path1, path2, path3, output_path)

            # Mostrar resultado
            st.success("✅ Consolidação concluída!")
            st.dataframe(df_final)

            # Botão para download
            st.download_button(
                label="⬇️ Baixar consolidação",
                data=open(output_path, "rb").read(),
                file_name="consolidacao.xlsx"
            )

        except Exception as e:
            st.error(f"❌ Erro ao consolidar: {e}")
