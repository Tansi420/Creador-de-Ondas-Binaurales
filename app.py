import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Fábula Interactiva: Texto a Audio",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con "colorcitos y cositas" estéticas
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        border-radius: 20px;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
    }
    .fabula-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        border-left: 6px solid #6c5ce7;
        margin-bottom: 20px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #ffeaa7;
    }
    .download-btn {
        display: inline-block;
        background-color: #00b894;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 184, 148, 0.3);
    }
    .download-btn:hover {
        background-color: #00a884;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3342/3342137.png", width=80)
    st.markdown("### 🎛️ Panel de Control")
    st.info("Escribe, selecciona tu idioma preferido y convierte cualquier texto o la fábula clásica en voz alta al instante.")
    st.markdown("---")
    option_lang = st.selectbox(
        "🌐 Selecciona el lenguaje",
        ("Español", "English")
    )
    if option_lang == "Español":
        lg = 'es'
    else:
        lg = 'en'

# ---------------------------------------------------------
# CABECERA PRINCIPAL
# ---------------------------------------------------------
col_title, col_img = st.columns([3, 1])

with col_title:
    st.title("🎧 Conversor Mágico de Texto a Audio")
    st.markdown("### Dale vida a tus lecturas y fábulas con voz de alta calidad.")

with col_img:
    try:
        image = Image.open('gato_raton.png')
        st.image(image, width=220, caption="El Gato y el Ratón")
    except Exception:
        st.warning("Imagen 'gato_raton.png' no encontrada. Asegúrate de incluirla en tu directorio.")

st.markdown("---")

# ---------------------------------------------------------
# CREACIÓN DE DIRECTORIO TEMPORAL
# ---------------------------------------------------------
try:
    os.makedirs("temp", exist_ok=True)
except Exception:
    pass

# ---------------------------------------------------------
# SECCIÓN DE LA FÁBULA (ESTILIZADA EN TARJETA)
# ---------------------------------------------------------
st.markdown("### 📜 Una pequeña Fábula de Franz Kafka")

fabula_texto = (
    "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. "
    "Al principio era tan grande que le tenía miedo. Corría y corría y por cierto que me alegraba ver esos muros, "
    "a diestra y siniestra, en la distancia. Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto "
    "y ahí en el rincón está la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo -dijo el gato-... y se lo comió."
)

st.markdown(
    f"""
    <div class="fabula-card">
        <p style="font-size: 17px; line-height: 1.6; color: #2d3436;">
            <i>"{fabula_texto}"</i>
        </p>
        <p style="text-align: right; font-weight: bold; color: #6c5ce7; margin-bottom: 0;">— Franz Kafka</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# ENTRADA DE TEXTO
# ---------------------------------------------------------
st.markdown("### ✍️ Tu Turno")
st.write("Puedes copiar la fábula de arriba o escribir cualquier texto personalizado que desees escuchar:")
text = st.text_area("Ingrese el texto a escuchar:", value=fabula_texto, height=130)

# ---------------------------------------------------------
# FUNCIÓN DE TEXTO A VOZ
# ---------------------------------------------------------
def text_to_speech(text_input, tld_val, lang_code):
    tts = gTTS(text_input, lang=lang_code, tld=tld_val, slow=False)
    try:
        my_file_name = text_input[0:20].strip().replace(" ", "_")
    except Exception:
        my_file_name = "audio"
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return my_file_name, text_input

# ---------------------------------------------------------
# ACCIÓN DE CONVERSIÓN
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ Convertir a Audio"):
    if text.strip() == "":
        st.warning("Por favor, ingresa algún texto para poder convertirlo.")
    else:
        with st.spinner("🎙️ Sintetizando voz y generando audio..."):
            result, output_text = text_to_speech(text, 'com', lg)
            audio_path = f"temp/{result}.mp3"
            
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                st.success("¡Audio generado con éxito!")
                st.markdown("#### 🎧 Reproductor:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)

                # Botón de descarga estilizado
                with open(audio_path, "rb") as f:
                    data = f.read()
                bin_str = base64.b64encode(data).decode()
                href = f'<a class="download-btn" href="data:application/octet-stream;base64,{bin_str}" download="{result}.mp3">📥 Descargar Audio MP3</a>'
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("Ocurrió un error al generar el archivo de audio.")

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
