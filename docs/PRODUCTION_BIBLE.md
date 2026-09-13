# Production Bible — Iris (anime TV show pipeline)

Working reference for generating this show in ComfyUI. Built 2026-09-13, setup-only session
(no video/image generation was run to produce this doc — all examples below are pulled from
prior nights' proven output already on disk).

## 0. What this project actually has right now

- **World/characters**: locked. 19 reference sheets, one validated hero shot + clip.
- **Script**: **missing.** No episode/dialogue document found on disk (Documents, OneDrive,
  Projects) or on GitHub (`Gthebear/1st-attempt` is empty). Everything below is built against
  the character bible only. Point Claude at the actual script text before doing scene-specific
  prompt work — right now there's nothing to adapt into shots beyond the kitchen scene already
  proven.
- **Voice**: TTS engines are installed and load cleanly (see §5), but there are **no character
  voice samples** for this show (Iris, Smith family, Breaker X, Vanguard-E) anywhere on disk.
  The `sarah_*` / `clara_*` / `nurse_*` audio files in `~/ComfyUI/input/` belong to a different
  (podcast/HeyGen) project — do not reuse them here.

## 1. Visual style spec (apply to every still)

**Clean Cel-Shaded Neo-Cyberpunk Anime** — fusion of modern 2D western prestige animation
(*Invincible*) and Japanese action anime (*Cyberpunk: Edgerunners*, *One-Punch Man*).

- **Inking**: bold, uniform, closed vector-style black outlines. No sketchy/pencil texture.
  Internal lines thin, used only for mechanical seams, panel gaps, facial features, fabric folds.
  Zero feathering; silhouette stays clean even at distance/high motion.
- **Shading**: hard 2-to-3-tone cel shading, clean break lines. No airbrush gradients, no
  diffused digital fades. Tight geometric specular highlights on metal/plastic/cyberware.
- **Palette**: dual-temperature grade — warm interior (tungsten, honey oak, warm beige) vs.
  high-saturation synthetic exterior (cyan, magenta, electric violet, neon teal). Emissives
  (forehead marker, visors, conduits) get tight edge-glow, not blown-out bloom.
- **Proportions**: semi-realistic grounded anatomy, stylized anime facial features. Silhouette
  differs by faction — domestic/Iris: slender, civilian drapery over discreet panel seams.
  Corporate enforcers (Vanguard-E): sleek, digitigrade, matte armor, razor contours. Industrial/
  underground (Breaker X): heavy hunched mass, exposed hydraulics, asymmetrical weathering.

**Keyword block to append to every prompt** (proven in the kitchen shot, reuse verbatim):
```
clean cel-shaded 2D anime, crisp black vector lineart, hard-edge shadows, 2-tone cel shading,
flat vibrant base colors with sharp rim lighting, detailed mechanical panel lines,
no airbrushing, no painterly fuzziness
```

## 2. Character & asset roster

All files live in `~/ComfyUI-ltx25/input/` (copied from `~/ComfyUI/input/`, the canonical set).

| Character | Reference sheets |
|---|---|
| **Iris** (android caregiver, protagonist) | `andr_turnaround.png` (identity/multi-angle), `andr_expression_matrix.png`, `andr_mechanical_detail.png`, `andr_env_light_street.png`, `andr_env_light_warehouse.png`, `andr_arsenal_external_weapon.png`, `andr_arsenal_trenchcoat_modular.png`, `andr_arsenal_transforming_hands.png` |
| **Smith family** | `smith_mother.png`, `smith_father.png`, `smith_daughter_items.png`, `smith_son_items.png`, `smith_kids_figures.png`, `smith_residence_exterior.png`, `smith_street_view.png`, `smith_transport_harbor.png` |
| **Antagonists** | `breaker_x_reference.png` — **Breaker-X**, "Black-market brute, Serial B-665": heavy bulky industrial mech, orange/rust weathering, reinforced actuator pistons, exposed wiring, no face (fully armored). `vanguard_e_reference.png` — **Vanguard-E**, "Enforcer-class, Serial V-01": sleek black armored humanoid, integrated forearm blade mechanism, glowing red visor, monomolecular edge blade, power core/thrusters. Both are full mech designs, not humans in armor — no face to identity-lock, the whole silhouette is the character. |
| **Locked hero shots** | `locked_iris_kitchen_chris.png` — validated end-to-end, produced `output/video/hunyuan_video_1.5_00010_.mp4` (3.375s, silent, clean identity lock, no OOM). Same file (MD5-identical) is named `locked_iris_kitchen_ep1_opening.png` in the frozen `~/ComfyUI/input/` store — same image, two names, not a duplicate/conflict. |

Chris's own likeness set (`locked_shot*_chris.png`, `chris_ref.jpg`) is a **separate** project
(warehouse/action sequence, see `benchmarks/2026-09-12/STATUS.md`) — don't mix into Iris shots.

## 3. Proven pipeline (validated over two nights, reuse as-is)

**Step A — Qwen Image Edit** (`qwen_image_edit_2509_fp8_e4m3fn.safetensors` +
`Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors` LoRA, 4 steps, CFG 1.0):
relights/reposes a locked reference image into the new shot's setting, keeping identity fixed.
~20-30s per image.

**Step B — HunyuanVideo 1.5 480p i2v** (`hunyuanvideo1.5_480p_i2v_step_distilled_fp8_scaled`,
8-step distilled sampler, EasyCache on): animates the locked still. 832×480, 81 frames = 3.375s
at the proven setting; up to ~120 frames (~5s) is untested but plausible — verify on a low-stakes
shot before relying on it. ~120-160s per clip on the RTX 5060 Ti. **No audio output** — this
model has no audio channel, hence the separate TTS setup in §5.

**Real proven prompt (kitchen scene, positive, Hunyuan i2v)**:
> A young woman android caregiver stands in a warm suburban kitchen at night, drying a plate.
> She glances up naturally toward the rain-streaked window with relaxed, natural blinking and
> subtle head movement, calm expression, the green light on her forehead marker staying steady,
> a neon cyberpunk city skyline glowing softly through the window behind her with light rain
> falling. Clean cel-shaded anime style, alive and dynamic rather than static, warm interior
> lighting against cool neon exterior light.

**Real proven prompt (Qwen Image Edit, identity-lock + anti-drift wording)**:
> Keep his face, hair and identity exactly the same as the reference photo, do not alter his
> facial features or hairstyle. A tactical operative wearing dark tactical gear (vest, gloves,
> dark cargo pants) lies on the ground amid broken glass and dust, pushing himself up on one
> arm, rain falling through broken skylights above, debris and dust in the air, dramatic
> cinematic action-movie lighting from above, dazed but determined expression, no helmet or
> headgear, keep his exact same short dark hair, not bald, not shaved head.

## 4. Prompt construction rules (learned the hard way — apply every time)

1. **Restate identity-lock every single time**, in both the Qwen Edit prompt *and* the Hunyuan
   motion prompt, not just one. "Operative" or a character name alone is not enough — the model
   drifts toward genre archetypes (e.g. bald/helmeted "tactical" look) unless you explicitly
   name the feature to preserve (hair color/length, marker color, specific wardrobe piece).
2. **Wardrobe reverts silently** to the reference photo's actual clothing if the new scene's
   wardrobe isn't restated explicitly in every prompt — "in tactical gear" alone isn't sticky.
3. Always close the prompt with the style keyword block from §1.
4. One locked still per shot, generated independently from the character reference sheet — do
   **not** chain Hunyuan output frames into the next shot's input. Drift compounds across a
   chain; independent generation from the same locked reference does not.
5. Frame count: default 81 (3.375s). Treat anything above that as untested per-shot.

## 5. Audio (installed tonight, 2026-09-13)

`ComfyUI_Fill-ChatterBox` and `ComfyUI-FishAudioS2` custom nodes were copied from the frozen
`~/ComfyUI` install into `~/ComfyUI-ltx25/custom_nodes/` and now load cleanly (confirmed via
`/object_info` after two dependency-fix restarts — missing `s3tokenizer` and `conformer`
packages installed, both resolved). Available node classes:

- `FL_ChatterboxTTS`, `FL_ChatterboxTurboTTS`, `FL_ChatterboxMultilingualTTS`,
  `FL_ChatterboxVC` (voice conversion), `FL_ChatterboxDialogTTS` (**multi-speaker dialogue —
  the one to use for scenes with more than one character talking**)
- `FishS2TTS`, `FishS2VoiceCloneTTS`, `FishS2MultiSpeakerTTS`, `FishS2MultiSpeakerSplitTTS`

Model weights already present (read via `extra_model_paths.yaml` → `comfyui_frozen`):
`~/ComfyUI/models/chatterbox/chatterbox/` (t3_cfg, s3gen, ve, tokenizer) and
`~/ComfyUI/models/fishaudioS2/` (s2-pro, s2-pro-fp8).

**Known risk, not yet execution-tested**: installing `comfyui_controlnet_aux` (§6) bumped
`protobuf` to 7.36.1, and pip flagged that `descript-audiotools` (a FishAudioS2 dependency)
wants `protobuf<3.20`. The server restarts clean and both node packs *import* successfully, but
this hasn't been exercised by an actual TTS run — if a FishAudio generation throws a protobuf
error, pin protobuf down or isolate FishAudioS2 into its own venv.

**Open gap**: no character voice references exist. Confirmed via `/object_info`:
`FL_ChatterboxDialogTTS`'s `speaker_A_Audio` and `speaker_B_Audio` are **required** inputs —
the node cannot run at all without at least two voice reference clips. Before any dialogue
audio can be produced, decide per character: synthetic base voice (pick from ChatterBox/
FishAudio's built-ins) vs. recorded/cloned reference (needs a clean ~10-20s sample per
character).

Two dialogue workflows are already built and waiting on those files:
`workflows/chatterbox_dialog_ep1_kitchen_james_iris.json` (Iris/James, 4 lines) and
`workflows/chatterbox_dialog_ep1_hallway_sierra_iris.json` (Iris/Sierra, 8 lines) — both built
from the ChatterBox node's own example workflow (safest possible base, ships from the author),
with placeholder filenames `VOICE_IRIS_ref.wav` / `VOICE_JAMES_ref.wav` /
`VOICE_SIERRA_ref.wav` that don't exist yet. Drop in real files under those names and both
workflows should run as-is. See `docs/SHOT_LIST_ep1_cold_open.md` for the full line breakdown
and voice-casting notes (age/gender/tone per character).

## 6. ControlNet (installed tonight, 2026-09-13)

- **Model**: `Qwen-Image-InstantX-ControlNet-Union.safetensors` (3.5GB), downloaded to
  `~/ComfyUI/models/controlnet/` (shared store, matches existing model-storage convention).
  Supports canny / depth / pose / lineart / softedge / normal in one file.
- **Node path**: `ControlNetLoader` → `SetUnionControlNetType` (pick the control type) →
  `ControlNetApplyAdvanced`, feeding into the Qwen Image Edit graph. All three nodes confirmed
  present via `/object_info`.
- **Preprocessors**: installed `comfyui_controlnet_aux` (Fannovel16) for generating the actual
  control images from a reference photo/sketch — confirmed present: `DWPreprocessor` (pose),
  `DepthAnythingV2Preprocessor` + 5 other depth variants, `LineartStandardPreprocessor`, `Canny`
  (built-in).
- **Not yet done**: no ControlNet workflow has been built or tested — this just makes the
  capability available. Worth using when a shot needs a specific pose/composition that text
  description + reference-image conditioning alone won't reliably hit (action choreography,
  precise multi-character blocking). For everything the current pipeline already nails (identity,
  lighting, simple staged poses), don't add ControlNet complexity — it's not needed there.

## 7. LoRA training — evaluated, not set up

Character-specific LoRA training was considered (per the brief that prompted this session) and
**deliberately not installed**. Qwen-Image LoRA training (ai-toolkit, the standard tool) needs
~24-48GB VRAM even quantized; this workstation's RTX 5060 Ti has 16GB. It would not run
acceptably here, and the existing reference-image-conditioned Qwen Edit pipeline is already
achieving reliable identity lock without training (see §3-4). Revisit only if a specific,
concrete consistency failure shows up that reference-conditioning can't fix — don't build this
pre-emptively.

## 6b. Ambience / SFX (installed tonight, 2026-09-13)

Downloaded **Stable Audio 3 Small-SFX** (`stable_audio_3_small_sfx.safetensors`, 2.3GB,
`~/ComfyUI/models/checkpoints/`) + its text encoder (`t5gemma_b_b_ul2.safetensors`, 1.2GB,
`~/ComfyUI/models/text_encoders/`) — purpose-built for SFX/short ambiance (vs. the general
music-oriented 1.0 model), runs on ≤8GB VRAM, native ComfyUI support (`CheckpointLoaderSimple`
+ `CLIPLoader` + `KSampler` + `VAEDecodeAudio`, no custom nodes). Both files integrity-verified.

Workflow built: `workflows/stable_audio3_ep1_kitchen_ambience.json` — "soft rain, distant city
hum, occasional kitchen clink," 60s placeholder duration (adjust once the picture edit's actual
length is known). This is a separate tool from the ChatterBox/FishAudio dialogue setup in §5 —
ambience/SFX vs. character voice are different jobs, don't conflate them.

## 7b. Model integrity check (2026-09-13, safetensors header parse — no generation run)

Every model file the pipeline and the new ControlNet setup depend on was verified structurally
intact (header parses, tensor count sane, not truncated):

| File | Size | Tensors |
|---|---|---|
| `qwen_image_edit_2509_fp8_e4m3fn.safetensors` | 20.4GB | 1933 |
| `Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors` | 849.6MB | 2160 |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | 9.4GB | 1446 |
| `qwen_image_vae.safetensors` | 253.8MB | 194 |
| `Qwen-Image-InstantX-ControlNet-Union.safetensors` | 3.5GB | 181 |
| `hunyuanvideo15_vae_fp16.safetensors` | 2.5GB | 218 |
| `sigclip_vision_patch14_384.safetensors` | 856.5MB | 448 |
| `hunyuanvideo1.5_480p_i2v_step_distilled_fp8_scaled.safetensors` | 8.3GB | 1932 |
| `byt5_small_glyphxl_fp16.safetensors` | 438.6MB | 111 |

Note: the Hunyuan-side models (`hunyuanvideo15_vae_fp16`, `sigclip_vision_patch14_384`,
`hunyuanvideo1.5_480p_i2v_step_distilled_fp8_scaled`, `byt5_small_glyphxl_fp16`) live directly
under `~/ComfyUI-ltx25/models/`, not in the shared `~/ComfyUI` store like the Qwen-side models —
worth knowing if you're ever chasing a "model not found" error.

## 8. Open items for Chris

1. Where's the actual episode script/dialogue? Nothing found locally or on GitHub.
2. Character voice decision (synthetic vs. cloned) — needed before any dialogue audio.
3. ControlNet workflow hasn't been built/tested yet — only the models/nodes are in place.
