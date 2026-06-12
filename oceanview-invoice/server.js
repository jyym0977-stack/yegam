const express = require('express');
const path = require('path');
const os = require('os');
const fs = require('fs');

const app = express();
const PORT = 3000;

// 바탕화면의 BILL.xlsx 경로
const BILL_PATH = path.join(os.homedir(), 'Desktop', 'BILL.xlsx');

// 정적 파일 (HTML, 이미지 등) 서빙
app.use(express.static(__dirname));

// 서버 상태 확인
app.get('/api/status', (req, res) => {
  const exists = fs.existsSync(BILL_PATH);
  res.json({
    ok: true,
    billExists: exists,
    billPath: BILL_PATH
  });
});

// BILL.xlsx 파일 전송
app.get('/api/bill', (req, res) => {
  if (!fs.existsSync(BILL_PATH)) {
    return res.status(404).json({
      error: `BILL.xlsx 파일을 찾을 수 없습니다.\n경로: ${BILL_PATH}`
    });
  }
  res.sendFile(BILL_PATH);
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`\n✅ OceanView Invoice 서버 시작됨`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   엑셀 경로: ${BILL_PATH}`);
  console.log(`\n   종료하려면 이 창을 닫으세요.\n`);
});
