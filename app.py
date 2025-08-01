import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Evaluación de Desempeño", layout="centered")
st.title("INFORME POR COLABORADOR - EVALUACIÓN DE DESEMPEÑO")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Selectbox para elegir evaluado
    nombres = df['Nombres y apellidos del evaluado/a'].dropna().unique()
    selected_name = st.selectbox("Seleccione el nombre del evaluado/a:", nombres)

    if selected_name:
        filtered_df = df[df['Nombres y apellidos del evaluado/a'] == selected_name]

        if not filtered_df.empty:
            person = filtered_df.iloc[0]

            st.subheader("DATOS DEL EVALUADO")
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

            # Buscar columnas con competencias
            competencia_cols = [col for col in df.columns if "COMPETENCIAS DE GESTIÓN" in col]

            competencias_dict = {}
            descripciones_dict = {}
            for col in competencia_cols:
                match = re.search(r"Competencia:\s*(.*?)\s*\[(.*?)\]", col)
                if match:
                    nombre = match.group(1).strip()
                    descripcion = match.group(2).strip()
                    if nombre not in competencias_dict:
                        competencias_dict[nombre] = []
                        descripciones_dict[nombre] = descripcion
                    competencias_dict[nombre].append(col)

            # Calcular promedios
            resumen = {}
            for nombre, columnas in competencias_dict.items():
                promedio = person[columnas].mean()
                resumen[nombre] = promedio

            resumen_df = pd.DataFrame(list(resumen.items()), columns=['Competencia', 'Puntaje Promedio'])
            resumen_df['Puntaje Promedio'] = resumen_df['Puntaje Promedio'].round(2)
            resumen_df.index = range(1, len(resumen_df) + 1)

            st.subheader("RESULTADOS")
            st.table(resumen_df)

            promedio_final = resumen_df['Puntaje Promedio'].mean().round(2)
            st.markdown(f"**Promedio general de competencias:** {promedio_final}")

            # Gráfico visual mejorado
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(resumen_df.index, resumen_df['Puntaje Promedio'], color="#4c72b0")
            ax.set_xlim(0, 5)
            ax.set_xlabel("Puntaje Promedio")
            ax.set_title("Promedio por Competencia (Escala 0 a 5)")
            ax.set_yticks(resumen_df.index)
            ax.set_yticklabels([f"{i}. {comp}" for i, comp in zip(resumen_df.index, resumen_df['Competencia'])])
            for bar, score in zip(bars, resumen_df['Puntaje Promedio']):
                ax.text(score + 0.05, bar.get_y() + bar.get_height() / 2,
                        f"{score}", va='center', fontsize=10)
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
                caps = str(person[capacitacion_col]).split(',')
                for cap in caps:
                    st.write(f"- {cap.strip()}")
            else:
                st.write("No se registró capacitación.")

            # Análisis e interpretación automática
            st.subheader("ANÁLISIS Y RECOMENDACIÓN AUTOMÁTICA")

            if promedio_final < 3:
                st.write("🔴 **Alerta:** El promedio del colaborador es menor a 3, indicando un desempeño bajo.")
                peores = resumen_df.nsmallest(2, 'Puntaje Promedio')
                st.write("Se recomienda una capacitación inmediata en las siguientes competencias:")
                for comp in peores['Competencia']:
                    st.write(f"- {comp}")

            elif 3 <= promedio_final < 4.5:
                st.write("🟠 **Observación:** El colaborador tiene un nivel medio de desempeño (promedio entre 3 y 4.4).")
                st.write("Se recomienda continuar reforzando competencias clave para mejorar el rendimiento.")
                peores = resumen_df.nsmallest(2, 'Puntaje Promedio')
                st.write("Competencias a mejorar:")
                for comp in peores['Competencia']:
                    st.write(f"- {comp}")

            else:
                st.write("🟢 **Excelente:** El colaborador tiene un promedio alto (4.5 o más).")
                st.write("Se recomienda seguir potenciando sus habilidades y considerar su perfil para promociones o mayor responsabilidad.")
                mejores = resumen_df[resumen_df['Puntaje Promedio'] == 5]
                if not mejores.empty:
                    st.write("Competencias destacadas:")
                    for comp in mejores['Competencia']:
                        descripcion = descripciones_dict.get(comp, "")
                        st.write(f"- **{comp}**: {descripcion} (Puntaje: 5)")
