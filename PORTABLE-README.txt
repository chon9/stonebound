STONEBOUND / 棋缘物语 — Portable Windows edition

Double-click Stonebound.exe. No Python, Git, Node or setup commands are needed.
双击Stonebound.exe即可游玩，无需安装Python、Git或Node。

Windows 10/11 x64 and Microsoft Edge WebView2 are required. WebView2 is already
present on most current Windows installations. If absent, install Microsoft's
WebView2 Evergreen Runtime once: https://developer.microsoft.com/microsoft-edge/webview2/
需要Windows 10/11 64位及Microsoft Edge WebView2（多数现代Windows已自带）。

The game runs in its own desktop window. English / 简体中文 can be selected with
the top-right language button or Settings. Dialogue, items, rules and controls
are translated. The choice is saved with your progress.
游戏在独立窗口中运行。右上角语言按钮或设置中可选择英文/简体中文，语言随存档保存。

EXPANDED ADVENTURE
24 rivals in 8 chapters, 24 boards and 24 stone sets, and 16 manga pages with
48 illustrated panels. Read arrivals before encounters and conclusions after
three chapter wins. Replay unlocked manga in Chronicle. Eight keepsakes are
earned by completing chapters. New materials appear on the actual Go board.
8章、24位棋友、48件藏品、16篇漫画（共48格）。每章三场胜利解锁结章与专属纪念品。
故事册可重看已解锁漫画，漫画对白可即时切换中英文。旧存档自动补发已完成章节纪念品。

GHOST MASTER / 棋灵师父
Yangui (砚归), an original ancient Go-master ghost, travels with you. Read his
awakening and homecoming manga, plus eight chapter reflections in Chronicle.
Ask Sensei shows an actual KataGo move recommendation and a territory estimate.
Large estimated point losses trigger Classical Chinese advice with translations.
原创新棋灵「砚归」相伴八章旅途，另有觉醒与归来两篇漫画（故事共18篇、54格）。
「请教师父」可看KataGo推荐落点与地盘估计；明显失误会触发文言训诫，并附白话说明。

TERRITORY / 地盘标示
During play, Ask Sensei enables a toggleable ownership estimate. Black/white
squares mark confident empty points; gray dots are uncertain. After two passes,
final territory and crossed-out dead stones match the Chinese area count.
After resignation, the overlay is an estimate and the result remains W+R.
局中形势仅为估计；双方停着后显示终局地盘、死子红叉与中国规则计分。
认输时只显示形势估计，结果仍为W+R。启程画面可回看上一局。

BACKGROUND MUSIC / 背景音乐
Four CC0 tracks by The Cynic Project play in a looping playlist, bundled for
offline use. Music starts after your first interaction at 22% volume. Use the
musical-note button to pause/resume, or Settings to adjust volume and select
tracks. Stone sounds and music have separate switches. Preferences are saved.
内含The Cynic Project的四首CC0音乐，约九分半钟循环播放，可离线聆听。
首次操作后开始播放，默认音量22%。顶部音符按钮可暂停／继续，设置中可调音量和选曲。
音乐与落子音效独立控制，偏好随存档保存。完整曲目来源见MUSIC.md。

PORTABLE SAVES
Everything stays in the data folder beside the EXE, including save.json,
engine caches and webview state. Move the EXE and data folder together.
Choose a writable folder such as Downloads, Desktop, or a USB drive.
存档、引擎缓存等保存在EXE旁的data文件夹。迁移时请将EXE与data一起复制。

The source version's .runtime/save.json can be copied to data/save.json
while the game is closed. Never replace a save you want to keep without a backup.
开发版本的.runtime/save.json可在关闭游戏后复制为data/save.json。

ACTUAL KATRAIN / KATAGO AI
Python, the pinned KaTrain core, KataGo and its neural-network model, fonts and
artwork are embedded. The portable build defaults to the generic x64 CPU engine,
so a dedicated GPU or OpenCL driver is not required. CPU turns can be slower.
内含Python、KaTrain核心、KataGo及模型、字体与美术。默认使用通用CPU引擎，无需独立显卡。

Choose Settings > AI processor > CPU / GPU to switch without losing the current
board. The choice is saved after successful startup. GPU uses bundled OpenCL
KataGo and needs compatible graphics drivers; first startup may take a few
minutes to tune. A failed switch keeps the previous engine and board.
设置 > AI运算设备可选择CPU或GPU，保留当前棋局，切换成功后自动保存选择。
GPU需要支持OpenCL的显卡驱动，首次启动可能需要数分钟调优。失败时保留原引擎。

19x19 stone placement no longer waits for engine analysis. Your stone appears
immediately while Sensei and your rival think in the background.
19路落子不再等待引擎分析，棋子立即显示，师父与对手继续在后台思考。

Advanced users can still configure custom model/search settings using
engine-config.json beside the EXE. An explicit in-game choice selects the
bundled executable, overriding a custom executable path.

SCORING
Chinese area scoring, 6.5 komi. Play out unsettled groups before both players pass.
采用中国规则，贴6.5目。双方停着前，请先走清尚未确定死活的棋块。

TROUBLESHOOTING
If startup fails, see data/desktop.log. The first launch may take a few seconds
to unpack and load the model. This release is unsigned; no signing identity is
configured. Redistribution notices are in THIRD_PARTY_NOTICES.md and embedded
in the executable. Extract the ZIP to a folder before running.
遇到启动问题请查看data/desktop.log。首次启动需要解包并载入模型，请稍候。
