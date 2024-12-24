from typing import Callable, Dict, Optional

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from pandas import DataFrame


class PlotHandler:
    """
    Класс для обработки и отрисовки различных типов графиков на основе данных из DataFrame.

    Attributes:
        _axis_label_multiplier (int): Множитель частоты меток по осям X и Y.
        _font_size (float): Размер шрифта для меток на графиках.
        plot_functions (Dict[str, Callable]): Словарь, связывающий названия графиков с функциями их отрисовки.
    """

    _axis_label_multiplier: int = 4
    _font_size: float = 6.5

    def __init__(self):
        """Инициализация словаря с функциями для построения графиков."""
        self.plot_functions: Dict[str, Callable] = {
            "Гистограмма": self._plot_histogram,
            "Диаграмма рассеяния": self._plot_scatter,
            "Линейный график": self._plot_line,
            "Столбчатая диаграмма": self._plot_bar,
            "Круговая диаграмма": self._plot_pie,
        }

    def plot(self, df: DataFrame, chart_type: str, x_column: str, y_column: Optional[str], column_to_plot: str,
             ax: plt.Axes) -> bool:
        """
        Основной метод для выбора и отрисовки графика.

        Args:
            df (DataFrame): DataFrame с данными.
            chart_type (str): Тип графика для отрисовки.
            x_column (str): Название столбца для оси X.
            y_column (Optional[str]): Название столбца для оси Y, может быть None.
            column_to_plot (str): Название столбца(ов) для отрисовки.
            ax (plt.Axes): Объект Axes для отрисовки графика.

        Returns:
            bool: True, если график успешно построен, иначе False.
        """
        try:
            if chart_type == "Диаграмма рассеяния" and not (
                    pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column])):
                self._plot_scatter(df, x_column, y_column, column_to_plot, ax)
                return True

            if chart_type == "Линейный график" and not (
                    pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column])):
                self._show_error_message("Для линейного графика оба столбца должны содержать числовые данные.")
                return False

            plot_function = self.plot_functions.get(chart_type)
            if not plot_function:
                raise ValueError(f"Неизвестный тип графика: {chart_type}")
            plot_function(df, x_column, y_column, column_to_plot, ax)
            return True

        except KeyError as e:
            self._show_error_message(f"Столбец '{e}' не найден в данных.")
            return False
        except (ValueError, TypeError) as e:
            self._show_error_message(f"Ошибка при построении графика: {e}")
            return False

    def _plot_histogram(self, df: DataFrame, x_column: str, y_column: Optional[str], column: str, ax: plt.Axes) -> None:
        """Отрисовывает гистограмму."""
        self._plot_categorical_or_numerical(df, column, ax, 'hist')
        self._adjust_labels(ax, len(df[column].dropna()))

    def _plot_line(self, df: DataFrame, x_column: str, y_column: str, column: str, ax: plt.Axes) -> None:
        """Отрисовывает линейный график."""
        x_data = df[x_column].dropna()
        y_data = df[y_column].dropna()
        ax.plot(x_data, y_data)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Линейный график: {x_column} vs {y_column}")
        self._adjust_labels(ax, len(x_data))

        if not x_data.empty:
            ax.set_xlim(min(x_data), max(x_data))
            ax.set_ylim(min(y_data), max(y_data))

    def _plot_bar(self, df: DataFrame, x_column: str, y_column: Optional[str], column: str, ax: plt.Axes) -> None:
        """Отрисовывает столбчатую диаграмму."""
        self._plot_categorical_or_numerical(df, column, ax, 'bar')
        self._adjust_labels(ax, len(df[column].dropna()))

    def _plot_categorical_or_numerical(self, df: DataFrame, column: str, ax: plt.Axes, plot_type: str) -> None:
        """
        Отрисовывает гистограмму или столбчатую диаграмму в зависимости от типа данных.

        Args:
            df (DataFrame): DataFrame с данными.
            column (str): Название столбца для отрисовки.
            ax (plt.Axes): Объект Axes для отрисовки графика.
            plot_type (str): Тип графика ('hist' для гистограммы, 'bar' для столбчатой диаграммы).
        """
        data = df[column].dropna()

        if pd.api.types.is_numeric_dtype(data):
            if plot_type == 'bar':
                self._plot_numeric_bar(data, ax, column)
            else:
                self._plot_numeric_column(data, ax, column, plot_type)

        else:
            self._plot_categorical_column(data, ax, column, plot_type)
        ax.set_title(f"График для столбца '{column}'")

    def _plot_numeric_bar(self, data: pd.Series, ax: plt.Axes, column: str) -> None:
        """Отрисовывает столбчатую диаграмму для числовых данных."""
        if data.empty:
            return

        x_data = np.arange(len(data))
        ax.bar(x_data, data.values)

        self._set_axis_labels(ax, column, "Значение")

        if not data.empty:
            ax.set_xticks(x_data)
            ax.set_xticklabels(data.index.astype(str))
            ax.set_xlim(min(x_data) - 1, max(x_data) + 1)

    def _plot_numeric_column(self, data: pd.Series, ax: plt.Axes, column: str, plot_type: str) -> None:
        """Отрисовывает график для числовых данных."""
        if plot_type == 'hist':
            ax.hist(data, bins=10)
            ax.set_ylabel("Частота")
        self._set_axis_labels(ax, column, "Значение")

        if not data.empty:
            ax.set_xlim(min(data), max(data))

    def _plot_categorical_column(self, data: pd.Series, ax: plt.Axes, column: str, plot_type: str) -> None:
        """Отрисовывает график для категориальных данных."""
        counts = data.value_counts()
        if plot_type == 'hist' or plot_type == 'bar':
            ax.bar(counts.index, counts.values)
        self._set_axis_labels(ax, column, "Количество")
        plt.xticks(rotation=90, ha="right")

    def _set_axis_labels(self, ax: plt.Axes, x_label: str, y_label: str) -> None:
        """Устанавливает подписи осей."""
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

    def _plot_scatter(self, df: DataFrame, x_column: str, y_column: str, column: str, ax: plt.Axes) -> None:
        """
         Отрисовывает диаграмму рассеяния.

        Args:
            df (DataFrame): DataFrame с данными.
            x_column (str): Название столбца для оси X.
            y_column (str): Название столбца для оси Y.
            column (str): Не используется, но оставлен для совместимости.
            ax (plt.Axes): Объект Axes для отрисовки графика.
        """
        x_data = df[x_column].dropna()
        y_data = df[y_column].dropna()
        if pd.api.types.is_numeric_dtype(x_data) and pd.api.types.is_numeric_dtype(y_data):
            self._plot_numeric_scatter(x_data, y_data, x_column, y_column, ax)
        else:
            self._plot_categorical_scatter(x_data, y_data, x_column, y_column, ax)

    def _plot_numeric_scatter(self, x_data: pd.Series, y_data: pd.Series, x_column: str, y_column: str,
                              ax: plt.Axes) -> None:
        """Отрисовывает диаграмму рассеяния для числовых данных."""
        ax.scatter(x_data, y_data)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Диаграмма рассеяния: {x_column} vs {y_column}")
        self._adjust_labels(ax, len(x_data), 'x')
        self._adjust_labels(ax, len(y_data), 'y')

    def _plot_categorical_scatter(self, x_data: pd.Series, y_data: pd.Series, x_column: str, y_column: str,
                                  ax: plt.Axes) -> None:
        """Отрисовывает диаграмму рассеяния для категориальных данных."""
        x_values = x_data.tolist()
        y_values = y_data.tolist()

        if not x_values or not y_values:
            self._show_error_message("Нет данных для построения диаграммы рассеяния")
            return

        unique_x = sorted(list(set(x_values)))
        x_positions = np.arange(len(unique_x))
        x_pos = [x_positions[unique_x.index(val)] for val in x_values]

        unique_y = sorted(list(set(y_values)))
        y_positions = np.arange(len(unique_y))
        y_pos = [y_positions[unique_y.index(val)] for val in y_values]

        ax.scatter(x_pos, y_pos)

        ax.set_xticks(x_positions)
        ax.set_xticklabels(unique_x)

        ax.set_yticks(y_positions)
        ax.set_yticklabels(unique_y)

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Диаграмма рассеяния (категориальные значения): {x_column} vs {y_column}")
        plt.xticks(rotation=90, ha="right")
        plt.yticks(rotation=0, ha="right")
        self._adjust_labels(ax, len(x_values), 'x')
        self._adjust_labels(ax, len(y_values), 'y')

    def _plot_pie(self, df: DataFrame, x_column: str, y_column: Optional[str], column: str, ax: plt.Axes) -> None:
        """Отрисовывает круговую диаграмму."""
        data = df[column].dropna().value_counts()
        data = self._group_small_categories(data)

        num_colors: int = len(data)
        colors = self._get_colors(num_colors)
        wedges, texts, auto_texts = ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=colors)

        for wedge in wedges:
            wedge.set_edgecolor('black')

        ax.legend(wedges, data.index, loc="center left", bbox_to_anchor=(0.8, 0.5), fontsize=self._font_size, ncol=2)
        ax.axis('equal')
        ax.set_title(f"Круговая диаграмма для столбца '{column}'")
        if len(data) > 10:
            for text in texts:
                text.set_visible(False)
            for auto_text in auto_texts:
                auto_text.set_visible(False)

    def _group_small_categories(self, data: pd.Series) -> pd.Series:
        """Группирует категории с малым количеством элементов в 'Другие'."""
        if len(data) > 10:
            other = data[data < 2].sum()
            data = data[data >= 2]
            data['Другие'] = other
        return data

    def _get_colors(self, num_colors: int) -> list:
        """Возвращает список цветов для графика."""
        if num_colors <= 20:
            cmap = plt.get_cmap('tab20')
        elif num_colors <= 40:
            cmap = plt.get_cmap('tab20b')
        elif num_colors <= 60:
            cmap = plt.get_cmap('tab20c')
        else:
            cmap = plt.cm.get_cmap('hsv', num_colors)
        return [cmap(i) for i in np.linspace(0, 1, num_colors)]

    def _adjust_labels(self, ax: plt.Axes, data_length: int, axis: str = 'x') -> None:
        """Настраивает метки на осях графика."""
        max_ticks = 8
        if data_length > 1000:
            max_ticks = 15
        if data_length <= 5:
            max_ticks = data_length
        if axis in ('x', 'y'):
            max_ticks = min(data_length, max_ticks * self._axis_label_multiplier)

        if axis == 'x':
            ax.xaxis.set_major_locator(ticker.MaxNLocator(max_ticks))
            for label in ax.get_xticklabels():
                label.set_fontsize(self._font_size)
        elif axis == 'y':
            ax.yaxis.set_major_locator(ticker.MaxNLocator(max_ticks))
            for label in ax.get_yticklabels():
                label.set_fontsize(self._font_size)

        plt.tight_layout()

    def _show_error_message(self, message: str) -> None:
        """Выводит сообщение об ошибке."""
        QMessageBox.warning(None, "Ошибка", message)