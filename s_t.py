import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

text = st.text_input("Que he dicho ?")

tts_button = Button(label="Habla", width=100)

tts_button.js_on_event("button_click", CustomJS(code=f"""
    var u = new SpeechSynthesisUtterance();
    u.text = "{text}";
    u.lang = 'en-US';

    speechSynthesis.speak(u);
    """))

st.bokeh_chart(tts_button)
