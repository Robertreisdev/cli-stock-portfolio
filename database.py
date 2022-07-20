import sqlite3
import urllib.request
import urllib.parse
import json


API_TOKEN = ""


def get_stock_ticker(ticker):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stockportfolio WHERE stock_ticker = ?", (ticker,))
    exist = c.fetchall()
    if exist:
        print(exist)
    else:
        print(f"Stock {ticker} not in portfolio!")
    conn.commit()
    conn.close()


def buy_stock(ticker, price=0, amt=0):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stockportfolio WHERE stock_ticker = ?", (ticker,))
    exist = c.fetchall()
    amt = int(amt)
    price = float(price)
    if not exist:
        print("value not in table")
        c.execute("INSERT INTO stockportfolio VALUES (?,?,?)", (ticker, price, amt))
        print(f"stock {ticker} added to portfolio")
    else:
        prev_price = exist[0][1]
        prev_amount = exist[0][2]
        total_purchase = (amt * price) + (prev_price * prev_amount)
        total_stock_amt = amt + prev_amount
        new_avg_share = round((total_purchase / total_stock_amt), 2)

        c.execute(
            "UPDATE stockportfolio SET purchase_price = ?, amount = ? WHERE stock_ticker = ?",
            (
                new_avg_share,
                total_stock_amt,
                ticker,
            ),
        )
        print(
            f"stock {ticker} has been updated with {total_stock_amt} shares at a cost basis of {new_avg_share}"
        )
    conn.commit()
    conn.close()


def sell_stock(ticker, price=0, amt=0):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stockportfolio WHERE stock_ticker = ?", (ticker,))
    exist = c.fetchall()
    amt = int(amt)
    price = float(price)
    if not exist:
        print("value not in table")
        print(f"stock {ticker} cannot be removed from portfolio")
    else:
        prev_amt = exist[0][2]
        if prev_amt < amt:
            amt = prev_amt
            print("No shorting stocks here!")
        amt = prev_amt - amt
        if amt == 0:
            c.execute("DELETE FROM stockportfolio WHERE stock_ticker = ?", (ticker,))
        else:
            c.execute(
                "UPDATE stockportfolio SET amount = ? WHERE stock_ticker = ?",
                (
                    amt,
                    ticker,
                ),
            )
        p_l = round((price * amt), 2)
        print(f"stock {ticker} has been sold with a return of {p_l}")
        conn.commit()
        conn.close()
        return p_l


def get_all_tickers():
    tickers = {}
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stockportfolio")
    for row in c:
        tickers[row[0]] = [row[1], row[2]]

    return tickers


def api_request(ticker):
    if isinstance(ticker, dict):
        url = f"https://cloud.iexapis.com/v1/stock/market/batch?symbols={','.join(ticker.keys()).lower()}&types=quote&token={API_TOKEN}"
    else:
        url = f"https://cloud.iexapis.com/v1/stock/market/batch?symbols={ticker}&types=quote&token={API_TOKEN}"
    stock_api_request = urllib.request.urlopen(url)
    data = stock_api_request.read()
    encoding = stock_api_request.info().get_content_charset("utf-8")
    final_Data = json.loads(data.decode(encoding))

    return final_Data


def pl_changes():
    ticker_arr = get_all_tickers()
    final_Data = api_request(ticker_arr)
    daily_changes = {}
    open_changes = {}

    for stock in ticker_arr:
        daily_changes[stock] = round(
            (final_Data[stock]["quote"]["change"] * ticker_arr[stock][1]), 2
        )
        open_changes[stock] = round(
            (
                (
                    final_Data[stock]["quote"][
                        "delayedPrice"
                        if final_Data[stock]["quote"]["delayedPrice"]
                        else "previousClose"
                    ]
                    - ticker_arr[stock][0]
                )
                * ticker_arr[stock][1]
            ),
            2,
        )
    return [daily_changes, open_changes]


def stock_lookup(ticker):
    final_Data = api_request(ticker)
    current_price = final_Data[ticker]["quote"][
        "delayedPrice"
        if final_Data[ticker]["quote"]["delayedPrice"]
        else "previousClose"
    ]
    print(f"Current price of {ticker} is {current_price}")


def display_pl():
    daily, open = pl_changes()

    print()
    print("{:<8} {:<15} {:<10} {:<10}".format("    ", "Stock", "Change", "Open P/L"))
    print("{:<8} {:<15} {:<10} {:<10}".format("    ", "------", "------", "------"))
    for stock_name in daily:
        print(
            "{:<8} {:<15} {:<10} {:<10}".format(
                "    ", stock_name, format(daily[stock_name], ".2f"), open[stock_name]
            )
        )
    print()


def display_portfolio():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stockportfolio")
    portfolio = c.fetchall()
    if portfolio:

        print(
            "{:<8} {:<15} {:<10} {:<10}".format(
                "    ", "Stock", "Avg Price", "Quantity"
            )
        )

        print(
            "{:<8} {:<15} {:<10} {:<10}".format(
                "    ", "-----", "---------", "--------"
            )
        )

        for stock in portfolio:
            print(
                "{:<8} {:<15} {:<10} {:<10}".format(
                    "    ", stock[0], format(stock[1], ".2f"), stock[2]
                )
            )

        print()

    else:
        print(
            "Portfolio currently empty \ntry adding some stocks with the `buy` command!"
        )
    conn.close()
