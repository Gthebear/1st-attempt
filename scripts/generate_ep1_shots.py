#!/usr/bin/env python3
"""
Generates Episode 1 Cold Open shots end-to-end: Qwen Image Edit (locked still) ->
HunyuanVideo 1.5 i2v (motion clip), using the exact proven flattened API prompts from
2026-09-12's successful run (extracted from logs_qwen_shot1.jsonl) and the proven Hunyuan
template converted via graph_to_api.py. Only leaf values are patched (image, prompt, seed,
filename) - structure is untouched.

Usage: python3 generate_ep1_shots.py [shot_id ...]   (default: all SHOTS)
"""
import json
import sys
import time
import shutil
import urllib.request
from pathlib import Path

SERVER = "http://127.0.0.1:8189"
INPUT_DIR = Path("/home/chris/ComfyUI-ltx25/input")
OUTPUT_DIR = Path("/home/chris/ComfyUI-ltx25/output")
QWEN_BASE = Path("/tmp/proven_qwen_edit_api_base.json")
HUNYUAN_BASE = Path("/tmp/hunyuan_base_api.json")

STYLE = ("Clean cel-shaded 2D anime, crisp black vector lineart, hard-edge shadows, "
         "2-tone cel shading, flat vibrant base colors with sharp rim lighting, "
         "detailed mechanical panel lines, no airbrushing, no painterly fuzziness.")
IRIS_LOCK = ("Keep her exact same face, hairstyle, and identity as the reference photo, "
             "do not alter her facial features. Keep the same warm suburban kitchen at night, "
             "rain-streaked window, neon cyberpunk city skyline outside, same wardrobe.")
STREET_LOCK = ("Keep the exact same street layout, houses, monorail line on stilts, distant "
                "neon skyline, and rain as the reference photo - do not redesign the "
                "environment, only change camera framing/motion as described.")

# shot_id -> (still_ref_image, still_prompt, still_seed, motion_prompt, frames)
SHOTS = {
    "2.2": ("locked_iris_kitchen_chris.png",
        f"{IRIS_LOCK} She sets a plate down on the counter, notices a child's inhaler left "
        f"out, and is moving it toward a drawer - a small, practiced, unhurried act of care. {STYLE}",
        910002222,
        "A young woman android caregiver in a warm suburban kitchen at night sets a plate "
        "down on the counter, notices a child's inhaler left out, and moves it toward a "
        "drawer with a small, practiced, unhurried motion. Calm expression, green forehead "
        "marker steady, natural subtle movement. Clean cel-shaded anime style, alive and "
        "dynamic rather than static.", 81),
    "2.7": ("locked_iris_kitchen_chris.png",
        f"{IRIS_LOCK} Close-up on her face, calm and thoughtful, watching something offscreen "
        f"to the side (James leaving the room), green forehead marker steady, unchanged. {STYLE}",
        910002777,
        "Close-up on a young woman android caregiver's face in a warm kitchen at night, calm "
        "and thoughtful expression, eyes tracking something offscreen to the side, slow "
        "natural blink, green forehead marker glowing steady. Clean cel-shaded anime style, "
        "subtle alive movement.", 81),
    "5.1": ("locked_iris_kitchen_chris.png",
        f"{IRIS_LOCK} It is later at night, the house is quiet. She is alone, wiping the "
        f"counter with a cloth, no plate or dishes this time, rain against the window, green "
        f"marker steady, calm routine expression. {STYLE}",
        910005111,
        "A young woman android caregiver alone in a quiet suburban kitchen late at night, "
        "wiping the counter with a cloth in slow calm circular motions, rain against the "
        "window behind her, green forehead marker glowing steady, calm routine expression. "
        "Clean cel-shaded anime style.", 81),
    "5.2": ("locked_iris_kitchen_chris.png",
        f"{IRIS_LOCK} She has paused mid-motion, head tilted a few degrees as if listening to "
        f"something outside, alert but still calm, green marker still steady, cloth still in "
        f"hand. {STYLE}",
        910005222,
        "A young woman android caregiver in a kitchen at night pauses mid-motion, head "
        "tilting a few degrees as if listening to something outside, subtle alert but calm "
        "expression, green forehead marker steady, cloth still in hand. Clean cel-shaded "
        "anime style, subtle natural movement.", 81),
    "5.3": ("locked_iris_kitchen_chris.png",
        "Keep her exact same face, hairstyle, and identity as the reference photo, do not "
        "alter her facial features. Keep the same warm suburban kitchen at night, "
        "rain-streaked window, neon cyberpunk city skyline outside, same wardrobe. She has "
        "turned fully to face the window, tense and alert, and the light on her forehead "
        "marker is now red instead of green - a clear color change indicating an alert "
        f"state, everything else about her appearance unchanged. {STYLE}",
        910005333,
        "A young woman android caregiver in a kitchen at night turns fully to face the "
        "window, tense and alert posture, the light on her forehead marker glowing red "
        "instead of green, rain against the glass behind her. Clean cel-shaded anime style, "
        "deliberate tense movement.", 81),
    "5.4": ("locked_iris_kitchen_chris.png",
        "Keep her exact same face, hairstyle, and identity as the reference photo, do not "
        "alter her facial features. Extreme close-up, hold on her face, red forehead marker "
        "glowing, tense and watchful expression, unmoving, rain-streaked window softly out "
        f"of focus behind her. {STYLE}",
        910005444,
        "Extreme close-up, hold on a young woman android caregiver's face at night, red "
        "forehead marker glowing steady, tense watchful expression, almost unmoving, only "
        "the faintest natural breathing motion, rain-streaked window softly out of focus "
        "behind her. Clean cel-shaded anime style.", 81),
    "1.1": ("smith_street_view.png",
        f"{STREET_LOCK} Wide, completely static establishing shot of the street at night, "
        f"rain ticking on car roofs, quiet and calm. {STYLE}",
        910001111,
        "Wide static shot of a quiet suburban street at night in the rain, a monorail line "
        "passing silently on stilts in the background, distant neon city skyline glowing "
        "beyond the rooftops, rain ticking on car roofs, calm and still. Clean cel-shaded "
        "anime style, minimal subtle motion only in the rain and distant lights.", 81),
    "1.3": ("smith_residence_exterior.png",
        "Keep the exact same house design, solar roof, and neighborhood as the reference "
        "photo - do not redesign it. Slow push-in framing toward the house, its windows "
        "glowing warm gold against the wet dark night, rain falling, neighboring houses "
        f"cooler and dimmer by contrast. {STYLE}",
        910001333,
        "Slow push-in toward a suburban house at night, its windows glowing warm gold "
        "against the wet dark, rain falling steadily, neighboring houses cooler and dimmer "
        "by contrast, solar roof panels reflecting faint light. Clean cel-shaded anime "
        "style, slow deliberate camera push, subtle rain motion.", 81),
}


def api(path, data=None):
    url = SERVER + path
    if data is not None:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST",
                                      headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        if not body:
            return {}
        return json.loads(body)


def queue_and_wait(prompt, label, timeout=600):
    result = api("/prompt", {"prompt": prompt})
    if "prompt_id" not in result:
        raise RuntimeError(f"{label}: queue failed: {result}")
    pid = result["prompt_id"]
    print(f"[{label}] queued as {pid}")
    start = time.time()
    while time.time() - start < timeout:
        hist = api(f"/history/{pid}")
        if pid in hist:
            entry = hist[pid]
            status = entry.get("status", {})
            if status.get("completed") is True:
                print(f"[{label}] completed in {time.time()-start:.1f}s")
                return entry
            if status.get("status_str") == "error":
                raise RuntimeError(f"{label}: execution error: {status}")
        time.sleep(3)
    raise TimeoutError(f"{label}: timed out after {timeout}s waiting on {pid}")


def find_output_image(entry):
    for node_out in entry.get("outputs", {}).values():
        for img in node_out.get("images", []):
            return img["filename"], img.get("subfolder", ""), img.get("type", "output")
    raise RuntimeError("no image output found")


def find_output_video(entry):
    # SaveVideo reports its output under "images" too (with an "animated" marker),
    # not a separate "videos"/"gifs" key - confirmed via a live /history response.
    for node_out in entry.get("outputs", {}).values():
        for key in ("images", "videos", "gifs"):
            for v in node_out.get(key, []):
                return v["filename"], v.get("subfolder", ""), v.get("type", "output")
    raise RuntimeError("no video output found")


def generate_shot(shot_id):
    ref_image, still_prompt, still_seed, motion_prompt, frames = SHOTS[shot_id]
    safe_id = shot_id.replace(".", "")

    # --- Stage 1: Qwen Image Edit ---
    qwen_prompt = json.loads(QWEN_BASE.read_text())
    qwen_prompt["78"]["inputs"]["image"] = ref_image
    qwen_prompt["433:111"]["inputs"]["prompt"] = still_prompt
    qwen_prompt["433:3"]["inputs"]["seed"] = still_seed
    qwen_prompt["469"]["inputs"]["filename_prefix"] = f"Qwen_ep1_shot{safe_id}"

    entry = queue_and_wait(qwen_prompt, f"shot{shot_id} qwen-edit")
    still_name, still_sub, still_type = find_output_image(entry)
    print(f"[shot{shot_id}] still -> {still_name}")

    api("/free", {"unload_models": True, "free_memory": True})

    # Copy the generated still into input/ so Hunyuan can load it
    src = OUTPUT_DIR / still_sub / still_name if still_sub else OUTPUT_DIR / still_name
    dst_name = f"locked_ep1_shot{safe_id}.png"
    shutil.copy(src, INPUT_DIR / dst_name)

    # --- Stage 2: HunyuanVideo 1.5 i2v ---
    hy_prompt = json.loads(HUNYUAN_BASE.read_text())
    hy_prompt["80"]["inputs"]["image"] = dst_name
    hy_prompt["44"]["inputs"]["text"] = motion_prompt
    hy_prompt["78"]["inputs"]["length"] = frames
    hy_prompt["127"]["inputs"]["noise_seed"] = still_seed + 1
    hy_prompt["102"]["inputs"]["filename_prefix"] = f"video/ep1_shot{safe_id}"

    entry = queue_and_wait(hy_prompt, f"shot{shot_id} hunyuan-i2v", timeout=600)
    video_name, video_sub, video_type = find_output_video(entry)
    print(f"[shot{shot_id}] video -> {video_sub}/{video_name}")

    api("/free", {"unload_models": True, "free_memory": True})
    return {"shot": shot_id, "still": still_name, "video": f"{video_sub}/{video_name}"}


if __name__ == "__main__":
    targets = sys.argv[1:] or list(SHOTS.keys())
    results = []
    for shot_id in targets:
        try:
            results.append(generate_shot(shot_id))
        except Exception as e:
            print(f"[shot{shot_id}] FAILED: {e}")
            results.append({"shot": shot_id, "error": str(e)})
    print("\n=== SUMMARY ===")
    for r in results:
        print(json.dumps(r))
