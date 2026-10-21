# Quiet moves · 静听棋声

Stonebound includes four relaxing recordings by **The Cynic Project** (cynicmusic / Alex Smith), originally released for Pixelsphere. The author offers each track under **CC0 1.0 Universal**, as shown on its individual OpenGameArt page. License labels were checked on 21 October 2026.

| Track | Length | Original source and CC0 declaration |
| --- | --- | --- |
| Vaporware | 2:45 | [Calm Piano 1 (Vaporware)](https://opengameart.org/content/calm-piano-1-vaporware) |
| Another August | 3:27 | [Another August](https://opengameart.org/content/another-august) |
| Synthwave 4k | 2:38 | [Calm Ambient 1 (Synthwave 4k)](https://opengameart.org/content/calm-ambient-1-synthwave-4k) |
| Happy Lullaby | 0:40 | [Happy Lullaby (song17)](https://opengameart.org/content/happy-lullaby-song17) |

Credit: **The Cynic Project / [cynicmusic.com](https://cynicmusic.com/) / [pixelsphere.org](https://pixelsphere.org/)**.

The original MP3 recordings are bundled unchanged in `web/assets/music/`. The playlist repeats after about 9½ minutes. Chinese display titles are mood labels used by the game; the original titles and artist are retained in the manifest and these credits.

The [CC0 dedication](https://creativecommons.org/publicdomain/zero/1.0/) and [legal text](resources/licenses/music/CC0-1.0.txt) accompany the distribution. In the portable ZIP, the legal text is at `licenses/music/CC0-1.0.txt`; the EXE embeds the same notice. Source pages, download URLs, durations, byte sizes and SHA-256 hashes are recorded in [playlist.json](web/assets/music/playlist.json).

## Listening in the game

Music begins after the first interaction with the game. Use the musical-note button in the header to pause or resume. **Settings → Background music** contains volume, track selection and previous/next controls. Music and stone sounds have independent switches. Volume, enabled state and the last manually selected track are saved with the player profile. Music continues through menus, manga, dialogue and games; automatic track changes do not restart when game state refreshes.

音乐会在首次操作后开始。顶部音符按钮可暂停／继续；在**设置 → 背景音乐**中可调节音量、选择曲目或切换上一首／下一首。音乐与落子音效独立控制，偏好随存档保存。菜单、漫画与对局之间切换时，音乐会继续播放。全部曲目随游戏提供，可离线聆听。

## Asset maintenance

`scripts/fetch-music.py` downloads these four source files and records their metadata. This optional authoring utility needs `ffprobe` to validate MP3 format and duration; playing or building the game uses the checked-in files and does not need FFmpeg or network access for music.
