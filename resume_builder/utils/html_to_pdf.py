from xhtml2pdf import pisa
import io

def convert_html_to_pdf(source_html):
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.StringIO(source_html), dest=result)
    if not pdf.err:
        return result.getvalue()
    return None
