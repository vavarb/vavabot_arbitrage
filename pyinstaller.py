import PyInstaller.__main__

PyInstaller.__main__.run([
    'vavabot_arbitrage_1_2_2.py',
    '--onefile',
    '--noconsole',
    '--key=karenarthur12345',
    '--icon=icon_noctuline_wall_e_eve.ico'

])

# pyinstaller my_script.py --onefile --windowed