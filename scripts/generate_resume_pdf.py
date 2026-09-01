"""Generate Single-Page PDF Resume for Ishaan Gupta using ReportLab."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


def generate_pdf(filename: str = "resume/Ishaan_Gupta_Resume.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Tight 0.28-inch (20 pt) margins to guarantee exact 1-page fit
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    usable_width = 612 - 40  # 572 pt

    # Typography Styles tailored for 1-page layout
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#111111')
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=9.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333')
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=10.5,
        textColor=colors.HexColor('#111111')
    )

    left_bold = ParagraphStyle(
        'LeftBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=10,
        textColor=colors.HexColor('#111111')
    )

    left_regular = ParagraphStyle(
        'LeftRegular',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=9.5,
        textColor=colors.HexColor('#333333')
    )

    right_text = ParagraphStyle(
        'RightText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=9.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#333333')
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=9.8,
        textColor=colors.HexColor('#222222')
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=9.5,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=0.5,
        textColor=colors.HexColor('#222222')
    )

    story = []

    # 1. Header
    story.append(Paragraph("ISHAAN GUPTA", name_style))
    story.append(Spacer(1, 1))
    contact_text = (
        "guptaishaan361@gmail.com &nbsp;|&nbsp; +91-9264955782 &nbsp;|&nbsp; Lucknow, India &nbsp;|&nbsp; "
        "github.com/Ishaan012846 &nbsp;|&nbsp; LinkedIn &nbsp;|&nbsp; LeetCode"
    )
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 3))

    def add_section_header(title_text):
        story.append(Paragraph(title_text, section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#111111'), spaceAfter=2, spaceBefore=1))

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
    
    add_two_column_row(Paragraph("DIT University", left_bold), Paragraph("Dehradun, Uttarakhand", right_text))
    add_two_column_row(Paragraph("B.Tech in Computer Science - CGPA: 6.17", left_regular), Paragraph("July 2023 – July 2027", right_text))
    story.append(Spacer(1, 1.5))

    add_two_column_row(Paragraph("Red Rose Senior Secondary School", left_bold), Paragraph("Lucknow, Uttar Pradesh", right_text))
    add_two_column_row(Paragraph("Class XII - 81%", left_regular), Paragraph("July 2020 – July 2022", right_text))
    story.append(Spacer(1, 1.5))

    add_two_column_row(Paragraph("City Montessori School", left_bold), Paragraph("Lucknow, Uttar Pradesh", right_text))
    add_two_column_row(Paragraph("Class X - 84%", left_regular), Paragraph("Completed July 2020", right_text))
    story.append(Spacer(1, 3))

    # 3. PROFESSIONAL SUMMARY
    add_section_header("PROFESSIONAL SUMMARY")
    summary_txt = (
        "B.Tech Computer Science student specializing in Software Engineering, Cybersecurity & AI Systems. "
        "Skilled in Java, Python, Web VAPT, Data Structures & Algorithms, SQL, and MLOps. Built high-impact "
        "projects including an automated Web Application VAPT Lab, a Corrective RAG (CRAG) pipeline, and an "
        "Enterprise AI Operations platform. Proven leadership managing large-scale university events."
    )
    story.append(Paragraph(summary_txt, body_style))
    story.append(Spacer(1, 3))

    # 4. SKILLS
    add_section_header("SKILLS")
    skills = [
        ("Programming Languages", "C, Python, Java, JavaScript, HTML5, CSS3, SQL"),
        ("Libraries / Frameworks", "LangChain, FastAPI, ChromaDB, PyTorch, OpenCV, NumPy, MediaPipe, Java Swing"),
        ("Security & MLOps Tools", "OWASP ZAP, Nmap, Burp Suite, Docker, Kubernetes, Prometheus, Grafana, MLflow, Git, GitHub"),
        ("Databases & Concepts", "MySQL, RESTful APIs, OOP, Data Structures & Algorithms (DSA), Multithreading, Web VAPT, OWASP Top 10, CVSS v3.1")
    ]
    for cat, val in skills:
        txt = f"<b>{cat}:</b> {val}"
        story.append(Paragraph(txt, body_style))
        story.append(Spacer(1, 0.5))
    story.append(Spacer(1, 3))

    # 5. PROJECTS
    add_section_header("PROJECTS")

    # Project 1: Web Application VAPT Lab
    add_two_column_row(Paragraph("Web Application VAPT Lab & Security Assessment", left_bold), Paragraph("Python, Docker, OWASP ZAP, Nmap, Burp Suite, HTML/CSS/JS", right_text))
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/web-vapt-lab</i></font>", left_regular))
    story.append(Paragraph("&bull; Engineered isolated local VAPT lab containerizing OWASP Juice Shop (127.0.0.1:3000) with Python scope-validation modules.", bullet_style))
    story.append(Paragraph("&bull; Automated service version enumeration (Nmap) and passive vulnerability scanning (OWASP ZAP baseline) normalized into JSON schemas.", bullet_style))
    story.append(Paragraph("&bull; Conducted manual Burp Suite assessments validating SQLi, XSS, and IDOR flaws, generating Markdown reports & static HTML dashboard.", bullet_style))
    story.append(Spacer(1, 2))

    # Project 2: Corrective RAG
    add_two_column_row(Paragraph("Corrective RAG (CRAG) System", left_bold), Paragraph("Python, LangChain, OpenAI API, ChromaDB, FastAPI", right_text))
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/crag-ai-system</i></font>", left_regular))
    story.append(Paragraph("&bull; Engineered Corrective Retrieval-Augmented Generation (CRAG) pipeline, reducing LLM hallucination rates by 35% via relevancy scoring.", bullet_style))
    story.append(Paragraph("&bull; Implemented query re-writing & hallucination detection with automated Tavily web search fallbacks, boosting factual accuracy to 92%.", bullet_style))
    story.append(Paragraph("&bull; Utilized ChromaDB vector embeddings and LangChain framework to orchestrate self-corrective retrieval processing 50+ queries/min.", bullet_style))
    story.append(Spacer(1, 2))

    # Project 3: Enterprise AI Operations Platform
    add_two_column_row(Paragraph("Enterprise AI Operations Platform", left_bold), Paragraph("Python, FastAPI, Docker, Kubernetes, Prometheus, MLflow", right_text))
    story.append(Paragraph("<font color='#444444'><i>github.com/Ishaan012846/enterprise-ai-ops</i></font>", left_regular))
    story.append(Paragraph("&bull; Developed end-to-end Enterprise AI Operations platform to monitor, auto-scale, and manage 10+ production ML microservices.", bullet_style))
    story.append(Paragraph("&bull; Integrated real-time telemetry & latency tracking via Prometheus/Grafana dashboards, maintaining 99.9% uptime.", bullet_style))
    story.append(Paragraph("&bull; Containerized microservices using Docker & orchestrated Kubernetes deployments with API gateway security, cutting overhead by 40%.", bullet_style))
    story.append(Spacer(1, 3))

    # 6. POSITIONS OF RESPONSIBILITY & ACHIEVEMENTS
    add_section_header("POSITIONS OF RESPONSIBILITY & ACHIEVEMENTS")
    story.append(Paragraph("&bull; <b>Overall Coordinator - Avahan 2024:</b> Managed operations, logistics, budgeting, and 40+ student committee for DIT freshman program (3,000+ students).", bullet_style))
    story.append(Paragraph("&bull; Solved 120+ Data Structures & Algorithms (DSA) problems on LeetCode using Java.", bullet_style))
    story.append(Spacer(1, 3))

    # 7. CERTIFICATIONS
    add_section_header("CERTIFICATIONS")
    certs_text = "&bull; Java (Basic) – HackerRank &nbsp;&nbsp;|&nbsp;&nbsp; &bull; Problem Solving (Basic) – HackerRank &nbsp;&nbsp;|&nbsp;&nbsp; &bull; SQL (Basic) – HackerRank &nbsp;&nbsp;|&nbsp;&nbsp; &bull; OCI AI Foundations – Oracle"
    story.append(Paragraph(certs_text, bullet_style))

    # Build document
    doc.build(story)
    print(f"[+] PDF generated successfully: {filename}")


if __name__ == "__main__":
    generate_pdf()
