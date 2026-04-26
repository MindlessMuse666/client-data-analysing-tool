import sqlite3
from typing import Optional

import pandas as pd
from PyQt6.QtWidgets import QMessageBox


class DataHandler:
    """
    Класс для обработки данных, включая загрузку из CSV, сохранение в базу данных SQLite,
    сортировку и управление путями к файлам.

    Attributes:
        df (pd.DataFrame): DataFrame для хранения данных.
        db_name (str): Имя файла базы данных SQLite.
        _last_file_path_file (str): Имя файла для хранения последнего пути к файлу.
    """
    def __init__(self, db_name: str = "database.db", last_file_path_file: str = "last_open_file.txt"):
        """
        Инициализирует DataHandler с указанным именем базы данных и файлом для хранения последнего пути.

        Args:
            db_name (str, optional): Имя файла базы данных SQLite. По умолчанию "database.db".
            last_file_path_file (str, optional): Имя файла для хранения последнего пути к файлу. По умолчанию "last_open_file.txt".
        """
        self.df = pd.DataFrame()
        self.db_name = db_name
        self._last_file_path_file = last_file_path_file

    def load_csv(self, file_name: str) -> None:
        """
        Загружает данные из CSV файла в DataFrame.

        Args:
            file_name (str): Путь к CSV файлу.
        """
        try:
            try:
                self.df = pd.read_csv(file_name, sep=';', encoding='utf-8', on_bad_lines='skip')
                self.save_to_db()
            except UnicodeDecodeError:
                QMessageBox.critical(None, "Ошибка", "Кодировка файла не соответствует 'utf-8'.")
                self.load_last_file_path()
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка при загрузке CSV: {e}")
            self.df = pd.DataFrame()

    def save_last_file_path(self, file_path: str) -> None:
        """
        Сохраняет путь к последнему открытому файлу.

        Args:
            file_path (str): Путь к файлу.
        """
        try:
            with open(self._last_file_path_file, "w") as f:
                f.write(file_path)
        except Exception as e:
            print(f"Ошибка сохранения пути к последнему файлу: {e}")

    def load_last_file_path(self) -> Optional[str]:
        """
        Загружает путь к последнему открытому файлу.

        Returns:
            Optional[str]: Путь к файлу, если он существует, иначе None.
        """
        try:
            with open(self._last_file_path_file, "r") as f:
                return f.readline().strip()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Ошибка загрузки пути к последнему файлу: {e}")
            return None

    def save_to_db(self) -> None:
        """
        Сохраняет текущий DataFrame в базу данных SQLite.
        """
        conn = None
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

    def sort_dataframe(self, column_name: str, ascending: bool) -> None:
        """
        Сортирует DataFrame по указанному столбцу.

        Args:
            column_name (str): Имя столбца для сортировки.
            ascending (bool): True для сортировки по возрастанию, False по убыванию.
        """
        self.df.sort_values(by=column_name, ascending=ascending, inplace=True)

    def load_from_db(self) -> None:
        """
        Загружает данные из базы данных SQLite в DataFrame.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name,
                                   detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            df = pd.read_sql_query("SELECT * FROM client_data", conn)
            if not df.empty:
                self.df = df
                print("Данные успешно загружены из базы данных.")
            else:
                print("База данных пуста.")
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Ошибка базы данных", f"Ошибка при загрузке данных из базы: {e}")
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Произошла непредвиденная ошибка: {e}")
        finally:
            if conn:
                conn.close()