import json
import os
import psycopg2
import requests
from environs import Env
from config import config

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

CURRENCY_RATES_FILE = "currency_rates.json"
API_KEY = env('EXCHANGE_RATE_API_KEY')


def get_currency_rate(currency: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={'apikey': API_KEY})
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def save_to_json(data: dict) -> None:
    """Сохраняет данные в json файл"""

    with open(CURRENCY_RATES_FILE, "a") as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data_list, json_file)



def creat_db(database_name, params):
    # Подключаемся к базе данных
    # conn = psycopg2.connect(dbname="postgres", **params)
    # Устанавливаем autocommit, чтобы изменения сохранялись сразу же
    # conn.autocommit = True
    # Получаем курсор
    # cur = conn.cursor()
    # Удаляем базу данных, если она уже существует
    # cur.execute(f'DROP DATABASE IF EXISTS {database_name};')
    #  Создаем базу данных
    # cur.execute(f'CREATE DATABASE {database_name};')

    # conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            # удаляем таблицу currency_rate, если она уже существует
            cur.execute("DROP TABLE IF EXISTS currency_rate")
            # Создаем таблицу companies, если она не существует
            cur.execute("CREATE TABLE currency_rate (currency VARCHAR(5), rate FLOAT, timestamp TIMESTAMP)")

            # Получаем данные из JSON файла
            with open("currency_rates.json") as json_file:
                currencies = json.load(json_file)

            # Добавляем данные из JSON файла в таблицу
            for currency in currencies:
                cur.execute("INSERT INTO currency_rate (currency, rate, timestamp) VALUES (%s, %s, %s)",
                            (currency.get("currency"), currency.get("rate"), currency.get("timestamp")))

            # Фиксируем изменения
            conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    params = config()
    creat_db('test_db', params)
