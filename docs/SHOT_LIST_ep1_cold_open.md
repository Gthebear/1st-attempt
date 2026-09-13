# Episode 1 Cold Open ("Green") — Shot list & asset audit

Built 2026-09-13 against the real script (`script_episode1_cold_open.md`) and the actual
reference images (viewed directly, not inferred from filenames — two real discrepancies found
below).

**Update 2026-09-14, with generation clearance**: all 8 ready shots (2.2, 2.7, 5.1-5.4, 1.1,
1.3) generated end-to-end via `benchmarks/2026-09-13/generate_ep1_shots.py` — Qwen Edit still
+ Hunyuan i2v clip each, all verified valid. Ambience audio generated via Stable Audio 3.
Three partial sequences assembled and sent to Chris: `ep1_scene1_street.mp4` (6.75s),
`ep1_scene2_kitchen_open.mp4` (10.125s, includes the proven 2.1 + new 2.2/2.7),
`ep1_scene5_kitchen_climax.mp4` (13.5s, the green→red marker beat). All in
`output/video/`. Visual quality checked directly (not just "did it not crash"): identity held
throughout, style consistent, red marker reads clearly and dramatically in 5.3/5.4.

## Continuity issues found — need Chris's call before generating

1. **House name mismatch.** `smith_residence_exterior.png` reads **"RESIDENCE EXTERIOR (THE
   McNEIL HOME)"** in-image. The script says **"SMITH HOUSE"** throughout. Either an earlier
   draft used "McNeil" before the family was renamed, or this asset is misfiled. If any signage/
   text ever needs to render in-shot (mailbox, delivery label) this will show the wrong name.
   Flagging rather than guessing which is correct.
2. **Marker color mismatch.** The script's climax: *"green fading, replaced by a slow-rising
   amber, the first time we've seen it change."* But the actual character design sheet
   (`andr_mechanical_detail.png`) only establishes **two** marker states: green and **red** —
   no amber anywhere in the reference set, including the tactical/armed loadout sheet
   (`andr_arsenal_trenchcoat_modular.png`), which is still green. Recommend using **red**
   for shot 5.3/5.4 to match the established design bible, unless Chris wants amber as a
   deliberate third state — that would need a new reference sheet made first (generation,
   not done tonight).

## Asset audit (confirmed by actually viewing the images, not just filenames)

| Character/location | What's actually there | Usable for this episode? |
|---|---|---|
| Iris | `andr_turnaround.png` (6-angle, apron/blue dress "domestic mode"), `andr_expression_matrix.png` (9 expressions, green marker), `andr_mechanical_detail.png` (green vs. red marker states, hand/eye detail), `andr_arsenal_trenchcoat_modular.png` (tactical loadout, marker still green — this is a *mode* not a marker-color thing) | Yes, well covered |
| James Smith | `smith_father.png` — single clear 3/4 reference, "FATHER (GENTLE, NORMAL)" | Yes, adequate for medium/wide shots. No turnaround, so extreme angles are a stretch. |
| Sierra Smith (12) | `smith_kids_figures.png` (clear face, red/orange curly hair, jacket — left figure), `smith_daughter_items.png` (props/wardrobe only, no face) | Yes, one clear reference. Single angle only — no turnaround. **Note:** the two kids in `smith_kids_figures.png` have no name labels on the sheet itself — left=Sierra/right=Jacob is inferred by relative age (girl looks slightly older) and by pairing with the items-sheet genders, not confirmed by any text on the asset. Worth a quick confirm from Chris before relying on it. |
| Jacob Smith (10) | `smith_kids_figures.png` (right figure, short blond hair), `smith_son_items.png` (props/wardrobe only, no face) | Yes, one clear reference, same limitation and same left/right caveat as above. |
| Mother | `smith_mother.png` exists, clear reference | **Not used** — she doesn't appear in this scene. |
| EXT. suburban street | `smith_street_view.png` — "STREET VIEW & COMMUNITY LAYOUT," matches the script beat almost exactly (monorail on stilts, skyline beyond, rain, residential street) | Yes, strong match |
| INT. kitchen | `locked_iris_kitchen_chris.png` — already validated end-to-end (rendered clip exists) | Yes, proven |
| INT. upstairs hallway | **Nothing.** Checked both `input/` folders in full (including the `3d/`, `_archive/`, and `AI Avatars/` subfolders) — no bedroom/hallway/interior asset exists anywhere on this machine. | **Blocked** |
| INT. Jacob's room | **Nothing.** Same exhaustive check as above. | **Blocked** |
| House exterior | `smith_residence_exterior.png` — see naming issue above | Usable, name issue aside |

## Shot list

### Scene 1 — EXT. Suburban street, night, rain
- **1.1** Wide static establishing — street, monorail on stilts, skyline glow beyond, rain on car roofs. Ref: `smith_street_view.png`.
- **1.2** (optional, minor) delivery drone passing overhead — connective tissue, skippable if time-limited.
- **1.3** Slow push toward the one warm-lit house. Ref: `smith_residence_exterior.png` (mind the name issue).

### Scene 2 — INT. Kitchen, continuous
- **2.1** Wide/medium, Iris drying a plate at the counter. **Already proven** — reuse `locked_iris_kitchen_chris.png` / `output/video/hunyuan_video_1.5_00010_.mp4` directly, no new render needed.
- **2.2** Medium, she sets the plate down, notices the inhaler, moves it to a drawer. *(Built tonight as `qwen_edit_ep1_shot22_notices_inhaler.json`, prompt matches the actual script action.)*
- **2.3** Insert/cutaway — neon skyline through the window, rain. Can reuse the window portion of the locked kitchen still, or `andr_env_light_street.png` framing.
- **2.4** James enters, pours water at the tap. **New**: two-character shot (Iris + James) — no precedent yet for compositing two character refs into one Qwen Edit still. First one to test.
- **2.5** Dialogue coverage (shot/reverse or OTS) for the "Sierra still awake?" exchange (4 lines).
- **2.6** James glances at the window, exits.
- **2.7** Close-up, Iris watching him go, green marker steady, calm/thoughtful. *(Built tonight as `qwen_edit_ep1_shot27_watches_james_leave.json`.)*

### Scene 3 — INT. Upstairs hallway (Sierra's room), moments later — **BLOCKED, no location reference**
- 3.1 Sierra under the covers with a tablet.
- 3.2 Iris/Sierra dialogue (6 lines), Iris takes the tablet.

### Scene 4 — INT. Jacob's room, continuous — **BLOCKED, no location reference**
- 4.1 Jacob half-asleep, Iris straightens the blanket, turns off the lamp. No dialogue this scene.

### Scene 5 — INT. Kitchen, later
- **5.1** Iris alone, wiping the counter, rain against the window, marker steady. Variant of the proven kitchen still — solo, no plate. *(Built tonight: `qwen_edit_ep1_shot51_alone_wiping_counter.json`.)*
- **5.2** She pauses, head tilts — reaction beat, hears car doors/voices. *(Built tonight: `qwen_edit_ep1_shot52_reaction_head_tilt.json`.)*
- **5.3** She turns fully toward the window, marker shifts (green → **red**, pending Chris's call above). *(Built tonight: `qwen_edit_ep1_shot53_turns_marker_shifts.json` — uses red.)*
- **5.4** Hold on her face — the episode's money shot. Marker in its new state, tension, cut to black. *(Built tonight: `qwen_edit_ep1_shot54_hold_on_face_red.json`.)*

### Also built tonight
- **1.1** street establishing → `qwen_edit_ep1_shot11_street_establishing.json` (ref: `smith_street_view.png`)
- **1.3** push toward the house → `qwen_edit_ep1_shot13_push_to_house.json` (ref: `smith_residence_exterior.png`, mind the naming issue)

### Not built — needs a decision or new asset first
- **2.4-2.6** (James + Iris together, dialogue coverage, James exits) — needs two-character
  compositing. **Confirmed technically supported**: `TextEncodeQwenImageEditPlus` (the node
  already at the core of the proven pipeline) natively takes `image1`/`image2`/`image3`
  optional inputs, and the subgraph in `qwen_edit_2509.json` already exposes `image2 (optional)`
  and `image3 (optional)` ports wired straight to both the positive and negative prompt nodes
  (verified via the subgraph's internal link list, not guessed). What's *not* done: wiring an
  actual second `LoadImage` node (→ `smith_father.png`) to that port requires adding a new node
  + link to the graph, not just patching an existing widget value — that's a materially
  different (and untested) kind of edit than everything else built tonight, which only ever
  patched values on existing nodes. Recommend this be the **first** render of the night once
  you're back — a single deliberate test, not a batch — rather than trusting a hand-spliced
  graph I couldn't execute to verify.
- **Scene 3 & 4** (hallway, Jacob's room) — no location reference exists for either.
- Generator script: `benchmarks/2026-09-13/build_iris_kitchen_shots.py` — rerunning it regenerates all 8 files above from the proven `qwen_edit_2509.json` base; extend the `SHOTS` list to add more.

## Dialogue lines (for ChatterboxDialogTTS / FishS2MultiSpeakerTTS setup, not run tonight)

| Speaker | Lines | Voice notes |
|---|---|---|
| **James** | "Sierra still awake?" / "She'll say twenty." / "Good night for staying in." | Adult male, warm, tired-but-content |
| **Iris** | "Reading. I told her lights out in ten." / "I said ten." / "Ten minutes was generous." / "It's a racing game." / "No." / "Not yet." | Adult female, measured, precise, minimal inflection — android calm, never rushed |
| **Sierra** | "It's educational." / "Educational racing game." / "Do you sleep?" / "Ever get bored?" | 12-year-old girl, a little cheeky/testing |
| **Jacob** | *(none — he's asleep/half-asleep throughout)* | n/a for this scene |

Still no voice samples for any of these four — see PRODUCTION_BIBLE.md §5 gap. Casting notes
above are enough to pick sensible synthetic base voices once you're ready.

## What's genuinely ready to generate first (once you're back and want to)
Scene 2 (kitchen) is the safest starting point — proven environment, proven identity-lock,
existing shot2/shot3 workflow files already built. Scenes 1 and 5 are next (good references,
no new compositing challenges). Scenes 3 and 4 need a location reference generated first.
Shot 2.4 (Iris + James together) is the first real test of multi-character compositing in this
pipeline — worth doing as a deliberate small test before assuming it works.
