from archive.gui import MainWindow
from bot import Bot
from archive.gui import MainWindow
import sys
import threading
from PyQt6.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()

    bot = Bot(window)
    window.equalBots(bot)
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()