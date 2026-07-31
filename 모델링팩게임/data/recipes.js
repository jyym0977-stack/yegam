// 레시피 4유형 (설계도 v1.0 §3 — 전 항목 은송님 확정)
// 배합 공통: 기본 = 가루 1 : 물 0.8 / 첨가 = 가루 1 : 물 0.5 : 첨가물 0.5
// 붓는 법: 절반 먼저 → 나머지 조금씩 / 완성 판정: 스패츌러 뒤집어도 안 떨어짐
const RECIPES = {
  R1: {
    name: '쿨링 진정 레시피',
    sub: '지금 필요한 건 소방수',
    emoji: '🧊',
    color: '#7fb5d6',
    liquid: { label: '찬물(냉장 정수)', color: '#a8d8f0', emoji: '🧊' },
    additive: null,
    preStep: { title: '알로에겔 1차 진정', desc: '팩 전에 알로에겔을 도톰하게 올려 열을 먼저 내리고, 살살 걷어내 주세요.' },
    ratioText: '가루 1 : 찬물 0.8',
    reason: '겔로 열을 먼저 내리고, 차가운 물로 믹싱한 팩이 마무리해요.',
    warn: '⚠️ 열이 올라 약해진 피부에 멘톨·쿨링 성분은 비추! 온도로만 시원하게.',
    care: ['🫧 세안 — 미온수로 깨끗하게', '💦 토너 — 결 정돈', '🌿 알로에겔 1차 진정 → 살살 걷어내기', '🥣 모델링팩 — 찬물로만 믹싱', '🤲 마무리 — 남은 에센스 두드려 흡수'],
  },
  R2: {
    name: '수분 폭탄 레시피',
    sub: '속당김 비상사태 해제',
    emoji: '💧',
    color: '#6fa8dc',
    liquid: { label: '물 절반', color: '#bfe3f5', emoji: '💧' },
    additive: { label: '수분앰플(또는 수딩젤)', color: '#ffd1e0', emoji: '🩷' },
    preStep: null,
    ratioText: '가루 1 : 물 0.5 : 수분앰플 0.5',
    reason: '수분앰플 듬뿍 바르고, 팩에도 수분을 섞어요. 수분 폭탄 넣고 모델링팩으로 덮기!',
    warn: null,
    care: ['🫧 세안 — 미온수로 깨끗하게', '💦 토너 — 결 정돈', '💧 수분앰플 듬뿍 선도포 ★핵심', '🥣 모델링팩 — 물 0.5 + 앰플 0.5 믹싱', '🤲 마무리 — 남은 에센스 두드려 흡수'],
  },
  R3: {
    name: '극진정 레시피',
    sub: '오늘은 아무것도 자극하지 않기',
    emoji: '🌿',
    color: '#8fbc8f',
    liquid: { label: '상온수', color: '#d8eede', emoji: '🌿' },
    additive: null,
    preStep: null,
    ratioText: '가루 1 : 상온수 0.8',
    reason: '수분 진정 앰플 바르고, 팩은 그대로 기본 믹싱. 찬물도 첨가물도 오늘은 쉬어요 — 자극 요소를 하나라도 줄이는 게 우선이니까.',
    warn: '⚠️ 뒤집어진 날엔 새 성분 추가 금지. 온도 자극(찬물)도 피해요.',
    care: ['🫧 세안 — 미온수로 순하게', '💦 토너 — 결 정돈', '🌿 수분 진정 앰플 선도포 ★핵심', '🥣 모델링팩 — 상온수로 기본 믹싱', '🤲 마무리 — 문지르지 말고 두드려 흡수'],
  },
  R4: {
    name: '산뜻 클린 레시피',
    sub: '군더더기 없는 기본기',
    emoji: '🫧',
    color: '#c9a86b',
    liquid: { label: '정수', color: '#cfe8f0', emoji: '💧' },
    additive: null,
    preStep: null,
    ratioText: '가루 1 : 물 0.8',
    reason: '흡착력은 팩이 알아서 해요. 황금비만 지키면 끝 — 기본 배합이 가장 산뜻해요.',
    warn: null,
    care: ['🫧 세안 — 미온수로 깨끗하게', '💦 토너 — 결 정돈', '💧 가벼운 앰플 선도포', '🥣 모델링팩 — 황금비 기본 믹싱', '🤲 마무리 — 가볍게 보습'],
  },
};

const PACK_MINUTES = 15; // 팩 유지 시간 (확정)
const LINKS = {
  store: 'https://www.instagram.com/yegam_song', // TODO: 8/3 공구 링크로 교체
  follow: 'https://www.instagram.com/yegam_song',
};
