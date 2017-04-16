# -*- mode: python -*-

block_cipher = None

data_and_path = [('.\\ntfy\\icon.*','ntfy'),
                  ('.\\ntfy\\shell_integration\*', 'ntfy\\shell_integration')
                ]
a = Analysis(['__main__.py'],
             pathex=['.'],
             binaries=None,
             datas=data_and_path,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ntfy',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ntfy')
