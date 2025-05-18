from xhtml2pdf import pisa
import streamlit as st
import io

def export_pdf(data):
    html = f"""
    <html>
    <body>
    <h1>{data.get('name', 'Name not provided')}</h1>
    <p>Email: {data.get('email', 'Email not provided')}</p>
    <h3>Skills</h3>
    <p>{data.get('skills', 'Skills not provided')}</p>
    <h3>Experience</h3>
    <p>{data.get('experience', 'Experience not provided')}</p>
    </body>
    </html>
    """

    # Generate PDF in memory
    result = io.BytesIO()
    pdf_status = pisa.CreatePDF(src=html, dest=result)

    if not pdf_status.err:
        st.download_button(
            label="📄 Download PDF",
            data=result.getvalue(),
            file_name="resume.pdf",
            mime="application/pdf"
        )
        st.success("PDF created successfully ✅")
    else:
        st.error("Failed to create PDF ❌")
