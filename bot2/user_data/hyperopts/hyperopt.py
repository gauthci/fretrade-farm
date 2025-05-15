from freqtrade.optimize.hyperopt import IHyperOpt
from freqtrade.optimize.space import Categorical, Dimension, Integer, Real

class AggressiveRSIHopt(IHyperOpt):
    @staticmethod
    def indicator_space():
        return [
            Integer(20, 40, name='rsi_buy'),
            Integer(60, 80, name='rsi_sell'),
            Real(-0.1, -0.01, name='stoploss'),
            Real(0.01, 0.1, name='trailing_stop_positive'),
            Real(0.01, 0.1, name='trailing_stop_positive_offset'),
        ]

    @staticmethod
    def sell_indicator_space():
        return []

    @staticmethod
    def generate_buy_signal(dataframe, metadata, params):
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        boll = ta.BBANDS(dataframe['close'], timeperiod=20)
        dataframe['bb_lowerband'] = boll['lowerband']
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)

        dataframe.loc[
            (dataframe['rsi'] < params['rsi_buy']) &
            (dataframe['close'] < dataframe['bb_lowerband']) &
            (dataframe['ema_50'] > dataframe['ema_200']),
            'buy'] = 1
        return dataframe

    @staticmethod
    def generate_sell_signal(dataframe, metadata, params):
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        boll = ta.BBANDS(dataframe['close'], timeperiod=20)
        dataframe['bb_upperband'] = boll['upperband']

        dataframe.loc[
            (dataframe['rsi'] > params['rsi_sell']) |
            (dataframe['close'] > dataframe['bb_upperband']),
            'sell'] = 1
        return dataframe

