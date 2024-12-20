# Инструмент для анализа клиентских данных (RU)

## Функции приложения:

### 1. База данных `SQLite`:
  * Хранение данных, которые были импортированы из выбранного пользователем csv-файла.
  * Сохранения данных, которые были импортированы из выбранного пользователем csv-файла.
  * Данные сохраняются в 3-х случаях:
    * При начальном импорте `csv-файла`.
    * При нажатии на кнопку сохранения данных.
    * Перед закрытием приложения.

### 2. Поле выбора **"Построить график"** представляет собой список из доступных типов графиков:
  * Линейный график.
  * Диаграмма рассеяния.
  * Линейный график.
  * Столбчатая диаграмма.
  * Круговая диаграмма.

Также теперь для каждого из типа графика можно **выбрать столбец**, по которому этот график будет построен.

### 3. Редактирование полей столбцов:
  * После ввода новых данных происходит их **валидация** (то есть, если пользователь изменит число на строку и затем попытается создать график по этому столбцу - выпадет предупреждение).
  * Синхронизирована кодировка. Благодаря этому теперь нет ошибок `invalid syntax` при использовании кириллицы в полях столбцов.

# Скриншоты приложения:

## Frontend-GUI:

### Макет frontend-GUI из `Qt Designer` (пока не встроен в бекэнд) (от 19.12):
![client-data-analising-tool](https://github.com/user-attachments/assets/1670b795-0cc3-4086-b6b1-05291ad1060c)

### Макет frontend-GUI из `Qt Designer` (пока не встроен в бекэнд) (от 21.12):
![image](https://github.com/user-attachments/assets/88fdd81d-d99e-46d3-a75c-8965f5edcc89)

---

## Backend-GUI:

### Backend-GUI (от 17.12):
![image](https://github.com/user-attachments/assets/da5b0dcd-2d52-4cb5-906a-7ed101bfcb0d)
![image](https://github.com/user-attachments/assets/7114b210-6474-4d8a-bb5c-34c7137e6d79)

### Backend-GUI (от 19.12):
![image](https://github.com/user-attachments/assets/3f06b4d0-cfa4-4621-9ae5-f43d4834a22b)

### Backend-GUI (от 21.12):
![image](https://github.com/user-attachments/assets/bd9e3733-818d-44ce-bae5-d6bb4f1adc66)

---

Начиная с `21.12`, интерфейсы синхронизированы.

---

# Авторы проекта:

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
