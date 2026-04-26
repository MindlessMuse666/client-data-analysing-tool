from PyQt6.QtCore import QMetaObject, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QGridLayout, QComboBox, QTableView, \
    QStatusBar, QSizePolicy, QLayout, QHeaderView

from static.resources.resource_pathes.resource_pathes import (choice_icon_path, save_icon_path, graph_icon_path,
                                                              main_icon_path, sort_icon_path, report_icon_path,
                                                              fullscreen_icon_path)
from static.styles.styles import button_style, label_style, combobox_style, tableview_style, application_style


def _get_icon(icon_path: str) -> QIcon:
    """
    Создает и возвращает объект QIcon на основе пути к изображению.

    Args:
        icon_path (str): Путь к файлу изображения иконки.

    Returns:
        QIcon: Объект QIcon.
    """
    icon: QIcon = QIcon()
    icon.addPixmap(
        QPixmap(icon_path),
        QIcon.Mode.Normal,
        QIcon.State.Off
    )
    return icon

def _get_label(label_text: str) -> QLabel:
    """
    Создает и возвращает объект QLabel с заданным текстом и стилем.

    Args:
        label_text (str): Текст для метки.

    Returns:
        QLabel: Объект QLabel.
    """
    label: QLabel = QLabel(label_text)
    label.setStyleSheet(label_style)
    label.setSizePolicy(
        QSizePolicy.Policy.Maximum,
        QSizePolicy.Policy.Maximum
    )
    return label


class GuiMainWindow:
    """
    Класс для настройки графического интерфейса главного окна приложения.

    Этот класс содержит методы для инициализации и настройки всех виджетов
    и элементов управления главного окна, таких как кнопки, таблицы, выпадающие списки
    и панели.

     Attributes:
        central_widget (QWidget): Центральный виджет окна.
        main_layout (QVBoxLayout): Основной вертикальный макет для всего окна.
        file_path_info_label (QLabel): Метка "Путь к файлу:".
        top_panel (QWidget): Панель в верхней части окна.
        top_panel_layout (QHBoxLayout): Горизонтальный макет для верхней панели.
        file_path_label (QLabel): Метка для отображения пути к файлу.
        choice_button (QPushButton): Кнопка "Выбрать файл".
        save_button (QPushButton): Кнопка "Сохранить данные".
        graph_type_label (QLabel): Метка "Тип графика:".
        plot_settings_panel (QWidget): Панель настроек графика.
        plot_settings_layout (QGridLayout): Сетка для панели настроек графика.
        graph_type_combo_box (QComboBox): Выпадающий список для выбора типа графика.
        x_axis_label (QLabel): Метка "Ось X:".
        x_axis_combo_box (QComboBox): Выпадающий список для выбора оси X.
        y_axis_label (QLabel): Метка "Ось Y:".
        y_axis_combo_box (QComboBox): Выпадающий список для выбора оси Y.
        column_label (QLabel): Метка "Столбец:".
        column_combo_box (QComboBox): Выпадающий список для выбора столбца.
        build_graph_button (QPushButton): Кнопка "Построить график".
        sort_panel (QWidget): Панель для сортировки.
        sort_panel_layout_label (QLabel): Метка "Сортировать по:".
        sort_panel_layout (QHBoxLayout): Горизонтальный макет для панели сортировки.
        sort_column_combo_box (QComboBox): Выпадающий список для выбора столбца сортировки.
        sort_order_combo_box (QComboBox): Выпадающий список для выбора порядка сортировки.
        sort_button (QPushButton): Кнопка "Отсортировать".
        data_table (QTableView): Таблица для отображения данных.
        report_panel (QWidget): Панель для отчетов.
        report_panel_layout (QHBoxLayout): Горизонтальный макет для панели отчетов.
        report_button (QPushButton): Кнопка "Создать отчёт".
        expand_table_button (QPushButton): Кнопка "Раскрыть таблицу".
        status_bar (QStatusBar): Строка состояния.
    """
    def setup_gui(self, MainWindow: QWidget) -> None:
        """
        Настраивает графический интерфейс главного окна.

        Args:
            MainWindow (QWidget): Главное окно приложения.
        """
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
        self.central_widget: QWidget = QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.main_layout: QVBoxLayout = QVBoxLayout(self.central_widget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        """ Верхняя панель: Путь к файлу, кнопки "Выбрать файл" и "Сохранить данные" """
        self.file_path_info_label: QLabel = _get_label("Путь к файлу:")
        self.top_panel: QWidget = QWidget(self.central_widget)
        self.top_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.top_panel_layout: QHBoxLayout = QHBoxLayout(self.top_panel)
        self.top_panel_layout.addWidget(self.file_path_info_label)

        self.file_path_label: QLabel = _get_label("")
        self.file_path_label.setParent(self.top_panel)
        self.top_panel_layout.addWidget(self.file_path_label)

        self.choice_button: QPushButton = QPushButton("Выбрать файл")
        self.choice_button.setStyleSheet(button_style)
        choice_icon: QIcon = _get_icon(choice_icon_path)
        self.choice_button.setIcon(choice_icon)
        self.choice_button.setIconSize(icon_size)
        self.top_panel_layout.addWidget(self.choice_button)

        self.save_button: QPushButton = QPushButton("Сохранить данные")
        self.save_button.setStyleSheet(button_style)
        save_icon: QIcon = _get_icon(save_icon_path)
        self.save_button.setIcon(save_icon)
        self.save_button.setIconSize(icon_size)
        self.top_panel_layout.addWidget(self.save_button)

        self.main_layout.addWidget(self.top_panel)

        """ Панель настроек графика """
        self.graph_type_label: QLabel = _get_label("Тип графика:")
        self.plot_settings_panel: QWidget = QWidget(self.central_widget)
        self.plot_settings_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.plot_settings_layout: QGridLayout = QGridLayout(self.plot_settings_panel)
        self.plot_settings_layout.addWidget(self.graph_type_label, 0, 0)

        self.graph_type_combo_box: QComboBox = QComboBox()
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
        self.x_axis_combo_box: QComboBox = QComboBox()
        self.x_axis_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.x_axis_label, 1, 0)
        self.plot_settings_layout.addWidget(self.x_axis_combo_box, 1, 1)

        self.y_axis_label: QLabel = _get_label("Ось Y:")
        self.y_axis_combo_box: QComboBox = QComboBox()
        self.y_axis_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.y_axis_label, 2, 0)
        self.plot_settings_layout.addWidget(self.y_axis_combo_box, 2, 1)

        self.column_label: QLabel = _get_label("Столбец:")
        self.column_combo_box: QComboBox = QComboBox()
        self.column_combo_box.setStyleSheet(combobox_style)
        self.plot_settings_layout.addWidget(self.column_label, 3, 0)
        self.plot_settings_layout.addWidget(self.column_combo_box, 3, 1)

        self.build_graph_button: QPushButton = QPushButton("Построить график")
        self.build_graph_button.setStyleSheet(button_style)
        graph_icon: QIcon = _get_icon(graph_icon_path)
        self.build_graph_button.setIcon(graph_icon)
        self.build_graph_button.setIconSize(icon_size)
        self.plot_settings_layout.addWidget(self.build_graph_button, 4, 0, 1, 2)

        self.main_layout.addWidget(self.plot_settings_panel)

        """ Панель сортировки """
        self.sort_panel: QWidget = QWidget(self.central_widget)
        self.sort_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.sort_panel_layout_label: QLabel = _get_label("Сортировать по:")
        self.sort_panel_layout: QHBoxLayout = QHBoxLayout(self.sort_panel)
        self.sort_panel_layout.addWidget(self.sort_panel_layout_label)

        self.sort_column_combo_box: QComboBox = QComboBox()
        self.sort_column_combo_box.setStyleSheet(combobox_style)
        self.sort_panel_layout.addWidget(self.sort_column_combo_box)

        self.sort_order_combo_box: QComboBox = QComboBox()
        self.sort_order_combo_box.setStyleSheet(combobox_style)
        self.sort_order_combo_box.addItems([
            "Возрастанию",
            "Убыванию"
        ])
        self.sort_panel_layout.addWidget(self.sort_order_combo_box)

        self.sort_button: QPushButton = QPushButton("Отсортировать")
        sort_icon: QIcon = _get_icon(sort_icon_path)
        self.sort_button.setIcon(sort_icon)
        self.sort_button.setIconSize(icon_size)
        self.sort_button.setStyleSheet(button_style)
        self.sort_panel_layout.addWidget(self.sort_button)

        self.main_layout.addWidget(self.sort_panel)

        self.data_table: QTableView = QTableView()
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
        self.report_panel: QWidget = QWidget(self.central_widget)
        self.report_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.report_panel_layout: QHBoxLayout = QHBoxLayout(self.report_panel)
        self.report_button: QPushButton = QPushButton("Создать отчёт")
        report_icon: QIcon = _get_icon(report_icon_path)
        self.report_button.setIcon(report_icon)
        self.report_button.setIconSize(icon_size)
        self.report_button.setStyleSheet(button_style)
        self.report_panel_layout.addWidget(self.report_button)

        self.expand_table_button: QPushButton = QPushButton("Раскрыть таблицу")
        expand_icon: QIcon = _get_icon(fullscreen_icon_path)
        self.expand_table_button.setIcon(expand_icon)
        self.expand_table_button.setIconSize(icon_size)
        self.expand_table_button.setStyleSheet(button_style)
        self.report_panel_layout.addWidget(self.expand_table_button)

        self.main_layout.addWidget(self.report_panel)

        """ Установка центрального виджета """
        MainWindow.setCentralWidget(self.central_widget)
        self.status_bar: QStatusBar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        QMetaObject.connectSlotsByName(MainWindow)