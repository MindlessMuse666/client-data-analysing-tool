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
            conn = sqlite3.connect(self.db_name,
                                   detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.df.to_sql("client_data",
                           conn,
                           if_exists="replace",
                           index=False)

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