layout_style = """
    QHBoxLayout {
        background-color: #f0f0f0;
        spacing: 10px;
    }
    QGridLayout {
        background-color: #f0f0f0;
        spacing: 10px;
    }
    QSplitter::handle {
        background-color: #d0d0d0;
    }
"""

application_style = """
QWidget {
    background-color: qlineargradient(
        spread:pad,
        x1:0,
        y1:0,
        x2:1,
        y2:1,
        stop:0 #c8d9e6,
        stop:1 #567c8d
    );
    font: 16pt "Secession Text";
    border: 2px solid #567c8d;
    border-radius: 8px;
}
"""

button_style = """
    QPushButton {
        background-color: #f5efeb;
        color: #2f4156;
        border: 2px solid #567c8d;
        border-radius: 8px;
        padding: 12px 25px;
    }
    QPushButton:hover {
        background-color: #e0d6cd;
    }
    QPushButton:pressed {
        background-color: #c8d9e6;
        padding-top: 12px;
        padding-bottom: 10px;
    }
"""

combobox_style = """
    QComboBox {
        background-color: #f5efeb;
        color: #2f4156;
        border: 2px solid #567c8d;
        border-radius: 8px;
        padding: 12px 25px;
        min-height: 20px;
    }
    QComboBox:hover {
        background-color: #e0d6cd;
    }
    QComboBox:pressed {
        background-color: #c8d9e6;
        padding-top: 12px;
        padding-bottom: 10px;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 2px solid #567c8d;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        background-color: #f5efeb;
    }
    QComboBox::down-arrow {
        image: url(static/resources/arrow_down_24dp.svg);
    }
    QComboBox QAbstractItemView {
        border: 2px solid #567c8d;
        border-radius: 8px;
        background-color: #f5efeb;
        color: #2f4156;
        selection-background-color: #c8d9e6;
    }
"""

label_style = """
    QLabel {
        color: #2f4156;
        background-color: #f5efeb;
        font: 14pt "Secession Light";
        border: 2px solid #567c8d;
        border-radius: 8px;
        padding: 3px;
    }
"""

tableview_style = """
    QTableView {
        background-color: #f5efeb;
        gridline-color: #d0d0d0;
        border: 2px solid #567c8d;
        border-radius: 8px;
        color: #2f4156;
    }
    QHeaderView::section {
        background-color: #e0d6cd;
        color: #2f4156;
        border: 1px solid #d0d0d0;
        padding: 5px;
    }
    QTableView QAbstractItemView::item {
        border: 0.5px solid #e0d6cd;
        color: #2f4156;
    }
    QTableView::item:selected {
        background-color: #c8d9e6;
    }
    QTableView::item:hover {
        background-color: #e0d6cd;
    }
"""