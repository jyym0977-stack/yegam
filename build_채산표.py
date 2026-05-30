import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter

# ─────────────────────────────────────────────
# 1. RAW DATA
# ─────────────────────────────────────────────

# Smart-store settlements per month
smartstore = {
    '11': [35814, 1291870, 1641903, 1047735, 5223456, 1190484, 1883886,
           8679907, 1897884, 5905619, 214882, 103588, 6765981, 301329],
    '12': [67176, 3000, 1145284, 1269742, 731869, 6604493, 1631143,
           2702962, 7057239, 799233, 8235636, 71820, 81428, 35814, 588571],
    '01': [935902, 2181436, 524302, 483343, 1837916, 336871, 2176666,
           25750, 28692, 100058, 25653, 22256, 89933, 25185],
    '02': [],
    '03': [],
    '04': [],
}

# Corporate / B2B receipts
corporate_income = {
    '11': 464431 + 1044913,          # 프링즈 + 제이케이인
    '12': 1082750 + 2011979,          # 제이케이인 + 프링즈
    '01': 0,
    '02': 9042040 + 11203637,         # 에이비티제 + 퍼프마켓
    '03': 3036580,                     # 에코마인
    '04': 2089998,                     # 라누보
}

# Small individual sales (confirmed)
individual_sales = {
    '11': 112900,                      # 배서영
    '12': 63500 + 9900 + 9900 + 36900 + 3500,  # 이지연 등
    '01': 74000 + 66900 + 22900,       # 이지혜, 김은주, 김혜미
    '02': 0,
    '03': 0,
    '04': 0,
}

# ── COGS (bank transfers) ──
# 택배비
delivery_bank = {
    '11': 95000 + 1397330 + 1025460,
    '12': 870460 + 528210 + 356510 + 14000,
    '01': 322390,
    '02': 172530,
    '03': 0,
    '04': 770000 + 1700000,           # 티태그 + 패키징
}

# 재고 매입 (쑥차, 모델링팩, 발토시, 도자기컵, 틴케이스)
inventory_bank = {
    '11': 25300000 + 506000,          # 쑥차
    '12': 11000000 + 4300000 + (1360000 + 672000 + 132000 + 567000 +
                                  655000 + 169000 + 108000 + 600000),  # 쑥차 + 모델링팩 + 발토시
    '01': 0,
    '02': 0,
    '03': 2100000 + 1086800,          # 도자기컵 + 틴케이스
    '04': 0,
}

# ── 인건비 (bank) ──
labor_bank = {
    '11': 0,
    '12': 2200000 + 580000,
    '01': 0,
    '02': 0,
    '03': 0,
    '04': 0,
}

# ── 운영비 (bank) ──
opex_bank = {
    '11': 110000,                     # 세무사
    '12': 110000 + 1000000 + 132000 + 160000,  # 세무사 + 사은품
    '01': 110000,
    '02': 110000,
    '03': 110000 + 1760000,           # 세무사 + 디자인비
    '04': 110000 + 150000,            # 세무사 + 에리카메이크
}

# ── 기타 (bank, 신뢰도 하 포함) ──
# 12월: 교육비 1,160,000 / 하명옥 1,155,000
# 01월: 송명희 23,400 / 김민지 122,810 / (주)일송개발 24,000,000 /
#        택배-대여금 1,000,000 / 등록면허세 40,500
# 02월: 윤수연 440,000
# 03월: 김민지 50,860 / 김정배 1,000,000
# 04월: 조경이 302,000 / (주)디앤피 187,220 / 김은경 90,000
other_bank = {
    '11': 0,
    '12': 1160000 + 1155000,
    '01': 23400 + 122810 + 24000000 + 1000000 + 40500,
    '02': 440000,
    '03': 50860 + 1000000,
    '04': 302000 + 187220 + 90000,
}

# ── 카드 내역 월평균 (모든 달에 동일 적용) ──
CARD_COGS   = 1436945
CARD_INS    = 234697
CARD_OPEX   = 135270
CARD_OTHER  = 141890

months = ['11', '12', '01', '02', '03', '04']
month_labels = ['2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04']
month_ko = ['25년11월', '25년12월', '26년1월', '26년2월', '26년3월', '26년4월']

# ── Compute totals per month ──
def monthly_totals(m):
    revenue = sum(smartstore[m]) + corporate_income[m] + individual_sales[m]
    cogs    = delivery_bank[m] + inventory_bank[m] + CARD_COGS
    labor   = labor_bank[m]
    ins     = CARD_INS
    opex    = opex_bank[m] + CARD_OPEX
    other   = other_bank[m] + CARD_OTHER
    return {
        '매출': revenue,
        '매출원가': cogs,
        '인건비': labor,
        '사대보험': ins,
        '운영비': opex,
        '기타': other,
    }

data = {m: monthly_totals(m) for m in months}

# ── 6개월 평균 ──
keys = ['매출', '매출원가', '인건비', '사대보험', '운영비', '기타']
avg = {k: round(sum(data[m][k] for m in months) / 6) for k in keys}
avg['비용합계'] = sum(avg[k] for k in keys if k != '매출')
avg['영업이익'] = avg['매출'] - avg['비용합계']

# ─────────────────────────────────────────────
# 2. RAW TRANSACTIONS FOR 원본데이터 SHEET
# ─────────────────────────────────────────────

raw_transactions = [
    # (날짜, 거래처, 금액, 분류, 신뢰도, 출처, 입출금)
    # ── 11월 입금 ──
    ('2025-11-01', '스마트스토어정산', 35814, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1291870, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1641903, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1047735, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 5223456, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1190484, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1883886, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 8679907, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 1897884, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 5905619, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 214882, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 103588, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 6765981, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '스마트스토어정산', 301329, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '주식회사 프링즈', 464431, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '주식회사 제이케이인', 1044913, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '배서영', 112900, '매출', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '강현준', 20000000, '제외(차입금)', '상', '카카오뱅크', '입금'),
    ('2025-11-01', '예금이자', 730, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 11월 출금 ──
    ('2025-11-01', '택배비', 95000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-11-07', '쑥차 구매', 25300000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-11-15', '택배비', 1397330, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-11-21', '택배비', 1025460, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-11-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2025-11-26', '대여금 상환', 20000000, '제외(차입금상환)', '상', '카카오뱅크', '출금'),
    ('2025-11-27', '쑥차 구매', 506000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-11-27', '강은송', 800000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    # ── 12월 입금 ──
    ('2025-12-01', '스마트스토어정산', 67176, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 3000, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 1145284, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 1269742, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 731869, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 6604493, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 1631143, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 2702962, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 7057239, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 799233, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 8235636, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 71820, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 81428, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 35814, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '스마트스토어정산', 588571, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '주식회사 제이케이인', 1082750, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '주식회사 프링즈', 2011979, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '이지연', 63500, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '백은미', 9900, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '홍지영', 9900, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '최선하', 36900, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '신혜영', 3500, '매출', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '강현준', 15000000, '제외(차입금)', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '강은송', 800000, '제외(자기이체)', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '강은송', 1000000, '제외(자기이체)', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '세이프박스', 100000, '제외(저축이체)', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '세이프박스', 30000, '제외(저축이체)', '상', '카카오뱅크', '입금'),
    ('2025-12-01', '예금이자', 797, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 12월 출금 ──
    ('2025-12-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2025-12-05', '쑥차 구매', 11000000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-10', '모델링팩 구매대금', 4300000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-10', '택배비', 870460, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-10', '사은품 구매', 1000000, '운영비', '상', '카카오뱅크', '출금'),
    ('2025-12-16', '택배비', 528210, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-17', '사은품비', 132000, '운영비', '상', '카카오뱅크', '출금'),
    ('2025-12-17', '사은품 구매비', 160000, '운영비', '상', '카카오뱅크', '출금'),
    ('2025-12-19', '인건비', 2200000, '인건비', '상', '카카오뱅크', '출금'),
    ('2025-12-23', '인건비-이은빈', 580000, '인건비', '상', '카카오뱅크', '출금'),
    ('2025-12-23', '택배비', 14000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-23', '교육비', 1160000, '기타', '중', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 1360000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 672000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 132000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 567000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 655000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 169000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 108000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '발토시', 600000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-26', '하명옥', 1155000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2025-12-26', '강은송', 5000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2025-12-24', '신혜영', 3500, '제외(환불)', '상', '카카오뱅크', '출금'),
    ('2025-12-30', '택배비', 356510, '매출원가', '상', '카카오뱅크', '출금'),
    ('2025-12-31', '대여금', 30000000, '제외(대여금)', '상', '카카오뱅크', '출금'),
    # ── 1월 입금 ──
    ('2026-01-01', '스마트스토어정산', 935902, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 2181436, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 524302, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 483343, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 1837916, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 336871, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 2176666, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 25750, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 28692, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 100058, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 25653, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 22256, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 89933, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '스마트스토어정산', 25185, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '이지혜', 74000, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '김은주', 66900, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '김혜미', 22900, '매출', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '강은송', 29867945, '제외(자기이체)', '상', '카카오뱅크', '입금'),
    ('2026-01-01', '예금이자', 556, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 1월 출금 ──
    ('2026-01-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2026-01-02', '환불', 26400, '매출원가차감(환불)', '상', '카카오뱅크', '출금'),
    ('2026-01-04', '택배비', 322390, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-01-11', '송명희', 23400, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-01-13', '(주)일송개발', 24000000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-01-14', '김민지', 122810, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-01-19', '카드값', 13300000, '제외(카드결제)', '상', '카카오뱅크', '출금'),
    ('2026-01-21', '택배-대여금', 1000000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-01-23', '강은송', 1456803, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-01-23', '등록면허세', 40500, '기타(세금)', '상', '카카오뱅크', '출금'),
    # ── 2월 입금 ──
    ('2026-02-01', '(주)에이비티제', 9042040, '매출', '상', '카카오뱅크', '입금'),
    ('2026-02-01', '퍼프마켓 수수료', 11203637, '매출', '상', '카카오뱅크', '입금'),
    ('2026-02-01', '국세환급금(동울산세무서)', 1361000, '제외(세금환급)', '상', '카카오뱅크', '입금'),
    ('2026-02-01', '예금이자', 703, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 2월 출금 ──
    ('2026-02-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2026-02-06', '택배비', 172530, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-02-10', '윤수연', 440000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    # ── 3월 입금 ──
    ('2026-03-01', '(주)에코마인', 3036580, '매출', '상', '카카오뱅크', '입금'),
    ('2026-03-01', '강은송', 3000000, '제외(자기이체)', '상', '카카오뱅크', '입금'),
    ('2026-03-01', '김정배', 1000000, '기타(신뢰도하)', '하', '카카오뱅크', '입금'),
    ('2026-03-01', '예금이자', 1596, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 3월 출금 ──
    ('2026-03-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2026-03-07', '김민지', 50860, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-03-19', '도자기컵', 2100000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-03-23', '틴케이스', 1086800, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-03-25', '강은송', 1000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-03-25', '강은송', 1000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-03-25', '강은송', 5000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-03-30', '디자인비', 1760000, '운영비', '상', '카카오뱅크', '출금'),
    # ── 4월 입금 ──
    ('2026-04-01', '주식회사 라누보', 2089998, '매출', '상', '카카오뱅크', '입금'),
    ('2026-04-01', '예금이자', 1116, '제외(이자)', '상', '카카오뱅크', '입금'),
    # ── 4월 출금 ──
    ('2026-04-01', '안희은세무사', 110000, '운영비', '상', '카카오뱅크', '출금'),
    ('2026-04-02', '조경이', 302000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-04-20', '티태그', 770000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-04-20', '패키징 비용', 1700000, '매출원가', '상', '카카오뱅크', '출금'),
    ('2026-04-22', '(주)디앤피', 187220, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    ('2026-04-23', '강은송', 2000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-04-27', '강은송', 1000000, '제외(자기이체)', '상', '카카오뱅크', '출금'),
    ('2026-04-28', '이혜연(에리카메이크)', 150000, '운영비', '상', '카카오뱅크', '출금'),
    ('2026-04-28', '김은경', 90000, '기타(신뢰도하)', '하', '카카오뱅크', '출금'),
    # ── 카드 내역 (월평균 대표값) ──
    ('카드내역 월평균', '네이버페이/쿠팡 등 (상품매입)', 1436945, '매출원가', '상', '카드(6개월평균)', '출금'),
    ('카드내역 월평균', '건강보험공단 (사대보험)', 234697, '사대보험/퇴직금', '상', '카드(6개월평균)', '출금'),
    ('카드내역 월평균', '아임웹/MANYCHAT/크몽 등 (운영비)', 135270, '운영비', '상', '카드(6개월평균)', '출금'),
    ('카드내역 월평균', '기타 카드거래', 141890, '기타', '중', '카드(6개월평균)', '출금'),
]

# ─────────────────────────────────────────────
# 3. UNCLASSIFIED / 신뢰도 하 목록
# ─────────────────────────────────────────────

unclear = [
    ('2025-12-26', '하명옥', 1155000, '기타', '출금', '개인명 이체. 사업 관련 여부 불명 — 거래 목적 확인 필요'),
    ('2026-01-13', '(주)일송개발', 24000000, '기타', '출금', '2,400만원 대규모 이체. 건물/부동산 관련? 목적 확인 필수'),
    ('2026-01-21', '택배-대여금', 1000000, '기타', '출금', '"대여금" 명칭 — 차입금 상환인지 다른 목적인지 확인'),
    ('2026-02-10', '윤수연', 440000, '기타', '출금', '개인명 이체. 사업 관련 여부 불명 — 용도 확인 필요'),
    ('2026-03-01', '김정배', 1000000, '기타', '입금', '개인명 입금. 제품 판매 대금? 차입금? 출처 확인 필요'),
    ('2026-04-02', '조경이', 302000, '기타', '출금', '개인명 이체. 용도 불명 — 인건비? 물품구매? 확인 필요'),
    ('2026-04-22', '(주)디앤피', 187220, '기타', '출금', '법인 이체. 거래 내용 불명 — 거래 목적 확인 필요'),
    ('2026-04-28', '김은경', 90000, '기타', '출금', '개인명 소액 이체. 용도 불명 — 확인 필요'),
    ('2026-01-14', '김민지', 122810, '기타', '출금', '개인명 이체. 1월 출금. 용도 불명 (3월 50,860원과 동일인)'),
    ('2026-03-07', '김민지', 50860, '기타', '출금', '개인명 이체. 3월 출금. 1월과 동일인 — 반복 거래 목적 확인'),
    ('2026-01-11', '송명희', 23400, '기타', '출금', '개인명 소액 이체. 용도 불명 — 확인 필요'),
]
# Sort by amount descending
unclear.sort(key=lambda x: x[2], reverse=True)

# ─────────────────────────────────────────────
# 4. BUILD EXCEL
# ─────────────────────────────────────────────

wb = openpyxl.Workbook()

# ── Styles ──
font_title   = Font(name='맑은 고딕', size=18, bold=True, color='000000')
font_sub     = Font(name='맑은 고딕', size=10, color='808080')
font_header  = Font(name='맑은 고딕', size=10, bold=True, color='FFFFFF')
font_cost_hdr= Font(name='맑은 고딕', size=10, italic=True, color='808080')
font_normal  = Font(name='맑은 고딕', size=10)
font_bold    = Font(name='맑은 고딕', size=10, bold=True)
font_profit  = Font(name='맑은 고딕', size=11, bold=True, color='DC3232')
font_note    = Font(name='맑은 고딕', size=9, color='606060')

fill_header  = PatternFill('solid', fgColor='333333')
fill_profit  = PatternFill('solid', fgColor='FFEBEB')
fill_alt     = PatternFill('solid', fgColor='F9F9F9')
fill_month   = PatternFill('solid', fgColor='2F5597')
fill_subhdr  = PatternFill('solid', fgColor='4472C4')
fill_unclear = PatternFill('solid', fgColor='FFF2CC')
fill_hdr_yl  = PatternFill('solid', fgColor='FFC000')

align_c = Alignment(horizontal='center', vertical='center', wrap_text=True)
align_l = Alignment(horizontal='left',   vertical='center', wrap_text=True)
align_r = Alignment(horizontal='right',  vertical='center')

thin_side   = Side(style='thin',   color='CCCCCC')
med_side    = Side(style='medium', color='DC3232')
dash_side   = Side(style='dashed', color='AAAAAA')

num_fmt  = '#,##0'
pct_fmt  = '0.0%'

def thin_border():
    return Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

def top_dash():
    return Border(top=Side(style='dashed', color='888888'))

def profit_border():
    return Border(left=med_side, right=med_side, top=med_side, bottom=med_side)

# ══════════════════════════════════════════════
# SHEET 1: 채산표
# ══════════════════════════════════════════════
ws1 = wb.active
ws1.title = '채산표'
ws1.column_dimensions['A'].width = 34
ws1.column_dimensions['B'].width = 20
ws1.column_dimensions['C'].width = 11

# Row 1: Title
ws1.merge_cells('A1:C1')
ws1['A1'] = '회사 채산표 (예감마켓)'
ws1['A1'].font = font_title
ws1['A1'].alignment = align_c
ws1.row_dimensions[1].height = 36

# Row 2: Subtitle
ws1.merge_cells('A2:C2')
ws1['A2'] = '(단위: 원 / 월)  |  분석기간: 2025년 11월 ~ 2026년 4월 (6개월 평균)'
ws1['A2'].font = font_sub
ws1['A2'].alignment = align_c
ws1.row_dimensions[2].height = 18

# Row 3: blank
ws1.row_dimensions[3].height = 6

# Row 4: Header
for col, val in zip('ABC', ['항목', '금액 (6개월 평균)', '비율']):
    c = ws1[f'{col}4']
    c.value = val
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_c
    c.border = thin_border()
ws1.row_dimensions[4].height = 22

# Row 5: 매출
ws1['A5'] = '매출'
ws1['B5'] = avg['매출']
ws1['C5'] = 1.0
for col in 'ABC':
    c = ws1[f'{col}5']
    c.font = font_bold
    c.alignment = align_l if col == 'A' else align_r
    c.border = thin_border()
ws1['B5'].number_format = num_fmt
ws1['C5'].number_format = pct_fmt
ws1['A5'].alignment = align_l

# Row 6: — 비용 —
ws1.merge_cells('A6:C6')
ws1['A6'] = '— 비용 —'
ws1['A6'].font = font_cost_hdr
ws1['A6'].alignment = align_c
ws1.row_dimensions[6].height = 18

# Cost rows: (row, label, key)
cost_rows = [
    (7,  '  매출원가  (상품매입·택배비·포장재)', '매출원가'),
    (8,  '  임대료',                              None),
    (9,  '  인건비',                              '인건비'),
    (10, '  사대보험 / 퇴직금',                   '사대보험'),
    (11, '  관리비  (전기·수도·CCTV·인터넷 등)',  None),
    (12, '  운영비  (광고비·플랫폼·복리후생 등)', '운영비'),
    (13, '  기타  ※ 신뢰도하 항목 포함 → 시트4', '기타'),
]

for r, label, key in cost_rows:
    ws1[f'A{r}'] = label
    ws1[f'A{r}'].font = font_normal
    ws1[f'A{r}'].alignment = align_l
    ws1[f'A{r}'].border = thin_border()

    val = avg.get(key, 0) if key else 0
    ws1[f'B{r}'] = val
    ws1[f'B{r}'].number_format = num_fmt
    ws1[f'B{r}'].font = font_normal
    ws1[f'B{r}'].alignment = align_r
    ws1[f'B{r}'].border = thin_border()

    ws1[f'C{r}'] = f'=IF(B5>0,B{r}/B5,"-")'
    ws1[f'C{r}'].number_format = pct_fmt
    ws1[f'C{r}'].font = font_normal
    ws1[f'C{r}'].alignment = align_r
    ws1[f'C{r}'].border = thin_border()

    # Alternate shading
    if r % 2 == 1:
        for col in 'ABC':
            ws1[f'{col}{r}'].fill = fill_alt

# Row 14: 비용 합계
ws1['A14'] = '비용 합계'
ws1['A14'].font = font_bold
ws1['A14'].border = Border(top=dash_side, left=thin_side, right=thin_side, bottom=thin_side)
ws1['A14'].alignment = align_l
ws1['B14'] = '=SUM(B7:B13)'
ws1['B14'].number_format = num_fmt
ws1['B14'].font = font_bold
ws1['B14'].border = Border(top=dash_side, left=thin_side, right=thin_side, bottom=thin_side)
ws1['B14'].alignment = align_r
ws1['C14'] = '=IF(B5>0,B14/B5,"-")'
ws1['C14'].number_format = pct_fmt
ws1['C14'].font = font_bold
ws1['C14'].border = Border(top=dash_side, left=thin_side, right=thin_side, bottom=thin_side)
ws1['C14'].alignment = align_r
ws1.row_dimensions[14].height = 22

# Row 15: 영업이익
ws1['A15'] = '영업이익'
ws1['B15'] = '=B5-B14'
ws1['C15'] = '=IF(B5>0,B15/B5,"-")'
ws1['B15'].number_format = num_fmt
ws1['C15'].number_format = pct_fmt
for col in 'ABC':
    c = ws1[f'{col}15']
    c.font = font_profit
    c.fill = fill_profit
    c.border = profit_border()
    c.alignment = align_r if col in 'BC' else align_l
ws1.row_dimensions[15].height = 26

# Row 17-20: Notes
ws1.row_dimensions[16].height = 8
note_rows = [
    (17, '【데이터 출처】 카카오뱅크 거래내역 (2025.11~2026.04, PDF 추출) + 카드 내역 6개월 평균'),
    (18, '【임대료/관리비】 카카오뱅크 및 카드 내역에서 임대료·관리비 이체 확인 안 됨 → 0원 처리'),
    (19, '【신뢰도하 항목】 기타에 임시 포함 — 시트4(분류불명) 확인 후 재분류 필요'),
    (20, '【(주)일송개발 2,400만원】 1월 대규모 이체 — 성격 확인 필수 (자산취득? 보증금?)'),
]
for r, note in note_rows:
    ws1.merge_cells(f'A{r}:C{r}')
    ws1[f'A{r}'] = note
    ws1[f'A{r}'].font = font_note
    ws1[f'A{r}'].alignment = align_l
    ws1.row_dimensions[r].height = 16

# ══════════════════════════════════════════════
# SHEET 2: 월별 상세
# ══════════════════════════════════════════════
ws2 = wb.create_sheet('월별 상세')
ws2.column_dimensions['A'].width = 28
for i, _ in enumerate(months):
    ws2.column_dimensions[get_column_letter(i + 2)].width = 16
ws2.column_dimensions[get_column_letter(len(months) + 2)].width = 16

# Title
ws2.merge_cells(f'A1:{get_column_letter(len(months)+2)}1')
ws2['A1'] = '월별 항목 상세 내역 (2025년 11월 ~ 2026년 4월)'
ws2['A1'].font = Font(name='맑은 고딕', size=14, bold=True, color='FFFFFF')
ws2['A1'].fill = fill_month
ws2['A1'].alignment = align_c
ws2.row_dimensions[1].height = 28

# Headers
headers = ['항목'] + month_ko + ['6개월 평균']
for ci, h in enumerate(headers, 1):
    c = ws2.cell(row=2, column=ci, value=h)
    c.font = Font(name='맑은 고딕', size=10, bold=True, color='FFFFFF')
    c.fill = fill_subhdr
    c.alignment = align_c
    c.border = thin_border()
ws2.row_dimensions[2].height = 22

# Data rows
row_defs = [
    ('매출', '매출'),
    ('매출원가', '매출원가'),
    ('인건비', '인건비'),
    ('사대보험/퇴직금', '사대보험'),
    ('운영비', '운영비'),
    ('기타 (신뢰도하 포함)', '기타'),
    ('비용 합계', '_cost'),
    ('영업이익', '_profit'),
]

for ri, (label, key) in enumerate(row_defs, 3):
    is_total  = key == '_cost'
    is_profit = key == '_profit'

    c = ws2.cell(row=ri, column=1, value=label)
    c.font = font_bold if (is_total or is_profit) else font_normal
    c.fill = fill_profit if is_profit else PatternFill()
    c.border = thin_border()
    c.alignment = align_l

    for ci, m in enumerate(months, 2):
        if is_total:
            col_letter = get_column_letter(ci)
            val = f'=SUM({col_letter}4:{col_letter}8)'
        elif is_profit:
            col_letter = get_column_letter(ci)
            val = f'={col_letter}3-{col_letter}9'
        else:
            val = data[m][key]

        cell = ws2.cell(row=ri, column=ci, value=val)
        cell.number_format = num_fmt
        cell.border = thin_border()
        cell.alignment = align_r
        cell.font = font_bold if (is_total or is_profit) else font_normal
        if is_profit:
            cell.fill = fill_profit
            cell.font = Font(name='맑은 고딕', size=10, bold=True, color='DC3232')

    # Average column
    avg_col = len(months) + 2
    avg_col_letter = get_column_letter(avg_col)
    data_range = f'{get_column_letter(2)}{ri}:{get_column_letter(len(months)+1)}{ri}'
    avg_cell = ws2.cell(row=ri, column=avg_col, value=f'=AVERAGE({data_range})')
    avg_cell.number_format = num_fmt
    avg_cell.border = thin_border()
    avg_cell.alignment = align_r
    avg_cell.font = Font(name='맑은 고딕', size=10, bold=True,
                         color='DC3232' if is_profit else '000000')
    if is_profit:
        avg_cell.fill = fill_profit

ws2.row_dimensions[3].height = 20

# ══════════════════════════════════════════════
# SHEET 3: 원본데이터 (통합)
# ══════════════════════════════════════════════
ws3 = wb.create_sheet('원본데이터 (통합)')
ws3.column_dimensions['A'].width = 14
ws3.column_dimensions['B'].width = 32
ws3.column_dimensions['C'].width = 16
ws3.column_dimensions['D'].width = 20
ws3.column_dimensions['E'].width = 10
ws3.column_dimensions['F'].width = 18
ws3.column_dimensions['G'].width = 8

ws3.merge_cells('A1:G1')
ws3['A1'] = '원본 거래 데이터 통합 (카카오뱅크 + 카드 내역)'
ws3['A1'].font = Font(name='맑은 고딕', size=13, bold=True, color='FFFFFF')
ws3['A1'].fill = fill_month
ws3['A1'].alignment = align_c
ws3.row_dimensions[1].height = 26

hdr3 = ['날짜', '거래처', '금액 (원)', '분류항목', '신뢰도', '출처', '입출금']
for ci, h in enumerate(hdr3, 1):
    c = ws3.cell(row=2, column=ci, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_c
    c.border = thin_border()
ws3.row_dimensions[2].height = 20

fill_red_bg = PatternFill('solid', fgColor='FFF0F0')
fill_grn_bg = PatternFill('solid', fgColor='F0FFF0')

for ri, (dt, party, amt, cat, trust, src, inout) in enumerate(raw_transactions, 3):
    row_fill = fill_grn_bg if inout == '입금' else (fill_red_bg if inout == '출금' else PatternFill())
    vals = [dt, party, amt, cat, trust, src, inout]
    for ci, val in enumerate(vals, 1):
        cell = ws3.cell(row=ri, column=ci, value=val)
        cell.font = font_normal
        cell.border = thin_border()
        cell.fill = row_fill
        cell.alignment = align_r if ci == 3 else align_l
    ws3.cell(row=ri, column=3).number_format = num_fmt

ws3.freeze_panes = 'A3'
ws3.auto_filter.ref = f'A2:G{len(raw_transactions)+2}'

# ══════════════════════════════════════════════
# SHEET 4: 분류불명
# ══════════════════════════════════════════════
ws4 = wb.create_sheet('분류불명')
ws4.column_dimensions['A'].width = 13
ws4.column_dimensions['B'].width = 22
ws4.column_dimensions['C'].width = 16
ws4.column_dimensions['D'].width = 14
ws4.column_dimensions['E'].width = 8
ws4.column_dimensions['F'].width = 52

ws4.merge_cells('A1:F1')
ws4['A1'] = '분류불명 거래 목록 (신뢰도 "하" — 사용자 확인 필요)'
ws4['A1'].font = Font(name='맑은 고딕', size=13, bold=True, color='FFFFFF')
ws4['A1'].fill = PatternFill('solid', fgColor='C55A11')
ws4['A1'].alignment = align_c
ws4.row_dimensions[1].height = 26

ws4.merge_cells('A2:F2')
ws4['A2'] = '※ 아래 항목들은 성격이 불명확합니다. 각 항목 확인 후 시트1(채산표)의 해당 금액을 조정해주세요.'
ws4['A2'].font = Font(name='맑은 고딕', size=9, italic=True, color='7F3F00')
ws4['A2'].fill = fill_unclear
ws4['A2'].alignment = align_l

hdr4 = ['날짜', '거래처', '금액 (원)', '임시분류', '입출금', '확인 필요 사항']
for ci, h in enumerate(hdr4, 1):
    c = ws4.cell(row=3, column=ci, value=h)
    c.font = font_header
    c.fill = fill_hdr_yl
    c.alignment = align_c
    c.border = thin_border()
ws4.row_dimensions[3].height = 20

for ri, (dt, party, amt, cat, inout, note) in enumerate(unclear, 4):
    vals = [dt, party, amt, cat, inout, note]
    for ci, val in enumerate(vals, 1):
        cell = ws4.cell(row=ri, column=ci, value=val)
        cell.font = font_normal
        cell.border = thin_border()
        cell.fill = fill_unclear
        cell.alignment = align_r if ci == 3 else align_l
    ws4.cell(row=ri, column=3).number_format = num_fmt

# Highlight the 24M row specially
for ci in range(1, 7):
    ws4.cell(row=5, column=ci).fill = PatternFill('solid', fgColor='FFD7C0')
    ws4.cell(row=5, column=ci).font = Font(name='맑은 고딕', size=10, bold=True)

ws4.freeze_panes = 'A4'

# ─────────────────────────────────────────────
# 5. SAVE
# ─────────────────────────────────────────────
out_path = '/Users/eunsongkang/Desktop/yegam/채산표_2026.xlsx'
wb.save(out_path)
print(f'Saved: {out_path}')

# Print summary for verification
print('\n=== 6개월 평균 채산표 요약 ===')
print(f"매출:      {avg['매출']:>15,}원  (100.0%)")
print(f"매출원가:  {avg['매출원가']:>15,}원  ({avg['매출원가']/avg['매출']*100:.1f}%)")
print(f"인건비:    {avg['인건비']:>15,}원  ({avg['인건비']/avg['매출']*100:.1f}%)")
print(f"사대보험:  {avg['사대보험']:>15,}원  ({avg['사대보험']/avg['매출']*100:.1f}%)")
print(f"운영비:    {avg['운영비']:>15,}원  ({avg['운영비']/avg['매출']*100:.1f}%)")
print(f"기타:      {avg['기타']:>15,}원  ({avg['기타']/avg['매출']*100:.1f}%)")
print(f"임대료:    {'0':>15}원  (0.0%)")
print(f"관리비:    {'0':>15}원  (0.0%)")
print(f"─────────────────────────────────")
print(f"비용합계:  {avg['비용합계']:>15,}원  ({avg['비용합계']/avg['매출']*100:.1f}%)")
print(f"영업이익:  {avg['영업이익']:>15,}원  ({avg['영업이익']/avg['매출']*100:.1f}%)")

print('\n=== 월별 매출 ===')
for m, ml in zip(months, month_labels):
    print(f"  {ml}: {data[m]['매출']:>15,}원")

print('\n=== 신뢰도하 항목 (금액 순) ===')
for dt, party, amt, cat, inout, note in unclear:
    print(f"  {dt}  {party:<20}  {amt:>12,}원  [{inout}]")
PYEOF
