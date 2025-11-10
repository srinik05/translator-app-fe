import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🌍 Voice/Text Translator", page_icon="🌎")
st.title("🌍 Voice/Text Translator")

input_type = st.radio("Choose input type:", ["Text", "Voice"])

# =======================
# Language mapping
# =======================
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

# Show full names in selectbox
selected_lang_name = st.selectbox("Select target language:", list(lang_map.keys()))

# Convert full name to code when sending to backend
target_lang = lang_map[selected_lang_name]


def safe_json_response(response):
    """Safely parse JSON response."""
    try:
        return response.json()
    except Exception:
        st.error("⚠️ Backend returned invalid response.")
        st.text(response.text)
        return {}


def translate_text_backend(text, lang):
    try:
        response = requests.post(
            f"{BACKEND_URL}/translate-text",
            json={"text": text, "target_lang": lang},
            timeout=60
        )
        return safe_json_response(response)
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {e}")
        return {}


def translate_voice_backend(file, lang):
    try:
        response = requests.post(
            f"{BACKEND_URL}/translate-voice",
            files={"file": file},
            data={"target_lang": lang},
            timeout=120
        )
        return safe_json_response(response)
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {e}")
        return {}


# =======================
# TEXT TRANSLATION MODE
# =======================
if input_type == "Text":
    text = st.text_area("Enter text to translate:")
    if st.button("Translate"):
        if text.strip():
            with st.spinner("Translating..."):
                data = translate_text_backend(text, target_lang)

            translated_text = data.get("translated_text")
            audio_file = data.get("audio")

            if translated_text:
                st.success("✅ Translation successful!")
                st.markdown(f"**Translation:** {translated_text}")

                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
                    st.markdown("🔊 Click play to hear the pronunciation")
            else:
                st.error(data.get("error", "Translation failed."))
        else:
            st.warning("⚠️ Please enter some text.")


# =======================
# VOICE TRANSLATION MODE
# =======================
else:
    audio_file = st.file_uploader("Upload voice file:", type=["wav", "mp3"])
    if st.button("Translate Voice"):
        if audio_file:
            with st.spinner("Converting and translating speech..."):
                data = translate_voice_backend(audio_file, target_lang)

            translated_text = data.get("translated_text")
            audio_path = data.get("audio")

            if translated_text:
                st.success("✅ Translation successful!")
                st.markdown(f"**Translation:** {translated_text}")

                if audio_path:
                    st.audio(audio_path, format="audio/mp3")
                    st.markdown("🔊 Click play to hear the pronunciation")
            else:
                st.error(data.get("error", "Speech translation failed."))
        else:
            st.warning("⚠️ Please upload an audio file first!")
