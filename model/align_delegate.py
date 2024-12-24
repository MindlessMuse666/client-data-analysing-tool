from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyledItemDelegate


class AlignDelegate(QStyledItemDelegate):
    """
    Делегат для выравнивания текста в ячейках таблицы.
    """
    def initStyleOption(self, option, index):
        """
        Инициализирует стиль для элемента таблицы, выравнивая текст по центру.

        Args:
            option (QStyleOptionViewItem): Параметры стиля элемента.
            index (QModelIndex): Индекс элемента.
        """
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter