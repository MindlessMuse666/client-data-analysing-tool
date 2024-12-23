import os

import matplotlib.pyplot as plt
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import (QFileDialog, QMessageBox, QMainWindow, QStyledItemDelegate, QHeaderView, QVBoxLayout,
                             QDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from data_processing.data_handling import DataHandler
from data_processing.report_generator import ReportGenerator
from frontend.client_data_analising_tool import GuiMainWindow
from model.pandas_model import PandasModel
from plotting.plot_handler import PlotHandler


class MainWindow(QMainWindow, GuiMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_gui(self)

        self.data_handler = DataHandler()
        self.plot_handler = PlotHandler()
        self.plot_window = None  # Изменили на PlotWindow
        self.report_generator = ReportGenerator()

        self.choice_button.clicked.connect(self._on_choice_button_clicked)
        self.save_button.clicked.connect(self._on_save_button_clicked)  # Добавили обработчик кнопки
        self.report_button.clicked.connect(self._on_report_button_clicked)
        self.build_graph_button.clicked.connect(self.plot_chart)
        self.sort_button.clicked.connect(self.sort_data)
        self.graph_type_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.x_axis_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.y_axis_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.column_combo_box.currentIndexChanged.connect(self.update_plot_button)

        self.showMaximized()
        self.update_plot_button()
        self.open_file()

    def closeEvent(self, event):
        self.data_handler.save_to_db()  # Сохраняем перед закрытием
        event.accept()

    @pyqtSlot()
    def open_file(self):
        self.last_file_path = self.data_handler.load_last_file_path()
        if self.last_file_path and os.path.exists(self.last_file_path):
            self._load_and_display_data(self.last_file_path)
            self.data_handler.load_from_db()  # Загружаем данные из БД при открытии
            self.display_data(self.data_handler.df)
        else:
            self._on_choice_button_clicked()

    def _open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

    def _on_choice_button_clicked(self):
        file_name, _ = self._open_file_dialog()
        if file_name:
            self._load_and_display_data(file_name)
            self.data_handler.save_to_db()

    def _load_and_display_data(self, file_name):
        try:
            self.data_handler.load_csv(file_name)
            self.display_data(self.data_handler.df)
            self.data_handler.save_last_file_path(file_name)
            self.file_path_label.setText(file_name)
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке файла: {e}")

    def sort_data(self):
        column_name = self.sort_column_combo_box.currentText()
        sort_order = self.sort_order_combo_box.currentText()
        if column_name:
            try:
                ascending = sort_order == "Возрастанию"
                self.data_handler.sort_dataframe(column_name, ascending)
                self.display_data(self.data_handler.df)
                self.data_handler.save_to_db()
            except KeyError:
                QMessageBox.warning(self, "Ошибка", f"Столбец '{column_name}' не найден.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сортировке: {e}")

    def display_data(self, df):
        model = PandasModel(df)
        self.data_table.setModel(model)
        self.x_axis_combo_box.clear()
        self.y_axis_combo_box.clear()
        self.column_combo_box.clear()
        self.sort_column_combo_box.clear()  # Очищаем комбобокс столбцов

        self.data_table.setModel(model)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        delegate = AlignDelegate()
        self.data_table.setItemDelegate(delegate)

        # Устанавливаем связь с dataChanged после установки модели
        self.data_table.model().dataChanged.connect(self._on_data_changed)

        if not df.empty:
            self.x_axis_combo_box.addItems(df.columns)
            self.y_axis_combo_box.addItems(df.columns)
            self.column_combo_box.addItems(df.columns)
            self.sort_column_combo_box.addItems(df.columns)  # Добавляем столбцы в комбобокс для сортировки

        self.update_plot_button()

    def _on_data_changed(self, topLeft, bottomRight, roles=None):
        if Qt.ItemDataRole.EditRole in (
                roles or [Qt.ItemDataRole.EditRole]):  # Проверка, что изменение - редактирование
            self.data_handler.save_to_db()

    def update_plot_button(self):
        chart_type = self.graph_type_combo_box.currentText()
        enabled = not self.data_handler.df.empty

        x_axis_visible = chart_type in ["Диаграмма рассеяния", "Линейный график"]
        y_axis_visible = chart_type in ["Диаграмма рассеяния", "Линейный график"]
        column_visible = chart_type not in ["Диаграмма рассеяния", "Линейный график"]

        self.x_axis_label.setVisible(x_axis_visible)
        self.y_axis_label.setVisible(y_axis_visible)
        self.column_label.setVisible(column_visible)

        self.x_axis_combo_box.setVisible(x_axis_visible)
        self.y_axis_combo_box.setVisible(y_axis_visible)
        self.column_combo_box.setVisible(column_visible)

        if chart_type == "Диаграмма рассеяния":
            enabled = enabled and self.x_axis_combo_box.count() > 0 and self.y_axis_combo_box.count() > 0 and self.x_axis_combo_box.currentIndex() != -1 and self.y_axis_combo_box.currentIndex() != -1
        elif chart_type == "Линейный график":
            enabled = enabled and self.x_axis_combo_box.count() > 0 and self.y_axis_combo_box.count() > 0 and self.x_axis_combo_box.currentIndex() != -1 and self.y_axis_combo_box.currentIndex() != -1
        elif chart_type in ["Гистограмма", "Столбчатая диаграмма", "Круговая диаграмма"]:
            enabled = enabled and self.column_combo_box.count() > 0 and self.column_combo_box.currentIndex() != -1

        self.build_graph_button.setEnabled(enabled)

    @pyqtSlot()
    def plot_chart(self):
        if not self.data_handler.df.empty:
            chart_type, x_axis, y_axis, column = self._get_plot_parameters()
            if self._validate_plot_parameters(chart_type, x_axis, y_axis, column):
                self._create_and_show_plot(chart_type, x_axis, y_axis, column)
        else:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")

    def _create_and_show_plot(self, chart_type, x_axis, y_axis, column):
        try:
            self.plot_window = PlotWindow(self.data_handler.df, chart_type, x_axis, y_axis, column, self)  # Передаём df
            self.plot_window.show()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при построении графика: {e}")

    def _get_plot_parameters(self):
        chart_type = self.graph_type_combo_box.currentText()
        x_axis = self.x_axis_combo_box.currentText() if chart_type in ["Диаграмма рассеяния", "Линейный график"] else None
        y_axis = self.y_axis_combo_box.currentText() if chart_type in ["Диаграмма рассеяния", "Линейный график"] else None
        column = self.column_combo_box.currentText() if chart_type not in ["Диаграмма рассеяния", "Линейный график"] else None
        return chart_type, x_axis, y_axis, column

    def _validate_plot_parameters(self, chart_type, x_axis, y_axis, column):
        if chart_type == "Диаграмма рассеяния":
            if not x_axis or not y_axis:
                QMessageBox.warning(self, "Ошибка", "Для диаграммы рассеяния необходимо выбрать оси X и Y.")
                return False
        elif chart_type == "Линейный график":
             if not x_axis or not y_axis:
                 QMessageBox.warning(self, "Ошибка", "Для линейного графика необходимо выбрать оси X и Y.")
                 return False
             if not (pd.api.types.is_numeric_dtype(self.data_handler.df[x_axis]) and pd.api.types.is_numeric_dtype(self.data_handler.df[y_axis])):
                 QMessageBox.warning(self, "Ошибка", "Оси X и Y должны содержать числовые данные.")
                 return False
        elif chart_type not in ["Диаграмма рассеяния", "Линейный график"] and not column:
            QMessageBox.warning(self, "Ошибка", f"Для {chart_type} необходимо выбрать столбец.")
            return False
        return True

    @pyqtSlot()
    def _on_save_button_clicked(self):
        self.data_handler.save_to_db()
        QMessageBox.information(self, "Успех", "Данные успешно сохранены в базу данных.")


    @pyqtSlot()
    def _on_report_button_clicked(self):
        if self.data_handler.df.empty:
            QMessageBox.warning(self, "Ошибка", "Нет данных для создания отчёта.")
            return
        self._save_report_to_file()


    def _save_report_to_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(".pdf")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить отчёт", "", "PDF files (*.pdf)")

        if file_path:
            try:
               self.report_generator.generate_report(self.data_handler.df, file_path)
               QMessageBox.information(self, "Успех", f"Отчет сохранен в {file_path}")
            except Exception as e:
               QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения отчета: {e}")

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class PlotWindow(QDialog):  # Изменили на QDialog
    def __init__(self, df, chart_type, x_axis, y_axis, column, parent=None):
        super().__init__(parent)
        self.setWindowTitle("График")
        self.plot_handler = PlotHandler()
        self.df = df
        self.chart_type = chart_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.column = column

        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_chart()

    def plot_chart(self):
        try:
            if not self.plot_handler.plot(self.df, self.chart_type, self.x_axis, self.y_axis, self.column, self.ax):
                plt.close(self.figure)
                return
            self.canvas.draw()
        except Exception:
            plt.close(self.figure)
            return