from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import IntParameter, DecimalParameter
import talib.abstract as ta
import pandas as pd


class SampleStrategy(IStrategy):
    timeframe = '5m'

    # Définition des paramètres hyperopt
    buy_rsi = IntParameter(10, 50, default=30, space='buy')
    sell_rsi = IntParameter(50, 90, default=70, space='sell')

    minimal_roi = {"0": 0.02}
    stoploss = -0.03

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe['close'], timeperiod=14)
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[:, 'buy'] = 0
        dataframe.loc[
            (dataframe['rsi'] < self.buy_rsi.value),
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[:, 'sell'] = 0
        dataframe.loc[
            (dataframe['rsi'] > self.sell_rsi.value),
            'sell'
        ] = 1
        return dataframe

