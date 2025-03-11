"""
Модуль для работы с базой данных MySQL

Содержит класс Database для:
- Инициализации подключения
- Создания таблицы
- Вставки данных
"""


from typing import List
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


class Database():
    """
    Класс для управления подключением и операциями с базой данных
    
    Аргументы:
    Использует переменные окружения из .env файла:
    - HOST: Адрес сервера БД
    - USER: Имя пользователя
    - PASSWORD: Пароль
    - DB_NAME: Название базы данных
    """
    def __init__(self):
        """Инициализация подключения и создание таблицы при необходимости"""
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chart_data (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        date DATE UNIQUE,
                        value DECIMAL(10,2)
                    )
                """
            )
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def insert_data(self, data: List):
        """
        Вставка данных в таблицу chart_data
        
        Аргументы:
        data: Список кортежей в формате (date, value)
        
        Обрабатывает:
        - Множественную вставку данных
        """
        try:
            query = "INSERT INTO chart_data (date, value) VALUES (%s, %s)"
            self.cursor.executemany(query, data)
            self.connection.commit()
            print("Данные успешно добавлены")
        except Error as e:
            print(f"Ошибка добавления данных: {e}")

