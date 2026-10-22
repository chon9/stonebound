<p align="center">
  <img src="web/assets/favicon.svg" width="72" alt="Stonebound seal">
</p>

<h1 align="center">Stonebound · 棋缘物语</h1>

<p align="center">
  <strong>Every stone begins a story.</strong><br>
  An original anime Go RPG, powered by the real KaTrain / KataGo AI core.
</p>

<p align="center">
  <a href="https://github.com/chon9/stonebound/releases/latest/download/Stonebound-Windows-x64.zip"><strong>Download for Windows</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/chon9/stonebound/releases/latest/download/Stonebound.exe">Standalone EXE</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/chon9/stonebound/releases">Release notes</a>
  &nbsp;·&nbsp;
  <a href="#run-from-source">Build from source</a>
</p>

<p align="center">
  <code>24 rivals</code> · <code>8 chapters</code> · <code>48 collectibles</code> · <code>54 manga panels</code><br>
  English / 简体中文 · Windows portable · Local single-player
</p>

---

An unsigned letter. Your grandmother’s old Go board. An ancient spirit who remembers her.

Follow the railway, wander through a lantern festival, listen to stories at the harbor, and find your way into the regional cup. Meet the person across the board, earn a keepsake, and carry a little of each place into your next game.

带着外婆的旧棋盘与一封未署名的信，走进一座即将失去棋社的小镇。从河畔到港口，从夏祭到地区杯，旧棋盘中的古代棋灵「砚归」与你同行，以一局局围棋结识朋友，拾起故事，也找回棋社的灯火。

## A look inside

These are screenshots of the playable game. Click an image to see it full size.

| Adventure · 落子，启程 | Manga · 翻开旅途的故事 |
| :---: | :---: |
| ![Illustrated adventure lobby with chapter and opponent selection](docs/screenshots/adventure.png) | ![Manga reader with original illustrated panels and Chinese dialogue](docs/screenshots/manga.png) |
| **At the board · 与棋友对弈** | **Your collection · 一方棋盘，一段故事** |
| ![Actual KaTrain-powered Go match with a rival portrait and a playable board](docs/screenshots/match.png) | ![Equipment collection with unlockable board and stone designs](docs/screenshots/collection.png) |

## What awaits

| | Your journey |
| :--- | :--- |
| **People worth meeting** | 24 original rivals across 8 districts, each with their own conversations and KaTrain-calibrated strength. |
| **A story you can turn the pages of** | 18 manga pages, 54 illustrated panels: eight chapter openings/conclusions plus the ghost master’s awakening and homecoming. Revisit your memories in the Chronicle. |
| **A board that becomes yours** | Collect 24 boards and 24 stone sets: porcelain, sea glass, star charts, kintsugi, jade and more. Preview materials, then play with them. |
| **Keepsakes you earn** | Finish each chapter’s three encounters to receive its exclusive keepsake. Victories also earn coins for the treasury. |
| **A ghost at your shoulder** | Yangui, an original ancient Go-master spirit, travels with you through eight chapter reflections and two manga episodes. |
| **Room to learn** | Ask Sensei for a real KataGo recommendation and territory preview. Large point losses earn a Classical Chinese rebuke, with a plain-language explanation. Undo and try again. |
| **See the board clearly** | Toggle black/white territory estimates during play; see final territory, neutral points and crossed-out dead stones after two passes. |
| **Quiet moves, quiet music** | Four bundled CC0 tracks with automatic playlist looping, independent volume and track controls. Works offline. |
| **Your language, your pace** | English and Simplified Chinese throughout the UI, conversations and manga. Progress, equipment and preferences save automatically. |

## A master who remembers your grandmother

**Yangui / 砚归** is an original Go-master ghost bound to Akari’s board. His awakening manga introduces a promise: *“I shall teach; thou shalt choose.”* Eight chapter reflections connect his memories to your journey; completing all eight chapters unlocks his homecoming manga. Revisit both episodes and unlocked reflections in **Chronicle**.

At the board, **Ask Sensei** reveals KataGo’s highest-ranked current suggestion, a learning prompt and a territory overlay. After your move, the game compares Black’s estimated lead **before and immediately after your move, before White replies**. Estimated losses of 3+ points receive a warning; 6+ points earn a sterner Classical Chinese rebuke:

> 缓急不分，轻重倒置！且静心审局，勿再轻投。

Chinese includes a modern explanation; English includes a translation. The commentary is authored, while move recommendations, ownership and point-loss estimates come from the actual KataGo analysis. Short searches can change their judgment; the master never scolds a move for differing from first choice alone.

师父「砚归」随八章故事同行。**请教师父**可查看推荐落点、白话教学与形势预览；严重失误时，他会以文言训诫，并显示估计目损与原推荐手。棋灵觉醒、归来漫画与逐章谈话均可在故事册重看。

| Ask Sensei · 请教师父 | The board remembers · 旧枰有灵 |
| :---: | :---: |
| ![Ghost master Yangui teaching with a real KataGo recommendation and mid-game territory overlay](docs/screenshots/sensei.png) | ![Original three-panel manga introducing the spirit bound to the grandmother’s Go board](docs/screenshots/spirit.png) |

After two passes, the board marks enclosed empty points in black or white, neutral points in gray, and removed dead stones with red crosses. Those marks use the same regions as the displayed **Chinese area count**. After resignation, a separate ownership estimate is shown; the result stays **W+R**. The last finished board can be reopened from Adventure.

![A completed real KataGo game with territory marks, dead-stone crosses and the final area count](docs/screenshots/territory.png)

## A soundtrack for quiet moves

Soft piano, ambient pads and gentle bells accompany the journey. Four **CC0** recordings by **The Cynic Project** repeat in a roughly 9½-minute playlist, bundled inside the game for offline play. [Track credits and source licenses →](MUSIC.md)

Music starts with your first interaction at a quiet default volume. The header’s musical-note button pauses or resumes it; **Settings → Background music** offers volume, track selection and previous/next controls. Music and stone sounds are independent, and your preferences are saved. Menu, comic and game transitions keep the same player running.

四首舒缓的CC0音乐随游戏提供，约九分半钟循环播放。顶部音符按钮可暂停／继续；**设置 → 背景音乐**可调节音量、选曲或切换上一首／下一首。音乐与落子音效独立控制，支持离线聆听。

<details>
<summary>See the soundtrack controls · 查看音乐控制画面</summary>

![Background-music playlist and volume controls](docs/screenshots/music.png)

</details>

## Portable Windows game

Download **[Stonebound-Windows-x64.zip](https://github.com/chon9/stonebound/releases/latest/download/Stonebound-Windows-x64.zip)** from GitHub Releases, extract it into a writable folder, and double-click **`Stonebound.exe`**. The local build is also available at `release/Stonebound.exe`. No Python, Git, Node, terminal, or setup commands are required on the playing computer.

The executable opens a dedicated desktop window. It embeds the Python runtime, unmodified pinned KaTrain core, KataGo, its neural-network model, original artwork, fonts, and both languages. It defaults to the generic x64 **CPU** version of KataGo, which works without a dedicated GPU or OpenCL driver. Choose **Settings → AI processor → CPU / GPU** to switch to the bundled OpenCL GPU engine. CPU turns can take longer than GPU turns.

Requires **Windows 10/11 x64 and Microsoft Edge WebView2**. WebView2 is already present on most current Windows installations; if missing, install Microsoft's [WebView2 Evergreen Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) once. The executable is unsigned. The first run needs a few seconds to unpack and load the model.

Everything writable stays in **`data/` beside the EXE**, including `save.json`, engine caches, and WebView2 state. Copy the EXE and its `data` folder together to move your game. Keep the game in a writable location such as a personal folder or USB drive. Only one desktop instance can open a given save directory at a time.

To migrate a source-version save, close both versions, back up the destination, and copy `.runtime/save.json` to `data/save.json` beside the EXE. Old saves retain coins, equipment, victories and preferences. Already completed chapters receive their new keepsakes automatically, without changing equipped items. Previously defeated rivals remain available for rematches.

See [PORTABLE-README.txt](PORTABLE-README.txt) for bilingual portable instructions. Startup diagnostics are written to `data/desktop.log`.

**中文快速开始：** 下载上方ZIP，解压到个人文件夹或U盘，双击 `Stonebound.exe`。右上角 **简 / EN** 可切换语言。存档位于EXE旁的 `data` 文件夹；搬家时将它与EXE一起复制。无需安装Python、Git或Node。

## The game interface

The redesign references the full-screen lobby and game navigation of [Little Kingdoms](https://3k.chon9.com/): an illustrated world backdrop, dark jade panels, gold frames and buttons, rival portrait stage, player HUD, and bottom navigation dock. Stonebound retains its own original setting, characters, graphics and Go gameplay.

- **Adventure:** select a rival and board size; start their story or resume your current match.
- **Travel:** explore the illustrated town through location markers and character encounters.
- **Treasury:** buy board and stone designs with earned coins. Story victories unlock stock.
- **Wardrobe:** preview and equip owned boards and stones.
- **Chronicle:** eight story chapters, 18 bilingual manga pages (54 illustrated panels), eight ghost-master reflections, completed-game memories, XP and victories.
- **Codex:** concise Go rules covering liberties, captures, territory, passes, hints and ko.
- **Settings:** CPU/GPU selection, persistent language and sound preferences, engine status and failure details.

The match screen presents the Go board with framed rival art, player indicators, a move counter, captured-stone counts, and concise controls. There are no analysis graphs or training tools in the play flow.

## The illustrated campaign

An unsigned letter brings the traveler and their grandmother Akari’s board to a riverside club that may lose its home. Follow an unfinished exhibition record through the station quarter, lantern market, harbor, misty foothills, city qualifiers and regional cup, then return to reopen the club. Each chapter has three rivals with their own conversations, an opening manga page and a conclusion page unlocked by three victories.

Read the panels left to right. Dialogue and narration are live text, so the reader can switch language without replacing the art. Read state is saved. Replay unlocked pages in Chronicle; locked conclusions contain no script text in the state response. Original art briefs are recorded in `content/art-prompts.json`.

Boards and stones use shared canvas materials in the treasury and actual matches, including porcelain, ripples, garden leaves, star charts, circuit lines, marble, kintsugi, veins, speckles, metallic bands and seals.

## English and Chinese

Use the top-right **简 / EN** button, or choose **English / 简体中文** in Settings. The interface, story dialogue, rival names, locations, cosmetic items, instructions, common gameplay errors and results are translated. Language and sound are saved in the player profile, so changing the native window's local port or moving the portable game does not reset them. Language can be changed during a match without changing the board.

## Choose CPU or GPU

Open **Settings → AI processor** and choose **CPU** or **GPU · OpenCL**. Both executables are bundled in the portable release. Your current board, story progress, coins and equipment stay intact; the successful choice is saved for future launches. Wait for the rival’s current turn to finish before switching.

- **CPU:** works without a dedicated graphics card. This is the portable default.
- **GPU:** uses the bundled OpenCL engine. Requires a supported graphics device and working OpenCL drivers. First startup may spend a few minutes tuning; a failed switch keeps the previous engine and position.

**19×19 placement is immediate:** the board paints your submitted stone before the server replies, and the server accepts legal moves without waiting for Sensei’s analysis. Coaching and AI thinking continue in the background. Rejected moves remove the tentative stone, and duplicate clicks are blocked. The rival’s thinking time still depends on the processor and board size.

在 **设置 → AI运算设备** 中选择 **CPU / GPU**。切换成功后自动记住选择，并保留当前棋局与进度；GPU启动失败则保留原引擎。19路落子不再等待师父分析，棋子会立即显示，AI在后台继续思考。

![CPU and GPU selection in the in-game settings](docs/screenshots/engine-settings.png)

## Game rules and progression

Play black against 24 increasingly strong KaTrain rivals (15 kyu through a configured 4 dan target) on **9×9, 13×13 or 19×19** boards. Captures, suicide prevention and ko use upstream KaTrain rules. Undo reverses your last move and the AI reply; hints come from KataGo analysis. No time limit.

Passing skips a turn; it does **not** concede the game. Choose **Resign** to give up. Two consecutive passes end a game. **Chinese area scoring** counts live stones and enclosed empty points, with **6.5 komi** for white. KataGo ownership identifies confidently dead stones; uncertain groups count as alive. **Play out unsettled groups before passing.** There is no manual dead-stone adjudication screen yet.

The rival now respects a searched KataGo pass, instead of letting the weakened rank policy replace it with another move. After you pass on a settled board, an additional friendly-pass check verifies confident territory, completed boundaries and no remaining dame, then compares actual KataGo evaluations after passing and after playing on. It accepts the ending when continued play has no meaningful gain; useful endgame moves and unsettled groups still require play.

This adapts the behavior of [KataGo’s GTP friendly-pass check](https://github.com/lightvector/KataGo/blob/v1.18.1/cpp/program/playutils.cpp#L1029) to the KaTrain analysis interface, using the same conservative dead-chain handling as Stonebound’s final count. A short explanation appears when the rival continues after your pass.

停一手并非认输；放弃本局请选择「认输」。棋局已经走清时，AI会比较继续落子与停着的KataGo评估，避免无意义地填自己的地盘或逐一提掉已确认的死子。尚有公气、官子或死活未定时，仍会继续下。

First wins earn 250–1,405 coins and unlock the next rival. Repeat wins earn 80 coins. Losses award 25 XP. Rewards and purchases are validated and saved by the backend; browser-provided scores do not award wins. Collect 24 boards and 24 stone sets: 40 shop catalog entries (including the two starting items) and eight chapter-completion keepsakes. Keepsakes require beating all three rivals in their chapter; they cannot be purchased. This is a local single-player game with no accounts, payments, or multiplayer.

## For developers

The portable download is ready to play. The sections below explain the AI core, source setup, packaging and verification.

## Actual KaTrain AI integration

Unmodified KaTrain source is checked out at `vendor/katrain`, pinned to:

```text
https://github.com/sanderland/katrain
f4981cf905cece90085ce4e3967415d0c16d525f
```

`stonebound/engine.py` imports upstream `KataGoEngine`, `Game`, `GameNode`, and `generate_ai_move`. Rivals use upstream `AI_RANK` with distinct `kyu_rank` settings. There is no substitute JavaScript bot. Visible engine errors preserve the position with retry/undo actions. Configured ranks are strength targets, not guaranteed human ratings on every board size.

The source checkout uses KaTrain's bundled OpenCL KataGo executable and `b10c384h6nbttflrs.bin.gz` model. The portable build adds the official generic x64 Eigen CPU executable from KataGo v1.18.1, verified against its published SHA-256. It uses the same KaTrain neural-network model and strategy.

For an advanced custom KataGo installation, place `engine-config.json` beside the EXE (or in the project root for source mode) using `engine-config.example.json` as a guide. Set absolute `katago`, `model` and `config` paths. `KATAGO_EXECUTABLE`, `KATAGO_MODEL`, and `KATAGO_CONFIG` environment variables also work. JSON accepts KaTrain's `max_visits`, `fast_visits` and `max_time`. Restart after changing engine configuration. A saved in-game CPU/GPU choice explicitly selects its bundled executable; custom model and search settings still apply. Remove the `ai_backend` preference from the backed-up save to return to automatic custom-executable selection.

## Run from source

The existing `Start-Stonebound.cmd` browser launcher still works. First-time source setup needs Git plus uv or Python 3.12:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/setup.ps1
.venv/Scripts/python.exe server.py --open
```

For a native window from source, install the optional desktop/build dependencies, then run:

```powershell
uv pip install --python .venv/Scripts/python.exe -r requirements-build.txt
.venv/Scripts/python.exe desktop.py
```

Python 3.11–3.13 is required by upstream KaTrain/pysgf; setup uses 3.12. Source saves remain in `.runtime/`. `STONEBOUND_DATA_DIR` or the desktop `--data-dir` option selects an alternate save directory. No JavaScript build is required.

## Rebuild the portable EXE

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-windows.ps1
```

The script installs pinned packaging dependencies, fetches and verifies CPU KataGo, builds the single-file Windows application from `Stonebound.spec`, and creates the portable ZIP with instructions and notices. Build artifacts go to `.build/` and `release/`. The packaging hook collects Kivy's event/config/storage primitives needed by KaTrain, keeping its analysis UI and media providers out of the executable.

## Verify

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
node --check web/app.js
.venv/Scripts/python.exe tests/integration.py
```

Browser checks use optional Playwright (`npm install`; install Chromium if needed). Use a separate save because tests play and resign actual games:

```powershell
# Terminal 1
$env:STONEBOUND_DATA_DIR = "$PWD/.runtime/browser-test"
.venv/Scripts/python.exe server.py --port 8766
# Terminal 2
npm run test:browser
```

The browser suite checks music continuity during real games, both languages, dialogue/items/rules, reload persistence, actual AI replies, hints, undo, keyboard play, saved results, mobile layouts and the absence of external runtime requests. The integration suite plays a complete real-engine game, checks victory rewards and purchases, then verifies backend restart with an active match.

The full-campaign visual suite uses an explicitly seeded test fixture, separate from actual-game verification:

```powershell
# Terminal 1
.venv/Scripts/python.exe tests/campaign_fixture.py
# Terminal 2
node tests/campaign-browser.mjs
.venv/Scripts/python.exe tests/expanded-ai.py
```

The fixture checks all portraits, 16 manga pages, bilingual reader navigation and read persistence, 48 material previews, keepsakes and mobile layouts. `expanded-ai.py` verifies actual KaTrain turns for new intermediate and final dan targets on 13×13 and 19×19.

The music suite checks actual MP3 decoding, first-interaction playback, automatic next-track and playlist wrap, pause/volume/track persistence, independent stone sounds, bilingual/mobile controls, failed-file recovery and local HTTP byte ranges:

```powershell
$env:STONEBOUND_TEST_URL = "http://127.0.0.1:8766"
node tests/music-browser.mjs
```

The CPU/GPU browser suite requires a machine with a working OpenCL GPU. It verifies immediate 19×19 painting while a request is deliberately held, duplicate-click prevention, rejected-move rollback, real CPU and GPU turns, mid-game switching without changing the board, and bilingual/mobile settings. Run against an isolated source or packaged server:

```powershell
$env:STONEBOUND_TEST_URL = "http://127.0.0.1:8773"
node tests/engine-browser.mjs
```

The endgame browser regression (`node tests/endgame-browser.mjs`) expects an isolated settled game with Black to move at `STONEBOUND_TEST_URL` (default port 8776). It checks that one player pass receives the rival’s pass and produces the final territory, then starts a fresh game to check that an opening pass does not force an ending, that pass guidance is bilingual, and that resignation still concedes. Structural and evaluation edge cases are covered in `tests/test_endgame.py`.

The ghost-master suite checks a real opening-pass mistake, calm feedback for the recommended move, current-position hints and ownership, undo invalidation, resignation estimates, bilingual spirit stories and mobile access. Run it against an isolated save with a ready engine. The final-territory suite uses the actual completed save written by `integration.py` in `.runtime/final-territory`.

```powershell
$env:STONEBOUND_TEST_URL = "http://127.0.0.1:8766"
node tests/sensei-browser.mjs
# In a separate terminal, serve the completed real-game fixture:
$env:STONEBOUND_DATA_DIR = "$PWD/.runtime/final-territory"
.venv/Scripts/python.exe server.py --port 8771
# In another terminal (the test server defaults to 8771):
$env:STONEBOUND_TEST_URL = "http://127.0.0.1:8771"
node tests/territory-browser.mjs
```

The EXE also supports isolated package verification without installing Python:

```powershell
release/Stonebound.exe --self-test engine-report.json --data-dir .runtime/package-test
release/Stonebound.exe --window-test window-report.json --data-dir .runtime/window-test
```

`--self-test` requires a fresh test save. It initializes the embedded CPU engine, plays a real AI turn and asks Sensei for a recommendation and 81-point ownership map. `--window-test` opens a hidden native window, checks the lobby, both manga readers and bundled MP3 decoding, writes a JSON report and closes. These modes are for development; normal play needs no command line.

Verified for this release: 60 rule/scoring/progression/preference/campaign/music/mentor/processor/placement tests; bilingual browser gameplay and mobile layouts; real KataGo mistake coaching, territory overlays and completed-game map/count agreement; native WebView2 rendering; and a relocated EXE running from a folder containing spaces and Chinese characters, with Python removed from PATH. The relocated build produced an actual KataGo reply and reopened with its saved Chinese preference. File size, SHA-256 and test reports are recorded in `release/BUILD-INFO.json`.

Original generated artwork and prompts are recorded in [ASSETS.md](ASSETS.md). Upstream notices and bundled-font licenses are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
