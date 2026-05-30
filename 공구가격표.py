from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 폰트 등록
sys_font_path = '/System/Library/Fonts/Supplemental/'
pdfmetrics.registerFont(TTFont('NanumSquare', sys_font_path + 'NotoSansGothic-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NanumSquareBold', sys_font_path + 'AppleGothic.ttf'))
pdfmetrics.registerFont(TTFont('NanumSquareEB', sys_font_path + 'AppleGothic.ttf'))

# 색상 정의
COLOR_BG = colors.HexColor('#FAFAF8')
COLOR_HEADER = colors.HexColor('#2D2D2D')
COLOR_SECTION = colors.HexColor('#4A4A4A')
COLOR_ACCENT = colors.HexColor('#7B9E87')  # 자연스러운 녹색 (소창/오가닉 느낌)
COLOR_ACCENT_LIGHT = colors.HexColor('#E8F0EA')
COLOR_PRICE = colors.HexColor('#C17B4E')   # 따뜻한 브라운 (가격 강조)
COLOR_DISCOUNT = colors.HexColor('#7B9E87')
COLOR_GIFT_BG = colors.HexColor('#FFF8F0')
COLOR_GIFT_BORDER = colors.HexColor('#C17B4E')
COLOR_LINE = colors.HexColor('#E0E0E0')
COLOR_WHITE = colors.white
COLOR_SECTION_BG1 = colors.HexColor('#F5F7F5')
COLOR_SECTION_BG2 = colors.HexColor('#FDFCFA')

output_path = os.path.expanduser("~/Desktop/yegam/오가닉소창_공구가격표.pdf")

c = canvas.Canvas(output_path, pagesize=A4)
W, H = A4

# 배경
c.setFillColor(COLOR_BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

y = H - 12*mm

# ─── 헤더 ───────────────────────────────────────────
c.setFillColor(COLOR_HEADER)
c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)

c.setFillColor(COLOR_WHITE)
c.setFont('NanumSquareEB', 18)
c.drawCentredString(W/2, H - 13*mm, '국내 유일 오가닉 소창')

c.setFont('NanumSquare', 10)
c.setFillColor(colors.HexColor('#BBBBBB'))
c.drawCentredString(W/2, H - 21*mm, '공구 특가 가격표')

y = H - 33*mm

# ─── 사은품 안내 박스 ─────────────────────────────────
gift_h = 18*mm
c.setFillColor(COLOR_GIFT_BG)
c.setStrokeColor(COLOR_GIFT_BORDER)
c.setLineWidth(1.2)
c.roundRect(10*mm, y - gift_h, W - 20*mm, gift_h, 3*mm, fill=1, stroke=1)

c.setFont('NanumSquareBold', 9)
c.setFillColor(COLOR_GIFT_BORDER)
c.drawCentredString(W/2, y - 6*mm, '🎁  사은품 혜택  (중복 미적용)')

c.setFont('NanumSquare', 8.5)
c.setFillColor(COLOR_SECTION)
gift_y = y - 12*mm
gap = (W - 20*mm) / 3
c.drawCentredString(10*mm + gap*0.5, gift_y, '65,000원 이상 → 사은품 ①')
c.drawCentredString(10*mm + gap*1.5, gift_y, '100,000원 이상 → 사은품 ②')
c.drawCentredString(10*mm + gap*2.5, gift_y, '150,000원 이상 → 사은품 ③')

y -= gift_h + 5*mm

# ─── 헬퍼 함수들 ──────────────────────────────────────
def section_title(c, title_kr, subtitle, y_pos):
    c.setFillColor(COLOR_ACCENT)
    c.rect(10*mm, y_pos - 7*mm, W - 20*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(COLOR_WHITE)
    c.setFont('NanumSquareBold', 10)
    c.drawString(14*mm, y_pos - 5.2*mm, title_kr)
    if subtitle:
        c.setFont('NanumSquare', 8)
        c.setFillColor(colors.HexColor('#DDEEDF'))
        c.drawRightString(W - 12*mm, y_pos - 5.2*mm, subtitle)
    return y_pos - 8*mm

def product_row(c, name, original, sale, discount, gift, y_pos, bg=True):
    row_h = 8*mm
    if bg:
        c.setFillColor(COLOR_SECTION_BG1)
        c.rect(10*mm, y_pos - row_h, W - 20*mm, row_h, fill=1, stroke=0)

    # 상품명
    c.setFont('NanumSquare', 8.5)
    c.setFillColor(COLOR_SECTION)
    c.drawString(14*mm, y_pos - 5.5*mm, name)

    # 정가 (취소선 효과)
    c.setFont('NanumSquare', 7.5)
    c.setFillColor(colors.HexColor('#AAAAAA'))
    orig_x = W/2 - 10*mm
    c.drawRightString(orig_x, y_pos - 5.5*mm, original)
    # 취소선
    tw = c.stringWidth(original, 'NanumSquare', 7.5)
    c.setStrokeColor(colors.HexColor('#AAAAAA'))
    c.setLineWidth(0.5)
    line_y = y_pos - 4.8*mm
    c.line(orig_x - tw, line_y, orig_x, line_y)

    # 공구가
    c.setFont('NanumSquareBold', 9.5)
    c.setFillColor(COLOR_PRICE)
    c.drawCentredString(W/2 + 12*mm, y_pos - 5.5*mm, sale)

    # 할인율
    c.setFont('NanumSquare', 7.5)
    c.setFillColor(COLOR_DISCOUNT)
    c.drawCentredString(W/2 + 28*mm, y_pos - 5.5*mm, discount)

    # 사은품
    if gift:
        c.setFont('NanumSquareBold', 7.5)
        c.setFillColor(COLOR_GIFT_BORDER)
        c.drawRightString(W - 12*mm, y_pos - 5.5*mm, gift)

    return y_pos - row_h

def col_header(c, y_pos):
    c.setFillColor(colors.HexColor('#EEEEEE'))
    c.rect(10*mm, y_pos - 5*mm, W - 20*mm, 5*mm, fill=1, stroke=0)
    c.setFont('NanumSquare', 7)
    c.setFillColor(colors.HexColor('#888888'))
    c.drawString(14*mm, y_pos - 3.8*mm, '구성')
    orig_x = W/2 - 10*mm
    c.drawRightString(orig_x, y_pos - 3.8*mm, '정가')
    c.drawCentredString(W/2 + 12*mm, y_pos - 3.8*mm, '공구가')
    c.drawCentredString(W/2 + 28*mm, y_pos - 3.8*mm, '할인율')
    c.drawRightString(W - 12*mm, y_pos - 3.8*mm, '사은품')
    return y_pos - 5*mm

# ─── 단품 섹션 ────────────────────────────────────────
y = section_title(c, '단품 구성', '', y)
y = col_header(c, y)

# 소창 수건
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_ACCENT)
c.drawString(14*mm, y - 3.8*mm, '🌿 소창 수건  (정가 18,000원/개)')
y -= 5*mm

y = product_row(c, '  3개', '54,000원', '48,600원', '10%↓', '', y, True)
y = product_row(c, '  5개', '90,000원', '79,500원', '11.7%↓', '사은품 ①', y, False)
y = product_row(c, '  10개', '180,000원', '159,000원', '11.7%↓', '사은품 ③', y, True)

y -= 1*mm

# 아기 목욕 수건
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_ACCENT)
c.drawString(14*mm, y - 3.8*mm, '👶 아기 목욕 수건  (정가 45,000원/개)')
y -= 5*mm

y = product_row(c, '  1개', '45,000원', '35,900원', '20.2%↓', '', y, True)
y = product_row(c, '  2개', '90,000원', '65,000원', '27.8%↓', '사은품 ①', y, False)

y -= 1*mm

# 어른 목욕 수건
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_ACCENT)
c.drawString(14*mm, y - 3.8*mm, '🧖 어른 목욕 수건  (정가 55,000원/개)')
y -= 5*mm

y = product_row(c, '  1개', '55,000원', '45,900원', '16.5%↓', '', y, True)
y = product_row(c, '  2개', '110,000원', '85,000원', '22.7%↓', '사은품 ①', y, False)

y -= 4*mm

# ─── 세트 섹션 ────────────────────────────────────────
y = section_title(c, '세트 구성', '세트 전용 특별 구성', y)
y = col_header(c, y)

# 고운 선물 세트
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_PRICE)
c.drawString(14*mm, y - 3.8*mm, '🎁 고운 선물 세트  ·  아기목욕 1개 + 소창 1개')
y -= 5*mm
y = product_row(c, '', '63,000원', '52,000원', '17.5%↓', '', y, True)

y -= 1*mm

# 오롯이 세트
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_PRICE)
c.drawString(14*mm, y - 3.8*mm, '🌿 오롯이 세트  ·  소창 4개 + 목욕수건 선택')
y -= 5*mm
y = product_row(c, '  어른 목욕 수건 선택', '127,000원', '109,000원', '14.2%↓', '사은품 ②', y, True)
y = product_row(c, '  아기 목욕 수건 선택 (-10,000원)', '117,000원', '99,000원', '15.4%↓', '사은품 ①', y, False)

y -= 1*mm

# 나란히 세트
c.setFillColor(COLOR_SECTION_BG2)
c.rect(10*mm, y - 5*mm, W-20*mm, 5*mm, fill=1, stroke=0)
c.setFont('NanumSquareBold', 8)
c.setFillColor(COLOR_PRICE)
c.drawString(14*mm, y - 3.8*mm, '🌿 나란히 세트  ·  소창 6개 + 목욕수건 선택')
y -= 5*mm
y = product_row(c, '  어른 2개', '218,000원', '179,000원', '17.9%↓', '사은품 ③', y, True)
y = product_row(c, '  어른 1개 + 아기 1개 (-10,000원)', '208,000원', '169,000원', '18.8%↓', '사은품 ③', y, False)
y = product_row(c, '  아기 2개 (-20,000원)', '198,000원', '159,000원', '19.7%↓', '사은품 ③', y, True)

y -= 4*mm

# ─── 하단 안내 ────────────────────────────────────────
c.setFillColor(COLOR_HEADER)
c.rect(0, 0, W, y + 2*mm, fill=1, stroke=0)

c.setFont('NanumSquare', 7.5)
c.setFillColor(colors.HexColor('#AAAAAA'))
c.drawCentredString(W/2, 8*mm, '* 소창 수건 5개/10개는 브랜드 협의 후 최종 확정  |  * 사은품 구성은 브랜드사 재고에 따라 결정')

c.save()
print(f"✅ PDF 저장 완료: {output_path}")
