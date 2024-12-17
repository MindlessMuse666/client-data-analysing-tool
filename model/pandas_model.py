from PyQt6.QtCore import Qt, QAbstractTableModel
import pandas as pd
from PyQt6.QtWidgets import QMessageBox

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
        self._dtypes = data.dtypes # сохраняем типы данных столбцов

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.columns[col])
        return None

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                row = index.row()
                col = index.column()
                try:
                    # Пытаемся преобразовать значение к исходному типу данных
                    if pd.api.types.is_numeric_dtype(self._dtypes.iloc[col]):
                        value = pd.to_numeric(value)
                    self._data.iloc[row, col] = value
                    self.dataChanged.emit(index, index)
                    return True
                except (ValueError, TypeError):
                    QMessageBox.warning(self, "Ошибка", f"Неверный тип данных для столбца '{self._data.columns[col]}'.")
        return False