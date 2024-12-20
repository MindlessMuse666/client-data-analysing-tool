import os

import matplotlib.pyplot as plt
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QFileDialog, QMessageBox, QMainWindow, QStyledItemDelegate, QHeaderView, QVBoxLayout,
                             QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from data_processing.data_handling import DataHandler
from frontend.client_data_analising_tool import Ui_MainWindow
from model.pandas_model import PandasModel
from plotting.plot_handler import PlotHandler


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("CheCloud")
        self.setWindowIcon(QIcon("static/images/main_icon.ico"))

        self.data_handler = DataHandler()
        self.plot_handler = PlotHandler()
        self.plot_widget = None

        self.choice_button.clicked.connect(self._on_choice_button_clicked)
        self.save_button.clicked.connect(self.save_to_db)
        self.build_graph_button.clicked.connect(self.plot_chart)
        self.sort_button.clicked.connect(self.sort_data)
        self.comboBox.currentIndexChanged.connect(self.update_plot_button)
        self.comboBox_2.currentIndexChanged.connect(self.update_plot_button)
        self.comboBox_3.currentIndexChanged.connect(self.update_plot_button)
        self.comboBox_4.currentIndexChanged.connect(self.update_plot_button)

        self.show()
        self.update_plot_button()
        self.open_file()

    @pyqtSlot()
    def open_file(self):
        self.last_file_path = self.data_handler.load_last_file_path()
        if self.last_file_path and os.path.exists(self.last_file_path):
            self._load_and_display_data(self.last_file_path)
        else:
            self._on_choice_button_clicked()

    def _open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

    def _on_choice_button_clicked(self):
        file_name, _ = self._open_file_dialog()
        if file_name:
            self._load_and_display_data(file_name)

    def _load_and_display_data(self, file_name):
        try:
            self.data_handler.load_csv(file_name)
            self.display_data(self.data_handler.df)
            self.data_handler.save_last_file_path(file_name)
            self.file_path_label.setText(f"Путь к файлу: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке файла: {e}")

    def sort_data(self):
        column_name = self.sort_column_combo.currentText()
        sort_order = self.sort_order_combo.currentText()
        if column_name:
            try:
                ascending = sort_order == "Возрастанию"
                self.data_handler.sort_dataframe(column_name, ascending)
                self.display_data(self.data_handler.df)
            except KeyError:
                QMessageBox.warning(self, "Ошибка", f"Столбец '{column_name}' не найден.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сортировке: {e}")

    def display_data(self, df):
        model = PandasModel(df)
        self.data_table.setModel(model)
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.sort_column_combo.clear()  # Очищаем комбобокс столбцов

        self.data_table.setModel(model)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        delegate = AlignDelegate()
        self.data_table.setItemDelegate(delegate)

        if not df.empty:
            self.comboBox_2.addItems(df.columns)
            self.comboBox_3.addItems(df.columns)
            self.comboBox_4.addItems(df.columns)
            self.sort_column_combo.addItems(df.columns) # Добавляем столбцы в комбобокс для сортировки

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

    @pyqtSlot()
    def plot_chart(self):
        if not self.data_handler.df.empty:
            chart_type, x_axis, y_axis, column = self._get_plot_parameters()
            if self._validate_plot_parameters(chart_type, x_axis, y_axis, column):
                fig, ax = plt.subplots(figsize=(10, 6))

                if self.plot_handler.plot(self.data_handler.df, chart_type, x_axis, y_axis, column, ax):
                    self._show_plot_widget(fig)
        else:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")

    def _create_and_show_plot(self, chart_type, x_axis, y_axis, column):
        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            self.plot_handler.plot(self.data_handler.df, chart_type, x_axis, y_axis, column, ax)
            self._show_plot_widget(fig)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при построении графика: {e}")

    def _get_plot_parameters(self):
        chart_type = self.comboBox.currentText()
        x_axis = self.comboBox_2.currentText() if chart_type == "Диаграмма рассеяния" else None
        y_axis = self.comboBox_3.currentText() if chart_type == "Диаграмма рассеяния" else None
        column = self.comboBox_4.currentText() if chart_type != "Диаграмма рассеяния" else None
        return chart_type, x_axis, y_axis, column

    def _validate_plot_parameters(self, chart_type, x_axis, y_axis, column):
        if chart_type == "Диаграмма рассеяния":
            if not x_axis or not y_axis:
                QMessageBox.warning(self, "Ошибка", "Для диаграммы рассеяния необходимо выбрать оси X и Y.")
                return False
        elif chart_type != "Диаграмма рассеяния" and not column:
            QMessageBox.warning(self, "Ошибка", f"Для {chart_type} необходимо выбрать столбец.")
            return False
        return True

    def _show_plot_widget(self, fig):
        if self.plot_widget:
            self.gridLayout.removeWidget(self.plot_widget)
            self.plot_widget.deleteLater()
        self.plot_widget = PlotWidget(fig)
        self.plot_widget.setWindowTitle("График")
        self.plot_widget.showMaximized()

    def save_to_db(self):
        self.data_handler.save_to_db()


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class PlotWidget(QWidget):
    def __init__(self, fig):
        super().__init__()
        self.canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)