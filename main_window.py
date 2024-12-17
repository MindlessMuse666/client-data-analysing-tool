import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTableView, QFileDialog, QHBoxLayout, QLabel, QHeaderView,
                             QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, pyqtSlot
from PyQt6.QtGui import QIcon
import sqlite3
# import matplotlib.backends.backend_qt6agg as mplt_backend


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CheCloud")
        self.setWindowIcon(QIcon('static/images/sato.ico'))
        self.df = pd.DataFrame()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # File selection
        button_layout = QHBoxLayout()
        self.file_label = QLabel("Файл не выбран")
        button_layout.addWidget(self.file_label)
        open_button = QPushButton("Выберите CSV файл")
        open_button.clicked.connect(self.open_file)
        button_layout.addWidget(open_button)
        main_layout.addLayout(button_layout)

        # Table
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_view)

        # Chart type selection
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Гистограмма", "Диаграмма рассеяния", "Линейный график", "Столбчатая диаграмма", "Круговая диаграмма"])
        self.chart_type_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.chart_type_combo)

        # X-axis selection
        self.x_axis_combo = QComboBox()
        self.x_axis_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.x_axis_combo)

        # Y-axis selection
        self.y_axis_combo = QComboBox()
        self.y_axis_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.y_axis_combo)

        # Column selection (for Histogram, Line chart, Bar chart, Pie chart)
        self.column_combo = QComboBox()
        self.column_combo.currentIndexChanged.connect(self.update_plot_button)
        main_layout.addWidget(self.column_combo)


        # Plot button
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_chart)
        self.plot_button.setEnabled(False)
        main_layout.addWidget(self.plot_button)

        # Save button
        save_button = QPushButton("Сохранить данные")
        save_button.clicked.connect(self.save_to_db)
        main_layout.addWidget(save_button)
        self.db_name = "client_data.db"

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

        if file_name:
            try:
                self.file_label.setText(file_name)
                df = pd.read_csv(file_name, sep=';')
                self.display_data(df)
                self.save_to_db()
            except pd.errors.EmptyDataError:
                self.display_data(pd.DataFrame())
                print("Файл пустой")
            except pd.errors.ParserError:
                self.display_data(pd.DataFrame())
                print("Ошибка парсинга файла")
            except Exception as e:
                print(f"Ошибка: {e}")
                self.display_data(pd.DataFrame())

    def display_data(self, df):
        self.df = df
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
        enabled = not self.df.empty
        self.x_axis_combo.setVisible(chart_type == "Диаграмма рассеяния")
        self.y_axis_combo.setVisible(chart_type == "Диаграмма рассеяния")
        self.column_combo.setVisible(chart_type != "Диаграмма рассеяния")

        if chart_type == "Диаграмма рассеяния":
            enabled = enabled and self.x_axis_combo.count() > 0 and self.y_axis_combo.count() > 0 and self.x_axis_combo.currentIndex() != -1 and self.y_axis_combo.currentIndex() != -1
        elif chart_type in ["Гистограмма", "Линейный график", "Столбчатая диаграмма", "Круговая диаграмма"]:
            enabled = enabled and self.column_combo.count() > 0 and self.column_combo.currentIndex() != -1

        self.plot_button.setEnabled(enabled)


    def plot_chart(self):
        if not hasattr(self, 'df'):
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите данные")
            return

        if self.df.empty:
            QMessageBox.warning(self, "Ошибка", "Таблица данных пуста")
            return

        chart_type = self.chart_type_combo.currentText()
        fig, ax = plt.subplots()

        try:
            if chart_type == "Гистограмма":
                column_to_plot = self.column_combo.currentText()
                if not pd.api.types.is_numeric_dtype(self.df[column_to_plot]):
                    QMessageBox.warning(self, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.hist(self.df[column_to_plot].dropna(), bins=10)
                ax.set_ylabel("Частота")

            elif chart_type == "Диаграмма рассеяния":
                x_column = self.x_axis_combo.currentText()
                y_column = self.y_axis_combo.currentText()
                ax.scatter(self.df[x_column], self.df[y_column])
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)

            elif chart_type == "Линейный график":
                column_to_plot = self.column_combo.currentText()
                if not pd.api.types.is_numeric_dtype(self.df[column_to_plot]):
                    QMessageBox.warning(self, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.plot(self.df[column_to_plot].dropna())
                ax.set_ylabel(column_to_plot)

            elif chart_type == "Столбчатая диаграмма":
                column_to_plot = self.column_combo.currentText()
                if not pd.api.types.is_numeric_dtype(self.df[column_to_plot]):
                    QMessageBox.warning(self, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.bar(self.df.index, self.df[column_to_plot].dropna())
                ax.set_ylabel(column_to_plot)

            elif chart_type == "Круговая диаграмма":
                column_to_plot = self.column_combo.currentText()
                if not pd.api.types.is_numeric_dtype(self.df[column_to_plot]):
                    QMessageBox.warning(self, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.pie(self.df[column_to_plot].dropna(), labels=self.df.index, autopct='%1.1f%%')

            ax.set_title(f"{chart_type}")
            plt.show()

        except KeyError:
            QMessageBox.warning(self, "Ошибка", f"Столбец не найден в данных.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при построении графика: {e}")

    def save_to_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Создаем таблицу
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                )
            ''')

            # Добавляем столбцы динамически с учетом кодировки
            for col in self.df.columns:
                cursor.execute(f"ALTER TABLE client_data ADD COLUMN '{col}' TEXT")

            # Вставляем данные с использованием параметризованных запросов
            for index, row in self.df.iterrows():
                placeholders = ", ".join(["?"] * len(row))
                cursor.execute(f"INSERT INTO client_data ({', '.join(['?'] * len(self.df.columns))}) VALUES ({placeholders})", tuple(row))

            conn.commit()
            print("Данные успешно сохранены в базу данных.")

        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Столбцы уже существуют. Данные обновлены.") #Если столбцы уже существуют, просто обновляем данные
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении данных: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении данных: {e}")
        finally:
            if conn:
                conn.close()

    def closeEvent(self, event):
        self.save_to_db()
        event.accept()



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
                    if pd.api.types.is_numeric_dtype(self._dtypes.iloc[col]):  # ИЗМЕНЕНО: используется .iloc
                        value = pd.to_numeric(value)
                    self._data.iloc[row, col] = value
                    self.dataChanged.emit(index, index)
                    return True
                except (ValueError, TypeError):
                    QMessageBox.warning(self, "Ошибка", f"Неверный тип данных для столбца '{self._data.columns[col]}'.")
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())