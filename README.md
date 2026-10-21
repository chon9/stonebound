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
  <code>24 rivals</code> · <code>8 chapters</code> · <code>48 collectibles</code> · <code>48 manga panels</code><br>
  English / 简体中文 · Windows portable · Local single-player
</p>

---

An unsigned letter. Your grandmother’s old Go board. A riverside club with an uncertain future.

Follow the railway, wander through a lantern festival, listen to stories at the harbor, and find your way into the regional cup. Meet the person across the board, earn a keepsake, and carry a little of each place into your next game.

带着外婆的旧棋盘与一封未署名的信，走进一座即将失去棋社的小镇。从河畔到港口，从夏祭到地区杯，以一局局围棋结识朋友，拾起故事，也找回棋社的灯火。

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
| **A story you can turn the pages of** | 16 manga pages, 48 illustrated panels, chapter openings and unlockable conclusions. Revisit your memories in the Chronicle. |
| **A board that becomes yours** | Collect 24 boards and 24 stone sets: porcelain, sea glass, star charts, kintsugi, jade and more. Preview materials, then play with them. |
| **Keepsakes you earn** | Finish each chapter’s three encounters to receive its exclusive keepsake. Victories also earn coins for the treasury. |
| **Room to learn** | Choose 9×9, 13×13 or 19×19. Take your time, ask KataGo for a hint, or undo a move. |
| **Quiet moves, quiet music** | Four bundled CC0 tracks with automatic playlist looping, independent volume and track controls. Works offline. |
| **Your language, your pace** | English and Simplified Chinese throughout the UI, conversations and manga. Progress, equipment and preferences save automatically. |

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

The executable opens a dedicated desktop window. It embeds the Python runtime, unmodified pinned KaTrain core, KataGo, its neural-network model, original artwork, fonts, and both languages. It defaults to the generic x64 **CPU** version of KataGo, which works without a dedicated GPU or OpenCL driver. CPU turns can take longer than GPU turns.

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
- **Chronicle:** eight story chapters, 16 bilingual manga pages (48 illustrated panels), completed-game memories, XP and victories.
- **Codex:** concise Go rules covering liberties, captures, territory, passes, hints and ko.
- **Settings:** persistent language and sound preferences; engine status and failure details.

The match screen presents the Go board with framed rival art, player indicators, a move counter, captured-stone counts, and concise controls. There are no analysis graphs or training tools in the play flow.

## The illustrated campaign

An unsigned letter brings the traveler and their grandmother Akari’s board to a riverside club that may lose its home. Follow an unfinished exhibition record through the station quarter, lantern market, harbor, misty foothills, city qualifiers and regional cup, then return to reopen the club. Each chapter has three rivals with their own conversations, an opening manga page and a conclusion page unlocked by three victories.

Read the panels left to right. Dialogue and narration are live text, so the reader can switch language without replacing the art. Read state is saved. Replay unlocked pages in Chronicle; locked conclusions contain no script text in the state response. Original art briefs are recorded in `content/art-prompts.json`.

Boards and stones use shared canvas materials in the treasury and actual matches, including porcelain, ripples, garden leaves, star charts, circuit lines, marble, kintsugi, veins, speckles, metallic bands and seals.

## English and Chinese

Use the top-right **简 / EN** button, or choose **English / 简体中文** in Settings. The interface, story dialogue, rival names, locations, cosmetic items, instructions, common gameplay errors and results are translated. Language and sound are saved in the player profile, so changing the native window's local port or moving the portable game does not reset them. Language can be changed during a match without changing the board.

## Game rules and progression

Play black against 24 increasingly strong KaTrain rivals (15 kyu through a configured 4 dan target) on **9×9, 13×13 or 19×19** boards. Captures, suicide prevention and ko use upstream KaTrain rules. Undo reverses your last move and the AI reply; hints come from KataGo analysis. No time limit.

Two consecutive passes end a game. **Chinese area scoring** counts live stones and enclosed empty points, with **6.5 komi** for white. KataGo ownership identifies confidently dead stones; uncertain groups count as alive. **Play out unsettled groups before passing.** There is no manual dead-stone adjudication screen yet.

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

To use an existing GPU KataGo installation, place `engine-config.json` beside the EXE (or in the project root for source mode) using `engine-config.example.json` as a guide. Set absolute `katago`, `model` and `config` paths. `KATAGO_EXECUTABLE`, `KATAGO_MODEL`, and `KATAGO_CONFIG` environment variables also work. JSON accepts KaTrain's `max_visits`, `fast_visits` and `max_time`. Restart after changing engine configuration.

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

The EXE also supports isolated package verification without installing Python:

```powershell
release/Stonebound.exe --self-test engine-report.json --data-dir .runtime/package-test
release/Stonebound.exe --window-test window-report.json --data-dir .runtime/window-test
```

`--self-test` requires a fresh test save. It initializes the embedded CPU engine and plays a real AI turn. `--window-test` opens a hidden native window, checks that the lobby rendered, writes a JSON report and closes. These modes are for development; normal play needs no command line.

Verified for this release: 26 rule/scoring/progression/preference/campaign/music tests; bilingual browser gameplay and mobile layouts; native WebView2 rendering; and a relocated EXE running from a folder containing spaces and Chinese characters, with Python removed from PATH. The relocated build produced an actual KataGo reply and reopened with its saved Chinese preference. File size, SHA-256 and test reports are recorded in `release/BUILD-INFO.json`.

Original generated artwork and prompts are recorded in [ASSETS.md](ASSETS.md). Upstream notices and bundled-font licenses are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
