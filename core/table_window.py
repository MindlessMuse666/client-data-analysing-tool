from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QVBoxLayout, QWidget, QTableView, QSizePolicy
from static.styles.styles import tableview_style


class TableWindow(QMainWindow):
    """
    Отдельное окно для отображения таблицы данных.

    Attributes:
        closed (pyqtSignal): Сигнал, испускаемый при закрытии окна.
        table_view (QTableView): Виджет для отображения таблицы.
    """
    closed = pyqtSignal()

    def __init__(self, model, parent=None):
        """
        Инициализирует окно таблицы с указанной моделью данных.

        Args:
            model (QAbstractTableModel): Модель данных для таблицы.
            parent (QWidget, optional): Родительский виджет. По умолчанию None.
        """
        super().__init__(parent)
        self.setWindowTitle("Таблица данных")
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table_view = QTableView()
        self.table_view.setStyleSheet(tableview_style)
        self.table_view.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.table_view.setModel(model)
        # --- Изменяем параметр ---
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        # --- Конец изменения параметра ---
        self.table_view.setMinimumSize(1000, 800)

        layout.addWidget(self.table_view)

    def showEvent(self, event):
        """
         Обработчик события показа окна.
         Разворачивает окно на весь экран.
        """
        super().showEvent(event)
        self.showMaximized()

    def closeEvent(self, event):
        """
        Обработчик события закрытия окна.
         Испускает сигнал закрытия окна.
        """
        self.closed.emit()
        super().closeEvent(event)