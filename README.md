# Клиентский инструмент для анализа данных
---

Этот инструмент предназначен для анализа данных, загруженных из `CSV-файлов`, их отображения, сортировки, построения графиков и создания отчетов. Приложение написано на `Python` с использованием библиотеки `PyQt6` для графического интерфейса, pandas для обработки данных и `matplotlib` для отрисовки графиков, `reportlab` для генерации отчётов.


## Особенности
---

-   **Загрузка данных:** Загрузка данных из `CSV-файлов` с разделителем `;`.
-   **Отображение данных:** Отображение загруженных данных в виде таблицы с возможностью редактирования.
-   **Сортировка данных:** Сортировка данных по выбранному столбцу в порядке возрастания или убывания.
-   **Построение графиков:**
    -   Гистограмма
    -   Диаграмма рассеяния
    -   Линейный график
    -   Столбчатая диаграмма
    -   Круговая диаграмма
-   **Генерация отчетов:** Создание отчетов в формате `PDF` с данными из таблицы.
-   **Сохранение:** Сохранение данных в базу данных `SQLite`.
-   **Открытие последнего файла:** Автоматическое открытие последнего использованного `CSV-файла` при запуске приложения.


## Структура проекта
---

```
client_data_analysing_tool/
├── core/
│  ├── main.py  # Точка входа в приложение
│  ├── main_window.py  # Основное окно приложения
│  └── table_window.py  # Отдельное окно таблицы данных
├── data_processing/
│  ├── data_handler.py  # Загрузка, сохранение, сортировка данных
│  └── report_handler.py  # Обработчик отчётов
├── frontend/
│  ├── gui_main_window.py  # UI-макет приложения 
│  └── align_delegate.py  # Делегат выравнивания текста в таблице
├── model/
│  └── pandas_model.py  # Модель отображения DataFrame в QTableView
├── plotting/
│  └── plot_handler.py  # Обработка и отрисовка графиков
├── static/
│  ├── fonts/
│  │  └── Secession_Text.ttf
│  ├── resources/
│  │  ├── resource_pathes/
│  │  │  └── resource_pathes.py # Пути к иконкам
│  │  ├── arrow_down_24dp.svg
│  │  ├── choice_24dp.svg
│  │  ├── delete_24dp.svg
│  │  ├── file_path_24dp.svg
│  │  ├── fullscreen_24dp.svg
│  │  ├── graph_24dp.svg
│  │  ├── main_icon.ico
│  │  ├── report_24dp.svg
│  │  ├── save_24dp.svg
│  │  └── sort_24dp.svg
│  └── styles/
│    └── styles.py  # CSS-стили UI-элементов
└──
```


## Установка
---

**1. Клонируйте репозиторий:** 
git clone <ваш_репозиторий>
    cd client_data_analysing_tool

**2. Создайте виртуальное окружение (рекомендуется):** python -m venv venv
  source venv/bin/activate # Для Linux/macOS
  venv\Scripts\activate # Для Windows

**3. Установите зависимости:** pip install -r requirements.txt

**4. Запустите приложение:** python core/main.py


## Использование
---

**Загрузка данных:**
  -  Нажмите кнопку "Выбрать файл" и выберите `CSV-файл` для загрузки.
  -  Путь к выбранному файлу отобразится в верхней части окна.
  -  Данные из файла отобразятся в таблице.
  -  Примечание: Файл должен быть в кодировке `utf-8`.

**Сохранение данных:**
  -  Нажмите кнопку `Сохранить данные` для сохранения изменений в базу данных.

**Сортировка данных:**
  -  Выберите столбец для сортировки из выпадающего списка.
  -  Выберите порядок сортировки (возрастание или убывание) из выпадающего списка.
  -  Нажмите кнопку `Отсортировать` для сортировки данных.

**Построение графиков:**
  -  Выберите тип графика из выпадающего списка `Тип графика:`.
  -  В зависимости от типа графика:
    -  Для гистограммы, столбчатой и круговой диаграмм: выберите столбец для построения графика из выпадающего списка `Столбец:`.
    -  Для диаграммы рассеяния и линейного графика: выберите ось `X` и `Y` из выпадающих списков.
  -  Нажмите кнопку `Построить график` для отображения графика в отдельном окне.

**Создание отчета:**
  -  Нажмите кнопку `Создать отчёт` для создания отчета в формате `PDF`.
  -  Выберите место для сохранения отчета.

**Раскрытие таблицы:**
  -  Нажмите кнопку `Раскрыть таблицу` для отображения данных в отдельном окне.

    
## GUI приложения
---

### Интерфейс готовой программы:
![image](https://github.com/user-attachments/assets/7b1dcf1e-290a-4d54-842c-7e7d49dea4a9)


## Построение графиков
---

### Гистограмма:
![image](https://github.com/user-attachments/assets/fc3e63f3-1884-4833-a9d2-92f0ac970f79)

### Диаграмма рассеяния:
![image](https://github.com/user-attachments/assets/ba62677f-4d8c-4fab-9586-946f6cf1bd37)

### Линейный график:
![image](https://github.com/user-attachments/assets/9fb356e8-845a-4f79-b8a4-74d8cf46fe44)

### Столбчатая диаграмма:
![image](https://github.com/user-attachments/assets/359bc1cd-2fc3-4725-8bf9-d8ed32dae141)

### Круговая диаграмма:
![image](https://github.com/user-attachments/assets/78d5fdb0-3d20-475a-85a3-99388661bdb8)


## Генерация отчетов
---

### Пример сгенерированного отчёта:
![image](https://github.com/user-attachments/assets/c79e57b6-71fd-464d-8028-acf112725c4f)

[Скачать отчёт в PDF](https://drive.google.com/file/d/1mxVdWQeT_ldl8Lcv4AjMIe8qELf0FjDQ/view?usp=drive_link)

## Зависимости
---

-  PyQt6
-  pandas
-  matplotlib
-  reportlab


## Авторы проекта
---

  * [Бедин Владислав](https://github.com/MindlessMuse666 "Владислав: https://github.com/MindlessMuse666"):
    * Team Lead
    * Backend
    * Frontend
  * [Киян Георгий](https://github.com/nineteentearz "Егор: https://github.com/nineteentearz"):
    * Backend
    * Frontend
  * [Вельдяева Александра](https://github.com/FrierenWay "Александра: https://github.com/FrierenWay"):
    * Analyst
    * Software Tester
    * Documentation
    * Database
  * [Букарев Кирилл](https://github.com/bukabtw "Кирилл: https://github.com/bukabtw"):
    * Analyst
    * Software Tester
    * Documentation
    * Database
  * [Гаврилова Дженнет](https://github.com/Jenko-zhulenko "Дженнет: https://github.com/Jenko-zhulenko"): 
    * Frontend
    * UI-Designer
    * Project Designer

