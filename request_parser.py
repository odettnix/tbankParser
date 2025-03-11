import requests
from datetime import datetime
from database import Database

def main():
    """
    Основная функция выполнения скрипта:
    1. С помощью библиотеки requests обращается к апи ТБанка
    2. Сохраняет данные в MySQL базу данных
    """
    try:
        url = 'https://www.tbank.ru/api/invest-gw/capital/funds/v1/indexes/TIPOUS/history?period=year&sessionId=iRcGCTZqVFsSnxxi9OuM1Zd9AUU7K6wt.auth-entity-mgmt-848874fcdd-78qpq&appName=web&appVersion=1.513.0&origin=web'
        response = requests.get(url).json()
        data = response["payload"]["index"][-10:]

        # Преобразуем данные в формат для вставки в базу MySQL
        data_sql =  [(datetime.fromisoformat(item["dateTime"]).date(), item['value']) for item in data]

        # Добавляем данные в бд 
        db = Database()
        db.insert_data(data_sql)
    except Exception as e:
        print(f"Ошибка в работе скрипта: {e}")

if __name__ == "__main__":
    main()