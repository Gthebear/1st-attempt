"""
Builds Qwen Image Edit workflow files for Episode 1 Cold Open shots that have adequate
reference material (see docs/SHOT_LIST_ep1_cold_open.md for the full audit — Scenes 3/4,
upstairs hallway and Jacob's room, are blocked: no location reference exists for either).

Base: ~/ComfyUI/workflows/qwen_edit_2509.json, the proven production template (same one
STATUS.md from 2026-09-12 describes copying fresh for every prior shot).

Setup only: writes workflow JSON files, does not queue or execute anything.
"""
import json
from pathlib import Path

SRC = Path("/home/chris/ComfyUI/workflows/qwen_edit_2509.json")
OUT_DIR = Path("/home/chris/ComfyUI-ltx25/workflows")

STYLE = ("Clean cel-shaded 2D anime, crisp black vector lineart, hard-edge shadows, "
         "2-tone cel shading, flat vibrant base colors with sharp rim lighting, "
         "detailed mechanical panel lines, no airbrushing, no painterly fuzziness.")

IRIS_LOCK = ("Keep her exact same face, hairstyle, and identity as the reference photo, "
             "do not alter her facial features. Keep the same warm suburban kitchen at night, "
             "rain-streaked window, neon cyberpunk city skyline outside, same wardrobe.")

STREET_LOCK = ("Keep the exact same street layout, houses, monorail line on stilts, distant "
                "neon skyline, and rain as the reference photo — do not redesign the "
                "environment, only change camera framing/motion as described.")

# (shot_id, slug, reference_image, prompt_body, note)
SHOTS = [
    ("2.2", "notices_inhaler", "locked_iris_kitchen_chris.png",
     f"{IRIS_LOCK} She sets a plate down on the counter, notices a child's inhaler left out, "
     "and is moving it toward a drawer — a small, practiced, unhurried act of care. "
     f"{STYLE}"),
    ("2.7", "watches_james_leave", "locked_iris_kitchen_chris.png",
     f"{IRIS_LOCK} Close-up on her face, calm and thoughtful, watching something offscreen "
     f"to the side (James leaving the room), green forehead marker steady, unchanged. {STYLE}"),
    ("5.1", "alone_wiping_counter", "locked_iris_kitchen_chris.png",
     f"{IRIS_LOCK} It is later at night, the house is quiet. She is alone, wiping the counter "
     f"with a cloth, no plate or dishes this time, rain against the window, green marker "
     f"steady, calm routine expression. {STYLE}"),
    ("5.2", "reaction_head_tilt", "locked_iris_kitchen_chris.png",
     f"{IRIS_LOCK} She has paused mid-motion, head tilted a few degrees as if listening to "
     "something outside, alert but still calm, green marker still steady, cloth still in "
     f"hand. {STYLE}"),
    # NOTE (kept out of the prompt string on purpose — Qwen renders text well and would draw
    # it into the image): script says the marker turns amber; the character design sheet
    # (andr_mechanical_detail.png) only defines green/red states. This prompt uses red to
    # match the design bible. Confirm with Chris before use — see SHOT_LIST_ep1_cold_open.md.
    ("5.3", "turns_marker_shifts", "locked_iris_kitchen_chris.png",
     "Keep her exact same face, hairstyle, and identity as the reference photo, do not alter "
     "her facial features. Keep the same warm suburban kitchen at night, rain-streaked window, "
     "neon cyberpunk city skyline outside, same wardrobe. She has turned fully to face the "
     "window, tense and alert, and the light on her forehead marker is now red instead of "
     "green — a clear color change indicating an alert state, everything else about her "
     f"appearance unchanged. {STYLE}"),
    ("5.4", "hold_on_face_red", "locked_iris_kitchen_chris.png",
     "Keep her exact same face, hairstyle, and identity as the reference photo, do not alter "
     "her facial features. Extreme close-up, hold on her face, red forehead marker glowing, "
     "tense and watchful expression, unmoving, rain-streaked window softly out of focus "
     f"behind her. {STYLE}"),
    ("1.1", "street_establishing", "smith_street_view.png",
     f"{STREET_LOCK} Wide, completely static establishing shot of the street at night, rain "
     f"ticking on car roofs, quiet and calm. {STYLE}"),
    # NOTE (kept out of the prompt on purpose): this reference image's in-scene label reads
    # "THE McNEIL HOME," not "SMITH HOUSE" as the script names the family. No in-frame text/
    # signage is requested in this prompt so it shouldn't surface, but flag it before using
    # this asset anywhere text might render — see SHOT_LIST_ep1_cold_open.md.
    ("1.3", "push_to_house", "smith_residence_exterior.png",
     "Keep the exact same house design, solar roof, and neighborhood as the reference photo — "
     "do not redesign it. Slow push-in framing toward the house, its windows glowing warm gold "
     "against the wet dark night, rain falling, neighboring houses cooler and dimmer by "
     f"contrast. {STYLE}"),
]

with open(SRC) as f:
    template = json.load(f)

def build(shot_id, slug, ref_image, prompt, seed):
    d = json.loads(json.dumps(template))  # deep copy
    for n in d["nodes"]:
        if n["id"] == 78:  # LoadImage
            n["widgets_values"] = [ref_image, "image"]
    sg = d["definitions"]["subgraphs"][0]
    for n in sg["nodes"]:
        if n["id"] == 111:  # positive TextEncodeQwenImageEditPlus
            n["widgets_values"] = [prompt]
        if n["id"] == 3:  # KSampler
            n["widgets_values"] = [seed, "randomize", 4, 1, "euler", "simple", 1]
    safe_id = shot_id.replace(".", "")
    out_path = OUT_DIR / f"qwen_edit_ep1_shot{safe_id}_{slug}.json"
    with open(out_path, "w") as f:
        json.dump(d, f, indent=2)
    print(f"shot {shot_id} ({slug}) -> {out_path}")

for i, (shot_id, slug, ref_image, prompt) in enumerate(SHOTS):
    build(shot_id, slug, ref_image, prompt, seed=910000000000 + i * 2222)
