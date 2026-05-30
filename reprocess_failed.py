import os
import json
import whisper
import imageio_ffmpeg

# ffmpeg 경로 설정
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = os.path.dirname(ffmpeg_bin) + ":" + os.environ.get("PATH", "")

REELS_DIR = os.path.expanduser("~/Desktop/yegam/합버전/reels")
OUTPUT_JSON = os.path.expanduser("~/Desktop/yegam/reels_data.json")

with open(OUTPUT_JSON, encoding="utf-8") as f:
    data = json.load(f)

failed = [r for r in data["reels"] if r["source"] == "whisper" and "[오류" in r["transcript"]]
print(f"재처리 대상: {len(failed)}개\n")

print("Whisper 모델(small) 로딩 중...")
model = whisper.load_model("small")
print("모델 로드 완료.\n")

success = 0
error = 0
for i, reel in enumerate(failed, 1):
    mp4_path = os.path.join(REELS_DIR, reel["date"], reel["filename"])
    print(f"[{i}/{len(failed)}] [{reel['date']}] {reel['filename']}")
    try:
        result = model.transcribe(mp4_path, language="ko")
        transcript = result["text"].strip()
        reel["transcript"] = transcript
        success += 1
    except Exception as e:
        reel["transcript"] = f"[오류: {e}]"
        print(f"  → 실패: {e}")
        error += 1

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n완료!")
print(f"  성공: {success}개")
print(f"  실패: {error}개")
print(f"  저장 위치: {OUTPUT_JSON}")
