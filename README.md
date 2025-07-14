# THData

Repositorio para el análisis de evaluación de competencias utilizando Streamlit.

### IMPORTANTE:
La app.py tiene actualizaciones por lo que se recomienda cambiar ese archivo en su ruta o clon de git creado en su equipo

---

## Estructura del proyecto

- `app.py` : Aplicación principal.
- `modules/` : Módulos y lógica auxiliar.
- `data/` : Datos de prueba.
- `requirements.txt` : Archivo con las dependencias necesarias.

---

## Configuración del entorno de desarrollo

Para garantizar la correcta ejecución de la aplicación, se recomienda crear un entorno virtual aislado y proceder con la instalación de las dependencias.

### 1. Clonación del repositorio

Ejecute el siguiente comando para clonar el repositorio localmente:

```bash
git clone https://github.com/KrlaMngs/THData.git
cd THData

```

### 2. Crear y activar el entorno virtual
Windows
```bash
python -m venv venv
venv\Scripts\activate
```
MacOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Instalar las dependencias
Con el entorno virtual activado, instale las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```
### 4. Ejecutar la aplicación
Inicie la aplicación Streamlit con el siguiente comando:
```bash
streamlit run app.py
```

Luego, abra la URL que aparecerá en la terminal (por defecto http://localhost:8501) en su navegador para interactuar con la aplicación.

### Uso de la aplicación
La aplicación permite cargar un archivo Excel con datos de evaluación de competencias, mostrando una vista previa, estadísticas descriptivas y gráficos básicos para el análisis.

### Notas adicionales
Asegúrese de mantener activado el entorno virtual mientras trabaje con la aplicación para evitar conflictos de dependencias.

Autor: Karla Andrea Calderon Faicann
