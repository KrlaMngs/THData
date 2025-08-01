import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from fpdf import FPDF
import tempfile

def generar_pdf(nombre, resumen, interpretacion, grafico_path, compromisos=None, fecha=None, capacitaciones=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Informe de Evaluación por Competencias", ln=True, align='C')
    pdf.ln(10)

    # Datos del evaluado
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Evaluado: {nombre}", ln=True)
    if fecha:
        pdf.cell(0, 10, f"Fecha de Evaluación: {fecha}", ln=True)
    pdf.ln(5)

    # Resultados
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Resultados por competencia:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", '', 11)
    for i, row in resumen.iterrows():
        competencia = row['Competencia']
        descripcion = row['Descripción']
        puntuacion = row['Puntaje']
        pdf.multi_cell(0, 10, f"{i+1}. {competencia}: {descripcion} (Puntaje: {puntuacion})")
        pdf.ln(2)

    # Gráfico
    if grafico_path:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Gráfico de Resultados:", ln=True)
        pdf.image(grafico_path, x=10, w=pdf.w - 20)
        pdf.ln(10)

    # Compromisos
    if compromisos:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Compromisos:", ln=True)
        pdf.set_font("Arial", '', 11)
        for comp in compromisos:
            pdf.multi_cell(0, 10, f"- {comp} ({fecha})")
        pdf.ln(5)

    # Capacitación
    if capacitaciones:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Capacitación Propuesta:", ln=True)
        pdf.set_font("Arial", '', 11)
        for cap in capacitaciones:
            pdf.multi_cell(0, 10, f"- {cap}")
        pdf.ln(5)

    # Interpretación
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Interpretación y Recomendaciones:", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, interpretacion)

    # Guardar PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- Streamlit app ---
st.set_page_config(page_title="Evaluación de Desempeño", layout="centered")
st.title("INFORME POR COLABORADOR - EVALUACIÓN DE DESEMPEÑO")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    nombres = df['Nombres y apellidos del evaluado/a'].dropna().unique()
    selected_name = st.selectbox("Seleccione el nombre del evaluado/a:", nombres)

    if selected_name:
        filtered_df = df[df['Nombres y apellidos del evaluado/a'] == selected_name]

        if not filtered_df.empty:
            person = filtered_df.iloc[0]
            fecha_eval = str(person.get('Marca temporal', 'Fecha no disponible'))

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
                st.write(f"**FECHA DE EVALUACIÓN:** {fecha_eval}")

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

            # Guardar gráfico
            grafico_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.savefig(grafico_temp.name, bbox_inches="tight")

            st.subheader("COMPROMISOS DE LAS COMPETENCIAS")
            compromisos_cols = [col for col in df.columns if 'Acuerdo - Compromiso' in col]
            compromisos = [str(person[c]) for c in compromisos_cols if pd.notna(person[c])]
            if compromisos:
                for comp in compromisos:
                    st.write(f"- {comp}")
            else:
                st.write("No se registraron compromisos.")

            st.subheader("CAPACITACIÓN")
            capacitacion_col = 'En relación al/los tema/s seleccionado/s, escriba que tipo de capacitación se propone'
            caps = []
            if capacitacion_col in person and pd.notna(person[capacitacion_col]):
                caps = str(person[capacitacion_col]).split(',')
                for cap in caps:
                    st.write(f"- {cap.strip()}")
            else:
                st.write("No se registró capacitación.")

            st.subheader("ANÁLISIS Y RECOMENDACIÓN AUTOMÁTICA")

            if promedio_final < 3:
                st.write("🔴 **Alerta:** El promedio del colaborador es menor a 3, indicando un desempeño bajo.")
                peores = resumen_df.nsmallest(2, 'Puntaje Promedio')
                st.write("Se recomienda capacitación inmediata en:")
                for comp in peores['Competencia']:
                    st.write(f"- {comp}")
                interpretacion = "Desempeño bajo. Capacitación urgente recomendada en:\n" + \
                                 "\n".join(f"- {comp}" for comp in peores['Competencia'])

            elif 3 <= promedio_final < 4.5:
                st.write("🟠 **Observación:** Nivel medio de desempeño.")
                peores = resumen_df.nsmallest(2, 'Puntaje Promedio')
                st.write("Competencias a reforzar:")
                for comp in peores['Competencia']:
                    st.write(f"- {comp}")
                interpretacion = "Nivel medio. Reforzar competencias:\n" + \
                                 "\n".join(f"- {comp}" for comp in peores['Competencia'])

            else:
                st.write("🟢 **Excelente:** Promedio alto.")
                mejores = resumen_df[resumen_df['Puntaje Promedio'] == 5]
                if not mejores.empty:
                    st.write("Competencias destacadas:")
                    for comp in mejores['Competencia']:
                        st.write(f"- {comp}: {descripciones_dict.get(comp)} (Puntaje: 5)")
                interpretacion = "Excelente desempeño. Considerar para desarrollo y liderazgo.\n" + \
                                 "\n".join(f"- {comp}: {descripciones_dict.get(comp)}" for comp in mejores['Competencia'])

            # Preparar para PDF
            resumen_df_pdf = resumen_df.copy()
            resumen_df_pdf["Descripción"] = resumen_df_pdf["Competencia"].map(descripciones_dict)
            resumen_df_pdf = resumen_df_pdf.rename(columns={"Puntaje Promedio": "Puntaje"})

            pdf_file_path = generar_pdf(
                selected_name,
                resumen_df_pdf,
                interpretacion,
                grafico_temp.name,
                compromisos=compromisos,
                fecha=fecha_eval,
                capacitaciones=[c.strip() for c in caps]
            )

            with open(pdf_file_path, "rb") as f:
                st.download_button(
                    label="📄 Descargar Informe en PDF",
                    data=f,
                    file_name=f"Informe_Evaluacion_{selected_name}.pdf",
                    mime="application/pdf"
                )
