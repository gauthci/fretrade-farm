from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class AggressiveRSIStrategy(IStrategy):
    timeframe = '5m'

    minimal_roi = {
        "0": 0.04,
        "30": 0.02,
        "60": 0
    }

    stoploss = -0.05
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    use_custom_stoploss = False
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    minimal_volume = 1000

    # Hyperoptable parameters
    rsi_buy = 30
    rsi_sell = 70

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
        boll = ta.BBANDS(dataframe['close'], timeperiod=20)
        dataframe['bb_upperband'] = boll['upperband']
        dataframe['bb_middleband'] = boll['middleband']
        dataframe['bb_lowerband'] = boll['lowerband']
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['volatility'] = (dataframe['high'] - dataframe['low']) / dataframe['close']
        dataframe['sma_volume'] = dataframe['volume'].rolling(window=20).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_buy) &
            (dataframe['close'] < dataframe['bb_lowerband']) &
            (dataframe['ema_50'] > dataframe['ema_200']) &
            (dataframe['volume'] > self.minimal_volume) &
            (dataframe['volatility'] > 0.005),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > self.rsi_sell) |
                (dataframe['close'] > dataframe['bb_upperband']) |
                (dataframe['close'] < dataframe['ema_200'])
            ) &
            (dataframe['volume'] > self.minimal_volume),
            'sell'] = 1
        return dataframe

