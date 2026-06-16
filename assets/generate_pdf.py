"""Convert HTML pitch deck to PDF for submission."""

import weasyprint
import os

html_path = r'E:\india-runs-ai-recruiter\assets\pitch-deck.html'
pdf_path = r'E:\india-runs-ai-recruiter\assets\pitch-deck.pdf'

doc = weasyprint.HTML(filename=html_path)
doc.write_pdf(pdf_path)

print(f'Saved: {pdf_path} ({os.path.getsize(pdf_path)} bytes)')
