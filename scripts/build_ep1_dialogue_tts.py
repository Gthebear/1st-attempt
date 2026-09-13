"""
Builds FL_ChatterboxDialogTTS workflow files for Episode 1 Cold Open's two dialogue exchanges,
from the ChatterBox node pack's own example workflow (custom_nodes/ComfyUI_Fill-ChatterBox/
workflows/Chatterbox.json) — using it as the safe base means the graph wiring is already
correct (shipped by the node's author), only widget values change.

Cannot be run end-to-end tonight: speaker_A_Audio/speaker_B_Audio are REQUIRED inputs (voice
reference clips), and no character voice samples exist yet for this show (see
PRODUCTION_BIBLE.md §5). This writes the dialogue text + wiring so only the two audio files
need dropping in once voices are cast/recorded — LoadAudio filenames are clearly-named
placeholders that don't exist yet, matching them in will make each workflow runnable.

Setup only: writes workflow JSON files, does not queue or execute anything.
"""
import json
from pathlib import Path

SRC = Path("/home/chris/ComfyUI-ltx25/custom_nodes/ComfyUI_Fill-ChatterBox/workflows/Chatterbox.json")
OUT_DIR = Path("/home/chris/ComfyUI-ltx25/workflows")

KEEP = {12, 20, 23, 24}  # LoadAudio(A), LoadAudio(B), FL_ChatterboxDialogTTS, PreviewAudio

EXCHANGES = {
    "kitchen_james_iris": {
        "speaker_a": ("Iris", "VOICE_IRIS_ref.wav"),
        "speaker_b": ("James", "VOICE_JAMES_ref.wav"),
        "lines": [
            ("B", "Sierra still awake?"),
            ("A", "Reading. I told her lights out in ten."),
            ("B", "She'll say twenty."),
            ("A", "I said ten."),
        ],
    },
    "hallway_sierra_iris": {
        "speaker_a": ("Iris", "VOICE_IRIS_ref.wav"),
        "speaker_b": ("Sierra", "VOICE_SIERRA_ref.wav"),
        "lines": [
            ("A", "Ten minutes was generous."),
            ("B", "It's educational."),
            ("A", "It's a racing game."),
            ("B", "Educational racing game."),
            ("B", "Do you sleep?"),
            ("A", "No."),
            ("B", "Ever get bored?"),
            ("A", "Not yet."),
        ],
    },
}

with open(SRC) as f:
    template = json.load(f)

def build(name, config):
    d = json.loads(json.dumps(template))
    d["nodes"] = [n for n in d["nodes"] if n["id"] in KEEP]
    d["links"] = [l for l in d["links"] if l[1] in KEEP and l[3] in KEEP]

    dialog_text = "\n".join(f"SPEAKER {spk}: {line}" for spk, line in config["lines"])

    for n in d["nodes"]:
        if n["id"] == 12:  # LoadAudio -> speaker A
            n["widgets_values"] = [config["speaker_a"][1], None, None]
        if n["id"] == 20:  # LoadAudio -> speaker B
            n["widgets_values"] = [config["speaker_b"][1], None, None]
        if n["id"] == 23:  # FL_ChatterboxDialogTTS
            n["widgets_values"] = [dialog_text, 0.5, 0.5, 0.8, 0, "randomize", False, False]

    out_path = OUT_DIR / f"chatterbox_dialog_ep1_{name}.json"
    with open(out_path, "w") as f:
        json.dump(d, f, indent=2)
    print(f"{name}: SPEAKER A = {config['speaker_a'][0]} ({config['speaker_a'][1]}, "
          f"missing), SPEAKER B = {config['speaker_b'][0]} ({config['speaker_b'][1]}, missing) "
          f"-> {out_path}")

for name, config in EXCHANGES.items():
    build(name, config)
