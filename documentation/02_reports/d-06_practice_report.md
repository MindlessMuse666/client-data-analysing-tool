# ТЗ-4. План разработки инструмента для анализа клиентских данных с использованием `Python` и `PyQt`.

**Список команды и роли:**
1. Fullstack-разработчики: Бедин Владислав (Тимлид), Киян Георгий
2. Аналитик данных / Администратор базы данных: Букарев Кирилл
3. UI/UX-дизайнер: Гаврилова Дженнет
4. Тестировщик / Документатор / Администратор базы данных: Вельдяева Александра

**Fullstack-разработчики (Frontend & Backend):**
  * Инициализация проекта `PyQT`.
  * Реализация базового интерфейса для загрузки файлов.
  * Настройка отображения данных таблицы.
  * Подключение локальной базы данных `SQLite` для хранения загруженных данных.
  * Включение функций фильтра к интерфейсу.
  * Оптимизация интерфейса.
  * Добавление инструкций по работе с приложением.

**Аналитик данных:**
  * Настройка обработки данных с использованием `Pandas`.
  * Реализация вычислений ключевых метрик.
  * Настройка функций фильтрации данных.
  * Построение графиков с использованием `Matplotlib`.
  * Тестирование вычисления ключевых метрик.

**UI/UX-дизайнер:**
  * Разработка макетов интерфейса (загрузка данных, таблиц, графиков).
  * Создание диаграммы вариантов использования (варианты использования).
  * Доработка интерфейса (анимации, обработка ошибок).
  * Уточнение визуального стиля.

**Тестировщик / Документатор:**
  * Проверка обработки данных, фильтрация и построение графиков.
  * Завершение технической документации:
    * UML-диаграммы.
    * Подробное описание методов анализа данных.
  * Составление пользовательской документации:
    * Руководство по работе с приложением.



## Отчет: 

### День 6.
**1. Fullstack-разработчики:**
  * Исправлен баг, при котором в приложении не отображались иконки (PyQt6 запретил пользоваться ресурсными qrc-файлами, поэтому теперь импорт идёт напрямую через проект).
  * Исправлен баг, при котором невозможно было выбрать новый csv-файл для анализа.
  * Исправлен баг, при котором не работала кнопка "Выбрать файл".
  * В скрипте `plot_handler.py` переработана бизнес-логика.
  * Улучшена круговая диаграмма. Теперь её график строится, ограничивая количество категорий в легенде.
  * Исправлен баг, при которой после построения графика с некорректными данными и вызова предупреждения об этом, выводился пустой график.
  * Реализована функция сортировки данных по убыванию/возрастанию столбца.

     
**2. UI/UX-дизайнер:**
  * Переделан фронтэнд-макет приложения.
  * Добавлены новые кнопки и поля заполнения, связанные с сортировкой.
  * Начата разработка более адаптивного интерфейса.
  
       
**3. Аналитик данных / Администратор базы данных:**
  * Рефакторинг скрипта `main_window.py`.
  * Проведён рефакторинг скрипта `plot_handler.py`.
  * Удалена лишняя функция `_create_and_show_plot` из скрипта `main_window.py`.

    
**4. Тестировщик / Документатор / Администратор базы данных:**
  * Изменена логика привязки элементов во фронтенд-макете `client_data_analising_tool.py` (В будущем необходимо сделать более весомый рефакторинг: выделить стили css отдельно от макета).
  * Проведён рефакторинг скрипта UI-макета (client_data_analising_tool.py).
  * Составлен отчет за шестой день.