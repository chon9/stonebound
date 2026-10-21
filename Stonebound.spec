# Build with .venv/Scripts/python.exe -m PyInstaller --noconfirm Stonebound.spec
from pathlib import Path
import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

root = Path(SPECPATH)
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_FILELOG'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'
os.environ['KIVY_LOG_MODE'] = 'PYTHON'
os.environ['KIVY_HOME'] = str(root/'.runtime/build-kivy')
katrain = root / 'vendor/katrain/katrain'
datas = [(str(root/'web'), 'web'), (str(root/'resources/cpu'), 'resources/cpu'),
         (str(root/'resources/licenses'), 'licenses/dependencies'),
         (str(katrain/'config.json'), 'katrain'), (str(katrain/'models/b10c384h6nbttflrs.bin.gz'), 'katrain/models'),
         (str(katrain/'i18n/locales/en'), 'katrain/i18n/locales/en'),
         (str(root/'vendor/katrain/LICENSE'), 'licenses/katrain'),
         (str(root/'THIRD_PARTY_NOTICES.md'), 'licenses'), (str(root/'ASSETS.md'), 'licenses'),
         (str(root/'content/art-prompts.json'), 'content'), (str(root/'content/art-corrections.json'), 'content')]
for file in (katrain/'KataGo').iterdir():
    if file.suffix.lower() in ('.exe', '.dll', '.cfg', '.pem'):
        datas.append((str(file), 'katrain/KataGo'))
datas += collect_data_files('webview')
datas += collect_data_files('kivy', includes=['data/logo/*'], subdir=None)
# PyInstaller's Kivy runtime hook expects its static files under kivy_install.
datas = [(source, destination.replace('\\', '/').replace('kivy/data/logo', 'kivy_install/data/logo')) for source, destination in datas]
a = Analysis([str(root/'desktop.py')], pathex=[str(root), str(root/'vendor/katrain')],
             binaries=collect_dynamic_libs('webview'), datas=datas,
             hiddenimports=['katrain.core.ai', 'katrain.core.engine', 'katrain.core.game',
                            'webview.platforms.winforms', 'webview.platforms.edgechromium', 'clr', 'pythonnet'],
             excludes=['PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'cefpython3', 'matplotlib', 'numpy', 'pandas', 'tkinter'],
             hookspath=[str(root/'scripts/hooks')], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='Stonebound', debug=False, strip=False, upx=False,
          console=False, icon=str(root/'web/assets/stonebound.ico'), disable_windowed_traceback=False)
