#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os, sys

# ── Đăng ký font Unicode hỗ trợ tiếng Việt ──────────────────────────────────
FONT_DIR = os.path.join(os.path.dirname(__file__))

def find_system_font(names):
    search_paths = [
        "/Library/Fonts/", "/System/Library/Fonts/", 
        os.path.expanduser("~/Library/Fonts/"),
        "/System/Library/Fonts/Supplemental/"
    ]
    for name in names:
        for d in search_paths:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

# Tìm DejaVu / Arial / Times cho Unicode
font_regular = find_system_font(["DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttf"])
font_bold    = find_system_font(["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Arial-BoldMT.ttf"])

USE_FONT = "Helvetica"
USE_FONT_BOLD = "Helvetica-Bold"

if font_regular:
    try:
        pdfmetrics.registerFont(TTFont("MyFont", font_regular))
        USE_FONT = "MyFont"
    except:
        pass

if font_bold:
    try:
        pdfmetrics.registerFont(TTFont("MyFontBold", font_bold))
        USE_FONT_BOLD = "MyFontBold"
    except:
        pass

# ── Màu sắc ─────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a3a5c")
MID_BLUE    = colors.HexColor("#2e5f8c")
LIGHT_BLUE  = colors.HexColor("#dbe8f5")
ACCENT      = colors.HexColor("#c0392b")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#d0d0d0")
DARK_GREY   = colors.HexColor("#555555")
WHITE       = colors.white
BLACK       = colors.black

# ── Page setup ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_LEFT   = 2.5 * cm
MARGIN_RIGHT  = 2.0 * cm
MARGIN_TOP    = 2.5 * cm
MARGIN_BOTTOM = 2.5 * cm
CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT

# ── Styles ──────────────────────────────────────────────────────────────────
def make_style(name, font=None, fontSize=10, leading=14, alignment=TA_LEFT,
               textColor=BLACK, spaceAfter=4, spaceBefore=2, bold=False,
               leftIndent=0, rightIndent=0):
    if font is None:
        font = USE_FONT_BOLD if bold else USE_FONT
    return ParagraphStyle(
        name=name, fontName=font, fontSize=fontSize, leading=leading,
        alignment=alignment, textColor=textColor,
        spaceAfter=spaceAfter, spaceBefore=spaceBefore,
        leftIndent=leftIndent, rightIndent=rightIndent
    )

st_header_code = make_style("header_code", fontSize=8, textColor=DARK_GREY)
st_doc_title   = make_style("doc_title", fontSize=16, bold=True,
                             textColor=DARK_BLUE, alignment=TA_CENTER,
                             spaceAfter=6, spaceBefore=6)
st_subtitle    = make_style("subtitle", fontSize=11, bold=True,
                             textColor=MID_BLUE, alignment=TA_CENTER, spaceAfter=2)
st_label       = make_style("label", fontSize=10, bold=True, textColor=DARK_BLUE)
st_value       = make_style("value", fontSize=10, textColor=BLACK)
st_section     = make_style("section", fontSize=11, bold=True,
                             textColor=WHITE, spaceAfter=4, spaceBefore=8)
st_body        = make_style("body", fontSize=9.5, leading=15, textColor=BLACK,
                             alignment=TA_JUSTIFY, spaceAfter=3)
st_body_bold   = make_style("body_bold", fontSize=9.5, leading=15, bold=True,
                             textColor=BLACK)
st_bullet      = make_style("bullet", fontSize=9.5, leading=15,
                             leftIndent=14, spaceAfter=2)
st_page_num    = make_style("page_num", fontSize=8, textColor=DARK_GREY,
                             alignment=TA_RIGHT)
st_cell        = make_style("cell", fontSize=8.2, leading=12,
                             alignment=TA_JUSTIFY, textColor=BLACK)
st_cell_bold   = make_style("cell_bold", fontSize=8.5, leading=13,
                             bold=True, alignment=TA_CENTER, textColor=DARK_BLUE)
st_cell_header = make_style("cell_header", fontSize=8.5, leading=12,
                             bold=True, alignment=TA_CENTER, textColor=WHITE)
st_sign        = make_style("sign", fontSize=9.5, alignment=TA_CENTER,
                             textColor=BLACK, spaceAfter=2)
st_sign_label  = make_style("sign_label", fontSize=9.5, bold=True,
                             alignment=TA_CENTER, textColor=BLACK)
st_note        = make_style("note", fontSize=8, textColor=DARK_GREY,
                             alignment=TA_CENTER)

# ── Header/Footer callback ───────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(DARK_BLUE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_LEFT, PAGE_H - 1.5*cm, PAGE_W - MARGIN_RIGHT, PAGE_H - 1.5*cm)
    # Code top-left
    canvas.setFont(USE_FONT, 7)
    canvas.setFillColor(DARK_GREY)
    canvas.drawString(MARGIN_LEFT, PAGE_H - 1.2*cm, "02.34-BM/ĐT/TPC")
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 1.2*cm, "Lần ban hành/sửa đổi: 1/0")
    # Footer
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(DARK_BLUE)
    canvas.line(MARGIN_LEFT, 1.5*cm, PAGE_W - MARGIN_RIGHT, 1.5*cm)
    page_no = doc.page
    total   = getattr(doc, '_total_pages', 4)
    canvas.setFont(USE_FONT, 7)
    canvas.setFillColor(DARK_GREY)
    canvas.drawString(MARGIN_LEFT, 1.0*cm, "Học phần: Vẽ Mỹ Thuật 1 — Ngành: Đồ Họa Kỹ Thuật Số")
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, 1.0*cm, f"{page_no}/4")
    canvas.restoreState()

# ── Helpers ──────────────────────────────────────────────────────────────────
def section_heading(text):
    """Trả về flowable heading với nền xanh đậm."""
    data = [[Paragraph(text, st_section)]]
    tbl  = Table(data, colWidths=[CONTENT_W])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), DARK_BLUE),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0), (-1,-1), 8),
    ]))
    return tbl

def info_row(label, value):
    data = [[Paragraph(label, st_label), Paragraph(value, st_value)]]
    tbl  = Table(data, colWidths=[4.5*cm, CONTENT_W - 4.5*cm])
    tbl.setStyle(TableStyle([
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LINEBELOW",  (0,0), (-1,-1), 0.3, MID_GREY),
    ]))
    return tbl

def p(text, style=None):
    if style is None: style = st_body
    return Paragraph(text, style)

def bp(text):
    return Paragraph(f"• {text}", st_bullet)

# ────────────────────────────────────────────────────────────────────────────
def build_doc():
    out_path = os.path.join(os.path.dirname(__file__), "VMT1_BangMoTaDoAn.pdf")
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title="Bảng Mô Tả Đồ Án – Vẽ Mỹ Thuật 1",
        author="Khoa Thiết Kế",
    )
    doc._total_pages = 4
    story = []

    # ══════════════════════════════════════════════════════════════
    # TRANG 1
    # ══════════════════════════════════════════════════════════════

    story.append(Spacer(1, 0.6*cm))

    # Tiêu đề chính
    title_data = [[Paragraph("BẢNG MÔ TẢ ĐỒ ÁN", st_doc_title)]]
    title_tbl  = Table(title_data, colWidths=[CONTENT_W])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LIGHT_BLUE),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LINEABOVE",    (0,0),(-1,0),  2, DARK_BLUE),
        ("LINEBELOW",    (0,-1),(-1,-1),2, DARK_BLUE),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Thông tin học phần
    story.append(info_row("Ngành:", "ĐỒ HỌA KỸ THUẬT SỐ"))
    story.append(info_row("Học phần:", "VẼ MỸ THUẬT 1"))

    story.append(Spacer(1, 0.5*cm))
    story.append(p("BÀI ĐỒ ÁN HỌC PHẦN: VẼ MỸ THUẬT 1", st_subtitle))

    # Meta info box
    meta_data = [
        [Paragraph("Đối tượng:", st_label),
         Paragraph("Sinh viên Chuyên ngành Đồ họa kỹ thuật số", st_value)],
        [Paragraph("Hình thức thực hiện:", st_label),
         Paragraph("Đồ án cá nhân", st_value)],
    ]
    meta_tbl = Table(meta_data, colWidths=[5*cm, CONTENT_W-5*cm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LIGHT_GREY),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("BOX",          (0,0),(-1,-1), 0.5, MID_GREY),
        ("LINEBELOW",    (0,0),(-1,-2), 0.3, MID_GREY),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── I. MỤC TIÊU ĐỒ ÁN ───────────────────────────────────────
    story.append(section_heading("I. MỤC TIÊU ĐỒ ÁN"))
    story.append(Spacer(1, 0.2*cm))
    story.append(p(
        "Sinh viên vận dụng các kiến thức và kỹ năng cơ bản của học phần Vẽ mỹ thuật 1 để rèn luyện "
        "khả năng quan sát, phân tích hình khối, tỷ lệ, đường nét, sắc độ, chất liệu và không gian."
    ))
    story.append(p(
        "Thông qua hệ thống bài ký họa, sinh viên từng bước hình thành kỹ năng tạo hình và tư duy thị "
        "giác, làm nền tảng cho các học phần chuyên ngành Đồ họa kỹ thuật số như Minh họa, Thiết kế "
        "nhân vật, Thiết kế đồ họa, Concept Art, Thiết kế game và các lĩnh vực sáng tạo hình ảnh."
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── II. NỘI DUNG ĐỒ ÁN ───────────────────────────────────────
    story.append(section_heading("II. NỘI DUNG ĐỒ ÁN"))
    story.append(Spacer(1, 0.2*cm))
    story.append(p("Sinh viên thực hiện tối thiểu <b>20 bài vẽ</b>, bao gồm các nhóm nội dung sau:"))
    story.append(Spacer(1, 0.2*cm))

    # Bảng nội dung
    noi_dung_header = [
        Paragraph("STT", st_cell_header),
        Paragraph("Nội dung", st_cell_header),
        Paragraph("Số lượng bài", st_cell_header),
        Paragraph("Yêu cầu", st_cell_header),
    ]
    noi_dung_data = [
        ["1", "Vẽ mô tả chất liệu", "02",
         "Thể hiện đặc điểm bề mặt, độ cứng – mềm, nhẵn – thô, sáng – tối của các chất liệu khác nhau"],
        ["2", "Ký họa tĩnh vật", "02",
         "Hoa, quả, vật dụng hằng ngày, đồ vật có hình khối cơ bản..."],
        ["3", "Ký họa cây", "05",
         "Nghiên cứu hình dáng, cấu trúc thân, cành, lá và đặc điểm riêng của cây"],
        ["4", "Ký họa kiến trúc", "03",
         "Nhà cửa, công trình, không gian kiến trúc, chi tiết kiến trúc..."],
        ["5", "Ký họa phong cảnh", "03",
         "Cảnh quan thiên nhiên, đường phố, không gian đô thị hoặc nông thôn..."],
        ["6", "Ký họa tự do", "05",
         "Lựa chọn đối tượng theo sở thích cá nhân, khuyến khích thể hiện cá tính và khả năng quan sát"],
    ]

    def cell(txt, bold=False, center=False):
        st = st_cell_bold if bold else st_cell
        if center:
            st = ParagraphStyle("cc", parent=st, alignment=TA_CENTER)
        return Paragraph(txt, st)

    table_rows = [noi_dung_header]
    for i, row in enumerate(noi_dung_data):
        table_rows.append([
            cell(row[0], center=True),
            cell(row[1], bold=True),
            cell(row[2], center=True),
            cell(row[3]),
        ])

    col_w = [1.2*cm, 4.5*cm, 2.5*cm, CONTENT_W - 1.2*cm - 4.5*cm - 2.5*cm]
    nd_tbl = Table(table_rows, colWidths=col_w, repeatRows=1)
    nd_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), USE_FONT_BOLD),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("ALIGN",        (1,1), (1,-1), "LEFT"),
        ("ALIGN",        (3,1), (3,-1), "LEFT"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("GRID",         (0,0), (-1,-1), 0.4, MID_GREY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_GREY]),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(nd_tbl)
    story.append(Spacer(1, 0.3*cm))

    # ── III. YÊU CẦU THỂ HIỆN ────────────────────────────────────
    story.append(section_heading("III. YÊU CẦU THỂ HIỆN"))
    story.append(Spacer(1, 0.1*cm))

    story.append(p("<b>1. Chất liệu và kỹ thuật</b>"))
    for txt in [
        "Thực hiện bằng <b>bút chì</b> hoặc <b>bút sắt màu đen</b>.",
        "Khổ giấy: <b>A4</b>.",
    ]:
        story.append(bp(txt))

    # ══════════════════════════════════════════════════════════════
    # TRANG 2
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 0.3*cm))

    for txt in [
        "Sử dụng giấy mỹ thuật hoặc loại giấy phù hợp với kỹ thuật thể hiện.",
        "Khuyến khích sinh viên khai thác đa dạng sắc độ, nét đậm – nhạt, nét nhanh – chậm và các phương pháp tạo hình phù hợp.",
    ]:
        story.append(bp(txt))
    story.append(Spacer(1, 0.2*cm))

    story.append(p("<b>2. Yêu cầu chuyên môn</b>"))
    story.append(p("Bài vẽ cần thể hiện được:"))
    for txt in [
        "Khả năng quan sát và phân tích đối tượng.",
        "Tỷ lệ và cấu trúc hình thể tương đối chính xác.",
        "Khả năng sử dụng đường nét và sắc độ.",
        "Khả năng diễn tả đặc điểm chất liệu.",
        "Khả năng tạo cảm giác không gian, chiều sâu và bố cục.",
        "Tính linh hoạt và khả năng biểu đạt cá nhân.",
    ]:
        story.append(bp(txt))
    story.append(Spacer(1, 0.2*cm))

    story.append(p("<b>3. Yêu cầu số lượng</b>"))
    for txt in [
        "Hoàn thành tối thiểu <b>20 bài vẽ</b> theo đúng 06 nhóm nội dung quy định.",
        "Sinh viên có thể thực hiện nhiều hơn số lượng tối thiểu để phát triển kỹ năng và lựa chọn bài tiêu biểu cho đồ án.",
    ]:
        story.append(bp(txt))
    story.append(Spacer(1, 0.35*cm))

    # ── IV. HỒ SƠ NỘP ĐỒ ÁN ──────────────────────────────────────
    story.append(section_heading("IV. HỒ SƠ NỘP ĐỒ ÁN"))
    story.append(Spacer(1, 0.2*cm))
    story.append(p("Sinh viên thực hiện các bước sau:"))
    story.append(Spacer(1, 0.15*cm))

    steps = [
        ("<b>Bước 1 – Hoàn thiện bài vẽ:</b>",
         "Hoàn thành toàn bộ hệ thống bài vẽ theo yêu cầu của đồ án.", []),
        ("<b>Bước 2 – Số hóa sản phẩm</b>", "", [
            "Scan hoặc chụp ảnh bài vẽ với chất lượng tốt.",
            "Đảm bảo hình ảnh rõ nét, không bị nghiêng, mất chi tiết hoặc sai lệch quá nhiều về sắc độ.",
            "Sắp xếp bài theo đúng trình tự các nhóm nội dung.",
        ]),
        ("<b>Bước 3 – Thiết kế hồ sơ PDF:</b>",
         "Tập hợp toàn bộ sản phẩm thành <b>01 file PDF</b>.", []),
    ]

    for title, desc, subs in steps:
        story.append(p(title, st_body_bold))
        if desc:
            story.append(p(desc))
        for s in subs:
            story.append(bp(s))
        story.append(Spacer(1, 0.1*cm))

    story.append(Spacer(1, 0.1*cm))
    story.append(p("File PDF cần bao gồm:"))
    pdf_items = [
        "Trang bìa.",
        "Thông tin sinh viên.",
        "Giới thiệu ngắn về đồ án.",
        "Các bài vẽ theo từng nhóm nội dung.",
        "Phần trình bày ý tưởng và cảm xúc đối với một số bài tiêu biểu.",
        "Nhận xét/đánh giá quá trình thực hiện.",
        "Trang kết thúc.",
    ]
    for i, item in enumerate(pdf_items, 1):
        story.append(bp(f"<b>{i}.</b> {item}"))

    story.append(Spacer(1, 0.4*cm))

    # ══════════════════════════════════════════════════════════════
    # TRANG 3 – Tiêu chí đánh giá (phần 1)
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 0.3*cm))
    story.append(section_heading("V. TIÊU CHÍ ĐÁNH GIÁ"))
    story.append(Spacer(1, 0.3*cm))

    # ─── Rubric header ────────────────────────────────────────────
    grades = [
        ("A+\n(9.5 – 10)", "Xuất sắc"),
        ("A\n(8.5 – 9.4)", "Giỏi"),
        ("B\n(7.0 – 8.4)", "Khá"),
        ("C\n(5.5 – 6.9)", "Trung bình"),
        ("D\n(4.0 – 5.4)", "TB Yếu"),
        ("F\n(Dưới 4)", "Không đạt"),
    ]

    def grade_cell(g, sub):
        return Paragraph(f"<b>{g}</b><br/><i>({sub})</i>",
                         ParagraphStyle("gc", parent=st_cell_header, fontSize=7.5, leading=11))

    hdr_row = [Paragraph("TIÊU CHÍ", st_cell_header)] + \
              [grade_cell(g, s) for g, s in grades]

    # ─── Nội dung chuyên môn ──────────────────────────────────────
    def c(txt):
        return Paragraph(txt, ParagraphStyle("rc", parent=st_cell, fontSize=7.8, leading=11.5))

    crit_nd = [
        Paragraph("Nội dung\nchuyên môn\n(Trọng số: 50%)",
                  ParagraphStyle("crit", parent=st_cell_bold, fontSize=8, leading=12)),
        c("Hoàn thành đầy đủ và vượt yêu cầu số lượng bài. Thể hiện rất tốt khả năng quan sát, tỷ lệ, "
          "hình khối, cấu trúc, chất liệu, không gian và sắc độ. Các nhóm bài có chất lượng đồng đều, "
          "thể hiện rõ sự tiến bộ.\n\nCó góc nhìn riêng, lựa chọn đối tượng và cách thể hiện giàu tính "
          "cá nhân. Bài ký họa tự do thể hiện rõ tư duy tạo hình và cá tính thị giác. Phần trình bày ý "
          "tưởng, cảm xúc sâu sắc, thuyết phục."),
        c("Hoàn thành đầy đủ yêu cầu. Bài vẽ thể hiện tốt khả năng quan sát, tỷ lệ, hình khối, chất "
          "liệu và không gian. Phần lớn bài có chất lượng tốt và ổn định.\n\nCó sự chủ động và dấu ấn "
          "cá nhân trong cách lựa chọn, quan sát và thể hiện. Trình bày được ý tưởng và cảm xúc rõ ràng."),
        c("Hoàn thành cơ bản các yêu cầu. Khả năng quan sát và thể hiện hình khối, tỷ lệ, chất liệu ở "
          "mức khá; một số bài còn hạn chế về cấu trúc hoặc sắc độ.\n\nCó một số yếu tố cá nhân trong "
          "cách thể hiện nhưng chưa thật nổi bật. Phần trình bày ý tưởng và cảm xúc tương đối rõ."),
        c("Hoàn thành phần lớn yêu cầu nhưng chất lượng bài chưa đồng đều. Khả năng quan sát, tỷ lệ, "
          "hình khối và diễn tả chất liệu còn hạn chế.\n\nCách thể hiện còn phụ thuộc nhiều vào mẫu; "
          "ít dấu ấn cá nhân. Trình bày ý tưởng còn chung chung."),
        c("Thiếu bài hoặc chưa đáp ứng đầy đủ các nhóm nội dung. Nhiều bài còn sai về tỷ lệ, hình khối, "
          "cấu trúc và khả năng diễn tả.\n\nÍt thể hiện sự chủ động và sáng tạo; chủ yếu sao chép đối "
          "tượng. Phần trình bày ý tưởng còn sơ sài."),
        c("Không hoàn thành yêu cầu cơ bản; thiếu nhiều bài hoặc nội dung không đúng chủ đề. Kỹ năng "
          "thể hiện chưa đạt yêu cầu.\n\nKhông thể hiện được ý tưởng hoặc dấu ấn cá nhân; không có phần "
          "trình bày ý tưởng/cảm xúc theo yêu cầu."),
    ]

    crit_ht = [
        Paragraph("Hình thức\n(Trọng số: 20%)",
                  ParagraphStyle("crit", parent=st_cell_bold, fontSize=8, leading=12)),
        c("Bài vẽ sạch, rõ, bố cục hợp lý; đường nét và sắc độ được kiểm soát tốt. Hồ sơ PDF được tổ "
          "chức khoa học, thẩm mỹ, hình ảnh scan/chụp chất lượng cao."),
        c("Trình bày đẹp, sạch và tương đối thống nhất. Bố cục bài vẽ hợp lý; file PDF đầy đủ, rõ ràng "
          "và có tính thẩm mỹ."),
        c("Trình bày tương đối tốt nhưng còn một số lỗi về bố cục, nét vẽ, sắc độ hoặc chất lượng hình "
          "ảnh số hóa."),
        c("Hình thức trình bày ở mức đạt; còn nhiều lỗi về bố cục, vệ sinh bài, chất lượng scan/chụp "
          "hoặc sắp xếp PDF."),
        c("Trình bày thiếu chỉn chu, nhiều bài chưa hoàn thiện; file PDF còn thiếu hoặc sắp xếp chưa "
          "hợp lý."),
        c("Không đảm bảo yêu cầu trình bày; bài vẽ hoặc hồ sơ PDF thiếu nghiêm trọng, khó đánh giá."),
    ]

    crit_kn = [
        Paragraph("Kỹ năng\n(Trọng số: 20%)",
                  ParagraphStyle("crit", parent=st_cell_bold, fontSize=8, leading=12)),
        c("Thành thạo kỹ thuật chì/bút sắt; kiểm soát tốt đường nét, đậm nhạt, sắc độ và chất liệu. "
          "Có khả năng quan sát và chuyển hóa đối tượng thành hình ảnh có tính tạo hình cao."),
        c("Sử dụng tốt kỹ thuật vẽ; đường nét, sắc độ và cách diễn tả tương đối linh hoạt. Có khả năng "
          "xử lý nhiều dạng đối tượng."),
        c("Nắm được kỹ thuật cơ bản; thể hiện được hình khối và sắc độ nhưng khả năng kiểm soát nét và "
          "chất liệu chưa thật ổn định."),
        c("Nắm được một số kỹ thuật cơ bản nhưng thao tác còn vụng; đường nét, sắc độ và hình khối còn "
          "thiếu chính xác."),
        c("Kỹ năng vẽ còn yếu; chưa kiểm soát được đường nét, tỷ lệ, sắc độ và hình khối."),
        c("Chưa hình thành kỹ năng cơ bản; bài vẽ không thể hiện được yêu cầu kỹ thuật của học phần."),
    ]

    rubric_data = [hdr_row, crit_nd, crit_ht, crit_kn]

    col_w_rubric = [2.8*cm] + [(CONTENT_W - 2.8*cm) / 6] * 6
    rubric_tbl = Table(rubric_data, colWidths=col_w_rubric, repeatRows=1)

    row_bg = [LIGHT_GREY, WHITE, LIGHT_GREY]
    rubric_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  DARK_BLUE),
        ("TEXTCOLOR",    (0,0), (-1,0),  WHITE),
        ("BACKGROUND",   (0,1), (0,-1),  LIGHT_BLUE),
        ("BACKGROUND",   (1,1), (-1,1),  WHITE),
        ("BACKGROUND",   (1,2), (-1,2),  LIGHT_GREY),
        ("BACKGROUND",   (1,3), (-1,3),  WHITE),
        ("FONTNAME",     (0,1), (0,-1),  USE_FONT_BOLD),
        ("GRID",         (0,0), (-1,-1), 0.4, MID_GREY),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("ALIGN",        (0,0), (0,-1),  "CENTER"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(rubric_tbl)

    # ══════════════════════════════════════════════════════════════
    # TRANG 4 – Chữ ký
    # ══════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 0.5*cm))

    # Chữ ký
    sign_data = [
        [
            Paragraph("Giảng viên phản biện duyệt đề", st_sign_label),
            Paragraph("Giảng viên ra đề", st_sign_label),
        ],
        [
            Paragraph("(Ghi rõ nhận xét; ý kiến đề xuất; ký và ghi rõ họ tên)", st_note),
            Paragraph("(Ký và ghi rõ họ tên)", st_note),
        ],
        [Spacer(1, 3*cm), Spacer(1, 3*cm)],
        [
            Paragraph("……………………………………………………<br/>"
                      "……………………………………………………<br/>"
                      "……………………………………………………<br/>"
                      "……………………………………………………",
                      ParagraphStyle("dots", parent=st_sign, textColor=DARK_GREY)),
            Paragraph("…………………………………………",
                      ParagraphStyle("dots", parent=st_sign, textColor=DARK_GREY)),
        ],
    ]
    sign_tbl = Table(sign_data, colWidths=[CONTENT_W/2, CONTENT_W/2])
    sign_tbl.setStyle(TableStyle([
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LINEABOVE",   (0,0), (-1,0),  1, DARK_BLUE),
    ]))
    story.append(sign_tbl)
    story.append(Spacer(1, 1*cm))

    # Ghi chú cuối
    note_box_data = [[
        Paragraph(
            "<b>Lưu ý:</b> Đồ án được nộp dưới dạng file PDF. Sinh viên chịu trách nhiệm về "
            "tính trung thực và bản quyền của toàn bộ nội dung trong hồ sơ đồ án.",
            ParagraphStyle("note_box", parent=st_body, fontSize=9, textColor=DARK_GREY)
        )
    ]]
    note_tbl = Table(note_box_data, colWidths=[CONTENT_W])
    note_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LIGHT_BLUE),
        ("BOX",          (0,0),(-1,-1), 0.5, MID_BLUE),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    story.append(note_tbl)

    # ── Build ────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅ Đã tạo file: {out_path}")
    return out_path

if __name__ == "__main__":
    build_doc()
