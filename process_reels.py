import os
import re
import json
import whisper
import imageio_ffmpeg

# ffmpeg 경로 설정 (imageio_ffmpeg 번들)
os.environ["PATH"] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + ":" + os.environ.get("PATH", "")

REELS_DIR = os.path.expanduser("~/Desktop/yegam/합버전/reels")
OUTPUT_JSON = os.path.expanduser("~/Desktop/yegam/reels_data.json")


def parse_srt(srt_path):
    with open(srt_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # 번호, 타임코드 제거하고 텍스트만 추출
    blocks = re.split(r"\n\n+", content.strip())
    lines = []
    for block in blocks:
        parts = block.strip().split("\n")
        # 첫 줄(번호), 둘째 줄(타임코드) 제거
        text_lines = [l.strip() for l in parts[2:] if l.strip()]
        lines.extend(text_lines)
    return " ".join(lines)


def transcribe_mp4(mp4_path, model):
    result = model.transcribe(mp4_path, language="ko")
    return result["text"].strip()


def main():
    print("Whisper 모델(small) 로딩 중...")
    model = whisper.load_model("small")
    print("모델 로드 완료.\n")

    reels = []
    date_folders = sorted([
        d for d in os.listdir(REELS_DIR)
        if os.path.isdir(os.path.join(REELS_DIR, d)) and re.match(r"\d{6}", d)
    ])

    total_srt = 0
    total_whisper = 0

    for date in date_folders:
        folder = os.path.join(REELS_DIR, date)
        files = os.listdir(folder)
        mp4_files = [f for f in files if f.endswith(".mp4")]
        srt_files = [f for f in files if f.endswith(".srt")]

        # srt 파일 처리
        for srt_file in srt_files:
            srt_path = os.path.join(folder, srt_file)
            stem = os.path.splitext(srt_file)[0]
            print(f"[{date}] SRT 파싱: {srt_file}")
            transcript = parse_srt(srt_path)
            reels.append({
                "date": date,
                "filename": srt_file,
                "source": "srt",
                "transcript": transcript
            })
            total_srt += 1

        # srt 없는 mp4만 whisper 처리
        srt_stems = {os.path.splitext(s)[0] for s in srt_files}
        for mp4_file in mp4_files:
            stem = os.path.splitext(mp4_file)[0]
            if stem in srt_stems:
                continue  # 이미 srt로 처리됨
            mp4_path = os.path.join(folder, mp4_file)
            print(f"[{date}] Whisper 변환: {mp4_file}")
            try:
                transcript = transcribe_mp4(mp4_path, model)
            except Exception as e:
                transcript = f"[오류: {e}]"
            reels.append({
                "date": date,
                "filename": mp4_file,
                "source": "whisper",
                "transcript": transcript
            })
            total_whisper += 1

    result = {"reels": reels}
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n완료!")
    print(f"  SRT 처리:     {total_srt}개")
    print(f"  Whisper 변환: {total_whisper}개")
    print(f"  총 처리:      {total_srt + total_whisper}개")
    print(f"  저장 위치:    {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
