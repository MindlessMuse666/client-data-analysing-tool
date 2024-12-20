from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """ Общие настройки """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        font = QtGui.QFont()
        font.setFamily("Secession Text")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/resources/main_icon.ico"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStatusTip("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: qlineargradient(\n"
"   spread:pad,\n"
"   x1:0,\n"
"   y1:0,\n"
"   x2:1,\n"
"   y2:1,\n"
"   stop:0 #c8d9e6,\n"
"   stop:1 #567c8d\n"
");\n"
"font: 16pt \"Secession Text\";")
        MainWindow.setIconSize(QtCore.QSize(24, 24))


        self.central_widget = QtWidgets.QWidget(parent=MainWindow)
        self.central_widget.setEnabled(True)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.main_layout = QtWidgets.QFrame(parent=self.central_widget)
        self.main_layout.setStyleSheet("")
        self.main_layout.setObjectName("main_layout")

        self.gridLayout = QtWidgets.QGridLayout(self.main_layout)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(0) # Убираем отступы между элементами

        self.comboBox_4 = QtWidgets.QComboBox(parent=self.main_layout)
        self.comboBox_4.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout.addWidget(self.comboBox_4, 2, 1, 1, 1)

        self.comboBox_2 = QtWidgets.QComboBox(parent=self.main_layout)
        self.comboBox_2.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   color: #2f4156;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 2, 2, 1, 1)

        self.main_buttons_panel = QtWidgets.QFrame(parent=self.main_layout)
        self.main_buttons_panel.setObjectName("main_buttons_panel")
        self.main_buttons_panel.setStyleSheet("background-color: transparent;") # Убираем фон # self.main_buttons_panel.setStyleSheet("background-color: rgbargba(200, 217, 230, 0);")
        self.main_buttons_panel.setEnabled(True)

        self.gridLayout_3 = QtWidgets.QGridLayout(self.main_buttons_panel)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setSpacing(10) # Небольшой отступ между кнопками

        """ Кнопка "Выбрать файл" """
        self.choice_button = QtWidgets.QPushButton(parent=self.main_buttons_panel)
        self.choice_button.setObjectName("choice_button")
        self.choice_button.setStyleSheet("QPushButton {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"}\n"
"QPushButton:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"QPushButton:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("static/resources/file_draft_24dp.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.choice_button.setIcon(icon1)
        self.choice_button.setIconSize(QtCore.QSize(24, 24))
        self.gridLayout_3.addWidget(self.choice_button, 0, 1, 1, 1)

        """ Кнопка "Сохранить данные" """
        self.save_button = QtWidgets.QPushButton(parent=self.main_buttons_panel)
        self.save_button.setStyleSheet("QPushButton {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"}\n"
"QPushButton:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"QPushButton:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("static/resources/save_24dp.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.save_button.setIcon(icon2)
        self.save_button.setIconSize(QtCore.QSize(24, 24))
        self.save_button.setObjectName("save_button")
        self.gridLayout_3.addWidget(self.save_button, 0, 2, 1, 1)

        """ Кнопка "Построить график" """
        self.build_graph_button = QtWidgets.QPushButton(parent=self.main_layout)
        self.build_graph_button.setObjectName("build_graph_button")
        self.build_graph_button.setStyleSheet("QPushButton {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"}\n"
"QPushButton:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"QPushButton:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("static/resources/graph_24dp.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.build_graph_button.setIcon(icon3)
        self.build_graph_button.setIconSize(QtCore.QSize(24, 24))


        self.save_button.raise_()
        self.build_graph_button.raise_()
        self.choice_button.raise_()

        self.gridLayout.addWidget(self.main_buttons_panel, 1, 0, 1, 4)



        self.comboBox = QtWidgets.QComboBox(parent=self.main_layout)
        self.comboBox.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"/* Дополнительный стиль для лучшей читаемости */\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.comboBox.setIconSize(QtCore.QSize(24, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.gridLayout.addWidget(self.comboBox, 2, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(parent=self.main_layout)
        self.comboBox_3.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"/* Дополнительный стиль для лучшей читаемости */\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 2, 3, 1, 1)

        """ Отображение: 
                Кнопки "Построить график"; 
                Типа графика;
                Трёх списков выбора столбцов для постройки графика. """
        self.gridLayout.addWidget(self.build_graph_button, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.comboBox_4, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.comboBox_2, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.comboBox_3, 2, 4, 1, 1)


        """ Текст "Путь к файлу" """
        self.file_path_label = QtWidgets.QLabel(parent=self.main_layout)
        self.file_path_label.setObjectName("file_path_label")
        self.file_path_label.setStyleSheet("QLabel {\n"
                                           "   color: #2f4156;\n"
                                           "   background-color: #f5efeb;\n"
                                           "   font: 14pt \"Secession Light\";\n"
                                           "   border: 2px solid #567c8d;\n"
                                           "   border-radius: 8px;\n"
                                           "   padding: 3px;\n"
                                           "}")
        self.file_path_label.setMinimumSize(QtCore.QSize(0, 0))
        self.file_path_label.setMouseTracking(False)
        self.file_path_label.setAutoFillBackground(False)
        self.file_path_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.file_path_label.setScaledContents(False)
        self.file_path_label.setWordWrap(False)
        self.file_path_label.setOpenExternalLinks(False)
        self.gridLayout.addWidget(self.file_path_label, 0, 0, 1, 4)


        # UI сортировки данных
        self.sort_column_combo = QtWidgets.QComboBox(parent=self.main_layout)
        self.sort_column_combo.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"/* Дополнительный стиль для лучшей читаемости */\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.sort_column_combo.setObjectName("sort_column_combo")

        self.sort_order_combo = QtWidgets.QComboBox(parent=self.main_layout)
        self.sort_order_combo.setStyleSheet("QComboBox {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"   min-height: 20px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n"
"\n"
"/* Стиль для раскрывающегося списка */\n"
"QComboBox::drop-down {\n"
"   subcontrol-origin: padding;\n"
"   subcontrol-position: top right;\n"
"   width: 20px;\n"
"   border-left: 2px solid #567c8d;\n"
"   border-top-right-radius: 8px;\n"
"   border-bottom-right-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(static/resources/arrow_down_24dp.svg);\n"
"}\n"
"\n"
"\n"
"/* Дополнительный стиль для лучшей читаемости */\n"
"QComboBox QAbstractItemView {\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;"
"   selection-background-color: #c8d9e6;\n"
"}")
        self.sort_order_combo.setObjectName("sort_order_combo")
        self.sort_order_combo.addItems(["Возрастанию", "Убыванию"])

        self.sort_button = QtWidgets.QPushButton(parent=self.main_layout)
        self.sort_button.setStyleSheet("QPushButton {\n"
"   background-color: #f5efeb;\n"
"   color: #2f4156;\n"
"   border: 2px solid #567c8d;\n"
"   border-radius: 8px;\n"
"   padding: 12px 25px;\n"
"}\n"
"QPushButton:hover {\n"
"   background-color: #e0d6cd;\n"
"}\n"
"QPushButton:pressed {\n"
"   background-color: #c8d9e6;\n"
"   padding-top: 12px;\n"
"   padding-bottom: 10px;\n"
"}\n")
        self.sort_button.setText("Отсортировать")
        self.sort_button.setObjectName("sort_button")


        """ Отображение: 
                Кнопки "Отсортировать"; 
                Столбца сортировки;
                Типа сортировки. """
        self.gridLayout.addWidget(self.sort_button, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.sort_column_combo, 3, 1, 1, 2)
        self.gridLayout.addWidget(self.sort_order_combo, 3, 3, 1, 2)


        """ Основная таблица с данными """
        self.data_table = QtWidgets.QTableView(parent=self.main_layout)
        self.data_table.setObjectName("data_table")
        self.data_table.setStyleSheet("QTableView {\n"
                                      "   background-color: #f5efeb;\n"
                                      "   gridline-color: #d0d0d0;\n"
                                      "   border: 2px solid #567c8d;\n"
                                      "   border-radius: 8px;\n"
                                      "   color: #2f4156;\n"
                                      "}\n"
                                      "QHeaderView::section { /* Заголовки столбцов */\n"
                                      "   background-color: #e0d6cd; /* Светло-бежевый фон заголовков */\n"
                                      "   color: #2f4156; /* Темно-синий текст заголовков */\n"
                                      "   border: 1px solid #d0d0d0;\n"
                                      "   padding: 5px;\n"
                                      "}\n"
                                      "QTableView QAbstractItemView::item {\n"
                                      "   border: 0.5px solid #e0d6cd;\n"
                                      "   color: #2f4156;\n"
                                      "}\n"
                                      "\n"
                                      "QTableView::item:selected{\n"
                                      "   background-color: #c8d9e6;\n"
                                      "}\n"
                                      "\n"
                                      "QTableView::item:hover{\n"
                                      "   background-color: #e0d6cd;\n"
                                      "}\n")
        self.data_table.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout.addWidget(self.data_table, 4, 0, 1, 5)  # Сдвинули вниз на 2 строки


        self.gridLayout_2.addWidget(self.main_layout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(parent=MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CheCloud"))
        self.choice_button.setText(_translate("MainWindow", "Выбрать файл"))
        self.save_button.setText(_translate("MainWindow", "Сохранить данные"))
        self.build_graph_button.setText(_translate("MainWindow", "Построить график"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Гистограмма"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Диаграмма рассеяния"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Линейный график"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Столбчатая диаграмма"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Круговая диаграмма"))
        self.file_path_label.setText(_translate("MainWindow", "Путь к файлу: "))