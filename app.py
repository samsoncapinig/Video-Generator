import streamlit as st
import requests
import time
import base64

# --- CONFIG ---
API_KEY = "YOUR_STABILITY_API_KEY"

IMAGE_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
VIDEO_API_URL = "https://api.stability.ai/v2beta/image-to-video"

st.set_page_config(page_title="AI Image to Video Generator", layout="centered")

st.title("🎬 AI Image → Video Generator")
st.write("Generate an image from prompt, then animate it into a video")

# --- INPUT ---
prompt = st.text_area("Enter your prompt:", height=120)
generate_btn = st.button("Generate Video")

# -----------------------------------
# 1. TEXT → IMAGE
# -----------------------------------
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    data = {
        "prompt": prompt,
        "output_format": "png"
    }

    response = requests.post(IMAGE_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        st.error(f"Image error: {response.text}")
        return None

    result = response.json()

    image_base64 = result["image"]

    image_bytes = base64.b64decode(image_base64)

    # Save image
    with open("generated.png", "wb") as f:
        f.write(image_bytes)

    return "generated.png"


# -----------------------------------
# 2. IMAGE → VIDEO
# -----------------------------------
def generate_video(image_path):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    files = {
        "image": open(image_path, "rb")
    }

    data = {
        "motion_bucket_id": 127,
        "fps": 6
    }

    response = requests.post(VIDEO_API_URL, headers=headers, files=files, data=data)

    if response.status_code != 200:
        st.error(f"Video error: {response.text}")
        return None

    return response.content  # returns video bytes


# --- MAIN FLOW ---
if generate_btn:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Step 1: Generating image..."):
            image_path = generate_image(prompt)

        if image_path:
            st.success("✅ Image generated!")
            st.image(image_path)

            time.sleep(1)

            with st.spinner("Step 2: Generating video..."):
                video_bytes = generate_video(image_path)

            if video_bytes:
                st.success("✅ Video generated!")

                # Save video
                with open("output.mp4", "wb") as f:
                    f.write(video_bytes)

                st.video("output.mp4")

                with open("output.mp4", "rb") as f:
                    st.download_button(
                        label="⬇️ Download Video",
                        data=f,
                        file_name="output.mp4",
                        mime="video/mp4"
                    )
