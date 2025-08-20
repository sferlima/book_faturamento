import subprocess
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Consolidador de Planilhas", layout="centered")

st.title("📊 Consolidador de Planilhas")

#upload dos arquivos
file1 = st.file_uploader("Upload da Planilha 1", type=["xlsx"])
if file1: st.write(f"✅ Arquivo 1 enviado: **{file1.name}**")

file2 = st.file_uploader("Upload da Planilha 2", type=["xlsx"])
if file2: st.write(f"✅ Arquivo 2 enviado: **{file2.name}**")

file3 = st.file_uploader("Upload da Planilha 3", type=["xlsx"])
if file3: st.write(f"✅ Arquivo 3 enviado: **{file3.name}**")


#consolidação das planilhas com o book_faturamento.py
if file1 and file2 and file3:
    if st.button("🔄 Consolidar planilhas"):
        
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        df3 = pd.read_excel(file3)

        subprocess.run(["python", "book_faturamento.py", file1, file2, file3])
        df_final = pd.read_excel("consolidacao.xlsx")
        
        st.subheader("Pre-visualização")
        st.dataframe(df_final.head(10))  

        
        output = BytesIO()
        df_final.to_excel(output, index=False)
        output.seek(0)

        st.download_button(
            label="⬇️ Baixar planilha consolidada",
            data=output,
            file_name="consolidacao.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
