from database import *
import time
import os


def handle_raw_input(raw_input):
    clean_input = raw_input.split()

    if not clean_input:
        clean_input = ["empty"]
    return clean_input


def list_of_cmds():
    print("list of commands to be added")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def app():
    running = True
    arg = handle_raw_input(input())

    while running:
        if arg[0] == "quit" or arg[0] == "q":
            print("Terminating Stock Portfolio")
            time.sleep(0.5)
            clear()
            running = False
            break
        elif arg[0] == "stock":
            get_stock_ticker(arg[1])
        elif arg[0] == "price":
            stock_lookup(arg[1])
        elif arg[0] == "show":
            display_pl()
        elif arg[0] == "buy":  
            buy_stock(arg[1], arg[2], arg[3])
        elif arg[0] == "sell":
            sell_stock(arg[1], arg[2], arg[3])
        elif arg[0] == "portfolio" or arg[0] == "port":
            display_portfolio()
        elif arg[0] == "empty":
            pass
        elif arg[0] == "clear":
            clear()
        else:
            print("Unknown command")
            list_of_cmds()

        arg = handle_raw_input(input())


if __name__ == "__main__":
    app()
