import datetime
from typing import List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
import pandas as pd


class ReportHandler:
    """
    Класс для генерации PDF отчетов на основе данных из DataFrame.

    Attributes:
        base_font_name (str): Базовое имя шрифта для отчета.
        base_text_color (reportlab.lib.colors.Color): Базовый цвет текста.
        base_alignment (int): Базовое выравнивание текста.
        base_leading (int): Базовый межстрочный интервал.
        title_style (ParagraphStyle): Стиль заголовка.
        end_page_style (ParagraphStyle): Стиль для текста в конце отчета.
        end_page_small_style (ParagraphStyle): Стиль для мелкого текста в конце отчета.
        end_page_smallest_style (ParagraphStyle): Стиль для самого мелкого текста в конце отчета.
        month_names (dict): Словарь с названиями месяцев.
    """

    def __init__(self, font_path: str = "static/fonts/Secession_Text.ttf"):
        """
        Инициализирует ReportHandler, регистрирует шрифт и устанавливает стили.

        Args:
            font_path (str, optional): Путь к файлу шрифта. По умолчанию "Secession_Text.ttf".
        """
        pdfmetrics.registerFont(TTFont('Secession_Text', font_path))
        self.styles = getSampleStyleSheet()

        self.base_font_name = 'Secession_Text'
        self.base_text_color = colors.black
        self.base_alignment = TA_CENTER
        self.base_leading = 7

        self.title_style = self._create_paragraph_style(
            name='TitleStyle',
            parent=self.styles['h1'],
            font_size=32,
            alignment=TA_CENTER
        )

        self.end_page_style = self._create_paragraph_style(
            name='EndPageStyle',
            parent=self.styles['Normal'],
            font_size=32,
            alignment=TA_CENTER
        )

        self.end_page_small_style = self._create_paragraph_style(
            name='EndPageSmallStyle',
            parent=self.styles['Normal'],
            font_size=16,
            alignment=TA_CENTER
        )

        self.end_page_smallest_style = self._create_paragraph_style(
            name='EndPageSmallestStyle',
            parent=self.styles['Normal'],
            font_size=12,
            alignment=TA_CENTER
        )

        self.month_names = {
            1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
            7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
        }

    def _create_paragraph_style(self, name: str, parent: ParagraphStyle, font_size: int, alignment: int = None,
                                text_color: colors.Color = None, leading: int = None) -> ParagraphStyle:
        """
        Создает и возвращает объект ParagraphStyle.

        Args:
            name (str): Имя стиля.
            parent (ParagraphStyle): Родительский стиль.
            font_size (int): Размер шрифта.
            alignment (int, optional): Выравнивание текста. По умолчанию None.
            text_color (colors.Color, optional): Цвет текста. По умолчанию None.
            leading (int, optional): Межстрочный интервал. По умолчанию None.

        Returns:
            ParagraphStyle: Созданный объект ParagraphStyle.
        """
        style = ParagraphStyle(
            name=name,
            parent=parent,
            fontName=self.base_font_name,
            fontSize=font_size,
            alignment=alignment if alignment is not None else self.base_alignment,
            textColor=text_color if text_color is not None else self.base_text_color,
            leading=leading if leading is not None else self.base_leading
        )
        return style

    def generate_report(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Генерирует PDF отчет на основе DataFrame и сохраняет его по указанному пути.

        Args:
            df (pd.DataFrame): DataFrame с данными.
            file_path (str): Путь для сохранения PDF файла.
        """
        custom_width = 29.7 * cm
        custom_height = 21 * cm
        doc = SimpleDocTemplate(file_path, pagesize=(custom_width, custom_height))
        elements = []

        self._generate_title_page(elements)
        elements.append(PageBreak())

        elements.append(Spacer(1, 12))
        self._create_tables_from_dataframe(df, elements)

        self._generate_end_page(elements, df)

        doc.build(elements)

    def _create_tables_from_dataframe(self, df: pd.DataFrame, elements: List) -> None:
        """
        Создает таблицы из DataFrame и добавляет их в список элементов.

        Args:
            df (pd.DataFrame): DataFrame с данными.
            elements (List): Список элементов для добавления таблиц.
        """
        max_width = 29.7 * cm - 2 * inch

        df_copy = df.copy()

        # Предварительная обработка данных и заголовков
        for column in df_copy.columns:
            df_copy[column] = df_copy[column].apply(self._split_long_text)

        col_widths, font_size = self._calculate_column_widths(df_copy, max_width)

        header_style = self._create_paragraph_style(
            name='HeaderStyle',
            parent=self.styles['Normal'],
            font_size=font_size,
            text_color=colors.whitesmoke,
            alignment=TA_CENTER
        )
        self._create_paragraph_style(
            name='NormalStyle',
            parent=self.styles['Normal'],
            font_size=font_size,
            alignment=TA_CENTER
        )

        data = [[Paragraph(self._split_long_text(col, max_length=12), header_style) for col in
                 df_copy.columns.to_list()]] + df_copy.values.tolist()

        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), self.base_font_name),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
            ('TOPPADDING', (0, 0), (-1, 0), 1),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self.base_font_name),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(table)

    def _split_long_text(self, text: str, max_length: int = 30) -> str:
        """
        Разделяет длинный текст на несколько строк, если он превышает заданную длину.

        Args:
            text (str): Текст для разделения.
            max_length (int, optional): Максимальная длина строки. По умолчанию 30.

        Returns:
            str: Разделенный текст.
        """
        if isinstance(text, str) and len(text) > max_length:
            return "\n".join(simpleSplit(text, self.base_font_name, 9, max_length))
        return str(text)

    def _calculate_text_width(self, text: str, font_size: int) -> float:
        """
        Вычисляет ширину текста с учетом шрифта.

        Args:
            text (str): Текст для вычисления ширины.
            font_size (int): Размер шрифта.

        Returns:
            float: Ширина текста.
        """
        return pdfmetrics.stringWidth(text, self.base_font_name, font_size)

    def _calculate_column_widths(self, df: pd.DataFrame, max_width: float) -> tuple[List[float], float]:
        """
        Вычисляет ширину колонок таблицы и размер шрифта.

        Args:
            df (pd.DataFrame): DataFrame с данными.
            max_width (float): Максимальная ширина для таблицы.

        Returns:
            tuple[List[float], float]: Список с ширинами колонок и размер шрифта.
        """
        col_widths = []
        font_size = 9

        for column in df.columns:
            max_text_width = max([self._calculate_text_width(str(x), font_size) for x in df[column]] + [
                self._calculate_text_width(column, font_size)])
            col_widths.append(max_text_width)

        total_width = sum(col_widths)

        while total_width > max_width and font_size > 4.5:
            font_size -= 0.5
            col_widths = []
            for column in df.columns:
                max_text_width = max([self._calculate_text_width(str(x), font_size) for x in df[column]] + [
                    self._calculate_text_width(column, font_size)])
                col_widths.append(max_text_width)
            total_width = sum(col_widths)

        if total_width > max_width:
            scale_factor = max_width / total_width
            col_widths = [width * scale_factor for width in col_widths]

        return col_widths, font_size

    def _generate_title_page(self, elements: List) -> None:
        """
        Создает и добавляет страницу с заголовком в список элементов.

        Args:
            elements (List): Список элементов для добавления страницы с заголовком.
        """
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%d ") + self.month_names[current_date.month] + current_date.strftime(
            " %Y")
        title = f"Отчёт за {formatted_date}"

        title_content = [
            Paragraph(title, self.title_style),
            Spacer(1, 0.5 * inch),
            Paragraph(f"Сформировано: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.end_page_small_style)
        ]
        elements.append(KeepTogether(title_content))

    def _generate_end_page(self, elements: List, df: pd.DataFrame) -> None:
        """
        Создает и добавляет страницу с информацией о конце отчета.

        Args:
            elements (List): Список элементов для добавления страницы с информацией о конце отчета.
            df (pd.DataFrame): DataFrame, для получения информации о количестве строк.
        """
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%d ") + self.month_names[current_date.month] + current_date.strftime(
            " %Y")
        end_page_content = [
            Paragraph("Конец отчёта", self.end_page_style),
            Spacer(1, 1 * inch),
            Paragraph(f"Дата создания отчёта: {formatted_date}", self.end_page_small_style),
            Spacer(1, .5 * inch),
            Paragraph(f"Количество строк в таблице: {len(df)}", self.end_page_small_style)
        ]
        elements.append(PageBreak())
        elements.append(KeepTogether(end_page_content))