import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from frontend.client_data_analising_tool import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = MainWindow() # Backend-макет
    window = Ui_MainWindow() # Backend+Frontend-макет
    # window.showMaximized()
    window.show()
    sys.exit(app.exec())