import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análisis de Evaluación de Competencias")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Datos cargados:")
    st.dataframe(df.head())

    # Buscar persona por nombre o cédula
    search_option = st.selectbox("Buscar por:", ["Nombres y apellidos del evaluado/a", "Número de cédula del evaluado/a"])
    search_value = st.text_input(f"Ingrese el {search_option}")

    if search_value:
        # Filtrar datos
        filtered_df = df[df[search_option].astype(str).str.contains(search_value, case=False, na=False)]

        if not filtered_df.empty:
            # Mostrar datos de la persona encontrada
            st.subheader("Datos del evaluado/a:")
            st.dataframe(filtered_df)

            # Buscar solo las columnas de competencias (numéricas)
            competencia_cols = filtered_df.select_dtypes(include='number').columns

            if len(competencia_cols) > 0:
                # Calcular promedio si hay varias filas (ejemplo: varias evaluaciones)
                competencias = filtered_df[competencia_cols].mean()

                st.subheader("Calificaciones en competencias:")
                fig, ax = plt.subplots(figsize=(8, 6))
                competencias.sort_values().plot(kind='barh', ax=ax, color='skyblue')
                ax.set_xlabel("Calificación promedio")
                ax.set_ylabel("Competencias")
                ax.set_title("Calificaciones por competencia")
                st.pyplot(fig)
            else:
                st.warning("No se encontraron columnas numéricas de competencias.")
        else:
            st.warning("No se encontró ningún registro con ese valor.")
