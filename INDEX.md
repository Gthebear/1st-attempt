# Tonight's session — 2026-09-13, setup only, no generation run

Start here. Everything below lives under `~/ComfyUI-ltx25/` unless noted; everything is also
backed up to `github.com/Gthebear/1st-attempt` (private repo, was empty before tonight).

1. **`docs/script_episode1_cold_open.md`** — the actual Episode 1 script (only copy that
   exists anywhere; wasn't on disk, GitHub, Drive, or Notion before Chris pasted it tonight).
2. **`docs/SHOT_LIST_ep1_cold_open.md`** — shot-by-shot breakdown against the real asset set,
   including two continuity issues found by actually viewing the reference images (house
   labeled "McNeil" not "Smith"; marker color script says amber, design sheet says red) and
   what's built vs. blocked.
3. **`docs/PRODUCTION_BIBLE.md`** — style spec, character/asset roster, the proven Qwen Edit +
   Hunyuan i2v pipeline with real prompts pulled from working files, ControlNet setup, audio/TTS
   setup, ambience/SFX setup, model integrity results, open gaps.
4. **`workflows/qwen_edit_ep1_shot*.json`** (8 files) — ready-to-queue Qwen Edit stills for the
   kitchen and street shots that have adequate reference material. Not run tonight.
5. **`workflows/chatterbox_dialog_ep1_*.json`** (2 files) — dialogue audio for the two real
   exchanges in the script. Cannot run until voice reference clips exist (required inputs).
6. **`workflows/stable_audio3_ep1_kitchen_ambience.json`** — rain/city-hum ambience bed.
7. **`benchmarks/2026-09-13/`** — the generator scripts behind items 4-6, plus
   `assemble_ep1_kitchen_scene.sh` (ffmpeg concat+mux, logic-tested tonight with the one real
   existing clip, not yet usable for the full cut since only one shot exists).

## What's still blocking real generation
- Scenes 3 & 4 (upstairs hallway, Jacob's room) have no location reference at all.
- Shots 2.4-2.6 (Iris + James together) need one new `LoadImage` node wired to the
  already-confirmed `image2` port — not done, flagged as the first thing to test by hand.
- Dialogue audio needs 3 voice reference clips (Iris, James, Sierra) — none exist.
- Script says amber marker, design sheet only has green/red — needs Chris's call.
- House exterior asset says "McNeil" not "Smith" — needs Chris's call.

## What's actually ready to generate first, once you're back
Scene 2 kitchen shots (2.2, 2.7) and Scene 5 kitchen shots (5.1-5.4) — proven environment,
proven identity lock, workflows already built. That's the safest starting point.
