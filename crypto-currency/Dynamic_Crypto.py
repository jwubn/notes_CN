import  pandas as pd
import  numpy as np

class Coin():

    Valid_list = ['BCH','Bitcoin','ETH','Lite']
    Total_coins = []

    Short_win = 20
    Long_win = 200
    Reset_const = 5
    Per_hand = 3000
    No_transac_period = 400
    Check_revenue = 103000
    Check_revenue_flag = False
    Cash_balance_limit = 30000
    Crypto_balance_limit = 70000


    Check_lose = 99500
    Check_lose_flag = False

    def __init__(self,coin_type,filtering_coef,return_thereshold,confidence_threshold):

        if coin_type in Coin.Valid_list:
            self.type = coin_type
            self.data = pd.DataFrame(columns=['open','high','low','close','volume'])
            self.property = pd.DataFrame(columns=['mean','return'])
            self.filtering_coef = filtering_coef
            self.reurn_thereshold = return_thereshold
            self.confidence_threshold = confidence_threshold
            self.buy_confidence = 0 # Initialize the buy confidence
            self.sell_confidence = 0 # Initialize the sell confidence
            self.confidence_list = np.repeat(0,Coin.Reset_const)
            self.position = 0 # Initialize the holding coin position
            self.prev_position = 0 # Initialize the previous holding position
            self.trading_coef_ = 0 # Initialize the trading signal of current min
            self.reset_conf_count = Coin.Reset_const # Initialize the reset period of confidence
            self.transaction_count = Coin.No_transac_period # Initialize the counter for clearance_check_no_transaction
            self.transaction_flag = False # Initialize the flag for indicating whether there is a transaction happen or not
            self.check_balance_flag = False # Initialize the flag of whether the check balance is turned on
            self.revenue = 0
            self.prev_200_balance = 0
            self.prev_200_balance_flag = False
            self.holdingperiod = pd.DataFrame(columns=['counter','holdings'])
            self.holdingperiod_all = pd.DataFrame(columns=['counter', 'holdings'])
            self.lock_revenue_flag = False
            self.lock_total_balance = 104000
            Coin.Total_coins.append(self) # Update the total coins are trading
            # print('Create coin {} successfully!'.format(coin_type))
        else:
            print('No such coin!')


    def update_data(self, data):
        self.data.loc[len(self.data)] = data
        if len(self.property) is not 0 :

            self.property.loc[len(self.property)] = [np.mean(data[0:4]),
                                                     (np.mean(data[0:4]) - self.property['mean'].values[-1])/ self.property['mean'].values[-1]]
        else:
            self.property.loc[len(self.property)] = [np.mean(data[0:4]), 0]

    def generate_trading_signal(self):
        self.reset_confidence()
        curr_return = self.property['return'].values[-1]
        return_list = self.property['return'].values
        sorted_return = np.sort(return_list)
        short_ave = np.mean(self.property['mean'].iloc[-Coin.Short_win:])
        long_ave = np.mean(self.property['mean'].iloc[-Coin.Long_win:])


        if curr_return > sorted_return[int((1 - self.filtering_coef) * len(sorted_return))]:

            if short_ave > long_ave:

                if curr_return > self.reurn_thereshold:

                    self.confidence_list[self.reset_conf_count] = 1

                    if np.sum(self.confidence_list) >= self.confidence_threshold:
                        # print('buy')
                        self.trading_coef_= 1
                        self.transaction_flag = True

        elif curr_return < sorted_return[int(self.filtering_coef * len(sorted_return))]:

            if short_ave < long_ave:

                if curr_return < self.reurn_thereshold:

                    self.confidence_list[self.reset_conf_count] = -1

                    if np.sum(self.confidence_list) <= - self.confidence_threshold:
                        # print('sell')
                        self.trading_coef_= -1
                        self.transaction_flag = True

        else:
            self.trading_coef_= 0
            self.confidence_list[self.reset_conf_count] = 0


    def clearance_check_balance(self, cash_balance, crypto_balance):
        if  ( crypto_balance > Coin.Crypto_balance_limit  or cash_balance < Coin.Cash_balance_limit) and self.check_balance_flag is not True:
            self.position = self.prev_position
            Coin.No_transac_period = 200
            self.check_balance_flag = True
            # print("Clear by check balance and set No_Transaction_period to {}".format(Coin.No_transac_period))

        elif self.check_balance_flag is True:
            self.position = self.prev_position
            if crypto_balance < Coin.Crypto_balance_limit  and cash_balance > Coin.Cash_balance_limit:
                Coin.No_transac_period = 300
                self.check_balance_flag = False
                # print('Reset No_transac_period to 300')

    # From total balance > 103000, reset the current position table.
    @classmethod
    def clearance_check_revenue(cls,total_balance, cash_balance):
        if total_balance >= cls.Check_revenue or cls.Check_revenue_flag is True:
            if cls.Check_revenue_flag is not True:
                cls.Check_revenue_flag = True
                cls.Check_revenue += 1000

            if cash_balance != total_balance:
                for which_coin in cls.Total_coins:
                    # print('victor',which_coin.holdingperiod)
                    which_coin.position = 0
                    which_coin.holdingperiod.drop(which_coin.holdingperiod.index[:], inplace=True)

            else:
                cls.Check_revenue_flag = False
                # print('Clear by making profits {}. Current cash balance is {}'.format(cls.Check_revenue - 1000,cash_balance))

    # From total balance < 99500, reset the current position table.
    @classmethod
    def clearance_check_lose(cls,total_balance, cash_balance):
        if total_balance <= cls.Check_lose or cls.Check_lose_flag:
            if cls.Check_lose_flag == False:
                cls.Check_lose_flag = True
                cls.Check_lose -= 500

            if cash_balance != total_balance:
                for which_coin in cls.Total_coins:
                    # print('victor',which_coin.holdingperiod)
                    which_coin.position = 0
                    which_coin.holdingperiod.drop(which_coin.holdingperiod.index[:], inplace=True)

            else:
                cls.Check_lose_flag = False

    def lock_revenue(self, total_revenue):
        if total_revenue > self.lock_total_balance or self.lock_revenue_flag:
            self.lock_revenue_flag = True
            self.position = 0

    def update_prev_position(self, position, counter, total_balance):
        self.prev_position = position
        if counter % 200 == 0:
            self.prev_200_balance = total_balance


    # update position
    def update_position(self, counter):

        self.position += self.trading_coef_ * Coin.Per_hand / self.property['mean'].values[-1]

        if (self.trading_coef_ * Coin.Per_hand / self.property['mean'].values[-1]) != 0:
            self.holdingperiod.loc[len(self.holdingperiod)] = [counter, self.trading_coef_ * Coin.Per_hand / self.property['mean'].values[-1]]
            self.holdingperiod_all.loc[len(self.holdingperiod)] = [counter, self.trading_coef_ * Coin.Per_hand / self.property['mean'].values[-1]]

    # For every 350 minutes clearing the position
    def clear_holdingperiod(self,counter):
        try:
            if (self.holdingperiod['counter'].values[0]+ 350) == counter:
                self.clear_position = self.holdingperiod.iloc[:,1]
                self.position -= self.clear_position.values[-1]
                self.holdingperiod.drop(self.holdingperiod.index[0],inplace = True)
        except:
            return

    # For every 5 minutes reset the number of confidence
    def reset_confidence(self):
        self.reset_conf_count -= 1
        if self.reset_conf_count == -1:
            self.buy_confidence = 0
            self.sell_confidence = 0
            self.reset_conf_count = Coin.Reset_const - 1

    @classmethod
    def coin_list(cls):
        return cls.Total_coins

