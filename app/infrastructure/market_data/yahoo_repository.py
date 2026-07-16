import yfinance as yf

from app.domain.repositories.price_repository import PriceRepository


class YahooRepository(PriceRepository):

    def get_history(self, ticker: str):

        stock = yf.Ticker(ticker)

        return stock.history(period="1y")