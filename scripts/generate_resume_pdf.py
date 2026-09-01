"""Generate PDF Resume for Ishaan Gupta using ReportLab."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_pdf(filename: str = "resume/Ishaan_Gupta_Resume.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Document Setup with 0.4 inch (28 pt) margins to ensure 1-page fit
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()
    usable_width = 556  # 612 - 56

    # Custom Typography Styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#111111')
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333')
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=12,
        textColor=colors.HexColor('#111111')
    )

    left_bold = ParagraphStyle(
        'LeftBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=colors.HexColor('#111111')
    )

    left_regular = ParagraphStyle(
        'LeftRegular',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#333333')
    )

    right_text = ParagraphStyle(
        'RightText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#333333')
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor('#222222')
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=11,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=1.5,
        textColor=colors.HexColor('#222222')
    )

    story = []

    # 1. Header
    story.append(Paragraph("ISHAAN GUPTA", name_style))
    story.append(Spacer(1, 2))
    contact_text = (
        "guptaishaan361@gmail.com &nbsp;|&nbsp; +91-9264955782 &nbsp;|&nbsp; Lucknow, India &nbsp;|&nbsp; "
        "github.com/Ishaan012846 &nbsp;|&nbsp; LinkedIn &nbsp;|&nbsp; LeetCode"
    )
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 6))

    # Helper function for section headings with dividing line
    def add_section_header(title_text):
        story.append(Paragraph(title_text, section_heading_style))
        story.append(Spacer(1, 1))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#111111'), spaceAfter=4, spaceBefore=1))

    # Helper for 2-column rows (Left title/subtitle, Right location/dates)
    def add_two_column_row(left_p, right_p):
        t = Table([[left_p, right_p]], colWidths=[usable_width * 0.72, usable_width * 0.28])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t)

    # 2. EDUCATION
    add_section_header("EDUCATION")
    
    add_two_column_row(
        Paragraph("DIT University", left_bold),
        Paragraph("Dehradun, Uttarakhand", right_text)
    )
    add_two_column_row(
        Paragraph("B.Tech in Computer Science - CGPA: 6.17", left_regular),
        Paragraph("July 2023 – July 2027", right_text)
    )
    story.append(Spacer(1, 3))

    add_two_column_row(
        Paragraph("Red Rose Senior Secondary School", left_bold),
        Paragraph("Lucknow, Uttar Pradesh", right_text)
    )
    add_two_column_row(
        Paragraph("Class XII - 81%", left_regular),
        Paragraph("July 2020 – July 2022", right_text)
    )
    story.append(Spacer(1, 3))

    add_two_column_row(
        Paragraph("City Montessori School", left_bold),
        Paragraph("Lucknow, Uttar Pradesh", right_text)
    )
    add_two_column_row(
        Paragraph("Class X - 84%", left_regular),
        Paragraph("Completed July 2020", right_text)
    )
    story.append(Spacer(1, 6))

    # 3. PROFESSIONAL SUMMARY
    add_section_header("PROFESSIONAL SUMMARY")
    summary_txt = (
        "B.Tech Computer Science student specializing in Software Engineering, Cybersecurity & AI Systems. "
        "Skilled in Java, Python, Web VAPT, Data Structures & Algorithms, SQL, and MLOps. Built high-impact "
        "projects including an automated Web Application VAPT Lab, a Corrective RAG (CRAG) pipeline, and an "
        "Enterprise AI Operations platform. Proven leadership managing large-scale university events."
    )
    story.append(Paragraph(summary_txt, body_style))
    story.append(Spacer(1, 6))

    # 4. SKILLS
    add_section_header("SKILLS")
    skills = [
        ("Programming Languages", "C, Python, Java, JavaScript, HTML5, CSS3, SQL"),
        ("Libraries / Frameworks", "LangChain, FastAPI, ChromaDB, PyTorch, OpenCV, NumPy, MediaPipe, Java Swing"),
        ("Security & MLOps Tools", "OWASP ZAP, Nmap, Burp Suite, Docker, Kubernetes, Prometheus, Grafana, MLflow, Git, GitHub, VS Code, IntelliJ IDEA"),
        ("Databases & Concepts", "MySQL, RESTful APIs, OOP, Data Structures & Algorithms (DSA), Multithreading, Web Application VAPT, OWASP Top 10, CVSS v3.1")
    ]
    for cat, val in skills:
        txt = f"<b>{cat}:</b> {val}"
        story.append(Paragraph(txt, body_style))
        story.append(Spacer(1, 1.5))
    story.append(Spacer(1, 4))

    # 5. PROJECTS
    add_section_header("PROJECTS")

    # Project 1: Web Application VAPT Lab
    add_two_column_row(
        Paragraph("Web Application VAPT Lab & Security Assessment", left_bold),
        Paragraph("Python, Docker, OWASP ZAP, Nmap, Burp Suite, HTML/CSS/JS", right_text)
    )
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/web-vapt-lab</i></font>", left_regular))
    story.append(Spacer(1, 1))
    story.append(Paragraph("&bull; Engineered an isolated local VAPT laboratory containerizing OWASP Juice Shop (127.0.0.1:3000), implementing Python scope-validation modules to strictly enforce loopback allowlists.", bullet_style))
    story.append(Paragraph("&bull; Automated service version enumeration (Nmap) and passive vulnerability scanning (OWASP ZAP baseline), normalizing findings into standardized JSON schema definitions.", bullet_style))
    story.append(Paragraph("&bull; Conducted manual security assessments via Burp Suite to validate SQL Injection, XSS, and IDOR vulnerabilities, generating Markdown reports and a responsive static HTML metrics dashboard.", bullet_style))
    story.append(Spacer(1, 4))

    # Project 2: Corrective RAG
    add_two_column_row(
        Paragraph("Corrective RAG (CRAG) System", left_bold),
        Paragraph("Python, LangChain, OpenAI API, ChromaDB, FastAPI", right_text)
    )
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/crag-ai-system</i></font>", left_regular))
    story.append(Spacer(1, 1))
    story.append(Paragraph("&bull; Engineered a Corrective Retrieval-Augmented Generation (CRAG) pipeline, reducing LLM hallucination rates by 35% via dynamic relevancy scoring.", bullet_style))
    story.append(Paragraph("&bull; Implemented query re-writing algorithms and hallucination detection with automated Tavily web search fallbacks, boosting factual accuracy to 92%.", bullet_style))
    story.append(Paragraph("&bull; Utilized ChromaDB vector embeddings and LangChain framework to orchestrate self-corrective retrieval workflows processing 50+ queries/min.", bullet_style))
    story.append(Spacer(1, 4))

    # Project 3: Enterprise AI Operations Platform
    add_two_column_row(
        Paragraph("Enterprise AI Operations Platform", left_bold),
        Paragraph("Python, FastAPI, Docker, Kubernetes, Prometheus, MLflow", right_text)
    )
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/enterprise-ai-ops</i></font>", left_regular))
    story.append(Spacer(1, 1))
    story.append(Paragraph("&bull; Developed an end-to-end Enterprise AI Operations (AIOps/MLOps) platform to monitor, auto-scale, and manage 10+ production ML microservices.", bullet_style))
    story.append(Paragraph("&bull; Integrated real-time telemetry, latency monitoring, and token usage tracking via Prometheus and Grafana dashboards, maintaining 99.9% uptime.", bullet_style))
    story.append(Paragraph("&bull; Containerized microservices using Docker and orchestrated Kubernetes deployments with API gateway security, cutting deployment overhead by 40%.", bullet_style))
    story.append(Spacer(1, 6))

    # 6. POSITIONS OF RESPONSIBILITY & ACHIEVEMENTS
    add_section_header("POSITIONS OF RESPONSIBILITY & ACHIEVEMENTS")
    story.append(Paragraph("&bull; <b>Overall Coordinator - Avahan 2024:</b> Managed end-to-end operations, crowd logistics, budgeting, and a committee of 40+ student volunteers for DIT University annual freshman program, serving 3,000+ incoming students.", bullet_style))
    story.append(Paragraph("&bull; Solved 120+ Data Structures & Algorithms (DSA) problems on LeetCode using Java.", bullet_style))
    story.append(Spacer(1, 4))

    # 7. CERTIFICATIONS
    add_section_header("CERTIFICATIONS")
    certs = [
        "Java (Basic) – HackerRank",
        "Problem Solving (Basic) – HackerRank",
        "SQL (Basic) – HackerRank",
        "OCI AI Foundations – Oracle"
    ]
    for c in certs:
        story.append(Paragraph(f"&bull; {c}", bullet_style))

    # Build document
    doc.build(story)
    print(f"[+] PDF generated successfully: {filename}")


if __name__ == "__main__":
    generate_pdf()
