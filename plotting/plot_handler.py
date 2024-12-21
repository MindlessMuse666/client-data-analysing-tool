import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from matplotlib import patches


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
                return False  # Возвращаем False, чтобы не строить график
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
        self._plot_categorical_or_numerical(df, column, ax, 'hist')

    def _plot_line(self, df, x_column, y_column, column, ax):
        self._plot_categorical_or_numerical(df, column, ax, 'plot')

    def _plot_bar(self, df, x_column, y_column, column, ax):
        self._plot_categorical_or_numerical(df, column, ax, 'bar')

    def _plot_categorical_or_numerical(self, df, column, ax, plot_type):
        data = df[column].dropna()
        if pd.api.types.is_numeric_dtype(data):
            if plot_type == 'hist':
                ax.hist(data, bins=10)
            elif plot_type == 'plot':
                x_data = df.index
                ax.plot(x_data, data)
            elif plot_type == 'bar':
                x_data = df.index
                ax.bar(x_data, data)
            ax.set_xlabel(column)
            ax.set_ylabel("Значение" if plot_type != 'hist' else "Частота")
        else:
            counts = data.value_counts()
            if plot_type == 'hist' or plot_type == 'bar':
                ax.bar(counts.index, counts.values)
            ax.set_xlabel(column)
            ax.set_ylabel("Количество")
            plt.xticks(rotation=45, ha="right")

        ax.set_title(f"График для столбца '{column}'")

    def _plot_scatter(self, df, x_column, y_column, column, ax):
        x_data = df[x_column].dropna()
        y_data = df[y_column].dropna()
        if not (pd.api.types.is_numeric_dtype(x_data) and pd.api.types.is_numeric_dtype(y_data)):
            QMessageBox.warning(None, "Ошибка", "Оси X и Y должны содержать числовые данные.")
            return
        ax.scatter(x_data, y_data)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Диаграмма рассеяния: {x_column} vs {y_column}")
        return True

    def _plot_pie(self, df, x_column, y_column, column, ax):
        data = df[column].dropna().value_counts()
        if len(data) > 10:  # Устанавливаем ограничение на 10 категорий
            other = data[data < 2].sum()  # Суммируем категории с количеством меньше 10 в категорию "Другие"
            data = data[data >= 2]  # Оставляем только категории с количеством больше или равно 10
            data['Другие'] = other  # Добавляем категорию "Другие"
        wedges, texts, autotexts = ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140)
        ax.legend(wedges, data.index, loc="center left", bbox_to_anchor=(1, 0.5))
        ax.axis('equal')
        ax.set_title(f"Круговая диаграмма для столбца '{column}'")
        if len(data) > 10:
            for text in texts:
                text.set_visible(False)
            for autotext in autotexts:
                autotext.set_visible(False)