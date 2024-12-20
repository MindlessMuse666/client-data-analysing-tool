import matplotlib.pyplot as plt
import pandas as pd
from PyQt6.QtWidgets import QMessageBox

class PlotHandler:
    def __init__(self):
        self.plot_functions = {
            "Гистограмма": self._plot_histogram,
            "Диаграмма рассеяния": self._plot_scatter,
            "Линейный график": self._plot_line,
            "Столбчатая диаграмма": self._plot_bar,
            "Круговая диаграмма": self._plot_pie,
        }

    def plot(self, df, chart_type, x_column, y_column, column_to_plot, ax):
        if chart_type == "Диаграмма рассеяния":
            if not (pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column])):
                QMessageBox.warning(None, "Ошибка", "Оси X и Y должны содержать числовые данные.")
                return False

        elif chart_type not in ["Диаграмма рассеяния"]:
            if not pd.api.types.is_numeric_dtype(df[column_to_plot]):
                QMessageBox.warning(None, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовые данные.")
                return False

        try:
            plot_function = self.plot_functions.get(chart_type)
            if plot_function:
                plot_function(df, x_column, y_column, column_to_plot, ax)
                return True
            else:
                raise ValueError(f"Неизвестный тип графика: {chart_type}")
        except KeyError as e:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{e}' не найден в данных.")
        except (ValueError, TypeError) as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка при построении графика: {e}")

    def _plot_histogram(self, df, x_column, y_column, column, ax):
        try:
            data = df[column].dropna()
            if not pd.api.types.is_numeric_dtype(data):
                QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не содержит числовых данных.")
                return False

            ax.hist(data, bins=10)
            ax.set_xlabel(column)
            ax.set_ylabel("Частота")
            ax.set_title(f"Гистограмма для столбца '{column}'")
        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не найден в данных.")
            return False

    def _plot_scatter(self, df, x_column, y_column, column, ax):
        try:
            x_data = df[x_column].dropna()
            y_data = df[y_column].dropna()
            if not pd.api.types.is_numeric_dtype(x_data) or not pd.api.types.is_numeric_dtype(y_data):
                QMessageBox.warning(None, "Ошибка", "Оси X и Y должны содержать числовые данные.")
                return False

            ax.scatter(x_data, y_data)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"Диаграмма рассеяния: {x_column} vs {y_column}")
            return True
        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{x_column}' или '{y_column}' не найден в данных.")
            return False

    def _plot_line(self, df, x_column, y_column, column, ax):
        try:
            data = df[column].dropna()
            if not pd.api.types.is_numeric_dtype(data):
                QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не содержит числовых данных.")
                return False

            ax.plot(data)
            ax.set_xlabel("Индекс")
            ax.set_ylabel(column)
            ax.set_title(f"Линейный график для столбца '{column}'")
            return True
        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не найден в данных.")
            return False

    def _plot_bar(self, df, x_column, y_column, column, ax):
        try:
            data = df[column].dropna()
            if not pd.api.types.is_numeric_dtype(data):
                QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не содержит числовых данных.")
                return False

            ax.bar(df.index, data)
            ax.set_xlabel("Индекс")
            ax.set_ylabel(column)
            ax.set_title(f"Столбчатая диаграмма для столбца '{column}'")
            plt.xticks(rotation=45, ha="right")
            return True
        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не найден в данных.")
            return False

    def _plot_pie(self, df, x_column, y_column, column, ax):
        try:
            data = df[column].dropna().value_counts()
            if len(data) == 0:
                QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' пуст.")
                return False

            wedges, texts, autotexts = ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140)
            ax.legend(wedges, data.index, loc="center left", bbox_to_anchor=(1, 0.5))
            ax.axis('equal')
            ax.set_title(f"Круговая диаграмма для столбца '{column}'")
            if len(data) > 10:
                for text in texts:
                    text.set_visible(False)
                for autotext in autotexts:
                    autotext.set_visible(False)
            return True
        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец '{column}' не найден в данных.")
            return False