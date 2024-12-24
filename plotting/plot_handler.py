# plotting/plot_handler.py

import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from matplotlib.ticker import MaxNLocator, FormatStrFormatter

class PlotHandler:
    def __init__(self):
        pass
    def plot(self, df, chart_type, x_axis, y_axis, column, ax):
        ax.clear()  # Очищаем оси перед построением нового графика
        try:
            if chart_type == "Диаграмма рассеяния":
                return self._plot_scatter(df, x_axis, y_axis, column, ax)
            elif chart_type == "Линейный график":
               return self._plot_line(df, x_axis, y_axis, ax)
            elif chart_type == "Гистограмма":
               return self._plot_hist(df, column, ax)
            elif chart_type == "Столбчатая диаграмма":
                return self._plot_bar(df, column, ax)
            elif chart_type == "Круговая диаграмма":
                return self._plot_pie(df, x_axis, y_axis, column, ax)
            else:
                return False # Return False if chart_type is not valid
            ax.yaxis.set_major_locator(MaxNLocator(10))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            return True
        except KeyError:
            QMessageBox.warning(None, "Ошибка", "Неверно указаны данные для построения графика")
            return False

    def _plot_scatter(self, df, x_column, y_column, column, ax):
        x_data = df[x_column]
        y_data = df[y_column]

        if pd.api.types.is_numeric_dtype(x_data) and pd.api.types.is_numeric_dtype(y_data):
            ax.scatter(x_data, y_data)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"Диаграмма рассеяния: {x_column} vs {y_column}")
        else:
            x_counts = x_data.value_counts()
            y_counts = y_data.value_counts()

            x_values = [x for x in x_counts.index for _ in range(x_counts[x])]
            y_values = [y for y in y_counts.index for _ in range(y_counts[y])]

            if len(x_values) == 0 or len(y_values) == 0:
                QMessageBox.warning(None, "Ошибка", "Нет данных для построения диаграммы рассеяния")
                return False
            ax.scatter(x_values, y_values)
            ax.set_xlabel(f"Количество значений в {x_column}")
            ax.set_ylabel(f"Количество значений в {y_column}")
            ax.set_title(f"Диаграмма рассеяния (Строковые данные): {x_column} vs {y_column}")
        self._adjust_labels(ax, len(x_data), is_y_axis_needed=True)
        return True

    def _plot_line(self, df, x_axis, y_axis, ax):
        ax.plot(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        return True

    def _plot_hist(self, df, column, ax):
        ax.hist(df[column])
        ax.set_xlabel(column)
        return True

    def _plot_bar(self, df, column, ax):
        value_counts = df[column].value_counts()
        ax.bar(value_counts.index, value_counts.values)
        ax.set_xlabel(column)
        return True

    def _plot_pie(self, df, x_column, y_column, column, ax):
        data = df[column].dropna().value_counts()
        if len(data) > 10:
            other = data[data < 2].sum()
            data = data[data >= 2]
            data['Другие'] = other
        wedges, texts, autotexts = ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140)
        ax.legend(wedges, data.index, loc="center left", bbox_to_anchor=(0.8, 0.5))
        ax.axis('equal')
        ax.set_title(f"Круговая диаграмма для столбца '{column}'")
        if len(data) > 10:
            for text in texts:
                text.set_visible(False)
            for autotext in autotexts:
                autotext.set_visible(False)

    def _adjust_labels(self, ax, data_length, is_y_axis_needed):
        if data_length > 18:
            x_step = data_length // 25 if data_length // 25 > 0 else 1
            y_step = data_length // 25 if data_length // 25 > 0 else 1
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=x_step))
            if is_y_axis_needed:
                ax.yaxis.set_major_locator(ticker.MultipleLocator(base=y_step))
            for label in ax.get_xticklabels():
                label.set_fontsize(6.5)
            for label in ax.get_yticklabels():
                label.set_fontsize(6.5)
        plt.tight_layout()
