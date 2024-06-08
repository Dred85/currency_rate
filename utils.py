import json
import os
import psycopg2
import requests
from environs import Env

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

def creat_db(dataname, params):
    # Подключаемся к базе данных
    conn = psycopg2.connect(dbname="postgres", **params)
    # Устанавливаем autocommit, чтобы изменения сохранялись сразу же
    conn.autocommit = True
    # Получаем курсор
    cur = conn.cursor()
    # Удаляем базу данных, если она уже существует
    cur.execute(f'DROP DATABASE IF EXISTS {database_name};')
    #  Создаем базу данных
    cur.execute(f'CREATE DATABASE {database_name};')

    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            # удаляем таблицу companies, если она уже существует
            cur.execute("DROP TABLE IF EXISTS companies")
            # Создаем таблицу companies, если она не существует
            cur.execute("CREATE TABLE companies (company_id INT PRIMARY KEY, company_name VARCHAR(255))")

            # Добавляем данные из JSON файла в таблицу
            for company_name, company_id in companies[0].items():
                cur.execute("INSERT INTO companies (company_id, company_name) VALUES (%s, %s)",
                            (company_id, company_name))

            # Фиксируем изменения
            conn.commit()

