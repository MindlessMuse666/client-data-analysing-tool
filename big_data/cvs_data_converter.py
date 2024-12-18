import csv
import os


def clean_csv(input_filepath):
    """ Удаляет два пробела перед каждой точкой с запятой в CSV-файле,
    перезаписывая исходный файл. Поддерживает кодировку cp1251.

    Args:
        input_filepath: Путь к исходному CSV-файлу. """
    try:
        # Создаем временный файл
        temp_filepath = input_filepath + ".tmp"

        with open(input_filepath, 'r', encoding='cp1251') as infile, \
                open(temp_filepath, 'w', encoding='cp1251', newline='') as outfile:

            reader = csv.reader(infile, delimiter=';')
            writer = csv.writer(outfile, delimiter=';')

            for row in reader:
                cleaned_row = [item.rstrip('  ') for item in row]
                writer.writerow(cleaned_row)

        # Заменяем исходный файл временным
        os.replace(temp_filepath, input_filepath)

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_filepath} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


input_file = r"C:\Users\vlad\PycharmProjects\client-data-analysing-tool\big_data\test_data_csv\client_test_data_1.csv"

clean_csv(input_file)
print(f"Файл {input_file} обработан и перезаписан.")