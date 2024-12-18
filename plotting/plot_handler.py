import matplotlib.pyplot as plt
import pandas as pd
from PyQt6.QtWidgets import QMessageBox

class PlotHandler:
    @staticmethod
    def plot(df, chart_type, x_column, y_column, column_to_plot):
        fig, ax = plt.subplots()

        try:
            if chart_type == "Гистограмма":
                column_to_plot = column_to_plot
                if not pd.api.types.is_numeric_dtype(df[column_to_plot]):
                    QMessageBox.warning(None, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.hist(df[column_to_plot].dropna(), bins=10)
                ax.set_ylabel("Частота")

            elif chart_type == "Диаграмма рассеяния":
                x_column = x_column
                y_column = y_column
                ax.scatter(df[x_column], df[y_column])
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)

            elif chart_type == "Линейный график":
                column_to_plot = column_to_plot
                if not pd.api.types.is_numeric_dtype(df[column_to_plot]):
                    QMessageBox.warning(None, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.plot(df[column_to_plot].dropna())
                ax.set_ylabel(column_to_plot)

            elif chart_type == "Столбчатая диаграмма":
                column_to_plot = column_to_plot
                if not pd.api.types.is_numeric_dtype(df[column_to_plot]):
                    QMessageBox.warning(None, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return
                ax.bar(df.index, df[column_to_plot].dropna())
                ax.set_ylabel(column_to_plot)

            elif chart_type == "Круговая диаграмма":
                column_to_plot = column_to_plot
                if not pd.api.types.is_numeric_dtype(df[column_to_plot]):
                    QMessageBox.warning(None, "Ошибка", f"Столбец '{column_to_plot}' не содержит числовых данных.")
                    return

                values = df[column_to_plot].dropna()
                bins = [0, 4, 8, 15, 18, 21, 26, 40, 50, 61, float('inf')]
                labels = ['0-3', '4-7', '8-14', '15-17', '18-20', '21-25', '26-39', '40-49', '50-60', '60+']
                categorized_data = pd.cut(values, bins=bins, labels=labels, right=False)
                grouped_data = categorized_data.value_counts()

                wedges, texts, autotexts = ax.pie(grouped_data, autopct='%1.1f%%', startangle=140)
                ax.legend(wedges, grouped_data.index, title="Диапазоны", loc="center left", bbox_to_anchor=(1, 0.5))


            ax.set_title(f"{chart_type}")
            plt.show()

        except KeyError:
            QMessageBox.warning(None, "Ошибка", f"Столбец не найден в данных.")
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка при построении графика: {e}")