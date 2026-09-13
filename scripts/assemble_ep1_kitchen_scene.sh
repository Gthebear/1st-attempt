#!/bin/bash
# Assembles the Episode 1 kitchen-scene clips (in story order) into one cut, muxes the
# ambience bed on top. Setup only — written tonight, not run, because the input clips
# (shots 2.2-2.7, 5.1-5.4) don't exist yet; only the original proven shot (00010) does.
#
# Usage once clips exist: fill in the SHOTS array below in story order (the filenames
# ffmpeg/ComfyUI actually wrote to output/video/), then run this script.
set -euo pipefail

OUT_DIR="/home/chris/ComfyUI-ltx25/output/video"
AMBIENCE="/home/chris/ComfyUI-ltx25/output/audio/ep1_kitchen_ambience_00001_.flac"
FINAL="$OUT_DIR/ep1_cold_open_kitchen_v1.mp4"

# Story order — replace placeholders with the real output filenames once each shot is
# rendered. hunyuan_video_1.5_00010_.mp4 (shot 2.1, wide/front-on) is the only one that
# exists tonight; everything else is TBD.
SHOTS=(
  "hunyuan_video_1.5_00010_.mp4"   # 2.1 — proven, exists
  # "hunyuan_video_1.5_SHOT22.mp4"  # 2.2 — notices inhaler
  # "hunyuan_video_1.5_SHOT27.mp4"  # 2.7 — watches James leave
  # "hunyuan_video_1.5_SHOT51.mp4"  # 5.1 — alone, wiping counter
  # "hunyuan_video_1.5_SHOT52.mp4"  # 5.2 — reaction, head tilt
  # "hunyuan_video_1.5_SHOT53.mp4"  # 5.3 — turns, marker shifts
  # "hunyuan_video_1.5_SHOT54.mp4"  # 5.4 — hold on face
)

echo "Checking all listed clips exist before touching anything..."
for shot in "${SHOTS[@]}"; do
  if [ ! -f "$OUT_DIR/$shot" ]; then
    echo "MISSING: $OUT_DIR/$shot — stopping, nothing written." >&2
    exit 1
  fi
done

LIST_FILE=$(mktemp)
trap 'rm -f "$LIST_FILE"' EXIT
for shot in "${SHOTS[@]}"; do
  echo "file '$OUT_DIR/$shot'" >> "$LIST_FILE"
done

# Re-encode on concat (safer than stream copy if resolution/params ever drift between
# clips — matches the approach STATUS.md's Step 3 called for).
SILENT="$OUT_DIR/ep1_cold_open_kitchen_v1_silent.mp4"
ffmpeg -y -f concat -safe 0 -i "$LIST_FILE" -c:v libx264 -pix_fmt yuv420p -crf 18 "$SILENT"

if [ -f "$AMBIENCE" ]; then
  ffmpeg -y -i "$SILENT" -i "$AMBIENCE" -c:v copy -c:a aac -shortest "$FINAL"
  rm -f "$SILENT"
  echo "Done, with ambience: $FINAL"
else
  mv "$SILENT" "$FINAL"
  echo "Done, SILENT (no ambience file found at $AMBIENCE — generate stable_audio3_ep1_kitchen_ambience.json first): $FINAL"
fi

ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$FINAL"
