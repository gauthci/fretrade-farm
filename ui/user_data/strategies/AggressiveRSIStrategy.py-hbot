from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import IntParameter
from pandas import DataFrame
import talib.abstract as ta


class AggressiveRSIStrategy(IStrategy):
    timeframe = '5m'
    max_open_trades = 4

    # Optimized minimal ROI tiers
    minimal_roi = {
        "0": 0.228,
        "27": 0.076,
        "56": 0.031,
        "166": 0
    }

    # Optimized stoploss
    stoploss = -0.339
    trailing_stop = False

    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False,  # correction: False
        'force_exit': 'market'
    }

    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    process_only_new_candles = True
    startup_candle_count = 0
    position_adjustment_enable = False
    max_entry_position_adjustment = -1
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperopt tunable parameters (from hyperopt result)
    buy_rsi = IntParameter(10, 50, default=13, space='buy')
    sell_rsi = IntParameter(50, 90, default=72, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, 'buy'] = 0
        dataframe.loc[
            (dataframe['rsi'] < self.buy_rsi.value) & (dataframe['close'] > dataframe['ema20']),
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, 'sell'] = 0
        dataframe.loc[
            (dataframe['rsi'] > self.sell_rsi.value) | (dataframe['close'] < dataframe['ema20']),
            'sell'
        ] = 1
        return dataframe

