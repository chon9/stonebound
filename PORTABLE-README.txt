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

For faster play on compatible hardware, place engine-config.json beside the EXE
and point its katago, model and config fields to your existing KataGo installation.
This changes acceleration, not the KaTrain AI strategy. Paths must be absolute.

SCORING
Chinese area scoring, 6.5 komi. Play out unsettled groups before both players pass.
采用中国规则，贴6.5目。双方停着前，请先走清尚未确定死活的棋块。

TROUBLESHOOTING
If startup fails, see data/desktop.log. The first launch may take a few seconds
to unpack and load the model. This release is unsigned; no signing identity is
configured. Redistribution notices are in THIRD_PARTY_NOTICES.md and embedded
in the executable. Extract the ZIP to a folder before running.
遇到启动问题请查看data/desktop.log。首次启动需要解包并载入模型，请稍候。
