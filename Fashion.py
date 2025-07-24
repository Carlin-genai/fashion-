import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
import os
import io

# Set page configuration
st.set_page_config(page_title="AI Fashion Design Generator", layout="wide")
st.title("👗 AI Fashion Silhouette & Outfit Designer")
st.caption("Draw, Upload, and Let AI Generate Stunning Outfit Designs")

# Sidebar inputs
st.sidebar.header("🪡 Design Parameters")
style = st.sidebar.selectbox("Outfit Style", ["Fusion Ethnic", "Boho Chic", "Minimalist Formal", "Runway Couture", "Casual Streetwear"])
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall", "Winter", "All-Season"])
fabrics = st.sidebar.text_input("Preferred Fabrics", "Chanderi, Organza, Cotton")
elements = st.sidebar.text_area("Design Elements", "Asymmetry, ruffles, slit, pleats")
design_principles = st.sidebar.multiselect("Design Principles", ["Balance", "Rhythm", "Contrast", "Emphasis", "Unity", "Proportion"], default=["Balance", "Emphasis"])
colors = st.sidebar.text_input("Color Preferences", "Peach, Mint Green, Off-white")
trend_palette = st.sidebar.text_input("Trending Palette Notes", "Pantone 2025 - Peach Fuzz, Soft Blue")
ai_review = st.sidebar.text_area("AI Critique Suggestion (Optional)", "Add layering for depth and use lighter fabrics for summer appeal")

# Uploads
st.subheader("📤 Upload References (Optional)")
col1, col2, col3 = st.columns(3)
with col1:
    ref_image = st.file_uploader("Upload a Sketch/Reference", type=["png", "jpg", "jpeg"])
with col2:
    fabric_swatch = st.file_uploader("Upload Fabric Swatch", type=["png", "jpg", "jpeg"])
with col3:
    user_design = st.file_uploader("Upload Your Design", type=["png", "jpg", "jpeg"])

# Drawing Canvas
st.subheader("🖌️ Draw a Silhouette")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.3)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=400,
    width=400,
    drawing_mode="freedraw",
    key="canvas"
)

# Show uploaded/drawn images
st.markdown("---")
st.subheader("📸 Preview Inputs")
if ref_image:
    st.image(ref_image, caption="Reference Image", use_column_width=True)
if fabric_swatch:
    st.image(fabric_swatch, caption="Fabric Swatch", use_column_width=True)
if user_design:
    st.image(user_design, caption="User Design", use_column_width=True)
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Drawn Silhouette", use_column_width=True)

# Prompt builder
def generate_prompt():
    prompt = f"Design a high-fashion women's outfit using a {style} silhouette suitable for {season}. "
    prompt += f"Key fabrics: {fabrics}. Include elements such as {elements}. "
    prompt += f"Use color scheme: {colors} with influence from trend palette: {trend_palette}. "
    prompt += f"Apply design principles: {', '.join(design_principles)}. "
    if ai_review:
        prompt += f"Note: {ai_review} "
    prompt += "Generate a realistic, high-resolution fashion illustration."
    return prompt

# Image generator from Hugging Face
@st.cache_data(show_spinner=False)
def generate_fashion_image(prompt):
    api_token = os.getenv("HUGGINGFACE_TOKEN")
    if not api_token:
        st.error("Please set your Hugging Face token in the environment variable 'HUGGINGFACE_TOKEN'")
        return None
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": prompt}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        st.error(f"API Error: {response.status_code}")
        return None

# Generate button
st.markdown("---")
if st.button("🎨 Generate Outfit Image"):
    with st.spinner("Creating fashion artwork with AI..."):
        final_prompt = generate_prompt()
        st.markdown("#### 📝 Final Prompt Sent to AI:")
        st.info(final_prompt)
        result_image = generate_fashion_image(final_prompt)
        if result_image:
            st.image(result_image, caption="👗 AI-Generated Fashion Illustration", use_column_width=True)

st.markdown("---")
st.caption("Built with 🧠 Streamlit, 🤖 Hugging Face, and your imagination ✨")
