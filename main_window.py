import sys
import pandas as pd
import PyQt6.QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTableView, QFileDialog, QHBoxLayout, QLabel)
from PyQt6.uic.properties import QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QHeaderView # Импортируем QHeaderView


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Data Analyzer")

        # Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Button for file selection
        button_layout = QHBoxLayout()
        self.file_label = QLabel("Файл не выбран")
        button_layout.addWidget(self.file_label)
        open_button = QPushButton("Выберите CSV файл")
        open_button.clicked.connect(self.open_file)
        button_layout.addWidget(open_button)
        main_layout.addLayout(button_layout)


        # Table to display data
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Растягиваем колонки
        main_layout.addWidget(self.table_view)


    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)", options=options)

        if file_name:
            try:
                self.file_label.setText(file_name)
                df = pd.read_csv(file_name)
                self.display_data(df)
            except pd.errors.EmptyDataError:
                self.display_data(pd.DataFrame()) #Обработка пустого файла
                print("Файл пустой")
            except pd.errors.ParserError:
                self.display_data(pd.DataFrame()) #Обработка ошибки парсинга
                print("Ошибка парсинга файла")
            except Exception as e:
                print(f"Ошибка: {e}")
                self.display_data(pd.DataFrame())


    def display_data(self, df):
        model = PandasModel(df)
        self.table_view.setModel(model)


class PandasModel(PyQt6.QtCore.QAbstractTableModel):
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.columns[col])
        return None


if __name__ == "__main__":
    import sys
    from PyQt6 import QtCore
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())