import argparse
import sys
from producer_sol import mqProducer
def main(ticker: str, price: float, sector:str) -> None:
    routingKey = f"Stock.{ticker}.{sector}"
    routingKey.strip()
    producer = mqProducer(routingKey=routingKey, exchange_name="Tech Lab Topic Exchange")
    message = f"{ticker} is now ${price}"
    producer.publishOrder(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Stock Ticker, Price and Type."
    )
    parser.add_argument(
        "-t", "--ticker", type = str, help = "Stock Ticker", required = True
    )
    parser.add_argument(
        "-p", "--price", type = str, help = "Stock Price", required = True
    )
    parser.add_argument(
        "-s", "--sector", type = str, help = "Stock Sector", required = True
    )
    args = parser.parse_args()
    sys.exit(main(args.ticker, args.price, args.sector))
