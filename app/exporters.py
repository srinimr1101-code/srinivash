import os
from datetime import datetime

from fpdf import FPDF

EXPORT_DIR = os.path.join("static", "exports")


def _latin(text):
    """Core PDF fonts are latin-1 only; replace anything else."""
    return (text or "").encode("latin-1", "replace").decode("latin-1")


def save_pdf(layout, title="ComicCraft Comic"):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for p in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 10, _latin(f"Panel {p['panel']}: {p['title']}"), new_x="LMARGIN", new_y="NEXT")
        if os.path.exists(p["image"]):
            pdf.image(p["image"], x=30, w=150)
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, _latin(p["scene"]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(0, 7, _latin(p["text"]), new_x="LMARGIN", new_y="NEXT")
    name = f"comic_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    path = os.path.join(EXPORT_DIR, name)
    pdf.output(path)
    return path.replace("\\", "/")
