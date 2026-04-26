import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from plotting.plot_handler import PlotHandler


class PlotWindow(QDialog):
    """
    Отдельное окно для отображения графика.

    Attributes:
        plot_handler (PlotHandler): Обработчик графиков.
        df (pd.DataFrame): DataFrame с данными.
        chart_type (str): Тип графика.
        x_axis (str): Ось X.
        y_axis (str): Ось Y.
        column (str): Столбец для графика.
        figure (Figure): Фигура matplotlib.
        ax (Axes): Объект Axes для отрисовки графика.
        canvas (FigureCanvas): Холст для отображения графика.
    """
    def __init__(self, df, chart_type, x_axis, y_axis, column, parent=None):
        """
        Инициализирует окно графика с указанными параметрами.

        Args:
            df (pd.DataFrame): DataFrame с данными.
            chart_type (str): Тип графика.
            x_axis (str): Ось X.
            y_axis (str): Ось Y.
            column (str): Столбец для графика.
            parent (QWidget, optional): Родительский виджет. По умолчанию None.
        """
        super().__init__(parent)
        self.setWindowTitle("График")
        self.plot_handler = PlotHandler()
        self.df = df
        self.chart_type = chart_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.column = column

        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_chart()

    def plot_chart(self):
        """
        Строит и отображает график.
        """
        try:
            if not self.plot_handler.plot(self.df, self.chart_type, self.x_axis, self.y_axis, self.column, self.ax):
                plt.close(self.figure)
                return
            self.canvas.draw()
        except Exception:
            plt.close(self.figure)
            return