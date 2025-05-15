from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

class ForceTradeTestStrategy(IStrategy):
    timeframe = '5m'
    startup_candle_count = 1  # Démarrage rapide

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['buy'] = 1  # ✅ Forcer un signal d'achat
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['sell'] = 1  # ✅ Forcer un signal de vente
        return dataframe

