import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# =====================
# SETTINGS
# =====================
TEMPLATE_PATH = "cert_template.png"  # your uploaded PNG
FONT_PATH = "arialbd.ttf"                     # change if you want custom font
PHOTO_BOX = (560, 390, 738, 585)           # (left, top, right, bottom) of red rectangle in template

# =====================
# UI
# =====================
st.title("📜 Star Student of the Month Certificate Generator")

month = st.text_input("Month", "August")
name = st.text_input("Student Name", "Aman Gupta")
student_class = st.text_input("Class", "10A")
adjective = st.text_input("Adjective", "Hardworking and Responsible")

uploaded_photo = st.file_uploader("Upload Student Photo", type=["jpg", "jpeg", "png"])

if st.button("Generate Certificate"):
    # Load template
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(base)

    # Fonts
    font_big = ImageFont.truetype(FONT_PATH, 35)
    font_medium = ImageFont.truetype(FONT_PATH, 30)
    font_small = ImageFont.truetype(FONT_PATH, 25)

    # Insert Month (adjust X,Y by trial)
    draw.text((860, 315), month, font=font_big, fill="red", anchor="mm")

    # Insert Name
    draw.text((460, 595), name, font=font_small, fill="black")

    # Insert Class
    draw.text((770, 590), student_class, font=font_medium, fill="black")

    # Insert Adjective (wrapped to 2 lines max)
    wrapped_adj = textwrap.fill(adjective, width=30)
    draw.text((520, 672), wrapped_adj, font=font_medium, fill="black")

    # Add Student Photo
    if uploaded_photo:
        photo = Image.open(uploaded_photo).convert("RGBA")
        # resize to fit box
        box_w = PHOTO_BOX[2] - PHOTO_BOX[0]
        box_h = PHOTO_BOX[3] - PHOTO_BOX[1]
        photo = photo.resize((box_w, box_h))
        base.paste(photo, (PHOTO_BOX[0], PHOTO_BOX[1]))

    # Save to in-memory file
    output = io.BytesIO()
    base.save(output, format="PNG")
    output.seek(0)

    st.image(base, caption="Generated Certificate", use_column_width=True)
    st.download_button("📥 Download Certificate", data=output,
                       file_name=f"certificate_{name}_{student_class}.png",
                       mime="image/png")
