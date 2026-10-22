# Third-party notices

Stonebound uses the unmodified KaTrain source at `vendor/katrain`, revision `f4981cf905cece90085ce4e3967415d0c16d525f` from https://github.com/sanderland/katrain.

KaTrain's source is Copyright 2020 Sander Land and/or other authors, licensed under MIT. The complete upstream notice, including notices for bundled components, is retained in `vendor/katrain/LICENSE`. The game's interface uses its own SVG icons and does not display the upstream Flaticon icons or DIGITAL-7 font.

KaTrain bundles KataGo, Copyright David J Wu and contributors. KataGo and its included dependencies have their own license notices: https://github.com/lightvector/KataGo. Preserve the upstream notices when redistributing the bundled executable, libraries, or model. This checkout includes the upstream notices; see `vendor/katrain/LICENSE` and the KataGo repository for component licenses.

The project uses Kivy (MIT), pysgf (MIT), and their runtime dependencies through the project virtual environment. Optional browser validation uses Playwright (Apache-2.0).

The portable Windows edition embeds Python, Kivy, pysgf, pywebview (BSD), pythonnet, clr-loader, and their required runtime libraries. PyInstaller is used under its bootloader redistribution exception. Available distribution license notices are collected in `resources/licenses`, embedded under `licenses/dependencies`, and provided in the portable ZIP's `licenses` directory. This includes KataGo's main license, vendored-library notices and `cpp/core/sha2.cpp`'s embedded notice. Microsoft Edge WebView2 is a system prerequisite; the complete browser runtime is not bundled.

The additional portable CPU executable is the official `katago-v1.18.1-eigen-windows-x64.zip` release from https://github.com/lightvector/KataGo/releases/tag/v1.18.1, verified against SHA-256 `074485cf150c38aa3bb14ac9f54f2952ffefbceb44673709bbb8a83650bf95d6`. Source and retrieval details are retained in `resources/cpu/SOURCE.txt` and `scripts/fetch-cpu-engine.py`.

The revised interaction layout references the full-screen presentation of https://3k.chon9.com/. Stonebound does not bundle that site's code, portraits or background art.

The bundled Latin variable fonts DM Sans and Manrope are distributed under the SIL Open Font License 1.1. Their complete notices are retained beside the font files in `web/assets/fonts/dmsans-OFL.txt` and `web/assets/fonts/manrope-OFL.txt`. The optional `scripts/fetch-fonts.py` retrieves them from Google Fonts; gameplay makes no request to Google Fonts.

The city and character illustrations are original AI-generated assets, not downloaded CC0 assets. Their prompts and generation method are recorded in `ASSETS.md`. They depict original characters and places.

Background music consists of four unmodified recordings by The Cynic Project / cynicmusic.com / pixelsphere.org, released under CC0 1.0 Universal on their individual OpenGameArt pages. Full track credits and source links are retained in `MUSIC.md`, recording hashes and download metadata in `web/assets/music/playlist.json`, and the CC0 text in `resources/licenses/music/CC0-1.0.txt`. The music is embedded for offline playback.

The analysis-client friendly-pass check in `stonebound/endgame.py` follows the approach of KataGo v1.18.1 `PlayUtils::maybeFriendlyPass`, with stricter board-settlement checks matching Stonebound’s scoring. KataGo’s copyright and MIT license are preserved in the bundled dependency notices.
