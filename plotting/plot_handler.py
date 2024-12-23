import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        self._adjust_labels(ax, len(df[column].dropna()), is_y_axis_needed=False)

    def _plot_line(self, df, x_column, y_column, column, ax):
        x_data = df[x_column].dropna()
        y_data = df[y_column].dropna()

        if not (pd.api.types.is_numeric_dtype(x_data) and pd.api.types.is_numeric_dtype(y_data)):
            QMessageBox.warning(None, "Ошибка", "Оси X и Y должны содержать числовые данные.")
            return
        ax.plot(x_data, y_data)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Линейный график: {x_column} vs {y_column}")
        self._adjust_labels(ax, len(x_data), is_y_axis_needed=True)
        if len(x_data) > 0:
             ax.set_xlim(min(x_data), max(x_data))
             ax.set_ylim(min(y_data), max(y_data))

    def _plot_bar(self, df, x_column, y_column, column, ax):
        self._plot_categorical_or_numerical(df, column, ax, 'bar')
        self._adjust_labels(ax, len(df[column].dropna()), is_y_axis_needed=False)

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
            if not data.empty:
                ax.set_xlim(min(data), max(data))
        else:
            counts = data.value_counts()
            if plot_type == 'hist' or plot_type == 'bar':
                ax.bar(counts.index, counts.values)
            ax.set_xlabel(column)
            ax.set_ylabel("Количество")
            plt.xticks(rotation=90, ha="right")
        ax.set_title(f"График для столбца '{column}'")

    def _plot_scatter(self, df, x_column, y_column, column, ax):
        x_data = df[x_column].dropna()
        y_data = df[y_column].dropna()
        plt.xticks(rotation=90, ha="right")

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

        self._adjust_labels(ax, len(x_data), is_y_axis_needed=True)
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