"""
Builds a Stable Audio 3 (Small-SFX) ambience-bed workflow for Episode 1's kitchen scenes —
"soft rain, distant city hum, occasional kitchen clink" per the original brief.

Base: the flat, simple audio_stable_audio_example.json template bundled with ComfyUI (no Qwen
reprompt subgraph, avoids needing the extra qwen3.5_2b_bf16.safetensors text encoder), with the
checkpoint/CLIP swapped to Stable Audio 3 Small-SFX — smaller, ≤8GB VRAM, purpose-built for SFX/
short ambiance (vs. the general-purpose 1.0 model the template shipped with).

Model files verified present and structurally intact tonight:
  ~/ComfyUI/models/checkpoints/stable_audio_3_small_sfx.safetensors (2.3GB)
  ~/ComfyUI/models/text_encoders/t5gemma_b_b_ul2.safetensors (1.2GB)

Setup only: writes a workflow JSON file, does not queue or execute anything. Duration is set to
60s as a placeholder — adjust EmptyLatentAudio's seconds value once the final kitchen-scene cut
length is known (concatenate the picture edit first, then match this to it, or loop/trim the
60s bed in ffmpeg).
"""
import json
from pathlib import Path

SRC = Path("/home/chris/ComfyUI-ltx25/venv/lib/python3.14/site-packages/"
           "comfyui_workflow_templates_json/templates/audio_stable_audio_example.json")
OUT = Path("/home/chris/ComfyUI-ltx25/workflows/stable_audio3_ep1_kitchen_ambience.json")

PROMPT = ("Soft steady rain against a window, distant low city hum and occasional faint neon "
          "hum, warm quiet domestic kitchen ambience, occasional soft ceramic plate or cutlery "
          "clink, no music, no voices, continuous atmospheric bed.")

with open(SRC) as f:
    d = json.load(f)

for n in d["nodes"]:
    if n["id"] == 4:  # CheckpointLoaderSimple
        n["widgets_values"] = ["stable_audio_3_small_sfx.safetensors"]
    if n["id"] == 10:  # CLIPLoader
        n["widgets_values"] = ["t5gemma_b_b_ul2.safetensors", "stable_audio", "default"]
    if n["id"] == 6:  # CLIPTextEncode positive
        n["widgets_values"] = [PROMPT]
    if n["id"] == 11:  # EmptyLatentAudio [seconds, batch_size]
        n["widgets_values"] = [60.0, 1]
    if n["id"] == 20:  # SaveAudioAdvanced
        n["widgets_values"] = ["audio/ep1_kitchen_ambience", "flac"]

with open(OUT, "w") as f:
    json.dump(d, f, indent=2)

print(f"-> {OUT}")
