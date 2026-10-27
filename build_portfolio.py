#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo hồ sơ đồ án PDF – Vẽ Mỹ Thuật 1
Sinh viên: Nguyễn Văn Ngà | MSSV: 2603ITA0022
"""

import os
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Đường dẫn ──────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "VMT1_NguyenVanNga_2603ita0022.pdf")

LOGO_TOPICA = os.path.join(BASE, "cover_image1.png")

# ─── Thông tin sinh viên ────────────────────────────────────────────────────
SV_NAME   = "Nguyễn Văn Ngà"
SV_MSSV   = "2603ITA0022"
SV_CLASS  = "Vẽ Mỹ Thuật 1"
SV_NGANH  = "Đồ Họa Kỹ Thuật Số"
SV_KHOA   = "K13"
SV_DATE   = "Huế, tháng 10 năm 2026"
GV_NAME   = ""   # để trống

# ─── 6 nhóm bài – ánh xạ tên file ─────────────────────────────────────────
GROUPS = [
    {
        "title": "Nhóm 1 – Vẽ Mô Tả Chất Liệu",
        "subtitle": "Thể hiện đặc điểm bề mặt: độ cứng – mềm, nhẵn – thô, sáng – tối",
        "color": "#1a3a5c",
        "images": [
            ("ky_hoa_chat_lieu_go_da_vai.jpg",
             "Chất liệu gỗ – đá – vải",
             "Bút sắt, A4. Diễn tả rõ độ nhám của đá, vân thô của gỗ và sự mềm mại của vải "
             "thông qua cách đổ bóng và hướng nét vẽ."),
            ("ky_hoa_chat_lieu_kim_loai_thuy_tinh_gom.jpg",
             "Chất liệu kim loại – thủy tinh – gốm",
             "Bút sắt, A4. Tương phản giữa bề mặt nhẵn bóng của kim loại/thủy tinh với độ "
             "mờ đục của gốm; phản chiếu ánh sáng được thể hiện qua vùng sáng mạnh."),
        ],
    },
    {
        "title": "Nhóm 2 – Ký Họa Tĩnh Vật",
        "subtitle": "Hoa, quả, vật dụng hằng ngày, đồ vật có hình khối cơ bản",
        "color": "#1e5c3a",
        "images": [
            ("ky_hoa_lo_hoa.jpg",
             "Lọ hoa",
             "Bút chì, A4. Nghiên cứu hình trụ, miệng lọ và bố cục hoa; chú ý diễn tả "
             "chiều sâu không gian qua ánh sáng và bóng đổ."),
            ("ky_hoa_cai_am_tra.jpg",
             "Cái ấm trà",
             "Bút sắt, A4. Tỷ lệ thân – vòi – tay cầm; bề mặt sứ được thể hiện qua "
             "vùng phản quang trên thân ấm."),
        ],
    },
    {
        "title": "Nhóm 3 – Ký Họa Cây",
        "subtitle": "Nghiên cứu hình dáng, cấu trúc thân, cành, lá và đặc điểm riêng của cây (6 bài)",
        "color": "#3a5c1a",
        "images": [
            ("ky_hoa_cay.jpg",
             "Ký họa cây (tổng quát)",
             "Bút sắt, A4. Thể hiện cấu trúc tổng thể và phân cành; mảng tối – sáng "
             "của tán lá được diễn tả bằng nét chéo dày – thưa."),
            ("ky_hoa_cay_bang.jpg",
             "Cây bàng",
             "Bút sắt, A4. Tán rộng ngang đặc trưng; chú ý vân thô của thân và "
             "các lớp lá xếp theo tầng."),
            ("ky_hoa_cay_co_thu.jpg",
             "Cây cổ thụ",
             "Bút chì, A4. Rễ nổi mạnh mẽ, thân xù xì nhiều u bướu; bóng đổ tạo "
             "chiều sâu khối tích lớn."),
            ("ky_hoa_cay_dua.jpg",
             "Cây dừa",
             "Bút sắt, A4. Dáng cây cong tự nhiên đặc trưng của vùng nhiệt đới; "
             "sống lá nhọn và bẹ lá được chú trọng."),
            ("ky_hoa_cay_thong.jpg",
             "Cây thông",
             "Bút sắt, A4. Dáng cây thông hình tháp đặc trưng; cành ngang đều đặn và từng chùm kim được diễn tả bằng nét ngắn, mau, tạo cảm giác dày dặn của tán lá."),
            ("ky_hoa_cay_phuong.jpg",
             "Cây phượng",
             "Bút sắt, A4. Cành phượng đan xen tạo nhịp điệu; chùm hoa được gợi "
             "bằng nét mau, tạo cảm giác rực rỡ."),
        ],
    },
    {
        "title": "Nhóm 4 – Ký Họa Kiến Trúc",
        "subtitle": "Nhà cửa, công trình, không gian kiến trúc, chi tiết kiến trúc",
        "color": "#5c3a1a",
        "images": [
            ("ky_hoa_kien_truc_nha_co.jpg",
             "Nhà cổ",
             "Bút sắt, A4. Chi tiết mái ngói, cột và cửa gỗ chạm khắc được thể hiện "
             "tỉ mỉ; phối cảnh một điểm tụ đơn giản."),
            ("ky_hoa_kien_truc_nha_tho.jpg",
             "Nhà thờ",
             "Bút sắt, A4. Kiến trúc Gothic với cổng vòm và tháp cao; đường thẳng đứng "
             "mạnh được nhấn để tăng cảm giác hùng vĩ."),
            ("ky_hoa_kien_truc_pho_co.jpg",
             "Phố cổ",
             "Bút chì, A4. Tầng mái thấp xen kẽ, hiên nhà và cửa đặc trưng phố cổ; "
             "phối cảnh hai điểm tụ tạo chiều sâu đường phố."),
        ],
    },
    {
        "title": "Nhóm 5 – Ký Họa Phong Cảnh",
        "subtitle": "Cảnh quan thiên nhiên, đường phố, không gian đô thị hoặc nông thôn (4 bài)",
        "color": "#1a4a5c",
        "images": [
            ("ky_hoa_bai_bien.jpg",
             "Bãi biển",
             "Bút sắt, A4. Đường chân trời thấp; sóng biển được diễn tả bằng nét lượn "
             "nhịp nhàng, tạo cảm giác mênh mông và thoáng đãng."),
            ("ky_hoa_phong_canh_song_nuoc_xoa_chu.jpg",
             "Phong cảnh sông nước",
             "Bút chì, A4. Mặt nước phẳng lặng phản chiếu cây và bầu trời; nét ngang nhẹ "
             "gợi sự tĩnh lặng của dòng sông vùng nông thôn."),
            ("ky_hoa_phong_canh_dong_lua.jpg",
             "Phong cảnh đồng lúa",
             "Bút chì, A4. Mảng ruộng lúa chín vàng trải rộng; bầu trời và mây được "
             "xử lý nhẹ để tôn lên không gian đồng quê bình yên."),
            ("ky_hoa_phong_canh_nui_non.jpg",
             "Phong cảnh núi non",
             "Bút sắt, A4. Các lớp núi lùi dần tạo chiều sâu; kỹ thuật đổ bóng chéo "
             "thể hiện độ đậm nhạt giữa các tầng núi."),
        ],
    },
    {
        "title": "Nhóm 6 – Ký Họa Tự Do",
        "subtitle": "Lựa chọn đối tượng theo sở thích, thể hiện cá tính và khả năng quan sát",
        "color": "#4a1a5c",
        "images": [
            ("ky_hoa_cai_ghe.jpg",
             "Cái ghế",
             "Bút sắt, A4. Góc nhìn ¾ làm nổi bật cấu trúc khung gỗ; bóng đổ trên "
             "mặt đất tăng cảm giác không gian thực."),
            ("ky_hoa_con_meo.jpg",
             "Con mèo",
             "Bút chì, A4. Dáng nằm cuộn tròn tạo hình khối tròn trịa; lông mèo "
             "được thể hiện bằng nét ngắn, mượt, theo chiều sinh trưởng."),
            ("ky_hoa_doi_giay.jpg",
             "Đôi giày",
             "Bút sắt, A4. Chất liệu da được gợi qua vùng phản quang; tỷ lệ hai chiếc "
             "giày so le tạo bố cục sinh động."),
            ("ky_hoa_ngoi_nha.jpg",
             "Ngôi nhà",
             "Bút chì, A4. Nhà nông thôn đơn sơ với vườn cây xung quanh; nét vẽ "
             "thoáng, gợi cảm giác thân quen, ấm cúng."),
            ("ky_hoa_xe_dap.jpg",
             "Xe đạp",
             "Bút sắt, A4. Cấu trúc khung kim loại phức tạp được đơn giản hoá tới "
             "mức tạo hình; bánh xe và xích được chú trọng chi tiết."),
        ],
    },
]

# ─── Font ───────────────────────────────────────────────────────────────────
def find_font(names):
    dirs = ["/Library/Fonts/", "/System/Library/Fonts/",
            os.path.expanduser("~/Library/Fonts/"),
            "/System/Library/Fonts/Supplemental/"]
    for n in names:
        for d in dirs:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None

FNT  = "Helvetica"
FNTB = "Helvetica-Bold"

fr = find_font(["DejaVuSans.ttf","Arial.ttf"])
fb = find_font(["DejaVuSans-Bold.ttf","Arial Bold.ttf","Arial-BoldMT.ttf"])
if fr:
    try: pdfmetrics.registerFont(TTFont("VF", fr)); FNT = "VF"
    except: pass
if fb:
    try: pdfmetrics.registerFont(TTFont("VFB", fb)); FNTB = "VFB"
    except: pass

# ─── Colours ────────────────────────────────────────────────────────────────
C_DARK    = colors.HexColor("#1a2a3a")
C_BLUE    = colors.HexColor("#1a3a5c")
C_LBLUE   = colors.HexColor("#dbe8f5")
C_GOLD    = colors.HexColor("#c9a84c")
C_GREY    = colors.HexColor("#f5f5f5")
C_MGREY   = colors.HexColor("#cccccc")
C_DGREY   = colors.HexColor("#666666")
C_WHITE   = colors.white
C_BLACK   = colors.black

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.5*cm, 2.0*cm, 2.0*cm, 2.0*cm
CW = PAGE_W - ML - MR

# ─── Helper styles ──────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName=FNT, fontSize=10, leading=14,
                    textColor=C_BLACK, spaceAfter=3, spaceBefore=2,
                    alignment=TA_LEFT)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

def p(text, style): return Paragraph(text, style)

# ─── Header / Footer ────────────────────────────────────────────────────────
_page_ctx = {}

# Toạ độ khung đỏ bìa (khớp với Word template)
_BORDER_L = 1.5*cm
_BORDER_R = PAGE_W - 1.5*cm
_BORDER_T = 2.5*cm     # top của khung (dưới header)
_BORDER_B = 1.5*cm     # bottom của khung

def _on_page(canvas, doc):
    pg = doc.page
    canvas.saveState()
    if pg == 1:
        # ── Header ngoài khung (giống Word: 02.43-BM/ĐT/TPC) ──
        canvas.setFont(TNR, 9)
        canvas.setFillColor(C_BLACK)
        canvas.drawString(_BORDER_L, PAGE_H - 1.8*cm, "02.43-BM/ĐT/TPC")
        canvas.drawRightString(_BORDER_R, PAGE_H - 1.8*cm, "Lần ban hành/sửa đổi: 1/0")
        # Đường kẻ dưới header
        canvas.setStrokeColor(C_BLACK)
        canvas.setLineWidth(0.5)
        canvas.line(_BORDER_L, PAGE_H - 2.0*cm, _BORDER_R, PAGE_H - 2.0*cm)
        # ── Khung viền đỏ ──
        canvas.setStrokeColor(colors.red)
        canvas.setLineWidth(2.5)
        canvas.rect(_BORDER_L, _BORDER_B,
                    _BORDER_R - _BORDER_L,
                    _BORDER_T - _BORDER_B + (PAGE_H - _BORDER_T - 2.1*cm),
                    stroke=1, fill=0)
        # ── Ngày ở cuối trang (căn giữa trong khung đỏ) ──
        canvas.setFont(TNRI, 13)
        canvas.setFillColor(C_BLACK)
        date_y = _BORDER_B + 1.2*cm
        canvas.drawCentredString(PAGE_W / 2.0, date_y,
                                "Hà Nội, ngày 14 tháng 10 năm 2026")
    else:
        # Header nội dung
        canvas.setStrokeColor(C_BLUE); canvas.setLineWidth(0.5)
        canvas.line(3*cm, PAGE_H-1.6*cm, PAGE_W-2.5*cm, PAGE_H-1.6*cm)
        canvas.setFont(TNRB, 7.5); canvas.setFillColor(C_BLUE)
        canvas.drawString(3*cm, PAGE_H-1.25*cm, "HỒ SƠ ĐỒ ÁN – VẼ MỸ THUẬT 1")
        canvas.setFont(TNR, 7.5); canvas.setFillColor(C_DGREY)
        canvas.drawRightString(PAGE_W-2.5*cm, PAGE_H-1.25*cm,
                               "Nguyễn Văn Ngà  |  MSSV: 2603ITA0022")
        # Footer
        canvas.line(3*cm, 1.5*cm, PAGE_W-2.5*cm, 1.5*cm)
        canvas.setFont(TNR, 7); canvas.setFillColor(C_DGREY)
        canvas.drawString(3*cm, 1.0*cm,
                          "Trường Đại học Phú Xuân – Viện Đào Tạo Quốc Tế TOPICA")
        canvas.drawRightString(PAGE_W-2.5*cm, 1.0*cm, f"Trang {pg}")
    canvas.restoreState()

# ─── Cover Page – tái tạo 100% theo mẫu Word ────────────────────────────────
TNR  = "TNR"   # Times New Roman regular
TNRB = "TNRB"  # Times New Roman bold
TNRI = "TNRI"  # Times New Roman italic

def _register_tnr():
    tnr_r = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
    tnr_b = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
    tnr_i = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"
    try:
        pdfmetrics.registerFont(TTFont("TNR",  tnr_r))
        pdfmetrics.registerFont(TTFont("TNRB", tnr_b))
        pdfmetrics.registerFont(TTFont("TNRI", tnr_i))
    except Exception as e:
        global TNR, TNRB, TNRI
        TNR  = FNT
        TNRB = FNTB
        TNRI = FNT

_register_tnr()

class StarRow(Flowable):
    """3 ngôi sao đen căn giữa trang, tạo khoảng cách chuẩn xác theo dòng chảy."""
    def __init__(self, count=3, r=4.2, spacing=24, height=16):
        super().__init__()
        self.count = count
        self.r = r
        self.spacing = spacing
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        import math
        # Căn giữa theo khổ trang A4: PAGE_W / 2
        cx = PAGE_W / 2.0 - 3.0*cm
        cy = self.height / 2.0
        def draw_star(c, x, y, r=4.2):
            c.setFillColor(C_BLACK)
            c.setStrokeColor(C_BLACK)
            c.setLineWidth(0.2)
            pts = []
            for i in range(10):
                angle = math.pi/2 + i * 2*math.pi/10
                rr = r if i % 2 == 0 else r * 0.4
                pts.append((x + rr*math.cos(angle), y + rr*math.sin(angle)))
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        offsets = [-(self.count - 1)/2.0 * self.spacing + i * self.spacing for i in range(self.count)]
        for off in offsets:
            draw_star(c, cx + off, cy, self.r)

def cover_elements():
    """Trang bìa tái tạo 100% theo mẫu Word 02.43-BM/ĐT/TPC."""
    els = []

    # Padding trên để tránh header ngoài khung
    els.append(Spacer(1, 0.6*cm))

    # ── Helpers ──────────────────────────────────────────────────────────────
    def tnr_c(txt, size, bold=False, spaceAfter=4, spaceBefore=0):
        """Paragraph TNR căn giữa."""
        fn = TNRB if bold else TNR
        return Paragraph(txt, ParagraphStyle(
            f"cv_{size}_{txt[:4]}",
            fontName=fn, fontSize=size, leading=int(size*1.4),
            alignment=TA_CENTER, textColor=C_BLACK,
            spaceAfter=spaceAfter, spaceBefore=spaceBefore,
        ))

    # ── 1. Tên trường – Bold, 13pt, căn giữa ────────────────────────────────
    els.append(tnr_c("BỘ GIÁO DỤC VÀ ĐÀO TẠO",    13, bold=True, spaceAfter=2))
    els.append(tnr_c("TRƯỜNG ĐẠI HỌC PHÚ XUÂN",     13, bold=True, spaceAfter=2))
    els.append(tnr_c("VIỆN ĐÀO TẠO QUỐC TẾ TOPICA", 13, bold=True, spaceAfter=2))

    # ── 2. Ba sao – cách tên Viện 0.3cm, cách logo TOPICA 1.3cm ─────────────
    els.append(Spacer(1, 0.3*cm))
    els.append(StarRow(count=3, r=4.5, spacing=24, height=16))
    els.append(Spacer(1, 1.3*cm))

    # ── 3. Logo TOPICA (8.26cm × 3.57cm, căn giữa) ──────────────────────────
    if os.path.exists(LOGO_TOPICA):
        logo = Image(LOGO_TOPICA, width=8.26*cm, height=3.57*cm)
        logo.hAlign = "CENTER"
        els.append(logo)
    els.append(Spacer(1, 1.2*cm))

    # ── 4. Tiêu đề đồ án – BOLD 24pt ─────────────────────────────────────────
    els.append(tnr_c("ĐỒ ÁN HỌC PHẦN", 24, bold=True, spaceAfter=4))

    # ── 5. Tên học phần – không bold, 16pt, căn giữa ─────────────────────────
    els.append(Paragraph(
        "VẼ MỸ THUẬT 1",
        ParagraphStyle("cv_sub", fontName=TNR, fontSize=16,
                       leading=24, alignment=TA_CENTER,
                       textColor=C_BLACK, spaceAfter=0)
    ))
    els.append(Spacer(1, 1.5*cm))

    # ── 6. Thông tin sinh viên – căn giữa chiều ngang trên trang ─────────────
    # Khối thông tin rộng ~7.8cm, đặt chính giữa chiều ngang trang A4 (leftIndent = 3.6cm)
    st_info = ParagraphStyle(
        "cv_info_line",
        fontName=TNR, fontSize=13, leading=28,
        alignment=TA_LEFT, textColor=C_BLACK,
        leftIndent=3.6*cm,
    )
    els.append(Paragraph(f"Sinh viên thực hiện: {SV_NAME}", st_info))
    els.append(Paragraph(f"Lớp: {SV_MSSV}", st_info))
    els.append(Paragraph(f"Khoá: {SV_KHOA}", st_info))
    els.append(Paragraph(f"Ngành: {SV_NGANH}", st_info))
    return els


# ─── Section heading flowable ───────────────────────────────────────────────
def section_banner(title, subtitle, hex_color):
    bg = colors.HexColor(hex_color)
    # lighten bg for subtitle row
    r,g,b = bg.red, bg.green, bg.blue
    lt = colors.Color(min(r+0.25,1), min(g+0.25,1), min(b+0.25,1), 1)
    st_t = S("bnt", fontSize=13, fontName=FNTB, textColor=C_WHITE,
             alignment=TA_LEFT, leading=18)
    st_s = S("bns", fontSize=9,  textColor=C_WHITE,
             alignment=TA_LEFT, leading=13)
    data = [
        [p(title, st_t)],
        [p(subtitle, st_s)],
    ]
    t = Table(data, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), bg),
        ("BACKGROUND",   (0,1),(-1,1), lt),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    return t


# ─── Image card ─────────────────────────────────────────────────────────────
IMG_W = CW       # 1 ảnh / trang cho GV dễ xem
IMG_H = 20*cm    # khung tối đa; ảnh giữ đúng tỷ lệ gốc

def image_card(img_path, title, caption):
    """Trả về một Table-card chứa ảnh + tiêu đề + chú thích."""
    full = os.path.join(BASE, img_path)
    if not os.path.exists(full):
        img_el = Spacer(IMG_W, IMG_H)
    else:
        try:
            img_el = Image(full, width=IMG_W, height=IMG_H, kind="proportional")
        except:
            img_el = Spacer(IMG_W, IMG_H)

    st_title   = S("ic_t", fontSize=9, fontName=FNTB, textColor=C_BLUE,
                   alignment=TA_LEFT, leading=13, spaceBefore=4, spaceAfter=2)
    st_caption = S("ic_c", fontSize=8, textColor=C_DGREY,
                   alignment=TA_JUSTIFY, leading=12)

    inner = Table(
        [[img_el], [p(title, st_title)], [p(caption, st_caption)]],
        colWidths=[getattr(img_el, "drawWidth", IMG_W)], hAlign="CENTER"
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), C_WHITE),
        ("BOX",          (0,0),(-1,-1), 0.5, C_MGREY),
        ("TOPPADDING",   (0,0),(-1,0),  0),
        ("BOTTOMPADDING",(0,0),(-1,0),  0),
        ("LEFTPADDING",  (0,0),(-1,0),  0),
        ("RIGHTPADDING", (0,0),(-1,0),  0),
        ("TOPPADDING",   (0,1),(-1,-1), 5),
        ("BOTTOMPADDING",(0,1),(-1,-1), 6),
        ("LEFTPADDING",  (0,1),(-1,-1), 7),
        ("RIGHTPADDING", (0,1),(-1,-1), 7),
    ]))
    return inner


def group_elements(group):
    """Trả về danh sách flowable cho 1 nhóm."""
    els = []
    els.append(Spacer(1, 0.3*cm))
    els.append(section_banner(group["title"], group["subtitle"], group["color"]))
    els.append(Spacer(1, 0.35*cm))

    for img_file, title, caption in group["images"]:
        els.append(image_card(img_file, title, caption))
        els.append(Spacer(1, 0.4*cm))

    return els


# ─── Back cover / closing page ──────────────────────────────────────────────
def closing_elements():
    els = []
    els.append(PageBreak())
    els.append(Spacer(1, 2*cm))

    st_hd = S("cl_hd", fontSize=14, fontName=FNTB, textColor=C_BLUE,
              alignment=TA_CENTER, leading=20)
    st_body= S("cl_b",  fontSize=10, textColor=C_DARK,
               alignment=TA_JUSTIFY, leading=16)
    st_sig = S("cl_sg", fontSize=10, alignment=TA_CENTER, textColor=C_DGREY)

    els.append(p("VI. NHẬN XÉT VÀ CẢM NHẬN", st_hd))
    els.append(HRFlowable(width=CW, thickness=1.5, color=C_GOLD, spaceAfter=12))
    els.append(Spacer(1, 0.2*cm))
    els.append(p(
        "Qua quá trình thực hiện 20 bài ký họa thuộc 6 nhóm nội dung của học phần Vẽ Mỹ Thuật 1, "
        "tôi đã từng bước rèn luyện được khả năng quan sát thực tế và chuyển hóa cảm xúc thị giác "
        "thành ngôn ngữ tạo hình. Từ việc nghiên cứu chất liệu bề mặt, ký họa tĩnh vật, cây cối "
        "cho đến kiến trúc và phong cảnh, mỗi bài vẽ là một trải nghiệm khám phá riêng biệt.",
        st_body))
    els.append(Spacer(1, 0.15*cm))
    els.append(p(
        "Tôi nhận thấy rõ sự tiến bộ trong việc kiểm soát đường nét và sắc độ qua từng nhóm bài. "
        "Đặc biệt, nhóm ký họa tự do đã cho phép tôi tự do biểu đạt cá tính và phong cách riêng, "
        "đặt nền móng cho các học phần chuyên ngành tiếp theo như Minh họa và Concept Art.",
        st_body))
    els.append(Spacer(1, 0.15*cm))
    els.append(p(
        "Đây là những viên gạch đầu tiên trên con đường học tập và sáng tạo. Tôi xin chân thành "
        "cảm ơn giảng viên hướng dẫn đã tận tình góp ý và đồng hành cùng tôi trong suốt học phần.",
        st_body))

    els.append(Spacer(1, 1.5*cm))

    # Chữ ký
    sig_data = [
        [p("Giảng viên đánh giá", S("sl1", fontName=FNTB, alignment=TA_CENTER, textColor=C_BLUE)),
         p(SV_DATE, S("sl2", alignment=TA_CENTER, textColor=C_DGREY))],
        [p("(Ký và ghi rõ họ tên)", S("sl3", fontSize=8, alignment=TA_CENTER, textColor=C_DGREY)),
         p("Sinh viên thực hiện", S("sl4", fontName=FNTB, alignment=TA_CENTER, textColor=C_BLUE))],
        [Spacer(1, 2.5*cm), Spacer(1, 2.5*cm)],
        [p("………………………………", S("sl5", alignment=TA_CENTER, textColor=C_DGREY)),
         p(SV_NAME, S("sl6", fontName=FNTB, alignment=TA_CENTER, textColor=C_DARK))],
    ]
    sig_tbl = Table(sig_data, colWidths=[CW/2, CW/2])
    sig_tbl.setStyle(TableStyle([
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LINEABOVE",   (0,0),(-1,0),  1, C_BLUE),
    ]))
    els.append(sig_tbl)
    return els


# ─── BUILD ──────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=3*cm, rightMargin=2.5*cm,   # khớp Word template
        topMargin=2.0*cm, bottomMargin=2.2*cm,
        title="Hồ Sơ Đồ Án – Vẽ Mỹ Thuật 1",
        author=SV_NAME,
    )

    story = []

    # ── Trang bìa ──────────────────────────────────────────────
    story += cover_elements()
    story.append(PageBreak())

    # ── Giới thiệu đồ án ───────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    st_intro_h = S("ih", fontSize=13, fontName=FNTB, textColor=C_BLUE,
                   alignment=TA_CENTER, leading=20)
    story.append(p("GIỚI THIỆU ĐỒ ÁN", st_intro_h))
    story.append(HRFlowable(width=CW, thickness=1.5, color=C_GOLD, spaceAfter=10))
    st_intro = S("intro", fontSize=10, leading=16, alignment=TA_JUSTIFY)
    story.append(p(
        "Hồ sơ đồ án này tập hợp <b>22 bài ký họa</b> được thực hiện trong học phần <b>Vẽ Mỹ Thuật 1</b>, "
        "thuộc chuyên ngành Đồ Họa Kỹ Thuật Số, Trường Đại học Phú Xuân. Các bài vẽ được sắp xếp "
        "theo 6 nhóm nội dung quy định, bao gồm:", st_intro))
    story.append(Spacer(1, 0.15*cm))

    nhom_info = [
        ("Nhóm 1", "Vẽ mô tả chất liệu",   "2 bài",  "#1a3a5c"),
        ("Nhóm 2", "Ký họa tĩnh vật",       "2 bài",  "#1e5c3a"),
        ("Nhóm 3", "Ký họa cây",            "6 bài",  "#3a5c1a"),
        ("Nhóm 4", "Ký họa kiến trúc",      "3 bài",  "#5c3a1a"),
        ("Nhóm 5", "Ký họa phong cảnh",     "4 bài",  "#1a4a5c"),
        ("Nhóm 6", "Ký họa tự do",          "5 bài",  "#4a1a5c"),
    ]
    def dot(hex_c):
        return f'<font color="{hex_c}">■</font>'

    for code, name, count, hc in nhom_info:
        story.append(p(
            f"{dot(hc)} <b>{code} – {name}</b>: {count}",
            S(f"ni_{code}", fontSize=10, leading=16, leftIndent=10)))

    story.append(Spacer(1, 0.3*cm))
    story.append(p(
        "Chất liệu sử dụng: bút chì và bút sắt màu đen. Khổ giấy: A4. "
        "Hồ sơ được số hóa và trình bày dưới dạng file PDF theo đúng yêu cầu của đề bài.",
        st_intro))
    story.append(PageBreak())

    # ── 6 nhóm bài vẽ ─────────────────────────────────────────
    for gi, group in enumerate(GROUPS):
        story += group_elements(group)
        if gi < len(GROUPS) - 1:
            story.append(PageBreak())

    # ── Trang kết thúc ─────────────────────────────────────────
    story += closing_elements()

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    print(f"✅  Đã xuất: {OUT}")


if __name__ == "__main__":
    build()
