from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# ── 폰트 등록 ──────────────────────────────────────────────
font_candidates = [
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/Library/Fonts/NanumGothic.ttf",
    "/Library/Fonts/NanumGothicBold.ttf",
]
font_name = "Helvetica"
for path in font_candidates:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont("KorFont", path))
            font_name = "KorFont"
            break
        except Exception:
            pass

# ── 색상 팔레트 ──────────────────────────────────────────────
PINK     = colors.HexColor("#E8647A")
PINK_LT  = colors.HexColor("#FDF0F2")
GRAY_DK  = colors.HexColor("#2D2D2D")
GRAY_MD  = colors.HexColor("#666666")
GRAY_LT  = colors.HexColor("#F5F5F5")
WHITE    = colors.white

W, H = A4

# ── 스타일 ──────────────────────────────────────────────────
def make_styles(fn):
    S = {}
    base = dict(fontName=fn, leading=18, textColor=GRAY_DK)

    S["cover_title"] = ParagraphStyle("cover_title",
        fontName=fn, fontSize=26, leading=36,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=8)
    S["cover_sub"] = ParagraphStyle("cover_sub",
        fontName=fn, fontSize=14, leading=22,
        textColor=colors.HexColor("#FFD6DC"), alignment=TA_CENTER, spaceAfter=6)
    S["cover_date"] = ParagraphStyle("cover_date",
        fontName=fn, fontSize=11, leading=16,
        textColor=colors.HexColor("#FFB3C0"), alignment=TA_CENTER)

    S["sec_title"] = ParagraphStyle("sec_title",
        fontName=fn, fontSize=15, leading=22,
        textColor=WHITE, spaceAfter=0, spaceBefore=0)
    S["h2"] = ParagraphStyle("h2",
        fontName=fn, fontSize=12, leading=18,
        textColor=PINK, spaceBefore=14, spaceAfter=6, **{})
    S["h3"] = ParagraphStyle("h3",
        fontName=fn, fontSize=10, leading=16,
        textColor=GRAY_DK, spaceBefore=8, spaceAfter=4, **{})
    S["body"] = ParagraphStyle("body",
        fontName=fn, fontSize=9.5, leading=16,
        textColor=GRAY_DK, spaceAfter=4)
    S["body_sm"] = ParagraphStyle("body_sm",
        fontName=fn, fontSize=8.5, leading=14,
        textColor=GRAY_MD, spaceAfter=3)
    S["bullet"] = ParagraphStyle("bullet",
        fontName=fn, fontSize=9.5, leading=16,
        textColor=GRAY_DK, leftIndent=12, spaceAfter=3,
        bulletIndent=0, bulletFontSize=9.5)
    S["check"] = ParagraphStyle("check",
        fontName=fn, fontSize=9.5, leading=16,
        textColor=GRAY_DK, leftIndent=16, spaceAfter=3)
    S["tag"] = ParagraphStyle("tag",
        fontName=fn, fontSize=8, leading=13,
        textColor=WHITE, alignment=TA_CENTER)
    S["quote"] = ParagraphStyle("quote",
        fontName=fn, fontSize=11, leading=18,
        textColor=PINK, alignment=TA_CENTER,
        spaceBefore=8, spaceAfter=8)
    S["footer"] = ParagraphStyle("footer",
        fontName=fn, fontSize=7.5, leading=12,
        textColor=GRAY_MD, alignment=TA_CENTER)
    S["number_big"] = ParagraphStyle("number_big",
        fontName=fn, fontSize=28, leading=32,
        textColor=PINK, alignment=TA_CENTER)
    S["number_label"] = ParagraphStyle("number_label",
        fontName=fn, fontSize=8, leading=12,
        textColor=GRAY_MD, alignment=TA_CENTER)
    return S

# ── 헬퍼 ──────────────────────────────────────────────────
def section_header(title, num, S):
    label = f"0{num}" if num < 10 else str(num)
    t = Table(
        [[Paragraph(f"SECTION {label}", S["tag"]),
          Paragraph(title, S["sec_title"])]],
        colWidths=[22*mm, 148*mm]
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), PINK),
        ("BACKGROUND", (1,0), (1,0), GRAY_DK),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    return t

def kpi_box(value, label, S):
    t = Table(
        [[Paragraph(value, S["number_big"])],
         [Paragraph(label, S["number_label"])]],
        colWidths=[42*mm]
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PINK_LT),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#F0C0C8")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return t

def month_card(month, emoji, title, goal, items, metrics, S):
    """한 달 카드"""
    elems = []
    # 헤더
    hdr = Table([[Paragraph(f"{emoji}  {month}  |  {title}", S["h2"])]],
                colWidths=[170*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), PINK_LT),
        ("LEFTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING",(0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    elems.append(hdr)
    elems.append(Spacer(1, 4))
    elems.append(Paragraph(f"목표: {goal}", S["body"]))
    elems.append(Spacer(1, 4))

    # 콘텐츠 아이디어
    elems.append(Paragraph("콘텐츠 아이디어", S["h3"]))
    for i, item in enumerate(items, 1):
        elems.append(Paragraph(f"{i}.  {item}", S["bullet"]))

    # 목표 지표
    elems.append(Spacer(1, 6))
    elems.append(Paragraph("목표 지표", S["h3"]))
    for m in metrics:
        elems.append(Paragraph(f"  ✓  {m}", S["check"]))
    elems.append(Spacer(1, 10))
    return elems

def make_table(headers, rows, col_widths, S):
    data = [[Paragraph(h, ParagraphStyle("th", fontName=S["body"].fontName,
             fontSize=9, leading=14, textColor=WHITE)) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S["body_sm"]) for c in row])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), GRAY_DK),
        ("BACKGROUND", (0,1), (-1,-1), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, GRAY_LT]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ]))
    return t

# ── 페이지 번호 ──────────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(font_name, 8)
    canvas.setFillColor(GRAY_MD)
    canvas.drawCentredString(W/2, 15*mm, f"— {doc.page} —")
    canvas.restoreState()

# ── 메인 빌드 ──────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=22*mm,
    )
    S = make_styles(font_name)
    story = []

    # ════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════
    cover_bg = Table(
        [[Paragraph("송예감 인스타그램<br/>성장 전략 보고서", S["cover_title"])],
         [Spacer(1, 10)],
         [Paragraph("퀄리티 팔로워 10만을 위한 3개월 실행 플랜", S["cover_sub"])],
         [Spacer(1, 6)],
         [Paragraph("2026년 5월 1일  |  릴스 611개 데이터 분석 기반", S["cover_date"])]],
        colWidths=[170*mm]
    )
    cover_bg.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PINK),
        ("TOPPADDING", (0,0), (-1,-1), 30),
        ("BOTTOMPADDING", (0,0), (-1,-1), 30),
        ("LEFTPADDING", (0,0), (-1,-1), 20),
        ("RIGHTPADDING", (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    story.append(Spacer(1, 50*mm))
    story.append(cover_bg)
    story.append(Spacer(1, 20*mm))

    # 핵심 수치 3개
    kpi_row = Table(
        [[kpi_box("611개", "분석 릴스 수", S),
          kpi_box("28개월", "데이터 기간", S),
          kpi_box("71.6%", "내러티브형 콘텐츠", S),
          kpi_box("10만", "목표 팔로워", S)]],
        colWidths=[42*mm, 42*mm, 42*mm, 42*mm],
        hAlign="CENTER"
    )
    story.append(kpi_row)
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 1: 현황 진단
    # ════════════════════════════════════
    story.append(section_header("현황 진단", 1, S))
    story.append(Spacer(1, 12))

    story.append(Paragraph("데이터 요약", S["h2"]))
    diag_data = [
        ["항목", "수치"],
        ["총 분석 릴스", "611개 (2023.07 ~ 2026.03)"],
        ["데이터 기간", "28개월"],
        ["유효 스크립트", "538개"],
        ["월 평균 업로드 (최근 6개월)", "16.7개"],
        ["주력 카테고리", "스킨케어/뷰티 (31%)"],
        ["내러티브형 비율", "71.6%"],
    ]
    story.append(make_table(diag_data[0], diag_data[1:], [80*mm, 90*mm], S))
    story.append(Spacer(1, 14))

    story.append(Paragraph("발견된 핵심 문제", S["h2"]))
    problems = [
        ("시그니처 약화", "모델링팩 언급 -72%  (초기 60회 → 최근 17회)"),
        ("정체성 희석", "'기타' 카테고리 53%  (2025년 기준)  — 채널 포지셔닝 불명확"),
        ("CTA 부재", "저장 유도 1.5%  (538개 중 단 8개만 삽입)"),
        ("콘텐츠 분산", "뷰티/여행/라이프/감성이 뒤섞여 알고리즘 카테고리 인식 불가"),
    ]
    prob_data = [["", "문제", "상세"]] + [[f"0{i+1}", p[0], p[1]] for i, p in enumerate(problems)]
    pt = Table([[Paragraph(r[0], ParagraphStyle("num", fontName=font_name, fontSize=11,
                 textColor=PINK, alignment=TA_CENTER, leading=16)),
                 Paragraph(r[1], ParagraphStyle("pb", fontName=font_name, fontSize=9,
                 textColor=GRAY_DK, leading=14)),
                 Paragraph(r[2], S["body_sm"])] for r in prob_data[1:]],
               colWidths=[12*mm, 38*mm, 120*mm])
    pt.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, GRAY_LT]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#E0E0E0")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(pt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("채널 강점", S["h2"]))
    strengths = [
        "내러티브형 콘텐츠 71.6%  —  친근한 1인칭 경험 공유로 신뢰감 형성",
        "고백/충격형 훅 46.8%  —  스크롤을 멈추게 하는 강력한 첫인상",
        "3년간 611개 제작  —  검증된 콘텐츠 생산 역량",
        "\"~거든요\" \"~더라고요\"  —  복제 불가능한 예감만의 구어체 톤",
        "주변 사람에서 인사이트 발견  —  \"제가 또 바로 물어봤죠\" 패턴",
    ]
    for s in strengths:
        story.append(Paragraph(f"  ✦  {s}", S["bullet"]))
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 2: 3개월 방향성
    # ════════════════════════════════════
    story.append(section_header("3개월 방향성", 2, S))
    story.append(Spacer(1, 12))

    # 방향 화살표
    arrow = Table(
        [[Paragraph("5월", ParagraphStyle("at", fontName=font_name, fontSize=12,
                    textColor=WHITE, alignment=TA_CENTER, leading=18)),
          Paragraph("재정비", ParagraphStyle("as", fontName=font_name, fontSize=9,
                    textColor=colors.HexColor("#FFD6DC"), alignment=TA_CENTER, leading=14)),
          Paragraph("▶", ParagraphStyle("arr", fontName=font_name, fontSize=16,
                    textColor=PINK, alignment=TA_CENTER, leading=20)),
          Paragraph("6월", ParagraphStyle("at", fontName=font_name, fontSize=12,
                    textColor=WHITE, alignment=TA_CENTER, leading=18)),
          Paragraph("시리즈 론칭", ParagraphStyle("as", fontName=font_name, fontSize=9,
                    textColor=colors.HexColor("#FFD6DC"), alignment=TA_CENTER, leading=14)),
          Paragraph("▶", ParagraphStyle("arr", fontName=font_name, fontSize=16,
                    textColor=PINK, alignment=TA_CENTER, leading=20)),
          Paragraph("7월", ParagraphStyle("at", fontName=font_name, fontSize=12,
                    textColor=WHITE, alignment=TA_CENTER, leading=18)),
          Paragraph("확장", ParagraphStyle("as", fontName=font_name, fontSize=9,
                    textColor=colors.HexColor("#FFD6DC"), alignment=TA_CENTER, leading=14)),
          ]],
        colWidths=[25*mm, 32*mm, 10*mm, 25*mm, 32*mm, 10*mm, 25*mm, 21*mm]
    )
    arrow.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(1,-1), GRAY_DK),
        ("BACKGROUND",(3,0),(4,-1), GRAY_DK),
        ("BACKGROUND",(6,0),(7,-1), GRAY_DK),
        ("BACKGROUND",(2,0),(2,-1), WHITE),
        ("BACKGROUND",(5,0),(5,-1), WHITE),
        ("TOPPADDING",(0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",(0,0),(-1,-1), 6),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(arrow)
    story.append(Spacer(1, 16))

    # 5월
    story.extend(month_card(
        "5월", "🔧", "재정비 (Foundation)",
        "정체성 재정립 + 업로드 구조 고정 + 모델링팩 복귀",
        [
            "요즘 모델링팩 이렇게 바뀌었어요 — 2026 버전 업데이트",
            "모델링팩 입문자가 가장 많이 실수하는 것 (3년 데이터 기준)",
            "환절기 피부 뒤집어졌을 때 모델링팩 조합",
            "지쳤을 때 저를 살린 3가지 — 모델링팩, 마그네슘, 목욕",
            "번아웃 왔을 때 제일 먼저 하는 스킨케어 루틴",
            "올리브영 vs 코스트코 — 같은 카테고리 솔직 비교",
            "봄 환절기 피부 응급처치 3스텝 (10분 완성)",
            "각질 제거 타이밍 잡는 법 — 이 신호 보이면 하세요",
            "5월 여행 전 면세점 활용법 — 숨겨진 혜택 3가지",
            "이 앱 하나로 정부 지원금 다 찾았어요 (청년 필수)",
        ],
        ["업로드 12개 이상", "모델링팩 콘텐츠 3개 이상", "전 영상 저장 유도 CTA 100% 삽입"],
        S
    ))

    # 주간 업로드 구조
    story.append(Paragraph("주간 업로드 구조 (주 3~4개)", S["h3"]))
    wt = make_table(
        ["요일", "콘텐츠 유형", "목적"],
        [
            ["화요일", "시그니처 뷰티 / 모델링팩 정보", "신규 유입 + 저장 유도"],
            ["목요일", "감성 에세이 + 뷰티 연결", "팬덤 형성 + 댓글 유도"],
            ["토요일", "제품 리뷰 / 비교", "공유 유도"],
        ],
        [28*mm, 82*mm, 60*mm], S
    )
    story.append(wt)
    story.append(Spacer(1, 6))
    story.append(PageBreak())

    # 6월
    story.extend(month_card(
        "6월", "🚀", "시리즈 론칭 (Series)",
        "알고리즘 최적화 + '모델링팩 = 예감' 포지셔닝 확립",
        [
            "[실험실 EP.01] 히알루론산 앰플 모델링팩에 넣어봤습니다",
            "[실험실 EP.02] 비타C 파우더 모델링팩 — 피부톤 변화 실험",
            "[피부고민 ①] 홍조 피부, 모델링팩으로 이렇게 잡아요",
            "[피부고민 ②] 각질 심한 날 전날 밤 루틴 완전 정복",
            "여름 전 피부 준비 — 선크림 레이어링 제대로 하는 법",
            "다이어트하면 피부 망가지는 이유 + 회복 루틴",
            "땀 많이 흘리는 여름, 모공 관리법",
            "감성에세이: 30대 되기 전 피부에 투자해야 하는 이유",
            "여름 여행 스킨케어 짐싸기 — 기내 반입 기준으로",
            "올여름 선크림 브랜드별 솔직 후기 (직접 발라봤어요)",
        ],
        ["업로드 14개 이상", "시리즈 각 2회씩 발행 (총 4편)", "댓글 수 전월 대비 30% 증가"],
        S
    ))

    story.append(Paragraph("론칭 시리즈 2개", S["h3"]))
    series_data = [
        ["시리즈", "내용", "CTA 포인트"],
        ["예감 모델링팩 실험실", "매월 새 재료 실험 → 비포/애프터 공개\nEP.01 히알루론산, EP.02 비타C...", "댓글로 다음 재료 투표 받기"],
        ["이 피부 고민엔 이 조합", "피부 고민별 모델링팩 솔루션 매핑\n홍조/각질/뒤집어짐 편", "저장 유도 최적 포맷"],
    ]
    story.append(make_table(series_data[0], series_data[1:], [45*mm, 75*mm, 50*mm], S))
    story.append(PageBreak())

    # 7월
    story.extend(month_card(
        "7월", "🌊", "확장 (Scale)",
        "여름 시즌 콘텐츠 집중 + 팬덤 이벤트 + 첫 협업",
        [
            "물놀이 후 피부 응급처치 — 모델링팩 타이밍이 핵심",
            "선탠 후 화끈거리는 피부 진정 루틴",
            "바다 여행 스킨케어 짐싸기 — 기내반입 vs 위탁",
            "땀 많이 흘리는 여름 모공 집중 관리 주간 루틴",
            "여름 뷰티 하울 — 올리브영/코스트코 여름 신상 픽",
            "에어컨 건조한 실내 피부 수분 지키는 법",
            "공항 면세점 꿀팁 — 이건 꼭 사야 해",
        ],
        ["업로드 16개 이상", "팬 Q&A 이벤트 1회 (스토리 질문 → 릴스 답변)", "협업 1건 타진 (크로스 태그 콜라보)"],
        S
    ))
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 3: 공구마켓 연동 전략
    # ════════════════════════════════════
    story.append(section_header("공구마켓 연동 전략", 3, S))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        '"공구는 갑자기 열리면 안 된다  —  문제 제기 → 해결 과정 → 공구 오픈"',
        S["quote"]
    ))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#F0C0C8"), spaceAfter=12))

    story.append(Paragraph("제품별 공구 타임라인", S["h2"]))
    story.append(make_table(
        ["시기", "제품", "선행 콘텐츠", "시즌 이유"],
        [
            ["5월 중순", "아기궁둥이 퍼프", "2개", "여름 선크림 시즌 시작"],
            ["6월 초", "클렌징밀크", "3개", "여름 피부 자극 민감 시기"],
            ["6월 말", "쑥차", "3개", "냉방 트러블 시즌"],
            ["7월 말", "소창수건", "2개", "여름 물놀이 후 관리 시즌"],
        ],
        [30*mm, 38*mm, 30*mm, 72*mm], S
    ))
    story.append(Spacer(1, 14))

    story.append(Paragraph("공구 퍼널 예시  —  아기궁둥이 퍼프", S["h2"]))
    funnel_steps = [
        ("STEP 1  선행 콘텐츠", "\"선크림 손으로 바르면 안 되는 이유 — 직접 비교해봤어요\""),
        ("STEP 2  선행 콘텐츠", "\"선크림 밀림/뭉침 해결법 — 도구 바꿨더니 완전 달라졌어요\""),
        ("STEP 3  공구 오픈", "\"제가 쓰는 그 퍼프 드디어 공구 열었어요 (링크 바이오)\""),
        ("STEP 4  공구 후기", "\"공구 받으신 분들 이렇게 쓰세요 — 선크림 레이어링 꿀팁\""),
    ]
    for step, desc in funnel_steps:
        row = Table(
            [[Paragraph(step, ParagraphStyle("st", fontName=font_name, fontSize=8.5,
                        textColor=WHITE, leading=14, alignment=TA_CENTER)),
              Paragraph(desc, S["body"])]],
            colWidths=[32*mm, 138*mm]
        )
        bg = PINK if "오픈" in step else GRAY_DK
        row.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0), bg),
            ("BACKGROUND",(1,0),(1,0), PINK_LT if "오픈" in step else GRAY_LT),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),
            ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#E0E0E0")),
        ]))
        story.append(row)
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))
    story.append(Paragraph("핵심 멘트  —  공구 신뢰도를 높이는 한 마디", S["h3"]))
    quote_box = Table(
        [[Paragraph(
            "\"이 제품 공구할까 말까 오래 고민했어요.<br/>"
            "근데 제 채널 보고 피부 관리 시작하신 분들한테<br/>"
            "이건 진짜 알려드려야 할 것 같아서요.\"",
            ParagraphStyle("qb", fontName=font_name, fontSize=10,
                           textColor=GRAY_DK, leading=18, alignment=TA_CENTER)
        )]],
        colWidths=[170*mm]
    )
    quote_box.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), PINK_LT),
        ("BOX",(0,0),(-1,-1), 1.5, PINK),
        ("TOPPADDING",(0,0),(-1,-1),16),
        ("BOTTOMPADDING",(0,0),(-1,-1),16),
        ("LEFTPADDING",(0,0),(-1,-1),20),
        ("RIGHTPADDING",(0,0),(-1,-1),20),
    ]))
    story.append(quote_box)
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 4: KPI 대시보드
    # ════════════════════════════════════
    story.append(section_header("3개월 핵심 지표 (KPI)", 4, S))
    story.append(Spacer(1, 12))

    story.append(make_table(
        ["지표", "5월", "6월", "7월"],
        [
            ["월 업로드 수", "12개+", "14개+", "16개+"],
            ["모델링팩 콘텐츠 비율", "25%+", "30%+", "25%+"],
            ["저장 유도 CTA 삽입률", "100%", "100%", "100%"],
            ["시리즈 에피소드 누적", "—", "4개", "8개+"],
            ["기타 콘텐츠 비율", "20% 이하", "15% 이하", "10% 이하"],
        ],
        [76*mm, 31*mm, 31*mm, 32*mm], S
    ))
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 5: 즉시 실행 액션 플랜
    # ════════════════════════════════════
    story.append(section_header("즉시 실행 액션 플랜", 5, S))
    story.append(Spacer(1, 12))

    action_groups = [
        ("오늘 당장", PINK, [
            "모든 스크립트 마지막에 저장 유도 문구 추가하는 습관 시작",
            "이번 주 업로드 예정 영상에 CTA 삽입",
        ]),
        ("이번 주", GRAY_DK, [
            "5월 콘텐츠 10개 주제 확정",
            "아기궁둥이 퍼프 선행 콘텐츠 1편 촬영 기획",
            "모델링팩 복귀 영상 1편 기획",
        ]),
        ("이번 달", colors.HexColor("#555555"), [
            "주간 업로드 구조 고정 (화 / 목 / 토)",
            "\"예감 모델링팩 실험실\" 시리즈 EP.01 발행",
            "아기궁둥이 퍼프 공구 오픈",
        ]),
    ]
    for group_title, bg_color, items in action_groups:
        hdr = Table(
            [[Paragraph(group_title, ParagraphStyle("gh", fontName=font_name,
               fontSize=10, textColor=WHITE, leading=16))]],
            colWidths=[170*mm]
        )
        hdr.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), bg_color),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("TOPPADDING",(0,0),(-1,-1),7),
            ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ]))
        story.append(hdr)
        for item in items:
            story.append(Paragraph(f"  □  {item}", S["check"]))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 6))
    story.append(Paragraph("당장 멈춰야 할 것", S["h2"]))
    stops = [
        "말 없이 음악만 있는 B컷 영상 업로드  (알고리즘이 스크립트 없는 영상 덜 노출)",
        "CTA 없이 영상 마무리  (저장/댓글 없으면 알고리즘이 외면)",
        "정부지원금/청년혜택 꿀팁  (뷰티 팔로워 타겟과 불일치, 이탈 유발)",
    ]
    for s in stops:
        story.append(Paragraph(f"  ✕  {s}", ParagraphStyle("stop",
            fontName=font_name, fontSize=9.5, leading=16,
            textColor=colors.HexColor("#CC3344"), leftIndent=16, spaceAfter=4)))
    story.append(PageBreak())

    # ════════════════════════════════════
    # SECTION 6: 콘텐츠 DNA
    # ════════════════════════════════════
    story.append(section_header("송예감 콘텐츠 DNA", 6, S))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        '"시청자보다 반 발짝 먼저 경험하고, 친구에게 말하듯 공유한다"',
        S["quote"]
    ))

    story.append(Paragraph("스크립트 4단계 구조", S["h2"]))
    struct = Table(
        [
            [Paragraph("01", ParagraphStyle("sn", fontName=font_name, fontSize=18,
              textColor=PINK, alignment=TA_CENTER, leading=22)),
             Paragraph("훅 (Hook)", ParagraphStyle("sl", fontName=font_name, fontSize=10,
              textColor=GRAY_DK, leading=16)),
             Paragraph("멈추게 만들기  |  고백/충격형 46.8%", S["body_sm"])],
            [Paragraph("02", ParagraphStyle("sn2", fontName=font_name, fontSize=18,
              textColor=PINK, alignment=TA_CENTER, leading=22)),
             Paragraph("브릿지 (Bridge)", ParagraphStyle("sl", fontName=font_name, fontSize=10,
              textColor=GRAY_DK, leading=16)),
             Paragraph("\"나도 그랬어\" 공감  |  1인칭 경험 71.6%", S["body_sm"])],
            [Paragraph("03", ParagraphStyle("sn3", fontName=font_name, fontSize=18,
              textColor=PINK, alignment=TA_CENTER, leading=22)),
             Paragraph("바디 (Body)", ParagraphStyle("sl", fontName=font_name, fontSize=10,
              textColor=GRAY_DK, leading=16)),
             Paragraph("구체적인 답  |  브랜드/가격/단점 필수", S["body_sm"])],
            [Paragraph("04", ParagraphStyle("sn4", fontName=font_name, fontSize=18,
              textColor=PINK, alignment=TA_CENTER, leading=22)),
             Paragraph("클로징 (Close)", ParagraphStyle("sl", fontName=font_name, fontSize=10,
              textColor=GRAY_DK, leading=16)),
             Paragraph("관계 맺기  |  저장/댓글/공유 중 1개 필수", S["body_sm"])],
        ],
        colWidths=[20*mm, 50*mm, 100*mm]
    )
    struct.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WHITE, GRAY_LT]),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#E0E0E0")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(0,0),(0,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),9),
        ("BOTTOMPADDING",(0,0),(-1,-1),9),
        ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    story.append(struct)
    story.append(Spacer(1, 14))

    story.append(Paragraph("영상 제작 전 체크리스트", S["h2"]))
    checks = [
        "첫 2문장 안에 멈출 이유가 있는가?",
        "\"안녕하세요\"로 시작하지 않았는가?",
        "본인 경험 또는 주변 사람 이야기가 들어갔는가?",
        "단점 또는 주의사항을 언급했는가?",
        "브랜드명 / 가격 / 구체적 수치가 있는가?",
        "마지막에 저장 / 댓글 / 공유 중 하나가 있는가?",
        "300자 내외인가?  (최대 400자)",
        "\"~거든요\" \"~더라고요\" 예감 특유의 톤이 살아있는가?",
    ]
    for c in checks:
        story.append(Paragraph(f"  □  {c}", S["check"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("예감 감각 언어 사전", S["h2"]))
    word_data = [
        ["질감", "피부 상태", "결과 표현", "강조 부사"],
        ["꾸덕한 / 말캉한", "쫀쫀한 / 탱글탱글", "싹 잡힙니다", "진짜 (347회)"],
        ["촉촉한 / 벨벳", "뽀얀 / 뒤집어진", "딱이에요", "꼭 (153회)"],
        ["보송한 / 가벼운", "촉촉 / 탱글", "야무지게", "딱 (144회)"],
    ]
    story.append(make_table(word_data[0], word_data[1:],
                            [42*mm, 42*mm, 42*mm, 44*mm], S))
    story.append(PageBreak())

    # ════════════════════════════════════
    # 마지막 페이지: 목표 포지셔닝
    # ════════════════════════════════════
    story.append(Spacer(1, 30*mm))
    final_box = Table(
        [[Paragraph("3개월 후 목표 포지셔닝", ParagraphStyle("ft", fontName=font_name,
              fontSize=11, textColor=colors.HexColor("#FFD6DC"), leading=18,
              alignment=TA_CENTER))],
         [Spacer(1, 8)],
         [Paragraph('"모델링팩 하면 예감, 예감 하면 모델링팩"', ParagraphStyle("fq",
              fontName=font_name, fontSize=18, textColor=WHITE, leading=26,
              alignment=TA_CENTER))],
         [Spacer(1, 8)],
         [Paragraph("진솔한 스킨케어 경험을 공유하는 라이프스타일 크리에이터", ParagraphStyle("fs",
              fontName=font_name, fontSize=11, textColor=colors.HexColor("#FFD6DC"),
              leading=18, alignment=TA_CENTER))]],
        colWidths=[170*mm]
    )
    final_box.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), PINK),
        ("TOPPADDING",(0,0),(-1,-1),28),
        ("BOTTOMPADDING",(0,0),(-1,-1),28),
        ("LEFTPADDING",(0,0),(-1,-1),20),
        ("RIGHTPADDING",(0,0),(-1,-1),20),
        ("ROUNDEDCORNERS",[8,8,8,8]),
    ]))
    story.append(final_box)
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph(
        "본 보고서는 2023.07 ~ 2026.03 릴스 611개 데이터 분석 기반으로 작성되었습니다.",
        S["footer"]
    ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF saved: {output_path}")

build_pdf("/Users/eunsongkang/Desktop/yegam/송예감_10만팔로워_전략보고서.pdf")
