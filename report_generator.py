from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, salary, roadmap, ai_roadmap):
    file_name = "career_report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Career Report", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Predicted Salary: {salary:.2f} LPA", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Roadmap:", styles["Heading2"]))
    for r in roadmap:
        content.append(Paragraph(f"- {r}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("AI Roadmap:", styles["Heading2"]))
    content.append(Paragraph(ai_roadmap, styles["Normal"]))

    doc.build(content)

    return file_name