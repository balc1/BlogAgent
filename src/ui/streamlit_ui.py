import streamlit as st
import requests
import json
import time

# FastAPI sunucunuzun adresi
# Bu adres, app.py'nin çalıştığı yerdir (genellikle http://127.0.0.1:8000)
API_URL = "http://127.0.0.1:8000/blogs"

st.set_page_config(layout="wide", page_title="AI Blog Agent")

st.title("🤖 AI Blog Generate Agent (LangGraph + Groq)")
st.markdown("""
""")

# Kullanıcı Girdileri
with st.sidebar:
    st.header("Blog Settings")
    topic_input = st.text_input("Blog Topic:", placeholder="Ex: The Future of AI in Healthcare")

    language_input = st.selectbox(
        "Language:",
        ("", "French", "Hindi") # Sadece API'nizin desteklediği diller
    )

    generate_button = st.button("🚀 Generate a Blog")

# İçerik Alanı
st.subheader("Generated Blog Output")
output_container = st.container(border=True, height=600)

if generate_button:
    if not topic_input:
        st.sidebar.error("Topic side will not be empty!")
    else:
        with st.spinner("Generating blog... Please wait."):
            try:
                # to API
                payload = {
                    "topic": topic_input,
                    "language": language_input.lower() # API lanuages
                }

                # FastAPI'ye POST isteği gönder
                response = requests.post(API_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

                if response.status_code == 200:
                    data = response.json()
                    state = data.get("data", {})
                    blog_data = state.get("blog", {})

                    title = blog_data.get("title", "Title Not Found")
                    content = blog_data.get("content", "Content Not Found")

                    output_container.subheader(title)
                    output_container.markdown(content)
                    st.sidebar.success("Blog generated successfully!")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Connection Error: FastAPI sunucusuna bağlanılamıyor. Sunucunun çalıştığından emin olun.")
            except Exception as e:
                st.error(f"Error : {e}")

else:
    output_container.info("please enter a topic and click 'Generate a Blog' to see the output here.")