import talib.abstract as ta
import pandas as pd

from freqtrade.strategy import IStrategy, IntParameter

class AggressiveRSIStrategy(IStrategy):
    minimal_roi = {
        "0": 0.202,
        "30": 0.074,
        "67": 0.021,
        "181": 0
    }

    stoploss = -0.345
    timeframe = '5m'

    # Optimized hyperopt parameters
    buy_rsi = IntParameter(40, 40, default=40, space='buy', optimize=False)
    sell_rsi = IntParameter(89, 89, default=89, space='sell', optimize=False)

    trailing_stop = True
    trailing_stop_positive = 0.346
    trailing_stop_positive_offset = 0.418
    trailing_only_offset_is_reached = False

    process_only_new_candles = True
    startup_candle_count = 50

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe['close'], timeperiod=14)
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (dataframe['rsi'] < self.buy_rsi.value),
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (dataframe['rsi'] > self.sell_rsi.value),
            'sell'
        ] = 1
        return dataframe

