from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

files = [
    ("docs/analyst_guide.md", "docs/analyst_guide.pdf"),
    ("docs/acceptance_checklist.md", "docs/acceptance_checklist.pdf"),
]

for md_file, pdf_file in files:
    doc = SimpleDocTemplate(pdf_file)
    story = []

    with open(md_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # Remove markdown formatting
            line = line.replace("#", "")
            line = line.replace("**", "")
            line = line.replace("`", "")
            line = line.replace("-", "•")

            story.append(Paragraph(line, styles["BodyText"]))

    doc.build(story)
    print(f"Created: {pdf_file}")

print("Done!")