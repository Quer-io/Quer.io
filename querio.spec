# -*- mode: python -*-

block_cipher = None


a = Analysis(['application/querio.py'],
             pathex=['application/', '/Users/ossi/Documents/Quer.io'],
             binaries=[],
             datas=[('application/configuration.ini', 'application'), ('application/userInterface.kv', 'application')],
             hiddenimports=[],
             hookspath=['hookfiles'],
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
          [],
          exclude_binaries=True,
          name='querio',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='querio')
app = BUNDLE(coll,
             name='querio.app',
             icon=None,
             bundle_identifier=None)
