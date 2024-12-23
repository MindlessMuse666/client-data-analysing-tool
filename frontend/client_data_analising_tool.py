from PyQt6.QtCore import QMetaObject, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QGridLayout, QComboBox, QTableView, \
    QStatusBar, QSizePolicy, QLayout, QHeaderView

from static.resources.resource_pathes.resource_pathes import (choice_icon_path, save_icon_path, graph_icon_path,
                                                              main_icon_path)
from static.styles.styles import button_style, label_style, combobox_style, tableview_style, application_style


def _get_icon(icon_path: str):
    icon: QIcon = QIcon()
    icon.addPixmap(
        QPixmap(icon_path),
        QIcon.Mode.Normal,
        QIcon.State.Off
    )
    return icon

def _get_label(label_text: str):
    label: QLabel = QLabel(label_text)  # Новый QLabel
    label.setStyleSheet(label_style)
    label.setSizePolicy(
        QSizePolicy.Policy.Maximum,
        QSizePolicy.Policy.Maximum
    )
    return label


class GuiMainWindow(object):
    def setup_gui(self, MainWindow):
        MainWindow.setObjectName("main_window")
        MainWindow.setWindowTitle("CheCloud")

        """ Устанавливаем иконку приложения """
        main_icon: QIcon = _get_icon(main_icon_path)
        icon_size = QSize(24, 24)
        MainWindow.setWindowIcon(main_icon)
        MainWindow.setIconSize(icon_size)

        """ Устанавливаем шрифт приложения """
        font = QFont()
        font.setFamily("Secession Text")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)

        """ Устанавливаем дополнительные настройки приложения """
        MainWindow.setAutoFillBackground(False)

        """ Устанавливаем css-стиль приложения """
        MainWindow.setStyleSheet(application_style)


        """ Вертикальный layout для всего окна """
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)


        """ Верхняя панель: Путь к файлу, кнопки "Выбрать файл" и "Сохранить данные" """
        self.file_path_info_label: QLabel = _get_label("Путь к файлу:")
        self.top_panel = QWidget(self.central_widget)
        self.top_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.top_panel_layout = QHBoxLayout(self.top_panel)
        self.top_panel_layout.addWidget(self.file_path_info_label)

        self.file_path_label: QLabel = _get_label("")
        self.file_path_label.setParent(self.top_panel)
        self.top_panel_layout.addWidget(self.file_path_label)

        self.choice_button = QPushButton("Выбрать файл")
        self.choice_button.setStyleSheet(button_style)
        choice_icon: QIcon = _get_icon(choice_icon_path)
        self.choice_button.setIcon(choice_icon)
        self.choice_button.setIconSize(icon_size)
        self.top_panel_layout.addWidget(self.choice_button)

        self.save_button = QPushButton("Сохранить данные")
        self.save_button.setStyleSheet(button_style)
        save_icon: QIcon = _get_icon(save_icon_path)
        self.save_button.setIcon(save_icon)
        self.save_button.setIconSize(icon_size)
        self.top_panel_layout.addWidget(self.save_button)

        self.main_layout.addWidget(self.top_panel)


        """ Панель настроек графика """
        self.graph_type_label: QLabel = _get_label("Тип графика:")
        self.plot_settings_panel = QWidget(self.central_widget)
        self.plot_settings_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.plot_settings_layout = QGridLayout(self.plot_settings_panel)
        self.plot_settings_layout.addWidget(self.graph_type_label, 0, 0)

        self.graph_type_combo_box = QComboBox() # comboBox
        self.graph_type_combo_box.addItems([
            "Гистограмма",
            "Диаграмма рассеяния",
            "Линейный график",
            "Столбчатая диаграмма",
            "Круговая диаграмма"
        ])
        self.graph_type_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.graph_type_combo_box, 0, 1)

        self.x_axis_label: QLabel = _get_label("Ось X:")
        self.x_axis_combo_box = QComboBox() # comboBox_2
        self.x_axis_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.x_axis_label, 1, 0)
        self.plot_settings_layout.addWidget(self.x_axis_combo_box, 1, 1)

        self.y_axis_label: QLabel = _get_label("Ось Y:")
        self.y_axis_combo_box = QComboBox() # comboBox_3
        self.y_axis_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.y_axis_label, 2, 0)
        self.plot_settings_layout.addWidget(self.y_axis_combo_box, 2, 1)

        self.column_label: QLabel = _get_label("Столбец:")
        self.column_combo_box = QComboBox() # comboBox_4
        self.column_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.column_label, 3, 0)
        self.plot_settings_layout.addWidget(self.column_combo_box, 3, 1)

        self.build_graph_button = QPushButton("Построить график")
        self.build_graph_button.setStyleSheet(button_style)
        graph_icon: QIcon = _get_icon(graph_icon_path)
        self.build_graph_button.setIcon(graph_icon)
        self.build_graph_button.setIconSize(icon_size)
        self.plot_settings_layout.addWidget(self.build_graph_button, 4, 0, 1, 2)

        self.main_layout.addWidget(self.plot_settings_panel)


        """ Панель сортировки """
        self.sort_panel = QWidget(self.central_widget)
        self.sort_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.sort_panel_layout_label: QLabel = _get_label("Сортировать по:")
        self.sort_panel_layout = QHBoxLayout(self.sort_panel)
        # self.sort_panel_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.sort_panel_layout.addWidget(self.sort_panel_layout_label)

        self.sort_column_combo_box = QComboBox()
        self.sort_column_combo_box.setStyleSheet(combobox_style)
        self.sort_panel_layout.addWidget(self.sort_column_combo_box)

        self.sort_order_combo_box = QComboBox()
        self.sort_order_combo_box.setStyleSheet(combobox_style)
        self.sort_order_combo_box.addItems([
            "Возрастанию",
            "Убыванию"
        ])
        self.sort_panel_layout.addWidget(self.sort_order_combo_box)

        self.sort_button = QPushButton("Отсортировать")
        self.sort_button.setStyleSheet(button_style)
        self.sort_panel_layout.addWidget(self.sort_button)

        self.main_layout.addWidget(self.sort_panel)

        self.data_table = QTableView()
        self.data_table.setStyleSheet(tableview_style)
        self.data_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.data_table.setMinimumSize(QSize(0, 0))

        self.main_layout.addWidget(self.data_table)


        """ Панель для отчета """
        self.report_panel = QWidget(self.central_widget)
        self.report_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.report_panel_layout = QHBoxLayout(self.report_panel)
        self.report_button = QPushButton("Создать отчёт")
        self.report_button.setStyleSheet(button_style)
        self.report_panel_layout.addWidget(self.report_button)
        self.main_layout.addWidget(self.report_panel)


        """ Установка центрального виджета """
        MainWindow.setCentralWidget(self.central_widget)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        QMetaObject.connectSlotsByName(MainWindow)