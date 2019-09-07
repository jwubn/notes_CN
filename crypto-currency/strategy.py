import  pandas as pd
import  numpy as np

from Dynamic_Crypto import Coin

def handle_bar(counter,  # a counter for number of minute bars that have already been tested
               time,  # current time in string format such as "2018-07-30 00:30:00"
               data,  # data for current minute bar (in format 2)
               init_cash,  # your initial cash, a constant
               transaction,  # transaction ratio, a constant
               cash_balance,  # your cash balance at current minute
               crypto_balance,  # your crpyto currency balance at current minute
               total_balance,  # your total balance at current minute
               position_current,  # your position for 4 crypto currencies at this minute
               memory,  # a class, containing the information you saved so far
               ):

    if counter is 0:
        #Initialize 4 coins
        Coin('BCH', filtering_coef =   0.03, return_thereshold = 0.002, confidence_threshold =   2)
        Coin('Bitcoin', filtering_coef=0.01, return_thereshold=0.005, confidence_threshold =     2)
        Coin('ETH', filtering_coef=    0.02, return_thereshold=0.001, confidence_threshold =     2)
        Coin('Lite',filtering_coef =   0.01, return_thereshold = 0.005, confidence_threshold =   2)
        memory.coin_list = Coin.coin_list()
        memory.cum_revenue = np.repeat(0.,4)


    position_new = position_current

    for which_coin in range(0,len(memory.coin_list)):

        memory.coin_list[which_coin].update_data(data=data[which_coin])
        flag = 0
        if counter > 200:
            memory.coin_list[which_coin].update_prev_position(position_current[which_coin], counter, total_balance)
            memory.coin_list[which_coin].generate_trading_signal()
            memory.coin_list[which_coin].update_position(counter)
            memory.coin_list[which_coin].clear_holdingperiod(counter)
            memory.coin_list[which_coin].clearance_check_balance(cash_balance,crypto_balance)
            memory.coin_list[which_coin].clearance_check_revenue(total_balance,cash_balance)
            position_new[which_coin] = memory.coin_list[which_coin].position

    return position_new, memory




