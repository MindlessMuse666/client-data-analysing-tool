import matplotlib.pyplot as plt
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
import matplotlib.ticker as ticker
import numpy as np

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
                # если не числовые данные, передаем в обработку
                self._plot_scatter(df, x_column, y_column, column_to_plot, ax)
                return True
        if chart_type == "Линейный график":
             if not (pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column])):
                 QMessageBox.warning(None, "Ошибка", "Для линейного графика оба столбца должны содержать числовые данные.")
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
            return False

    def _plot_histogram(self, df, x_column, y_column, column, ax):
        self._plot_categorical_or_numerical(df, column, ax, 'hist')
        self._adjust_labels(ax, len(df[column].dropna()))

    def _plot_line(self, df, x_column, y_column, column, ax):
         x_data = df[x_column].dropna()
         y_data = df[y_column].dropna()
         ax.plot(x_data, y_data)
         ax.set_xlabel(x_column)
         ax.set_ylabel(y_column)
         ax.set_title(f"Линейный график: {x_column} vs {y_column}")
         self._adjust_labels(ax, len(x_data))
         if len(x_data) > 0:
             ax.set_xlim(min(x_data), max(x_data))
             ax.set_ylim(min(y_data), max(y_data))


    def _plot_bar(self, df, x_column, y_column, column, ax):
       self._plot_categorical_or_numerical(df, column, ax, 'bar')
       self._adjust_labels(ax, len(df[column].dropna()))

    def _plot_categorical_or_numerical(self, df, column, ax, plot_type):
        data = df[column].dropna()
        if pd.api.types.is_numeric_dtype(data):
            if plot_type == 'hist':
                ax.hist(data, bins=10)
            elif plot_type == 'bar':
                x_data = df.index
                ax.bar(x_data, data)
            ax.set_xlabel(column)
            ax.set_ylabel("Значение" if plot_type != 'hist' else "Частота")
             # Устанавливаем лимиты только для числовых данных
            if not data.empty:
                ax.set_xlim(min(data), max(data))

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
                  return
             ax.scatter(x_values, y_values)
             ax.set_xlabel(f"Количество значений в {x_column}")
             ax.set_ylabel(f"Количество значений в {y_column}")
             ax.set_title(f"Диаграмма рассеяния (Строковые данные): {x_column} vs {y_column}")

        self._adjust_labels(ax, len(x_data))
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

    def _adjust_labels(self, ax, data_length):
        if data_length > 20:
            step = data_length // 10
            if step < 1:
                step = 1
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=step))
            for label in ax.get_xticklabels():
                label.set_fontsize(8)
        plt.tight_layout()