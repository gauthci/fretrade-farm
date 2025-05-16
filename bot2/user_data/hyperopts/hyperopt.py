from freqtrade.optimize.space import Integer, Real
import talib.abstract as ta

def custom_hyperopt():
    def indicator_space():
        return [
            Integer(20, 40, name='buy_rsi'),
            Integer(60, 80, name='sell_rsi'),
            Real(-0.1, -0.01, name='stoploss'),
            Real(0.01, 0.1, name='trailing_stop_positive'),
            Real(0.01, 0.1, name='trailing_stop_positive_offset'),
        ]

    def generate_buy_signal(dataframe, metadata, params):
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        boll = ta.BBANDS(dataframe['close'], timeperiod=20)
        dataframe['bb_lowerband'] = boll['lowerband']
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)

        dataframe.loc[
            (dataframe['rsi'] < params['buy_rsi']) &
            (dataframe['close'] < dataframe['bb_lowerband']) &
            (dataframe['ema_50'] > dataframe['ema_200']),
            'buy'] = 1
        return dataframe

    def generate_sell_signal(dataframe, metadata, params):
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        boll = ta.BBANDS(dataframe['close'], timeperiod=20)
        dataframe['bb_upperband'] = boll['upperband']

        dataframe.loc[
            (dataframe['rsi'] > params['sell_rsi']) |
            (dataframe['close'] > dataframe['bb_upperband']),
            'sell'] = 1
        return dataframe

    return {
        "buy": generate_buy_signal,
        "sell": generate_sell_signal,
        "indicator_space": indicator_space,
        "sell_indicator_space": lambda: [],
    }

