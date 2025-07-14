import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.title("INFORME POR COLABORADOR - EVALUACIÓN DE DESEMPEÑO")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Buscador de colaborador como lista desplegable
    nombres = df['Nombres y apellidos del evaluado/a'].dropna().unique()
    selected_name = st.selectbox("Seleccione el nombre del evaluado/a:", nombres)

    if selected_name:
        filtered_df = df[df['Nombres y apellidos del evaluado/a'] == selected_name]

        if not filtered_df.empty:
            person = filtered_df.iloc[0]

            # Mostrar encabezado
            st.subheader("INFORME POR COLABORADOR - EVALUACIÓN DE DESEMPEÑO")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**CEDULA:** {person.get('Número de cédula del evaluado/a', 'No disponible')}")
                st.write(f"**NOMBRE:** {person.get('Nombres y apellidos del evaluado/a', 'No disponible')}")
                st.write(f"**CARGO:** {person.get('Cargo', 'No disponible')}")
                st.write(f"**DEPARTAMENTO:** {person.get('Área / departamento', 'No disponible')}")
            with col2:
                st.write(f"**ÁREA:** {person.get('Área / departamento', 'No disponible')}")
                st.write(f"**EVALUADOR:** {person.get('Nombres y apellidos del evaluador', 'No disponible')}")
                st.write(f"**FECHA DE EVALUACIÓN:** {person.get('Marca temporal', 'No disponible')}")

            # Buscar columnas que contienen "COMPETENCIAS DE GESTIÓN"
            competencia_cols = [col for col in df.columns if "COMPETENCIAS DE GESTIÓN" in col]

            # Extraer nombre de la competencia entre "Competencia: " y "["
            competencias_dict = {}
            for col in competencia_cols:
                match = re.search(r"Competencia:\s*(.*?)\s*\[", col)
                if match:
                    competencia_name = match.group(1).strip()
                    if competencia_name not in competencias_dict:
                        competencias_dict[competencia_name] = []
                    competencias_dict[competencia_name].append(col)

            # Calcular promedio por competencia
            resumen = {}
            for nombre, columnas in competencias_dict.items():
                promedio = person[columnas].mean()
                resumen[nombre] = promedio

            # Crear DataFrame resumen
            resumen_df = pd.DataFrame(list(resumen.items()), columns=['Competencia', 'Puntaje Promedio'])
            resumen_df['Puntaje Promedio'] = resumen_df['Puntaje Promedio'].round(2)

            # Mostrar tabla
            st.subheader("RESULTADOS")
            st.table(resumen_df)

            # Gráfico
            fig, ax = plt.subplots(figsize=(8, 6))
            resumen_df.set_index('Competencia')['Puntaje Promedio'].plot(kind='barh', ax=ax, color='skyblue')
            ax.set_xlabel("Promedio")
            ax.set_xlim(0, 5)  # Limitar de 0 a 5
            ax.set_title("Promedio por competencia (0 a 5)")
            st.pyplot(fig)

            # Compromisos
            st.subheader("COMPROMISOS DE LAS COMPETENCIAS")
            compromisos_cols = [col for col in df.columns if 'Acuerdo - Compromiso' in col]
            compromisos = [str(person[c]) for c in compromisos_cols if pd.notna(person[c])]
            if compromisos:
                for comp in compromisos:
                    st.write(f"- {comp}")
            else:
                st.write("No se registraron compromisos.")

            # Capacitación
            st.subheader("CAPACITACIÓN")
            capacitacion_col = 'En relación al/los tema/s seleccionado/s, escriba que tipo de capacitación se propone'
            if capacitacion_col in person and pd.notna(person[capacitacion_col]):
                # Si tiene varias capacitaciones separadas por comas
                caps = str(person[capacitacion_col]).split(',')
                for cap in caps:
                    st.write(f"- {cap.strip()}")
            else:
                st.write("No se registró capacitación.")
        else:
            st.warning("No se encontró ningún colaborador con ese nombre.")
