import streamlit as st
import requests
import time

# --- CONFIG ---
API_KEY = "sk-SKF34vIczWNfGWemwoF03o8mCSS0Zd21f9eVUaGetR9XvSCK"
API_URL = "https://api.stability.ai/v2beta/video/generate"  # replace with real API

st.set_page_config(page_title="AI Video Generator", layout="centered")

st.title("🎬 AI Video Generator")
st.write("Turn your ideas into short AI-generated videos")

# --- INPUT ---
prompt = st.text_area("Enter your video prompt:", height=120)

duration = st.selectbox("Video duration (seconds)", [3, 5, 10])

generate_btn = st.button("Generate Video")

# --- FUNCTION ---
def generate_video(prompt, duration):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "duration": duration,
        "resolution": "720p"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        st.error(f"Error: {response.text}")
        return None

    job = response.json()

    job_id = job.get("id")
    status_url = f"{API_URL}/{job_id}"

    with st.spinner("Generating video..."):
        while True:
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()

            if status_data.get("status") == "completed":
                return status_data.get("video_url")

            elif status_data.get("status") == "failed":
                st.error("Video generation failed.")
                return None

            time.sleep(3)

# --- ACTION ---
if generate_btn:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        video_url = generate_video(prompt, duration)

        if video_url:
            st.success("✅ Video generated!")
            st.video(video_url)
            st.markdown(f"{video_url}")
