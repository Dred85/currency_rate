from datetime import datetime

from utils import get_currency_rate, save_to_json, creat_db
from config import config

params = config()


def main():
    """
    Основная функция программы. Получает от пользователя название валюты USD или EUR,
    получает и выводит на экран текущий курс валюты от API. Записывает данные в json файл.
    """
    while True:
        currency = input("Введите название валюты (USD или EUR): ").upper()
        if currency not in ["USD", "EUR"]:
            print("Некорректный ввод")
            continue

        rate = get_currency_rate(currency)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Курс {currency} к рублю: {rate:.2f}")
        data = {"currency": currency, "rate": rate, "timestamp": timestamp}
        save_to_json(data)
        creat_db('currency_rate', params)

        choice = input("Выберите действие: (1 - продолжить, 2 - выйти) ")
        if choice == "1":
            continue
        elif choice == "2":
            break
        else:
            print("Некорректный ввод")




if __name__ == "__main__":
    main()
