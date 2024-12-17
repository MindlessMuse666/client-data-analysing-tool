import sqlite3

import pandas as pd


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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                )
            ''')
            for col in self.df.columns:
                cursor.execute(f"ALTER TABLE client_data ADD COLUMN '{col}' TEXT")

            for index, row in self.df.iterrows():
                placeholders = ", ".join(["?"] * len(row))
                cursor.execute(f"INSERT INTO client_data ({', '.join(['?'] * len(self.df.columns))}) VALUES ({placeholders})", tuple(row))

            conn.commit()
            print("Данные успешно сохранены в базу данных.")

        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Столбцы уже существуют. Данные обновлены.")
            else:
                print(f"Ошибка при сохранении данных: {e}")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
        finally:
            if conn:
                conn.close()