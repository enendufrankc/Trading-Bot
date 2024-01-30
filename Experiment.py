from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 

import os
from dotenv import load_dotenv

# load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")

class MLTrader(Strategy):
    def initialise(self, symbol: str = "TSLA"):
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 

    def on_trading_iteration(self):
        if self.last_trade is None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"


start_date = datetime(2023,12,31)
end_date = datetime(2024,1,10)

broker = Alpaca(ALPACA_CREDS) 

strategy = MLTrader(
    name= "mlstrat", 
    broker=broker,
    parameters={"symbol": "TSLA"}
)

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol": "TSLA"}
)
