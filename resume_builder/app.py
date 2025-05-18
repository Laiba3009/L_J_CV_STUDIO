import streamlit as st
import base64
from streamlit.components.v1 import html
from auth.login import login, is_logged_in
from views.create_resume import render_template
from resume.builder import ResumeBuilder
from utils.html_to_pdf import convert_html_to_pdf
import sys
import os
sys.path.append(os.path.abspath("."))  # Adds project root to Python path

 # Make sure this is imported

# Page config
st.set_page_config(page_title="AI Resume Builder", layout="centered")

def show_landing_page():
    st.markdown("""
        <style>
            html, body, [data-testid="stApp"] {
                height: 100%;
                background-image: url('https://i.ibb.co/4ZDZfc6f/Blue-and-White-Bold-Congratulations-A4.png');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            .stButton > button {
                padding: 15px 30px;
                font-size: 18px;
                background: radial-gradient(circle, #aeeedf, #94bbe9);
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            .main .block-container {
                padding-top: 2rem;
                background-color: rgba(255,255,255,0.85);
                border-radius: 10px;
                padding: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; padding: 80px 20px;'>
            <h1 style='color: #ffffff; text-shadow: 2px 2px 4px #000;'>Create a Professional Resume</h1>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Create Resume"):
            st.session_state.page = "start_builder"
            st.rerun()

# --- Resume Builder ---
def show_resume_builder():
    if not is_logged_in():
        login()
        return

    st.title("🚀 AI Resume Builder")

    # Resume form
    builder = ResumeBuilder()
    form_data = builder.render_form()

    if form_data:
        st.success("✅ Resume Preview Ready")

        # Template selection below preview message
        st.subheader("🎨 Choose a Resume Template")
        template = st.radio("Select Template:", [
            "Template 1 (Free)",
            "Template 2 (Free)",
            "Template 3 (Free)"
        ])

        if template == "Template 1 (Free)":
            selected_template = "resume_template1.html"
        elif template == "Template 2 (Free)":
            selected_template = "resume_template2.html"
        else:
            selected_template = "resume_template3.html"

        rendered_html = render_template(selected_template, form_data)
        html(rendered_html, height=800, scrolling=True)

        # PDF generation
        pdf_data = convert_html_to_pdf(rendered_html)
        if pdf_data:
            b64_pdf = base64.b64encode(pdf_data).decode()
            download_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="resume.pdf">📄 Download PDF</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.error("❌ PDF generation failed.")

# --- Main app logic ---
def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if st.session_state.page == "landing":
        show_landing_page()
    elif st.session_state.page == "start_builder":
        show_resume_builder()

if __name__ == "__main__":
    main()
