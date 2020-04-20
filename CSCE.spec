# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['6\\CSCE', '470\\BurningBush\\icon.ico', 'TBB.py'],
             pathex=['C:\\Users\\hanna\\Documents\\Hanna\\TAMU\\Sem 6\\CSCE 470\\BurningBush'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='CSCE',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\hanna\\Documents\\Hanna\\TAMU\\Sem')
