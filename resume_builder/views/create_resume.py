import streamlit as st
from resume.builder import ResumeBuilder
from utils.html_to_pdf import convert_html_to_pdf
import base64
import streamlit.components.v1 as components


def show():
    st.title("L.J Cv Studio")

    st.title("📄 Create a Professional Resume")

    st.subheader("🎨 Choose a Resume Template")
    template = st.radio("Select Template:", ["Template 1", "Template 2", "Template 3"])
    template_file = {
        "Template 1": "resume_template1.html",
        "Template 2": "resume_template2.html",
        "Template 3": "resume_template3.html"
    }[template]

    builder = ResumeBuilder()
    form_data = builder.render_form()

    if form_data:
        st.success("✅ Resume Preview Ready")
        rendered_html = render_template(template_file, form_data)
        components.html(rendered_html, height=800, scrolling=True)

        # Download links
        b64_html = base64.b64encode(rendered_html.encode()).decode()
        st.markdown(f'<a href="data:text/html;base64,{b64_html}" download="resume.html">📥 Download Resume (HTML)</a>', unsafe_allow_html=True)

        pdf_data = convert_html_to_pdf(rendered_html)
        if pdf_data:
            b64_pdf = base64.b64encode(pdf_data).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="resume.pdf">📄 Download Resume (PDF)</a>', unsafe_allow_html=True)
        else:
            st.error("❌ PDF generation failed. Please try again.")


def render_template(template_name, context):
    from jinja2 import Environment, FileSystemLoader
    import os
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../templates")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    return env.get_template(template_name).render(context)
