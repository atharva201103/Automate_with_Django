from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol,exchange=None):
    if exchange=='NSE':
        symbol=f"{symbol}.NS"
    elif exchange=='NASDAQ':
        url=f"https://finance.yahoo.com/quote/{symbol}/"
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 "
        "Brave/137.0.0.0 "
        "Safari/537.36"
    )
}
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
    price_tag = soup.find("span", {"data-testid":"qsp-price"})
    price=price_tag.text.strip()
    print(f"Current price of {symbol} is {price}")
