# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import pkg_resources  # part of setuptools
import platform

__version__ = pkg_resources.get_distribution("canguru").version
script_path = pkg_resources.resource_filename('canguru', 'app.py')

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('canguru')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

system = platform.system()
if system == 'Linux':
    hiddenimports+=['can.interfaces.socketcan']
elif system == 'Windows':
    hiddenimports+=['can.interfaces.pcan']
    hiddenimports+=['can.interfaces.vector']
else:
    pass


a = Analysis(
    [script_path],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'CAN-Guru-v{__version__}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)