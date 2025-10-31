import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

# 🌻 Estilo y Decoración del tema Girasol
st.set_page_config(page_title="🌻 Traductor Girasol", page_icon="🌞", layout="centered")

# 🌻 Estilo CSS para colores cálidos y fondo floral
st.markdown("""
    <style>
        body {
            background-color: #fff8dc;
        }
        .main {
            background-color: #fffbea;
            border-radius: 20px;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #e1a72a;
            text-align: center;
            font-family: 'Comic Sans MS', cursive;
        }
        .stButton>button {
            background-color: #ffd54f;
            color: #4a3000;
            border-radius: 12px;
            border: 2px solid #e1a72a;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #ffeb3b;
            transform: scale(1.05);
        }
        .stSelectbox, .stTextInput {
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #fff7d6;
            border-right: 3px solid #e1a72a;
        }
    </style>
""", unsafe_allow_html=True)

# 🌻 Título e imagen principal
st.title("🌻 TRADUCTOR GIRASOL 🌞")
st.subheader("¡Deja que florezcan tus palabras en cualquier idioma!")

# Imagen decorativa
try:
    image = Image.open('imagen_traductor.jpg')
    st.image(image, width=300, caption="🌻 ¡Habla, traduce y florece! 🌻")
except:
    st.info("🌻 Sube tu imagen de girasol para personalizar el traductor.")

# 🌻 Sidebar decorada
with st.sidebar:
    st.subheader("🌼 Traductor de Voces 🌼")
    st.write("Presiona el botón 🌻, habla, y deja que el traductor "
             "transforme tus palabras en otro idioma con un toque soleado ☀️.")

# 🌻 Botón de grabación
st.write("🎙️ Toca el botón y habla lo que quieres traducir 🌻")

stt_button = Button(label="🌻 Escuchar tu voz 🎤", width=300, height=50)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# 🌻 Procesamiento del texto
if result:
    if "GET_TEXT" in result:
        st.success("🌻 ¡Texto capturado exitosamente! 🌞")
        st.write(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    st.header("🎧 Texto a Audio 🌻")
    translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    in_lang = st.selectbox(
        "🌸 Selecciona el lenguaje de Entrada:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    lang_dict = {"Inglés": "en", "Español": "es", "Bengali": "bn",
                 "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"}
    input_language = lang_dict[in_lang]
    
    out_lang = st.selectbox(
        "🌼 Selecciona el lenguaje de salida:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    output_language = lang_dict[out_lang]
    
    english_accent = st.selectbox(
        "🌻 Selecciona el acento del audio:",
        ("Defecto", "Español", "Reino Unido", "Estados Unidos",
         "Canadá", "Australia", "Irlanda", "Sudáfrica"),
    )
    tld_dict = {
        "Defecto": "com", "Español": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canadá": "ca", "Australia": "com.au",
        "Irlanda": "ie", "Sudáfrica": "co.za"
    }
    tld = tld_dict[english_accent]
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    display_output_text = st.checkbox("🌻 Mostrar el texto traducido")

    if st.button("✨ Convertir 🌞"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## 🎶 Tu audio floral:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown("## 🌼 Texto traducido:")
            st.write(f"💬 {output_text}")
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("🗑️ Deleted ", f)

    remove_files(7)

