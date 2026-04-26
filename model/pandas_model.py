from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from typing import Any


class PandasModel(QAbstractTableModel):
    """
    Модель для отображения Pandas DataFrame в QTableView.

    Attributes:
        _data (pd.DataFrame): DataFrame с данными.
        _dtypes (pd.Series): Типы данных столбцов DataFrame.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Инициализирует PandasModel с указанным DataFrame.

        Args:
            data (pd.DataFrame): DataFrame для отображения.
        """
        QAbstractTableModel.__init__(self)
        self._data = data
        self._dtypes = data.dtypes

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Возвращает количество строк в DataFrame.

        Args:
            parent (QModelIndex, optional): Родительский индекс. По умолчанию QModelIndex().

        Returns:
            int: Количество строк.
        """
        return len(self._data.values)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Возвращает количество столбцов в DataFrame.

        Args:
            parent (QModelIndex, optional): Родительский индекс. По умолчанию QModelIndex().

        Returns:
            int: Количество столбцов.
        """
        return self._data.columns.size

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Возвращает данные для отображения в ячейке.

        Args:
            index (QModelIndex): Индекс ячейки.
            role (Qt.ItemDataRole, optional): Роль данных. По умолчанию Qt.ItemDataRole.DisplayRole.

        Returns:
            Any: Значение для отображения или None, если индекс недействителен.
        """
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Возвращает данные для заголовка столбца.

        Args:
            section (int): Индекс столбца.
            orientation (Qt.Orientation): Ориентация заголовка.
            role (Qt.ItemDataRole, optional): Роль данных. По умолчанию Qt.ItemDataRole.DisplayRole.

        Returns:
            Any: Значение заголовка или None, если ориентация не горизонтальная или роль не DisplayRole.
        """
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.columns[section])
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """
        Возвращает флаги для элемента.

        Args:
            index (QModelIndex): Индекс элемента.

        Returns:
            Qt.ItemFlags: Флаги для элемента.
        """
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole = Qt.ItemDataRole.EditRole) -> bool:
        """
        Устанавливает данные в ячейку DataFrame.

        Args:
            index (QModelIndex): Индекс ячейки.
            value (Any): Новое значение.
            role (Qt.ItemDataRole, optional): Роль данных. По умолчанию Qt.ItemDataRole.EditRole.

        Returns:
             bool: True, если данные были установлены, иначе False.
        """
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                row = index.row()
                col = index.column()
                try:
                    if pd.api.types.is_numeric_dtype(self._dtypes.iloc[col]):
                        value = pd.to_numeric(value)
                    self._data.iloc[row, col] = value
                    self.dataChanged.emit(index, index)
                    return True
                except (ValueError, TypeError):
                    QMessageBox.warning(self, "Ошибка", f"Неверный тип данных для столбца '{self._data.columns[col]}'.")
        return False