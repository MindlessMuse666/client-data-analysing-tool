import sqlite3

import pandas as pd
from PyQt6.QtWidgets import QMessageBox


class DataHandler:
    def __init__(self):
        self.df = pd.DataFrame()
        self.db_name = "client_data.db"

    def load_csv(self, file_name):
        self.df = pd.read_csv(file_name, sep=';', encoding='cp1251', on_bad_lines='skip')

    def save_last_file_path(self, file_path):
        try:
            with open("last_file.txt", "w") as f:
                f.write(file_path)
        except Exception as e:
            print(f"Ошибка сохранения пути к последнему файлу: {e}")

    def load_last_file_path(self):
        try:
            with open("last_file.txt", "r") as f:
                return f.readline().strip()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Ошибка загрузки пути к последнему файлу: {e}")
            return None

    def save_to_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Создаем таблицу, если её не существует
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                )
            ''')
            conn.commit() # Commit после создания таблицы

            # Получаем список существующих столбцов
            cursor.execute("PRAGMA table_info(client_data)")
            existing_columns = {column[1] for column in cursor.fetchall()}

            # Добавляем новые столбцы, если они есть
            new_columns = set(self.df.columns) - existing_columns
            for col in new_columns:
                cursor.execute(f"ALTER TABLE client_data ADD COLUMN '{col}' TEXT")
            conn.commit()

            # Вставляем или обновляем данные.  Используем параметризованный запрос!
            cursor.execute("SELECT id FROM client_data")
            existing_ids = {row[0] for row in cursor.fetchall()}

            for index, row in self.df.iterrows():
                if index + 1 in existing_ids:
                    # Обновление существующей строки (предполагаем, что id соответствует индексу)
                    update_query = f"UPDATE client_data SET {', '.join([f'{col} = ?' for col in self.df.columns])} WHERE id = ?"
                    cursor.execute(update_query, tuple(row) + (index + 1,))
                else:
                    # Вставка новой строки
                    insert_query = f"INSERT INTO client_data ({', '.join(self.df.columns)}) VALUES ({', '.join(['?'] * len(self.df.columns))})"
                    cursor.execute(insert_query, tuple(row))
            conn.commit()
            print("Данные успешно сохранены в базу данных.")

        except sqlite3.Error as e:
            QMessageBox.critical(None, "Ошибка базы данных", f"Ошибка при работе с базой данных: {e}")
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Произошла непредвиденная ошибка: {e}")
        finally:
            if conn:
                conn.close()

    def sort_dataframe(self, column_name, ascending):
        self.df.sort_values(by=column_name, ascending=ascending, inplace=True)