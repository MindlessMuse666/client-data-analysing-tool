import os

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (QFileDialog, QMessageBox, QMainWindow, QStyledItemDelegate, QHeaderView, QVBoxLayout, QPushButton, QTableView, QLabel, QComboBox, QWidget, QVBoxLayout, QMenu, QApplication)

import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5agg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from data_processing.data_handling import DataHandler
from frontend.client_data_analising_tool import Ui_MainWindow
from model.pandas_model import PandasModel
from plotting.plot_handler import PlotHandler


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("CheCloud")
        self.setWindowIcon(QIcon('static/images/main_icon.ico'))
        self.data_handler = DataHandler()
        self.plot_handler = PlotHandler()

        #self.plot_widget = None

        # Связываем кнопки и комбобоксы с методами
        self.choice_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_to_db)
        self.build_graph_button.clicked.connect(self.plot_chart)
        self.comboBox.currentIndexChanged.connect(self.update_plot_button)  # Тип графика
        self.comboBox_2.currentIndexChanged.connect(self.update_plot_button) # Ось X (для диаграммы рассеяния)
        self.comboBox_3.currentIndexChanged.connect(self.update_plot_button) # Ось Y (для диаграммы рассеяния)
        self.comboBox_4.currentIndexChanged.connect(self.update_plot_button) # Колонка (для остальных типов графиков)


        self.last_file_path = self.data_handler.load_last_file_path()
        if self.last_file_path and os.path.exists(self.last_file_path):
            self.open_file(self.last_file_path)

        self.update_plot_button() # Инициализация состояния кнопки "Построить график"


    @pyqtSlot()
    def open_file(self, file_name=None):
        if file_name is None:
            file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")
            if not file_name:
                return

        try:
            self.file_path_label.setText(f"Путь к файлу: {file_name}")
            self.data_handler.load_csv(file_name)
            self.display_data(self.data_handler.df)
            self.data_handler.save_last_file_path(file_name)  # Сохраняем путь после успешной загрузки

        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке файла: {e}")

    def display_data(self, df):
        model = PandasModel(df)
        self.data_table.setModel(model)
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()

        self.data_table.setModel(model)
        # Автоматическое изменение размера столбцов
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Центрирование содержимого ячеек
        delegate = AlignDelegate()  # Создаем делегат для выравнивания
        self.data_table.setItemDelegate(delegate)

        if not df.empty:
            self.comboBox_2.addItems(df.columns)
            self.comboBox_3.addItems(df.columns)
            self.comboBox_4.addItems(df.columns)
        self.update_plot_button()



    def update_plot_button(self):
        chart_type = self.comboBox.currentText()
        enabled = not self.data_handler.df.empty

        self.comboBox_2.setVisible(chart_type == "Диаграмма рассеяния")
        self.comboBox_3.setVisible(chart_type == "Диаграмма рассеяния")
        self.comboBox_4.setVisible(chart_type != "Диаграмма рассеяния")


        if chart_type == "Диаграмма рассеяния":
            enabled = enabled and self.comboBox_2.count() > 0 and self.comboBox_3.count() > 0 and self.comboBox_2.currentIndex() != -1 and self.comboBox_3.currentIndex() != -1
        elif chart_type in ["Гистограмма", "Линейный график", "Столбчатая диаграмма", "Круговая диаграмма"]:
            enabled = enabled and self.comboBox_4.count() > 0 and self.comboBox_4.currentIndex() != -1

        self.build_graph_button.setEnabled(enabled)

    def plot_chart(self):
        if not self.data_handler.df.empty:
            chart_type = self.comboBox.currentText()
            x_axis = self.comboBox_2.currentText() if chart_type == "Диаграмма рассеяния" else None
            y_axis = self.comboBox_3.currentText() if chart_type == "Диаграмма рассеяния" else None
            column = self.comboBox_4.currentText() if chart_type != "Диаграмма рассеяния" else None

            # fig, ax = plt.subplots()
            # self.plot_handler.plot(self.data_handler.df, self.comboBox.currentText(),
            #                        self.comboBox_2.currentText(), self.comboBox_3.currentText(),
            #                        self.comboBox_4.currentText(), ax)  # Передаем ax в plot_handler
            #
            # if self.plot_widget:  # Удаляем старый виджет, если он есть
            #     self.gridLayout.removeWidget(self.plot_widget)
            #     self.plot_widget.deleteLater()
            #
            # self.plot_widget = PlotWidget(fig)  # Создаем новый виджет
            # self.gridLayout.addWidget(self.plot_widget, 4, 0, 1, 4)  # Добавляем его в layout
            # self.plot_widget.show()

            self.plot_handler.plot(self.data_handler.df, chart_type, x_axis, y_axis, column)
        else:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")

    def save_to_db(self):
        self.data_handler.save_to_db()


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter # Выравнивание по центру


# class PlotWidget(QWidget):  # Новый виджет для графика
#     def __init__(self, figure):
#         super().__init__()
#         self.figure = figure
#         canvas = FigureCanvas(figure)
#         layout = QVBoxLayout()
#         layout.addWidget(canvas)
#         self.setLayout(layout)