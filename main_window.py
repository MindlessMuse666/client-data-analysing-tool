import sys

import PyQt6.QtGui
import matplotlib.cm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTableView, QFileDialog, QHBoxLayout, QLabel, QHeaderView,
                             QMessageBox)
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.uic.Compiler.qtproxies import QtGui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CheCloud")
        self.setWindowIcon(QIcon('static/images/sato.ico'))

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
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

        if file_name:
            try:
                self.file_label.setText(file_name)
                df = pd.read_csv(file_name, sep=';')
                self.display_data(df)
            except pd.errors.EmptyDataError:
                self.display_data(pd.DataFrame())
                print("Файл пустой")
            except pd.errors.ParserError:
                self.display_data(pd.DataFrame())
                print("Ошибка парсинга файла")
            except Exception as e:
                print(f"Ошибка: {e}")
                self.display_data(pd.DataFrame())

        self.df = df


    def display_data(self, df):
        model = PandasModel(df)
        self.table_view.setModel(model)

        # Добавляем кнопку для построения графика
        plot_button = QPushButton("Построить гистограмму")
        plot_button.clicked.connect(self.plot_histogram)
        self.layout().addWidget(plot_button)

    def plot_histogram(self):
        if not hasattr(self, 'df'):
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите данные")
            return

        if self.df.empty:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")
            return

        try:
            # Выбор столбца для построения гистограммы (можно сделать более сложный выбор)
            column_to_plot = self.df.columns[0]

            fig, ax = plt.subplots()
            ax.hist(self.df[column_to_plot].dropna(), bins=10)  #dropna() - удаляем NaN
            ax.set_xlabel(column_to_plot)
            ax.set_ylabel("Частота")
            ax.set_title(f"Гистограмма для столбца '{column_to_plot}'")
            #turbo_cm = matplotlib.cm.get_cmap('turbo')
            #colors = [turbo_cm(v) for v in np.linspace(0, 1, len(self.df))] #Смена цвета столбцов
            #self.df.Count.plot(kind="bar", legend=False, color=colors)
            #Показываем график в отдельном окне
            plt.show()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при построении графика: {e}")


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
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
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.setWindowIcon(QIcon('sato.ico'))
    window.show()
    sys.exit(app.exec())