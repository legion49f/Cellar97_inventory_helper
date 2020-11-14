# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['GUI.pyw'],
             pathex=['C:\\Users\\Legion49F\\Documents\\Gitlab Projects\\cellar97-inventory-management-system\\BUILD'],
             binaries=[],
             datas=[('banner.png', '.'), ('cellar97.ico', '.')],
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
          name='Cellar 97 Inventory Management.exe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='cellar97.ico')
