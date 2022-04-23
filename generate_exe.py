"""Generate a bundled binary from the main.py with included usblib DLL and Assets folder.

This is the expected file / folder structure:

current_directory
 | - main.py
 | - hidapi.dll
 | - hidapi.lib
 | - hidapi.pdb
 | - README.md
 | - Assets
   | - Roboto-Regular.ttf
   | - Exit.png
   | - Pressed.png
   | - Released.png
   | - ...
"""

import PyInstaller.__main__


PyInstaller.__main__.run([
    'main.py',
    '--clean',
    # '--onefile',
    '--add-binary=hidapi.dll;.',
    '--add-binary=hidapi.lib;.',
    '--add-binary=hidapi.pdb;.',
    '--add-data=README.md;.',
    '--add-data=Assets;Assets',
    # '--noconsole'  # For final version
])
