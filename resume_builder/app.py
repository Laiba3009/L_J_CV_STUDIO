import streamlit as st
import base64
from streamlit.components.v1 import html
from auth.login import login, is_logged_in
from views.create_resume import render_template
from resume.builder import ResumeBuilder
from utils.html_to_pdf import convert_html_to_pdf
import sys
import os

sys.path.append(os.path.abspath("."))

# Page config
st.set_page_config(page_title="AI Resume Builder", layout="centered")

# --- Top-Left Logo Display ---
def show_top_left_logo():
    st.markdown("""
        <style>
            .top-left-logo {
                position: fixed;
                top: 65px; /* Previously 25px, now 20px lower */
                left: 25px;
                z-index: 1000;
                background-color: white;
                border-radius: 50%;
                padding: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
                transition: transform 0.2s ease-in-out;
            }

            .top-left-logo:hover {
                transform: scale(1.05);
            }

            .top-left-logo img {
                height: 55px;
                width: 55px;
                object-fit: cover;
                border-radius: 50%;
            }

            .top-left-logo a {
                text-decoration: none;
            }

            .block-container {
                padding-top: 100px !important;
            }

            #MainMenu, footer {
                visibility: hidden;
            }
        </style>

        <div class="top-left-logo">
            <a href="#" onclick="window.location.reload();">
                <img src="https://i.ibb.co/BKy1xSWW/IMG-20250519-WA0006.jpg" alt="Logo">
            </a>
        </div>
    """, unsafe_allow_html=True)


# --- Sidebar Navigation ---
def show_sidebar():
    with st.sidebar:
        st.markdown("## L.J cv studio")

        if st.button("🔐 Login"):
            st.session_state.page = "login"
            st.rerun()
        if st.button("🆕 Signup"):
            st.session_state.page = "signup"
            st.rerun()

# --- Landing Page ---
def show_landing_page():
    show_top_left_logo()
    show_sidebar()

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
                background: #aeeedf;
                background: radial-gradient(circle, rgba(174, 238, 223, 1) 0%, rgba(44, 198, 222, 0.99) 99%);
                font-size: 18px;
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
<style>
.footer-text {
    position: fixed;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 14px;
    color: white;
    z-index: 9999;
}
</style>

<p class="footer-text">Created by Laiba Jaweed © 2025</p>
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

# --- Resume Builder Page ---
def show_resume_builder():
    show_top_left_logo()
    show_sidebar()

    if not is_logged_in():
        login()
        return

    st.title("🚀 AI Resume Builder")

    builder = ResumeBuilder()
    form_data = builder.render_form()

    if form_data:
        st.success("✅ Resume Preview Ready")

        st.subheader("🎨 Choose a Resume Template")
        template = st.radio("Select Template:", [
            "Template 1 (Free)",
            "Template 2 (Free)",
            "Template 3 (Free)"
        ])

        selected_template = {
            "Template 1 (Free)": "resume_template1.html",
            "Template 2 (Free)": "resume_template2.html",
            "Template 3 (Free)": "resume_template3.html"
        }[template]

        rendered_html = render_template(selected_template, form_data)
        html(rendered_html, height=800, scrolling=True)

        pdf_data = convert_html_to_pdf(rendered_html)
        if pdf_data:
            b64_pdf = base64.b64encode(pdf_data).decode()
            download_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="resume.pdf">📄 Download PDF</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.error("❌ PDF generation failed.")

# --- Main App Routing ---
def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if st.session_state.page == "landing":
        show_landing_page()
    elif st.session_state.page == "start_builder":
        show_resume_builder()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "signup":
        st.info("Signup Page Placeholder")

if __name__ == "__main__":
    main()
