import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Análisis de Evaluación de Competencias")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Datos cargados:")
    st.dataframe(df.head())

    # Aquí puedes agregar más análisis y gráficos
    st.write("Estadísticas descriptivas:")
    st.write(df.describe())

    # Ejemplo gráfico simple
    st.write("Histograma de la primera columna numérica:")
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        fig, ax = plt.subplots()
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)
