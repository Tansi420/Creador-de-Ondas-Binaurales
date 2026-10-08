import os
import time
import glob
import base64
from gtts import gTTS
from PIL import Image
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Creador de Ondas Binaurales",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para un aspecto moderno y relajante
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        background-color: #4a90e2;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357abd;
        border-color: #357abd;
    }
    .wave-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #4a90e2;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2b6cb0;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎧 Guía de Sesión")
    st.info(
        "1. Selecciona o copia una de las **plantillas de ondas** recomendadas.\n"
        "2. Pégala en el campo de texto principal.\n"
        "3. Elige el idioma de síntesis de voz.\n"
        "4. Haz clic en **'Convertir a Audio'** para escuchar y descargar."
    )
    st.markdown("---")
    try:
        image = Image.open('monoaural.jpg')
        st.image(image, width=250, caption="Frecuencias Binaurales")
    except Exception:
        st.warning("Imagen 'monoaural.jpg' no encontrada.")
    st.markdown("---")
    st.success("Estado: Listo para relajar 🌊")

# ---------------------------------------------------------
# CABECERA PRINCIPAL
# ---------------------------------------------------------
st.title("🎧 Creador de Ondas Binaurales y Vocales")
st.markdown(
    "<p style='font-size: 17px; color: #555;'>Transforma secuencias de vocales y fonemas en ritmos constantes ideales para meditar, estudiar o practicar instrumentos musicales.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# Crear directorio temporal de forma segura
try:
    os.makedirs("temp", exist_ok=True)
except Exception:
    pass

# ---------------------------------------------------------
# PLANTILLAS DE ONDAS
# ---------------------------------------------------------
st.subheader("✨ Plantillas de Ondas Recomendadas")
st.write("Puedes copiar cualquiera de estas secuencias y hacerlas tan largas como quieras duplicándolas:")

# Tarjetas visuales para las plantillas
st.markdown("""
<div class="wave-card">
    <b>Onda 1 (Ritmo Constante / Estudiar):</b><br>
    <code style="color: #d63384;">mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm</code>
</div>

<div class="wave-card" style="border-left-color: #28a745;">
    <b>Onda 2 (Fluctuación Suave):</b><br>
    <code style="color: #28a745;">uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo...</code>
</div>

<div class="wave-card" style="border-left-color: #ffc107;">
    <b>Onda 3 (Armónicos Profundos):</b><br>
    <code style="color: #b8860b;">mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm</code>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENTRADA DE DATOS Y CONFIGURACIÓN
# ---------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area("✍️ Ingresa el texto u onda a escuchar:", placeholder="Pega aquí tu secuencia de vocales o fonemas...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    option_lang = st.selectbox(
        "🌐 Selecciona el idioma",
        ("Español", "English")
    )

if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# ---------------------------------------------------------
# CONVERSIÓN Y REPRODUCCIÓN
# ---------------------------------------------------------
def text_to_speech(text_input, tld_val, lang_code):
    tts = gTTS(text_input, lang=lang_code)
    try:
        my_file_name = text_input[0:20].strip().replace(" ", "_")
    except Exception:
        my_file_name = "audio"
    
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return my_file_name, text_input

if st.button("🚀 Convertir a Audio", use_container_width=True):
    if text.strip() == "":
        st.warning("⚠️ Por favor, ingresa o selecciona texto antes de convertir.")
    else:
        with st.spinner("🎵 Generando ondas de audio... Por favor espera."):
            result, output_text = text_to_speech(text, 'com', lg)
            audio_file_path = f"temp/{result}.mp3"
            
            if os.path.exists(audio_file_path):
                st.success("¡Audio generado con éxito!")
                st.markdown("### 🎧 Reproductor de Audio:")
                
                with open(audio_file_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                
                # Botón de descarga elegante en Base64
                b64_data = base64.b64encode(audio_bytes).decode()
                download_href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{result}.mp3" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:10px 20px;border-radius:8px;text-align:center;font-weight:bold;margin-top:15px;">📥 Descargar Archivo de Audio (.mp3)</div></a>'
                st.markdown(download_href, unsafe_allow_html=True)
            else:
                st.error("Hubo un error al crear el archivo de audio.")

# ---------------------------------------------------------
# LIMPIEZA AUTOMÁTICA DE ARCHIVOS ANTIGUOS
# ---------------------------------------------------------
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            try:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
            except Exception:
                pass

remove_files(7)        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #4a90e2;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2b6cb0;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎧 Guía de Sesión")
    st.info(
        "1. Selecciona o copia una de las **plantillas de ondas** recomendadas.\n"
        "2. Pégala en el campo de texto principal.\n"
        "3. Elige el idioma de síntesis de voz.\n"
        "4. Haz clic en **'Convertir a Audio'** para escuchar y descargar."
    )
    st.markdown("---")
    try:
        image = Image.open('monoaural.jpg')
        st.image(image, width=250, caption="Frecuencias Binaurales")
    except Exception:
        st.warning("Imagen 'monoaural.jpg' no encontrada.")
    st.markdown("---")
    st.success("Estado: Listo para relajar 🌊")

# ---------------------------------------------------------
# CABECERA PRINCIPAL
# ---------------------------------------------------------
st.title("🎧 Creador de Ondas Binaurales y Vocales")
st.markdown(
    "<p style='font-size: 17px; color: #555;'>Transforma secuencias de vocales y fonemas en ritmos constantes ideales para meditar, estudiar o practicar instrumentos musicales.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# Crear directorio temporal de forma segura
try:
    os.makedirs("temp", exist_ok=True)
except Exception:
    pass

# ---------------------------------------------------------
# PLANTILLAS DE ONDAS
# ---------------------------------------------------------
st.subheader("✨ Plantillas de Ondas Recomendadas")
st.write("Puedes copiar cualquiera de estas secuencias y hacerlas tan largas como quieras duplicándolas:")

# Tarjetas visuales para las plantillas
st.markdown("""
<div class="wave-card">
    <b>Onda 1 (Ritmo Constante / Estudiar):</b><br>
    <code style="color: #d63384;">mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm</code>
</div>

<div class="wave-card" style="border-left-color: #28a745;">
    <b>Onda 2 (Fluctuación Suave):</b><br>
    <code style="color: #28a745;">uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo...</code>
</div>

<div class="wave-card" style="border-left-color: #ffc107;">
    <b>Onda 3 (Armónicos Profundos):</b><br>
    <code style="color: #b8860b;">mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm</code>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENTRADA DE DATOS Y CONFIGURACIÓN
# ---------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area("✍️ Ingresa el texto u onda a escuchar:", placeholder="Pega aquí tu secuencia de vocales o fonemas...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    option_lang = st.selectbox(
        "🌐 Selecciona el idioma",
        ("Español", "English")
    )

if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# ---------------------------------------------------------
# CONVERSIÓN Y REPRODUCCIÓN
# ---------------------------------------------------------
def text_to_speech(text_input, tld_val, lang_code):
    tts = gTTS(text_input, lang=lang_code)
    try:
        my_file_name = text_input[0:20].strip().replace(" ", "_")
    except Exception:
        my_file_name = "audio"
    
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return my_file_name, text_input

if st.button("🚀 Convertir a Audio", use_container_width=True):
    if text.strip() == "":
        st.warning("⚠️ Por favor, ingresa o selecciona texto antes de convertir.")
    else:
        with st.spinner("🎵 Generando ondas de audio... Por favor espera."):
            result, output_text = text_to_speech(text, 'com', lg)
            audio_file_path = f"temp/{result}.mp3"
            
            if os.path.exists(audio_file_path):
                st.success("¡Audio generado con éxito!")
                st.markdown("### 🎧 Reproductor de Audio:")
                
                with open(audio_file_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                
                # Botón de descarga elegante en Base64
                b64_data = base64.b64encode(audio_bytes).decode()
                download_href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{result}.mp3" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:10px 20px;border-radius:8px;text-align:center;font-weight:bold;margin-top:15px;">📥 Descargar Archivo de Audio (.mp3)</div></a>'
                st.markdown(download_href, unsafe_allow_html=True)
            else:
                st.error("Hubo un error al crear el archivo de audio.")

# ---------------------------------------------------------
# LIMPIEZA AUTOMÁTICA DE ARCHIVOS ANTIGUOS
# ---------------------------------------------------------
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            try:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
            except Exception:
                pass

remove_files(7)        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #4a90e2;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2b6cb0;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎧 Guía de Sesión")
    st.info(
        "1. Selecciona o copia una de las **plantillas de ondas** recomendadas.\n"
        "2. Pégala en el campo de texto principal.\n"
        "3. Elige el idioma de síntesis de voz.\n"
        "4. Haz clic en **'Convertir a Audio'** para escuchar y descargar."
    )
    st.markdown("---")
    try:
        image = Image.open('monoaural.jpg')
        st.image(image, width=250, caption="Frecuencias Binaurales")
    except Exception:
        st.warning("Imagen 'monoaural.jpg' no encontrada.")
    st.markdown("---")
    st.success("Estado: Listo para relajar 🌊")

# ---------------------------------------------------------
# CABECERA PRINCIPAL
# ---------------------------------------------------------
st.title("🎧 Creador de Ondas Binaurales y Vocales")
st.markdown(
    "<p style='font-size: 17px; color: #555;'>Transforma secuencias de vocales y fonemas en ritmos constantes ideales para meditar, estudiar o practicar instrumentos musicales.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# Crear directorio temporal de forma segura
try:
    os.makedirs("temp", exist_ok=True)
except Exception:
    pass

# ---------------------------------------------------------
# PLANTILLAS DE ONDAS
# ---------------------------------------------------------
st.subheader("✨ Plantillas de Ondas Recomendadas")
st.write("Puedes copiar cualquiera de estas secuencias y hacerlas tan largas como quieras duplicándolas:")

# Tarjetas visuales para las plantillas
st.markdown("""
<div class="wave-card">
    <b>Onda 1 (Ritmo Constante / Estudiar):</b><br>
    <code style="color: #d63384;">mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm mmmmmmmm oooooooo uuuuuuuu mmmmmmmm</code>
</div>

<div class="wave-card" style="border-left-color: #28a745;">
    <b>Onda 2 (Fluctuación Suave):</b><br>
    <code style="color: #28a745;">uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo... uuuuuuuuu... oooooooo...</code>
</div>

<div class="wave-card" style="border-left-color: #ffc107;">
    <b>Onda 3 (Armónicos Profundos):</b><br>
    <code style="color: #b8860b;">mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm mmmmm-ooooooh-mmmmm-uuuuhhhh-mmmmm</code>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENTRADA DE DATOS Y CONFIGURACIÓN
# ---------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area("✍️ Ingresa el texto u onda a escuchar:", placeholder="Pega aquí tu secuencia de vocales o fonemas...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    option_lang = st.selectbox(
        "🌐 Selecciona el idioma",
        ("Español", "English")
    )

if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# ---------------------------------------------------------
# CONVERSIÓN Y REPRODUCCIÓN
# ---------------------------------------------------------
def text_to_speech(text_input, tld_val, lang_code):
    tts = gTTS(text_input, lang=lang_code)
    try:
        my_file_name = text_input[0:20].strip().replace(" ", "_")
    except Exception:
        my_file_name = "audio"
    
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return my_file_name, text_input

if st.button("🚀 Convertir a Audio", use_container_width=True):
    if text.strip() == "":
        st.warning("⚠️ Por favor, ingresa o selecciona texto antes de convertir.")
    else:
        with st.spinner("🎵 Generando ondas de audio... Por favor espera."):
            result, output_text = text_to_speech(text, 'com', lg)
            audio_file_path = f"temp/{result}.mp3"
            
            if os.path.exists(audio_file_path):
                st.success("¡Audio generado con éxito!")
                st.markdown("### 🎧 Reproductor de Audio:")
                
                with open(audio_file_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                
                # Botón de descarga elegante en Base64
                b64_data = base64.b64encode(audio_bytes).decode()
                download_href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{result}.mp3" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:10px 20px;border-radius:8px;text-align:center;font-weight:bold;margin-top:15px;">📥 Descargar Archivo de Audio (.mp3)</div></a>'
                st.markdown(download_href, unsafe_allow_html=True)
            else:
                st.error("Hubo un error al crear el archivo de audio.")

# ---------------------------------------------------------
# LIMPIEZA AUTOMÁTICA DE ARCHIVOS ANTIGUOS
# ---------------------------------------------------------
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            try:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
            except Exception:
                pass

remove_files(7)
