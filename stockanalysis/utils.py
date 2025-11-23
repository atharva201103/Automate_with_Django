from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol,exchange=None):
    if exchange=='NSE':
        symbol=f"{symbol}.NS"
        url=f"https://finance.yahoo.com/quote/{symbol}/"
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
    try:
        response=requests.get(url,headers=headers)
        soup=BeautifulSoup(response.content,'html.parser')
        current_price = soup.find("span", {"data-testid":"qsp-price"}).text.strip()
        previous_close=soup.find("fin-streamer",{"data-field":"regularMarketPreviousClose"}).text.strip()
        percentage_changed=soup.find("span",{"data-testid":"qsp-price-change"}).text.strip()
        week_low_high_range=soup.find("fin-streamer",{"data-field":"fiftyTwoWeekRange"}).text.strip()
        week_52_low,week_52_high=week_low_high_range.split(" - ")
        volume=soup.find("fin-streamer",{"data-field":"regularMarketVolume"}).text.strip()
        market_cap=soup.find("fin-streamer",{"data-field":"marketCap"}).text.strip()
        pe_ratio=soup.find("fin-streamer",{"data-field":"trailingPE"}).text.strip()
        label = soup.find("span", class_="label", string="Forward Dividend & Yield")

        value = None
        if label:
            li = label.find_parent("li")  # the <li> in the screenshot
            if li:
                value_span = li.find("span", class_="value")
                if value_span:
                    value = value_span.get_text(strip=True)

        dividend_yield = value if value else "N/A"

        

        # print(f"Current price of {symbol} is {current_price}")
        # print(f"Previous Close price of {symbol} is {previous_close}")
        # print(f"Percentage changed of {symbol} is {percentage_changed}")
        # print(f"52 Week Low of {symbol} is {week_52_low}")
        # print(f"52 Week High of {symbol} is {week_52_high}")
        # print(f"Volume of {symbol} is {volume}")
        # print(f"Market Cap of {symbol} is {market_cap}")
        # print(f"P/E Ratio of {symbol} is {pe_ratio}")
        # print(f"Dividend Yield of {symbol} is {dividend_yield}")

        stock_response= {
            "current_price": current_price,
            "previous_close": previous_close,
            "percentage_changed": percentage_changed,
            "week_52_low": week_52_low,
            "week_52_high": week_52_high,
            "volume": volume,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "dividend_yield": dividend_yield
        }
        return stock_response
        
    except Exception as e:
        print(f"Cannot Scrape data for this symbol: {symbol}. Error: {e}")