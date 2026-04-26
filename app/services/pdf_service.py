from datetime import datetime
from fpdf import FPDF


class CallSheetPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, self.title_text, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)


def generate_call_sheet_pdf(tour_name: str, venue: str, schedule_text: str) -> bytes:
    pdf = CallSheetPDF()
    pdf.title_text = f"CALL SHEET: {tour_name}"
    pdf.add_page()

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Venue: {venue}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(
        0,
        8,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Schedule", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 7, schedule_text)

    return bytes(pdf.output())
