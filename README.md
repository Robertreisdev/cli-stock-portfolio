# cli-stock-portfolio

A simple user-friendly CLI tool to create and manage your stock portfolio. 
Allowing users to track gains and losses when selling stocks. 
As well as look up real time stock data on your portfolio or any other stock provided you know its ticker right from the command line.
It will also keep track of your current dollar cost average (DCA) as you buy and sell stocks.

```bash

C:\Users> portfolio

       Stock           Change     Open P/L
        -----           ------     --------
        MSFT            -2.47      241.72
        AAPL            -9.3       90.51
        RTX             -4.29      -86.31
        WMT             -0.9       27.21
        TSLA            4.32       1800.6
        NVDA            10.17      112.86
        NFLX            5.43       207.33
        IBM             -5.37      59.76
        GME             15         64.92
        
        
        
C:\Users> sell MSFT 1 245.24 1

stock MSFT has been sold with a return of 15.12
```



Requirements
------------

cli-stock-portfolio requires the following to run:

  * [Python][py] 3.6+
  * API Key from [IEX cloud][ex]

[py]: https://www.python.org/
[ex]: https://iexcloud.io/
