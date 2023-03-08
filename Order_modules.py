import math
import MetaTrader5 as mt5

def Long(Y_symbol, X_symbol, hedge_ratio, money):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    Y_SIZE = int(math.ceil(money / Y_price) / 100) * 100
    X_SIZE = int(math.ceil(Y_SIZE * hedge_ratio) / 100) * 100


    ylot = Y_SIZE
    point = mt5.symbol_info(Y_symbol).point
    price = mt5.symbol_info_tick(Y_symbol).bid
    deviation = 20
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(ylot),
        "type": mt5.ORDER_TYPE_BUY,
        "price": Y_price,
        # "sl": price - 100 * point,
        # "tp": price + 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }



    xlot = X_SIZE
    point = mt5.symbol_info(X_symbol).point
    price = mt5.symbol_info_tick(X_symbol).ask
    deviation = 10
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(xlot),
        "type": mt5.ORDER_TYPE_SELL,
        "price": X_price,
        # "sl": price + 100 * point,
        # "tp": price - 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestSell, requestBuy)



def Short(Y_symbol, X_symbol, hedge_ratio, money):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    Y_SIZE = int(math.ceil(money / Y_price) / 100) * 100
    X_SIZE = int(math.ceil(Y_SIZE * hedge_ratio) / 100) * 100

    ylot = Y_SIZE
    deviation = 20
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(ylot),
        "type": mt5.ORDER_TYPE_SELL,
        "price": Y_price,
        # "sl": price - 100 * point,
        # "tp": price + 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }



    xlot = X_SIZE
    deviation = 10
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(xlot),
        "type": mt5.ORDER_TYPE_BUY,
        "price": X_price,
        # "sl": price + 100 * point,
        # "tp": price - 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestSell, requestBuy)




def Close_Long(Y_symbol, X_symbol, y_volume, x_volume):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    #point = mt5.symbol_info(Y_symbol).point
    #price = mt5.symbol_info_tick(Y_symbol).bid
    deviation = 20
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(y_volume),
        "type": mt5.ORDER_TYPE_SELL,
        "price": Y_price,
        # "sl": price - 100 * point,
        # "tp": price + 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    #point = mt5.symbol_info(X_symbol).point
    #price = mt5.symbol_info_tick(X_symbol).ask
    deviation = 10
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(x_volume),
        "type": mt5.ORDER_TYPE_BUY,
        "price": X_price,
        # "sl": price + 100 * point,
        # "tp": price - 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestSell, requestBuy)



def Close_Short(Y_symbol, X_symbol, y_volume, x_volume):

    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    #point = mt5.symbol_info(Y_symbol).point
    #price = mt5.symbol_info_tick(Y_symbol).bid
    deviation = 20
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(y_volume),
        "type": mt5.ORDER_TYPE_BUY,
        "price": Y_price,
        # "sl": price - 100 * point,
        # "tp": price + 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    #point = mt5.symbol_info(X_symbol).point
    #price = mt5.symbol_info_tick(X_symbol).ask
    deviation = 20
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(x_volume),
        "type": mt5.ORDER_TYPE_SELL,
        "price": X_price,
        # "sl": price + 100 * point,
        # "tp": price - 100 * point,
        # "deviation": deviation,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    return (requestSell, requestBuy)