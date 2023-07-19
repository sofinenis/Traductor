import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from apikey import apikey
import openai

st.title("Interfaces Multimodales Audio y Texto")

st.write("Interfaz de Audio a texto")
os.environ["OPENAI_API_KEY"] = "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"

text = st.text_input("Que decir?")

tts_button = Button(label="Decirlo", width=100)

tts_button.js_on_event("button_click", CustomJS(code=f"""
    var u = new SpeechSynthesisUtterance();
    u.text = "{text}";
    u.lang = 'es-es';   

    speechSynthesis.speak(u);
    """))

st.bokeh_chart(tts_button)

st.write("Interfaz de Audio a texto")
stt_button = Button(label="Habla", width=100)

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
        if ( value != "") {
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
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        if st.button('Traducir'):
           
           prompt = 'Traduce al inglés : ' + result.get("GET_TEXT")
           response = openai.Completion.create(
           engine='text-davinci-002',
           prompt=prompt,
           temperature=0.2,
           max_tokens=50,
           n=1,
           stop=None,
           #context=conversation_id,
           ) 

        
    


