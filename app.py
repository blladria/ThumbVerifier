import streamlit as st
import os
from PIL import Image
import io
import sys

# Importar nuestras utilidades
from utils_c2pa import extract_thumbnail, test_c2patool

brutalist_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

body {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
    background-color: #343a40 !important; /* Color de fondo oscuro */
    color: white !important; /* Texto blanco por defecto */
}

.stApp {
    background-color: #343a40 !important; /* Color de fondo oscuro para la app */
}

/* Títulos gigantes y brutales */
.main .block-container {
    padding-top: 2rem !important;
}

h1 {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
    font-size: 3.5rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    border: 3px solid black !important;
    padding: 1rem !important;
    background-color: #e0e0e0 !important; /* Gris flojo para el fondo del título */
    color: black !important; /* Texto del título en negro */
    margin-bottom: 2rem !important;
}

h2 {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    border: 2px solid black !important;
    padding: 0.5rem !important;
    background-color: #e0e0e0 !important; /* Gris flojo para h2 */
    color: black !important; /* Texto negro para h2 */
    margin: 1rem 0 !important;
}

h3 {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid black !important;
    padding-bottom: 0.5rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1.5rem !important;
    color: black !important; /* Asegura que el texto h3 sea negro */
}

/* Bordes brutales para todo */
.stTextInput > div > div > input,
.stFileUploader > div,
.stButton > button,
.stDataFrame {
    border: 2px solid black !important;
    border-radius: 0 !important;
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
}

/* Botones brutales */
.stButton > button {
    background-color: black !important;
    color: white !important;
    border: 2px solid black !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background-color: white !important;
    color: black !important;
    border: 2px solid black !important;
}

/* Métricas en cajas */
.stMetric {
    border: 2px solid black !important;
    background-color: #e0e0e0 !important; /* Gris flojo para métricas */
    padding: 1rem !important;
    border-radius: 0 !important;
    color: black !important; /* Texto negro para métricas */
}

.stMetric > div > div > div {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
    font-weight: 700 !important;
    color: black !important; /* Asegura texto negro en métricas */
}

/* Imágenes en cajas */
.stImage > div {
    border: 2px solid black !important;
    background-color: white !important;
    padding: 0.5rem !important;
}

/* Columnas con bordes */
.stColumns > div {
    border: 2px solid black !important;
    padding: 1rem !important;
    background-color: #e0e0e0 !important; /* Gris flojo para columnas */
    margin: 0.5rem !important;
    color: black !important; /* Texto negro en columnas */
}

/* Alertas personalizadas */
.brutal-success {
    border: 2px solid black !important;
    background-color: white !important;
    color: black !important;
    padding: 1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
}

.brutal-error {
    border: 2px solid black !important;
    background-color: #000000 !important;
    color: white !important;
    padding: 1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
}

.brutal-info {
    border: 2px solid black !important;
    background-color: #f0f2f6 !important;
    color: black !important;
    padding: 1rem !important;
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
}

/* Texto normal */
p, div, span {
    font-family: 'Roboto Mono', 'Courier New', monospace !important;
}

/* File uploader brutal */
.stFileUploader > div > div {
    border: 2px solid black !important;
    background-color: #f5f5f5 !important; /* Gris flojo para el uploader */
    padding: 1rem !important;
    color: black !important; /* Texto negro para mejor contraste */
}

.stFileUploader > div > div > button {
    background-color: black !important;
    color: white !important;
    border: 2px solid black !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
}

.stFileUploader > div > div > button:hover {
    background-color: white !important;
    color: black !important;
    border: 2px solid black !important;
}

/* Spinner brutal */
.stSpinner > div {
    border: 2px solid black !important;
    border-top: 2px solid white !important;
}
</style>
"""

# Inyectar CSS 
st.markdown(brutalist_css, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(
    page_title="THUMB VERIFIER",
    page_icon="",
    layout="wide"
)

def main():
    st.title("THUMB VERIFIER // C2PA INTEGRITY")
    st.markdown("""
    <div class="brutal-info">
    <strong>SISTEMA DE VALIDACIÓN DE INTEGRIDAD SEMÁNTICA</strong><br>
    COMPARACIÓN DE IMAGEN DE ALTA RESOLUCIÓN (QUERY) VS MINIATURA FIRMADA (THUMBNAIL)<br>
    INCUSTADA EN MANIFIESTO C2PA PARA DETECCIÓN DE MANIPULACIONES
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar que c2patool está disponible
    if not test_c2patool():
        st.markdown("""
        <div class="brutal-error">
        ESTADO: FALLO DEL SISTEMA<br>
        C2PATool.EXE NO ENCONTRADO O NO FUNCIONA<br>
        ASEGÚRESE DE QUE ESTÁ EN EL DIRECTORIO RAÍZ DEL PROYECTO
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Widget para subir archivo
    uploaded_file = st.file_uploader(
        "SUBIR ARCHIVO DE IMAGEN PARA ANÁLISIS",
        type=['jpg', 'jpeg', 'png', 'tiff', 'webp'],
        help="Subir imagen que contenga manifiesto C2PA"
    )
    
    if uploaded_file is not None:
        # Mostrar información del archivo
        st.markdown("### INFORMACIÓN DEL ARCHIVO")
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.metric("NOMBRE", uploaded_file.name)
        with col_info2:
            st.metric("TAMAÑO", f"{uploaded_file.size / 1024:.1f} KB")
        with col_info3:
            st.metric("TIPO", uploaded_file.type)
        
        # Guardar temporalmente el archivo subido
        temp_input_path = f"temp_{uploaded_file.name}"
        with open(temp_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extraer miniatura
        st.markdown("### EXTRACCIÓN DE MINIATURA C2PA")
        
        with st.spinner("EXTRAYENDO MINIATURA DEL MANIFIESTO C2PA..."):
            thumbnail_img = extract_thumbnail(temp_input_path)
        
        # Mostrar resultados en dos columnas
        st.markdown("### COMPARACIÓN VISUAL")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**IMAGEN ORIGINAL**")
            # Mostrar imagen original
            original_img = Image.open(uploaded_file)
            st.image(original_img, width='stretch')
            st.caption(f"Dimensiones: {original_img.size}")
        
        with col2:
            st.markdown("**MINIATURA FIRMADA (REFERENCIA C2PA)**")
            if thumbnail_img:
                st.image(thumbnail_img, width='stretch')
                st.caption(f"Dimensiones: {thumbnail_img.size}")
                st.markdown("""
                <div class="brutal-success">
                ESTADO: VERIFICADO<br>
                MINIATURA EXTRAÍDA EXITOSAMENTE
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="brutal-error">
                ESTADO: FALLO<br>
                NO SE PUDO EXTRAER LA MINIATURA
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class="brutal-info">
                <strong>CAUSAS PROBABLES:</strong><br>
                • LA IMAGEN NO TIENE MANIFIESTO C2PA<br>
                • EL MANIFIESTO NO CONTIENE MINIATURA<br>
                • FORMATO DE MANIFIESTO NO COMPATIBLE
                </div>
                """, unsafe_allow_html=True)
        
        # Limpiar archivo temporal
        try:
            os.remove(temp_input_path)
        except:
            pass
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="brutal-info">
    <strong>MÓDULO 1: EXTRACCIÓN DE MINIATURA Y UI BASE</strong><br>
    PRÓXIMOS MÓDULOS: MÉTRICAS CLÁSICAS → CRYPTO-ML (LPIPS/CLIP)
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
