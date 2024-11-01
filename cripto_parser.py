import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL для главной страницы с топовыми криптовалютами
url = "https://coinmarketcap.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# Извлечение таблицы с классом
table = soup.find("table", class_="sc-7b3ac367-3 etbcea cmc-table")

# Извлечение первых 10 криптовалют с ценами
top_10_cryptos = []

for row in table.select("tr")[:10]:
    # Получение названия криптовалюты
    name_tag = row.select_one("p.coin-item-name")
    # Получение символа криптовалюты
    symbol_tag = row.select_one("p.coin-item-symbol")
    # Получение текущей цены
    price_tag = row.select_one("div.sc-b3fc6b7-0.dzgUIj > span")
    # Получение объёма за 24 часа
    volume_tag = row.select_one("p.sc-71024e3e-0.bbHOdE.font_weight_500")

    # Проверка, что элементы найдены
    if name_tag and symbol_tag and price_tag and volume_tag:
        name = name_tag.text
        symbol = symbol_tag.text
        price = price_tag.text
        volume = volume_tag.text

         # Добавляем данные криптовалюты в список
        top_10_cryptos.append((name, symbol, price, volume))

# Вывод результата
for i, (name, symbol, price, volume) in enumerate(top_10_cryptos, start=1):
    print(f"{i}. {name} ({symbol}): {price}: {volume}")

# Создание DataFrame
top10_crypto_df = pd.DataFrame(top_10_cryptos, columns=['Name', 'Symbol', 'Price', 'Volume_24h'])

# Сохранение в CSV файл
top10_crypto_df.to_csv('top10_cryptos.csv', index=False)

# Вывод результата
print(top10_crypto_df)
