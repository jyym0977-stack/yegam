const express = require('express');
const path = require('path');
const os = require('os');
const fs = require('fs');
const http = require('http');
const { WebSocketServer } = require('ws');

const app = express();
const PORT = 3000;

const BILL_PATH = path.join(os.homedir(), 'Desktop', 'BILL.xlsx');

app.use(express.static(__dirname));

app.get('/api/status', (req, res) => {
  res.json({ ok: true, billExists: fs.existsSync(BILL_PATH), billPath: BILL_PATH });
});

app.get('/api/bill', (req, res) => {
  if (!fs.existsSync(BILL_PATH)) {
    return res.status(404).json({ error: `BILL.xlsx 파일을 찾을 수 없습니다.\n경로: ${BILL_PATH}` });
  }
  res.sendFile(BILL_PATH);
});

// HTTP 서버 + WebSocket 서버 생성
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

function broadcast(msg) {
  wss.clients.forEach(client => {
    if (client.readyState === 1) client.send(JSON.stringify(msg));
  });
}

// BILL.xlsx 변경 감지 → 브라우저에 자동 알림
let debounceTimer = null;
function watchFile() {
  if (!fs.existsSync(BILL_PATH)) {
    setTimeout(watchFile, 3000); // 파일 없으면 3초 후 재시도
    return;
  }
  fs.watch(BILL_PATH, (event) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      console.log(`[${new Date().toLocaleTimeString()}] BILL.xlsx 변경 감지 → 브라우저 자동 새로고침`);
      broadcast({ type: 'reload' });
    }, 800); // 저장 완료 후 0.8초 대기 (Excel 저장 시 임시파일 생성 방지)
  });
  console.log(`   파일 감지 중: ${BILL_PATH}`);
}

server.listen(PORT, '127.0.0.1', () => {
  console.log(`\n✅ OceanView Invoice 서버 시작됨`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   엑셀 경로: ${BILL_PATH}`);
  console.log(`\n   종료하려면 이 창을 닫으세요.\n`);
  watchFile();
});
