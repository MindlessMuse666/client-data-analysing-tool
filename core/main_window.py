import os
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QHeaderView
import pandas as pd

from data_processing.data_handler import DataHandler
from data_processing.report_handler import ReportHandler
from frontend.gui_main_window import GuiMainWindow
from model.pandas_model import PandasModel
from plotting.plot_handler import PlotHandler
from core.table_window import TableWindow
from model.align_delegate import AlignDelegate
from plotting.plot_window import PlotWindow


class MainWindow(QMainWindow, GuiMainWindow):
    """
    Основное окно приложения, объединяющее все функциональные компоненты.

    Attributes:
        data_handler (DataHandler): Обработчик данных.
        plot_handler (PlotHandler): Обработчик графиков.
        report_generator (ReportHandler): Обработчик отчетов.
        plot_window (PlotWindow): Окно для отображения графиков.
        table_window (TableWindow): Окно для отображения таблицы данных.
        last_file_path (str): Путь к последнему открытому файлу.
    """
    def __init__(self):
        """Инициализирует главное окно приложения."""
        super().__init__()

        self.setup_gui(self)

        self.data_handler = DataHandler()
        self.plot_handler = PlotHandler()
        self.report_generator = ReportHandler()

        self.plot_window = None
        self.table_window = None
        self.last_file_path = None

        self.choice_button.clicked.connect(self._on_choice_button_clicked)
        self.save_button.clicked.connect(self._on_save_button_clicked)
        self.report_button.clicked.connect(self._on_report_button_clicked)
        self.build_graph_button.clicked.connect(self.plot_chart)
        self.sort_button.clicked.connect(self.sort_data)
        self.graph_type_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.x_axis_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.y_axis_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.column_combo_box.currentIndexChanged.connect(self.update_plot_button)
        self.expand_table_button.clicked.connect(self._on_expand_table_button_clicked)

        self.showMaximized()
        self.update_plot_button()
        self.open_file()

    def closeEvent(self, event):
        """
         Обработчик события закрытия окна.
         Сохраняет данные в базу данных перед закрытием.
        """
        self.data_handler.save_to_db()
        event.accept()

    @pyqtSlot()
    def open_file(self):
        """
         Открывает последний открытый файл при запуске приложения.
         Если файл не найден или не существует, открывает диалог выбора файла.
        """
        self.last_file_path = self.data_handler.load_last_file_path()
        if self.last_file_path and os.path.exists(self.last_file_path):
            self._load_and_display_data(self.last_file_path)
            self.data_handler.load_from_db()
            self.display_data(self.data_handler.df)
        else:
            self._on_choice_button_clicked()

    def _open_file_dialog(self):
        """
        Открывает диалог выбора файла.

        Returns:
            tuple: Имя файла и его расширение.
        """
        return QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

    @pyqtSlot()
    def _on_choice_button_clicked(self):
        """
        Обработчик события нажатия кнопки выбора файла.
        Открывает диалог выбора файла и загружает данные.
        """
        file_name, _ = self._open_file_dialog()
        if file_name:
            self._load_and_display_data(file_name)
            self.data_handler.save_to_db()

    def _load_and_display_data(self, file_name):
        """
         Загружает данные из CSV файла и отображает их в таблице.
         Сохраняет путь к файлу в базу данных.

        Args:
            file_name (str): Путь к файлу.
        """
        try:
            self.data_handler.load_csv(file_name)
            self.display_data(self.data_handler.df)
            self.data_handler.save_last_file_path(file_name)
            self.file_path_label.setText(file_name[0: 80] + "...")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке файла: {e}")

    @pyqtSlot()
    def sort_data(self):
        """
        Обработчик события нажатия кнопки сортировки.
        Сортирует данные в таблице по выбранному столбцу и порядку.
        """
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
        """
        Отображает DataFrame в таблице.

        Args:
            df (pd.DataFrame): DataFrame для отображения.
        """
        model = PandasModel(df)
        self.data_table.setModel(model)
        self.x_axis_combo_box.clear()
        self.y_axis_combo_box.clear()
        self.column_combo_box.clear()
        self.sort_column_combo_box.clear()

        self.data_table.setModel(model)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        delegate = AlignDelegate()
        self.data_table.setItemDelegate(delegate)

        self.data_table.model().dataChanged.connect(self._on_data_changed)

        if not df.empty:
            self.x_axis_combo_box.addItems(df.columns)
            self.y_axis_combo_box.addItems(df.columns)
            self.column_combo_box.addItems(df.columns)
            self.sort_column_combo_box.addItems(df.columns)

        self.update_plot_button()

    def _on_data_changed(self, topLeft, bottomRight, roles=None):
        """
        Обработчик события изменения данных в таблице.
        Сохраняет изменения в базу данных.

        Args:
            topLeft (QModelIndex): Верхний левый индекс измененного элемента.
            bottomRight (QModelIndex): Нижний правый индекс измененного элемента.
            roles (list, optional): Список ролей данных, которые были изменены.
        """
        if Qt.ItemDataRole.EditRole in (
                roles or [Qt.ItemDataRole.EditRole]):
            self.data_handler.save_to_db()

    def update_plot_button(self):
        """
        Обновляет состояние кнопки построения графика.
        Управляет видимостью элементов управления осями.
        """
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
        """
        Обработчик события нажатия кнопки построения графика.
        Создает и отображает окно с графиком.
        """
        if not self.data_handler.df.empty:
            chart_type, x_axis, y_axis, column = self._get_plot_parameters()
            if self._validate_plot_parameters(chart_type, x_axis, y_axis, column):
                self._create_and_show_plot(chart_type, x_axis, y_axis, column)
        else:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")

    def _create_and_show_plot(self, chart_type, x_axis, y_axis, column):
        """
        Создает и отображает окно с графиком.

        Args:
            chart_type (str): Тип графика.
            x_axis (str): Ось X.
            y_axis (str): Ось Y.
            column (str): Столбец для графика.
        """
        try:
            self.plot_window = PlotWindow(self.data_handler.df, chart_type, x_axis, y_axis, column, self)
            self.plot_window.show()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при построении графика: {e}")

    def _get_plot_parameters(self):
        """
        Получает параметры для построения графика из выпадающих списков.

        Returns:
            tuple: Тип графика, ось X, ось Y, столбец.
        """
        chart_type = self.graph_type_combo_box.currentText()
        x_axis = self.x_axis_combo_box.currentText() if chart_type in ["Диаграмма рассеяния",
                                                                       "Линейный график"] else None
        y_axis = self.y_axis_combo_box.currentText() if chart_type in ["Диаграмма рассеяния",
                                                                       "Линейный график"] else None
        column = self.column_combo_box.currentText() if chart_type not in ["Диаграмма рассеяния",
                                                                           "Линейный график"] else None
        return chart_type, x_axis, y_axis, column

    def _validate_plot_parameters(self, chart_type, x_axis, y_axis, column):
        """
        Проверяет параметры для построения графика.

        Args:
            chart_type (str): Тип графика.
            x_axis (str): Ось X.
            y_axis (str): Ось Y.
            column (str): Столбец для графика.

        Returns:
            bool: True, если параметры валидны, иначе False.
        """
        if chart_type == "Диаграмма рассеяния":
            if not x_axis or not y_axis:
                QMessageBox.warning(self, "Ошибка", "Для диаграммы рассеяния необходимо выбрать оси X и Y.")
                return False
        elif chart_type == "Линейный график":
            if not x_axis or not y_axis:
                QMessageBox.warning(self, "Ошибка", "Для линейного графика необходимо выбрать оси X и Y.")
                return False
            if not (pd.api.types.is_numeric_dtype(self.data_handler.df[x_axis]) and pd.api.types.is_numeric_dtype(
                    self.data_handler.df[y_axis])):
                QMessageBox.warning(self, "Ошибка", "Оси X и Y должны содержать числовые данные.")
                return False
        elif chart_type not in ["Диаграмма рассеяния", "Линейный график"] and not column:
            QMessageBox.warning(self, "Ошибка", f"Для {chart_type} необходимо выбрать столбец.")
            return False
        return True

    @pyqtSlot()
    def _on_save_button_clicked(self):
        """
         Обработчик события нажатия кнопки сохранения данных.
         Сохраняет данные в базу данных.
        """
        self.data_handler.save_to_db()
        QMessageBox.information(self, "Успех", "Данные успешно сохранены в базу данных.")

    @pyqtSlot()
    def _on_report_button_clicked(self):
        """
        Обработчик события нажатия кнопки создания отчета.
        Создает и сохраняет PDF отчет.
        """
        if self.data_handler.df.empty:
            QMessageBox.warning(self, "Ошибка", "Нет данных для создания отчёта.")
            return
        self._save_report_to_file()

    def _save_report_to_file(self):
        """
         Сохраняет отчет в PDF файл.
        """
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

    @pyqtSlot()
    def _on_expand_table_button_clicked(self):
        """
        Обработчик события нажатия кнопки раскрытия таблицы.
        Открывает таблицу в отдельном окне.
        """
        try:
            model = self.data_table.model()
            if model:
                if self.table_window:
                    self.table_window.close()
                self.table_window = TableWindow(model, self)

                # --- применяем делегат после установки модели ---
                delegate = AlignDelegate()
                for column in range(model.columnCount()):
                    self.table_window.table_view.setItemDelegateForColumn(column, delegate)
                # --- end of applying delegate ---

                self.table_window.closed.connect(self._on_table_window_closed)
                self.table_window.show()
            else:
                QMessageBox.warning(self, "Ошибка", "Нет данных для отображения")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии таблицы: {e}")

    def _on_table_window_closed(self):
        """
        Обработчик события закрытия окна таблицы.
         Обнуляет ссылку на окно таблицы.
        """
        self.table_window = None
