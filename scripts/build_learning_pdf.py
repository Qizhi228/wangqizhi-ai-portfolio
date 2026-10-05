"""将中文学习文档生成 PDF。"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "docs" / "LEARNING_GUIDE.md"
OUTPUT = ROOT / "docs" / "LEARNING_GUIDE.pdf"
FONT = Path("/System/Library/Fonts/STHeiti Light.ttc")


def register_font() -> str:
    font_name = "WQZHeiti"
    pdfmetrics.registerFont(TTFont(font_name, str(FONT), subfontIndex=0))
    return font_name


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='WQZMono'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def build() -> None:
    font_name = register_font()
    pdfmetrics.registerFont(TTFont("WQZMono", str(FONT), subfontIndex=0))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("WQZTitle", parent=styles["Title"], fontName=font_name, fontSize=22, leading=29, textColor=colors.HexColor("#102a2a"), spaceAfter=12))
    styles.add(ParagraphStyle("WQZH1", parent=styles["Heading1"], fontName=font_name, fontSize=16, leading=22, textColor=colors.HexColor("#0d5952"), spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle("WQZH2", parent=styles["Heading2"], fontName=font_name, fontSize=12.5, leading=18, textColor=colors.HexColor("#14766d"), spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle("WQZBody", parent=styles["BodyText"], fontName=font_name, fontSize=9.5, leading=15, alignment=TA_LEFT, spaceAfter=6))
    styles.add(ParagraphStyle("WQZBullet", parent=styles["BodyText"], fontName=font_name, fontSize=9.5, leading=15, leftIndent=13, firstLineIndent=-8, spaceAfter=3))
    styles.add(ParagraphStyle("WQZCode", parent=styles["Code"], fontName=font_name, fontSize=8.2, leading=12, leftIndent=10, rightIndent=10, backColor=colors.HexColor("#f1f5f4"), borderColor=colors.HexColor("#d6e5e2"), borderWidth=.5, borderPadding=6, spaceAfter=8))
    styles.add(ParagraphStyle("WQZSmall", parent=styles["BodyText"], fontName=font_name, fontSize=8, leading=12, textColor=colors.HexColor("#61716f")))

    story = []
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    in_code = False
    code_lines = []
    table_lines = []

    def flush_table():
        nonlocal table_lines
        if not table_lines:
            return
        rows = []
        for line in table_lines:
            if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append([Paragraph(inline(cell), styles["WQZSmall"]) for cell in cells])
        if rows:
            table = Table(rows, repeatRows=1, colWidths=[45 * mm, 45 * mm, 85 * mm])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dff2ee")),
                ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#bfd4d0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(table)
            story.append(Spacer(1, 5))
        table_lines = []

    def flush_code():
        nonlocal code_lines
        if code_lines:
            story.append(Paragraph(inline("\n".join(code_lines)).replace("\n", "<br/>"), styles["WQZCode"]))
            code_lines = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_table()
            if in_code:
                flush_code()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        if line.startswith("|"):
            table_lines.append(line)
            continue
        flush_table()
        if not line.strip():
            story.append(Spacer(1, 3))
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["WQZTitle"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["WQZH1"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["WQZH2"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + inline(line[2:]), styles["WQZBullet"]))
        elif re.match(r"^\d+\. ", line):
            story.append(Paragraph(inline(line), styles["WQZBullet"]))
        else:
            story.append(Paragraph(inline(line), styles["WQZBody"]))
    flush_table()
    flush_code()

    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=17 * mm, leftMargin=17 * mm, topMargin=15 * mm, bottomMargin=15 * mm, title="王启智 AI 应用作品集学习文档", author="王启智")
    document.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
