import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableView,
                             QFileDialog, QHBoxLayout, QLabel, QHeaderView,
                             QMessageBox, QComboBox)

from data_processing.data_handling import DataHandler
from model.pandas_model import PandasModel
from plotting.plot_handler import PlotHandler


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CheCloud")
        self.setWindowIcon(QIcon('static/images/icon.ico'))
        self.data_handler = DataHandler()
        self.plot_handler = PlotHandler()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        button_layout = QHBoxLayout()
        self.file_label = QLabel("Файл не выбран")
        button_layout.addWidget(self.file_label)
        open_button = QPushButton("Выберите CSV файл")
        open_button.clicked.connect(self.open_file)
        button_layout.addWidget(open_button)
        main_layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_view)

        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Гистограмма", "Диаграмма рассеяния", "Линейный график", "Столбчатая диаграмма", "Круговая диаграмма"])
        self.chart_type_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.chart_type_combo)

        self.x_axis_combo = QComboBox()
        self.x_axis_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.x_axis_combo)

        self.y_axis_combo = QComboBox()
        self.y_axis_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.y_axis_combo)

        self.column_combo = QComboBox()
        self.column_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.column_combo)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_chart)
        self.plot_button.setEnabled(False)
        main_layout.addWidget(self.plot_button)

        save_button = QPushButton("Сохранить данные")
        save_button.clicked.connect(self.save_to_db)
        main_layout.addWidget(save_button)


        self.last_file_path = self.data_handler.load_last_file_path()
        if self.last_file_path and os.path.exists(self.last_file_path):
            self.open_file(self.last_file_path)


    @pyqtSlot()
    def open_file(self, file_name=None):
        if file_name is None:
            file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")
            if file_name is None:
                return

        try:
            self.file_label.setText(file_name)
            self.data_handler.load_csv(file_name)
            self.display_data(self.data_handler.df)
            self.data_handler.save_to_db()
            self.data_handler.save_last_file_path(file_name)

        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке файла: {e}")


    def display_data(self, df):
        model = PandasModel(df)
        self.table_view.setModel(model)
        self.x_axis_combo.clear()
        self.y_axis_combo.clear()
        self.column_combo.clear()

        if not df.empty:
            self.x_axis_combo.addItems(df.columns)
            self.y_axis_combo.addItems(df.columns)
            self.column_combo.addItems(df.columns)

        self.update_plot_button()

    def update_plot_button(self):
        chart_type = self.chart_type_combo.currentText()
        enabled = not self.data_handler.df.empty

        self.x_axis_combo.setVisible(chart_type == "Диаграмма рассеяния")
        self.y_axis_combo.setVisible(chart_type == "Диаграмма рассеяния")
        self.column_combo.setVisible(chart_type != "Диаграмма рассеяния")

        if chart_type == "Диаграмма рассеяния":
            enabled = enabled and self.x_axis_combo.count() > 0 and self.y_axis_combo.count() > 0 and self.x_axis_combo.currentIndex() != -1 and self.y_axis_combo.currentIndex() != -1
        elif chart_type in ["Гистограмма", "Линейный график", "Столбчатая диаграмма", "Круговая диаграмма"]:
            enabled = enabled and self.column_combo.count() > 0 and self.column_combo.currentIndex() != -1

        self.plot_button.setEnabled(enabled)

    def plot_chart(self):
        if not self.data_handler.df.empty:
            self.plot_handler.plot(self.data_handler.df, self.chart_type_combo.currentText(),
                                   self.x_axis_combo.currentText(), self.y_axis_combo.currentText(),
                                   self.column_combo.currentText())
        else:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")

    def save_to_db(self):
        self.data_handler.save_to_db()