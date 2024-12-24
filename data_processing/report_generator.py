import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether


class ReportGenerator:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        self.styles = getSampleStyleSheet()

        self.base_font_name = 'Arial'
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

    def _create_paragraph_style(self, name, parent, font_size, alignment=None, text_color=None, leading=None):
        """Создает и возвращает объект ParagraphStyle."""
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

    def generate_report(self, df, file_path):
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

    def _create_tables_from_dataframe(self, df, elements):
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

    def _split_long_text(self, text, max_length=30):
        if isinstance(text, str) and len(text) > max_length:
            return "\n".join(simpleSplit(text, self.base_font_name, 9, max_length))
        return str(text)

    def _calculate_text_width(self, text, font_size):
        """Вычисляет ширину текста с учетом шрифта."""
        return pdfmetrics.stringWidth(text, self.base_font_name, font_size)

    def _calculate_column_widths(self, df, max_width):
        col_widths = []
        font_size = 9  # Инициализируем размер шрифта

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

    def _generate_title_page(self, elements):
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

    def _generate_end_page(self, elements, df):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%d ") + self.month_names[current_date.month] + current_date.strftime(
            " %Y")
        columns_str = '\n'.join(df.columns.to_list())

        end_page_content = [
            Paragraph("Конец отчёта", self.end_page_style),
            Spacer(1, 1 * inch),
            Paragraph(f"Дата создания отчёта: {formatted_date}", self.end_page_small_style),
            Spacer(1, .5 * inch),
            Paragraph(f"Количество строк в таблице: {len(df)}", self.end_page_small_style)
        ]
        elements.append(PageBreak())
        elements.append(KeepTogether(end_page_content))
