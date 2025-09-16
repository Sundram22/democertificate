import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(page_title="Certificate Generator", layout="centered")

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "template_uploaded" not in st.session_state:
    st.session_state.template_uploaded = False
if "template_image" not in st.session_state:
    st.session_state.template_image = None
if "name_pos" not in st.session_state:
    st.session_state.name_pos = (650, 409)
if "year_pos" not in st.session_state:
    st.session_state.year_pos = (1028, 411)
if "semester_pos" not in st.session_state:
    st.session_state.semester_pos = (163, 460)
if "font_sizes" not in st.session_state:
    st.session_state.font_sizes = {"name":38, "year":38, "semester":38}

# -----------------------------
# Sidebar: Select Panel
# -----------------------------
panel = st.sidebar.selectbox("Choose Panel", ["Student", "Admin"])

# -----------------------------
# Admin Panel
# -----------------------------
if panel == "Admin":
    st.title("🔑 Admin Panel")
    
    if not st.session_state.admin_logged_in:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login = st.button("Login")
        
        # ✅ Auto login after checking credentials
        if login or st.session_state.admin_logged_in:
            if email == "admin@example.com" and password == "admin123":
                st.session_state.admin_logged_in = True
                st.success("✅ Login Successful")
            else:
                st.error("❌ Invalid Credentials")
    
    # Display admin options immediately after login
    if st.session_state.admin_logged_in:
        st.subheader("📤 Upload Certificate Template")
        uploaded_file = st.file_uploader("Upload PNG/JPG Certificate Template", type=["png","jpg","jpeg"])
        if uploaded_file:
            st.session_state.template_image = Image.open(uploaded_file).convert("RGB")
            st.session_state.template_uploaded = True
            st.success("✅ Template Uploaded Successfully")
        
        if st.session_state.template_uploaded:
            st.subheader("🖊 Set Text Positions & Font Sizes")
            template = st.session_state.template_image
            # Position sliders
            st.session_state.name_pos = (
                st.slider("Name X", 0, template.width, st.session_state.name_pos[0]),
                st.slider("Name Y", 0, template.height, st.session_state.name_pos[1])
            )
            st.session_state.year_pos = (
                st.slider("Year X", 0, template.width, st.session_state.year_pos[0]),
                st.slider("Year Y", 0, template.height, st.session_state.year_pos[1])
            )
            st.session_state.semester_pos = (
                st.slider("Semester X", 0, template.width, st.session_state.semester_pos[0]),
                st.slider("Semester Y", 0, template.height, st.session_state.semester_pos[1])
            )
            # Font sizes
            st.session_state.font_sizes["name"] = st.slider("Name Font Size", 20, 150, st.session_state.font_sizes["name"])
            st.session_state.font_sizes["year"] = st.slider("Year Font Size", 15, 100, st.session_state.font_sizes["year"])
            st.session_state.font_sizes["semester"] = st.slider("Semester Font Size", 15, 100, st.session_state.font_sizes["semester"])
            
            # Preview template with dummy text
            st.subheader("Preview Template with Dummy Text")
            cert_preview = template.copy()
            draw = ImageDraw.Draw(cert_preview)
            try:
                font_name = ImageFont.truetype("arial.ttf", st.session_state.font_sizes["name"])
                font_year = ImageFont.truetype("arial.ttf", st.session_state.font_sizes["year"])
                font_semester = ImageFont.truetype("arial.ttf", st.session_state.font_sizes["semester"])
            except:
                font_name = ImageFont.load_default()
                font_year = ImageFont.load_default()
                font_semester = ImageFont.load_default()

            def draw_centered_text(draw_obj, text, pos, font):
                bbox = draw_obj.textbbox((0,0), text, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x, y = pos
                draw_obj.text((x-w/2, y-h/2), text, font=font, fill=(0,0,0))

            draw_centered_text(draw, "Name", st.session_state.name_pos, font_name)
            draw_centered_text(draw, "Year", st.session_state.year_pos, font_year)
            draw_centered_text(draw, "Semester", st.session_state.semester_pos, font_semester)
            st.image(cert_preview, caption="Template Preview", use_container_width=True)

# -----------------------------
# Student Panel
# -----------------------------
if panel == "Student":
    st.title("🎓 Student Certificate Portal")
    
    if not st.session_state.template_uploaded:
        st.error("❌ No Event. Contact Admin.")
    else:
        name = st.text_input("Enter Your Name")
        year = st.text_input("Enter Your Year")
        semester = st.text_input("Enter Semester")
        
        name_size = st.session_state.font_sizes["name"]
        year_size = st.session_state.font_sizes["year"]
        semester_size = st.session_state.font_sizes["semester"]
        
        if st.button("Generate Certificate"):
            if not name.strip() or not year.strip() or not semester.strip():
                st.warning("⚠️ Please fill all fields to generate certificate.")
            else:
                template = st.session_state.template_image
                cert = template.copy()
                draw = ImageDraw.Draw(cert)
                try:
                    font_name = ImageFont.truetype("arial.ttf", name_size)
                    font_year = ImageFont.truetype("arial.ttf", year_size)
                    font_semester = ImageFont.truetype("arial.ttf", semester_size)
                except:
                    font_name = ImageFont.load_default()
                    font_year = ImageFont.load_default()
                    font_semester = ImageFont.load_default()
                
                def draw_centered_text(draw_obj, text, pos, font):
                    bbox = draw_obj.textbbox((0,0), text, font=font)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    x, y = pos
                    draw_obj.text((x-w/2, y-h/2), text, font=font, fill=(0,0,0))
                
                draw_centered_text(draw, name, st.session_state.name_pos, font_name)
                draw_centered_text(draw, year, st.session_state.year_pos, font_year)
                draw_centered_text(draw, semester, st.session_state.semester_pos, font_semester)
                
                st.image(cert, caption="🖼 Generated Certificate", use_container_width=True)
                
                pdf_buffer = BytesIO()
                cert.save(pdf_buffer, format="PDF")
                pdf_buffer.seek(0)
                
                st.success("🎉 Your certificate is ready!")
                st.download_button(
                    label="📥 Download Certificate PDF",
                    data=pdf_buffer,
                    file_name=f"certificate_{name.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

# -----------------------------
# Permanent Footer
# -----------------------------
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; 
            background-color: #f8f9fa; padding: 10px; 
            text-align: center; font-size: 16px; 
            font-family: Arial; color: #0b5394; 
            border-top: 1px solid #ddd;">
    ✅ Made by <b>Asst. Prof. Sundram Tiwari</b>
</div>
""", unsafe_allow_html=True)
