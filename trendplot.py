from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
# Import the backtrader platform
import backtrader as bt
import numpy as np
import random
import pandas as pd
import time
import talib

class trendline(bt.Indicator):
    lines = ('pos','time','pivot_h','pivot_l','ax','bx','by','long','short')
    plotinfo = dict(
        subplot=False,
        plotlinelabels=True, plotlinevalues=True, plotvaluetags=True,
    )

    plotlines = dict(
        #short=dict(marker='v', markersize=10.0, color='purple',
                         #fillstyle='full', ls=''),
        #long=dict(marker='^', markersize=10.0, color='green',
                           #fillstyle='full', ls=''),
        #pos=dict(_name='pos', color='black', ls='-', _skipnan=False)
        #dict(marker='v', markersize=4.0, color='red',fillstyle='full', ls=''),
    )
    params = (('left', 30),('right', 15),)

    def f_trendline(self,pivot_type):
        ay = 0.0
        slope = 0.0

        if pivot_type == 1:
            curr_pivot = self.lines.pivot_h[0]
            prev_pivot = self.lines.pivot_h[-1]
        elif pivot_type == 0:
            curr_pivot = self.lines.pivot_l[0]
            prev_pivot = self.lines.pivot_l[-1]           

        ay = curr_pivot
        deltax = 0
        if (curr_pivot - prev_pivot != 0):
            self.lines.ax[0] = self.lines.time[-15]
            self.lines.by[0] = prev_pivot
            self.lines.bx[0] = self.lines.ax[-1]
            deltax = self.lines.ax[0] - self.lines.bx[0]
            if (deltax != 0.0):
                deltay = ay - self.lines.by[0]
                slope = deltay / deltax
        else:
            self.lines.ax[0] = self.lines.ax[-1]
            self.lines.bx[0] = self.lines.bx[-1]
            self.lines.by[0] = self.lines.by[-1]

        #print(self.lines.ax[0] ,ay,self.lines.bx[0] ,self.lines.by[0] ,slope)
        return (self.lines.ax[0] ,ay,self.lines.bx[0] ,self.lines.by[0] ,slope)
 
    def line_get_price(self,_start_time,_start_price,_slope,_lookback_period):
        time = self.lines.time[0]
        bar_time = self.lines.time[0] - self.lines.time[-1]
        elapsed_time = (time-_start_time)
        #print(_start_price,elapsed_time,bar_time,_slope)
        return (_start_price + (elapsed_time-(_lookback_period*bar_time))*_slope)

    def line_cross(self,_start_time,_start_price,_slope):
        #Get current and previous price for the trendline
        if _slope==0.0:
            return 0
        current_value = self.line_get_price(_start_time,_start_price,_slope,0)
        previous_value = self.line_get_price(_start_time,_start_price,_slope,1)
        #Return 1 for crossover, -1 for crossunder and 0 for no cross detected
        #print(datetime.datetime.fromtimestamp(_start_time),current_value,previous_value)
        if self.data.close[-1]<previous_value and self.data.close[0]>current_value:
            return 1
        elif self.data.close[-1]>previous_value and self.data.close[0]<current_value:
            return -1
        else:
            return 0

    def __init__(self):
        #trendline
        mb = self.p.left+self.p.right+1
        self.high = bt.ind.Highest(self.data.high, period=mb)
        self.low = bt.ind.Lowest(self.data.low, period=mb)

        self.high_x0=0
        self.high_y0=0.0
        self.high_sl0=0.0
        self.high_x1=0
        self.high_y1=0.0
        self.high_sl1=0.0
        self.high_x2=0
        self.high_y2=0.0
        self.high_sl2=0.0
        self.high_x2=0
        self.high_y2=0.0
        self.high_sl2=0.0
        self.high_x3=0
        self.high_y3=0.0
        self.high_sl3=0.0
        self.high_x4=0
        self.high_y4=0.0
        self.high_sl4=0.0
        self.high_x5=0
        self.high_y5=0.0
        self.high_sl5=0.0
        self.high_x6=0
        self.high_y6=0.0
        self.high_sl6=0.0


        self.low_x0=0
        self.low_y0=0.0
        self.low_sl0=0.0
        self.low_x1=0
        self.low_y1=0.0
        self.low_sl1=0.0
        self.low_x2=0
        self.low_y2=0.0
        self.low_sl2=0.0
        self.low_x2=0
        self.low_y2=0.0
        self.low_sl2=0.0
        self.low_x3=0
        self.low_y3=0.0
        self.low_sl3=0.0
        self.low_x4=0
        self.low_y4=0.0
        self.low_sl4=0.0
        self.low_x5=0
        self.low_y5=0.0
        self.low_sl5=0.0
        self.low_x6=0
        self.low_y6=0.0
        self.low_sl6=0.0


    def next(self):
        self.lines.time[0] = self.data.num2date().timestamp()

        #pivot start
        self.lines.pivot_h[0] = self.lines.pivot_h[-1]
        self.lines.pivot_l[0] = self.lines.pivot_l[-1]

        if self.data.high[-self.p.left] == self.high:
            self.lines.pivot_h[0] = self.high[0]
        elif self.data.high[-self.p.right] == self.high:
            self.lines.pivot_h[0] = self.high[0]
            
        if self.data.low[-self.p.left] == self.low:
            self.lines.pivot_l[0] = self.low[0]
        elif self.data.high[-self.p.right] == self.high:
            self.lines.pivot_h[0] = self.high[0]
        #pivot end
        (phx1,phy1,phx2,phy2,slope_high) = self.f_trendline(1)
        (phx1,phy1,phx2,phy2,slope_low) = self.f_trendline(0)

        if (self.lines.pivot_h[-1] - self.lines.pivot_h[0] !=0 ):
            self.high_x6 = self.high_x5
            self.high_y6 = self.high_y5
            self.high_sl6 = self.high_sl5
            self.high_x5 = self.high_x4
            self.high_y5 = self.high_y4
            self.high_sl5 = self.high_sl4
            self.high_x4 = self.high_x3
            self.high_y4 = self.high_y3
            self.high_sl4 = self.high_sl3
            self.high_x3 = self.high_x2
            self.high_y3 = self.high_y2
            self.high_sl3 = self.high_sl2          
            self.high_x2 = self.high_x1
            self.high_y2 = self.high_y1
            self.high_sl2 = self.high_sl1
            self.high_x1 = self.high_x0
            self.high_y1 = self.high_y0
            self.high_sl1 = self.high_sl0
            self.high_x0 = phx1
            self.high_y0 = phy1
            self.high_sl0 = slope_high

        if (self.lines.pivot_l[-1] - self.lines.pivot_l[0]!=0 ):
            self.low_x6 = self.low_x5
            self.low_y6 = self.low_y5
            self.low_sl6 = self.low_sl5
            self.low_x5 = self.low_x4
            self.low_y5 = self.low_y4
            self.low_sl5 = self.low_sl4            
            self.low_x4 = self.low_x3
            self.low_y4 = self.low_y3
            self.low_sl4 = self.low_sl3
            self.low_x3 = self.low_x2
            self.low_y3 = self.low_y2
            self.low_sl3 = self.low_sl2
            self.low_x2 = self.low_x1
            self.low_y2 = self.low_y1
            self.low_sl2 = self.low_sl1
            self.low_x1 = self.low_x0
            self.low_y1 = self.low_y0
            self.low_sl1 = self.low_sl0
            self.low_x0 = phx1
            self.low_y0 = phy1
            self.low_sl0 = slope_low

        position = 0 
        if self.line_cross(self.high_x0,self.high_y0,self.high_sl0):
            position = 1
        if self.line_cross(self.high_x1,self.high_y1,self.high_sl1):
            position = 1
        if self.line_cross(self.high_x2,self.high_y2,self.high_sl2):
            position = 1
        if self.line_cross(self.high_x3,self.high_y3,self.high_sl3):
            position = 1
        if self.line_cross(self.high_x4,self.high_y4,self.high_sl4):
            position = 1
        if self.line_cross(self.high_x5,self.high_y5,self.high_sl5):
            position = 1
        if self.line_cross(self.high_x6,self.high_y6,self.high_sl6):
            position = 1

        if self.line_cross(self.low_x0,self.low_y0,self.low_sl0) == -1:
            position = -1
        if self.line_cross(self.low_x1,self.low_y1,self.low_sl1) == -1:
            position = -1
        if self.line_cross(self.low_x2,self.low_y2,self.low_sl2) == -1:
            position = -1
        if self.line_cross(self.low_x3,self.low_y3,self.low_sl3) == -1:
            position = -1
        if self.line_cross(self.low_x4,self.low_y4,self.low_sl4) == -1:
            position = -1
        if self.line_cross(self.low_x5,self.low_y5,self.low_sl5) == -1:
            position = -1
        if self.line_cross(self.low_x6,self.low_y6,self.low_sl6) == -1:
            position = -1
        
        if position ==1:
            self.lines.long[0] = self.data.low[0] - 100
        elif position ==-1:
            self.lines.short[0] = self.data.high[0] +100

        self.lines.pos[0] = position

class pivot(bt.Indicator):
    lines = ('pivot_h','pivot_l',)
    plotinfo = dict(
        subplot=False,
        plotlinelabels=True, plotlinevalues=True, plotvaluetags=True,
    )

    plotlines = dict(
        pivot_h=dict(marker='v', markersize=4.0, color='red',
                         fillstyle='full', ls=''),
        pivot_l=dict(marker='^', markersize=4.0, color='blue',
                           fillstyle='full', ls=''),
    )
    params = (('left', 15),('right', 30),)


    def __init__(self):
        mb = self.p.left+self.p.right+1
        self.high = bt.ind.Highest(self.data.high, period=mb)
        self.low = bt.ind.Lowest(self.data.low, period=mb)
        
    def next(self):    
        if self.data.high[-self.p.left] == self.high:
            self.lines.pivot_h[0] = self.high[0]
        else:
            self.lines.pivot_h[0] = float('nan')

        if self.data.low[-self.p.left] == self.low:
            self.lines.pivot_l[0] = self.low[0]
        else:
            self.lines.pivot_l[0] = float('nan')

class AcctStats(bt.Analyzer):
    """A simple analyzer that gets the gain in the value of the account; should be self-explanatory"""
 
    def __init__(self):
        self.start_val = self.strategy.broker.get_value()
        self.end_val = None
 
    def stop(self):
        self.end_val = self.strategy.broker.get_value()
 
    def get_analysis(self):
        return {"start": self.start_val, "end": self.end_val,
                "growth": self.end_val - self.start_val, "return": self.end_val / self.start_val}         
class PropSizer(bt.Sizer):
    """A position sizer that will buy as many stocks as necessary for a certain proportion of the portfolio
       to be committed to the position, while allowing stocks to be bought in batches (say, 100)"""
    params = {"prop": 0.1, "batch": 100}
 
    def _getsizing(self, comminfo, cash, data, isbuy):
        """Returns the proper sizing"""
 
        if isbuy:    # Buying
            target = self.broker.getvalue() * self.params.prop    # Ideal total value of the position
            price = data.close[0]
            shares_ideal = target / price    # How many shares are needed to get target
            batches = int(shares_ideal / self.params.batch)    # How many batches is this trade?
            shares = batches * self.params.batch    # The actual number of shares bought
 
            if shares * price > cash:
                return 0    # Not enough money for this trade
            else:
                return shares
 
        else:    # Selling
            return self.broker.getposition(data).size    # Clear the position

class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)
 
    plotinfo = {"plot": True, "subplot": True}
 
    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue()

class VMO(bt.Indicator):
    lines = ('slowvmo','trend','vmochange')
    params = (('s_period', 6), ('s_atrperiod', 5),
        ('trend_up',22),('trend_down',-100),
        ('up_extreme',1.5),('down_extreme',1.5),
        ('up_stoptrend',0.3),('down_stoptrend',0.3),
        )
    def __init__(self):
#        self.addminperiod(self.p.period)
        self.s_moveAvg = bt.talib.EMA(self.data.close,timeperiod=self.p.s_period)
        self.s_normalizationATR = bt.indicators.ATR(self.data, period=self.p.s_atrperiod)
        s_closeVsMA = self.data.close-self.s_moveAvg
        s_volatilityBasedCloseVsMA = s_closeVsMA/self.s_normalizationATR

        self.lines.slowvmo = s_volatilityBasedCloseVsMA
    def next(self):

        #self.lines.trend[0] = self.lines.trend[-1]

        upext = self.p.trend_up * self.p.up_extreme
        downext = self.p.trend_down * self.p.down_extreme
        self.lines.vmochange[0] = self.lines.slowvmo[0] - self.lines.slowvmo[-1]
        if self.lines.trend[-1] == 50 and (self.lines.slowvmo[-1]<upext and self.lines.slowvmo>upext):
            self.lines.trend[0] = 0
        elif self.lines.trend[-1] == 50 and (self.lines.slowvmo<self.p.trend_up *self.p.up_stoptrend):
            self.lines.trend[0] = 0
        elif self.lines.trend[-1] == -50 and (self.lines.slowvmo>self.p.trend_down *self.p.down_stoptrend or (self.lines.slowvmo[-1]>downext and self.lines.slowvmo<downext)):
            self.lines.trend[0] = 0
        elif self.lines.slowvmo[-1]<self.p.trend_up and self.lines.slowvmo>self.p.trend_up:
            self.lines.trend[0] = 50
        elif self.lines.slowvmo[-1]>self.p.trend_down and self.lines.slowvmo<self.p.trend_down:
            self.lines.trend[0] = -50
        else:
            self.lines.trend[0] = self.lines.trend[-1]

class SIU(bt.Strategy):
    params = (
        ('s_period',1400),
        ('s_atrperiod',1400),
        ('trend_up',19),
        ('up_extreme',2),
        ('up_stoptrend',0.6),
        ('down_atrperiod',1400),
        ('down_period',10),
        ('down_vmo',5),
        ('down_sl',0.3),
        ('down_tp',0.6),
        ('optim_fs',(1400, 1400, 15, 1.9, 0.2, 13, 9 ,0.2, 0.6)),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        #print('%s, %s' % (dt.strftime("%b %d %Y %H:%M:%S"), txt))
        #print('Portfolio Value: %.2f' % cerebro.broker.getvalue(), self.position.size)

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.trend = 0
        self.entryvmo = 0
        self.long_entry = 0
        

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.long2 = 0
        self.short2 = 0
        self.trendline = trendline(self.data)
        self.p.s_period,self.p.s_atrperiod,self.p.trend_up,self.p.up_extreme,self.p.up_stoptrend,self.p.down_period,self.p.down_vmo,self.p.down_sl,self.p.down_tp = self.p.optim_fs
        print(self.p.s_period,self.p.s_atrperiod,self.p.trend_up,self.p.up_extreme,self.p.up_stoptrend,self.p.down_period,self.p.down_vmo,self.p.down_sl,self.p.down_tp)
        self.vmo = VMO(self.data,s_period = self.p.s_period,s_atrperiod = self.p.s_atrperiod,trend_up = self.p.trend_up,up_extreme = self.p.up_extreme,up_stoptrend = self.p.up_stoptrend)
        self.shortfilter = bt.indicators.Average(self.vmo.vmochange,period=9)
        self.maxchg = bt.indicators.Average(self.vmo.vmochange,period=30)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        #Long module
        
        #prevlong = (self.trendline.pos[-1]== 1 or self.trendline.pos[-2]== -1 or self.trendline.pos[-3]== 1 or self.trendline.pos[-4]== 1 or self.trendline.pos[-5]== 1  or self.trendline.pos[-6]== 1  or self.trendline.pos[-7]== 1  or self.trendline.pos[-8]== 1)
        
        if self.vmo.trend[-1] != 0 and self.vmo.trend[0] == 0 and self.position.size>0:
            self.order = self.sell(size=self.position.size)
        
        if self.maxchg>-0.5 and self.vmo.trend == 50 and self.trendline.pos == 1 and self.position.size<3 and self.position.size>=0:
            self.order = self.buy(size=1)

        if self.vmo.trend == 50 and self.position.size>0:  #close long
            if (self.trendline.pos == -1):
                self.order = self.sell(size=1)
               
        
        #Short module
        if self.trendline.pos == -1 and self.vmo.slowvmo[-self.p.down_period] - self.vmo.slowvmo[0] > self.p.down_vmo and self.position.size>-3 and self.position.size<=0:
            #if self.position.size>0:
                #self.order = self.close()
            self.order = self.sell(size=3)
            self.entryvmo = self.vmo.slowvmo[0]

        sl = self.entryvmo + abs(self.entryvmo)*self.p.down_sl
        tp = self.entryvmo - abs(self.entryvmo)*self.p.down_tp
        if self.vmo.slowvmo[0]>sl and self.vmo.slowvmo[-1]<sl and self.position.size<0:
            self.order = self.close()
        if self.vmo.slowvmo[0]<tp and self.vmo.slowvmo[-1]>tp and self.position.size<0:
            self.order = self.close()


if __name__ == '__main__':
    # Create a cerebro entity
    start_time = time.time()
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'HSIF_1m.csv')

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
    dataname=datapath,

    fromdate=datetime.datetime(2016, 4, 5),
    todate=datetime.datetime(2020, 1, 30),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d %H:%M:%S'),
    timeframe=bt.TimeFrame.Minutes,
    datetime=1,
    high=4,
    low=5,
    open=2,
    close=3,
    volume=8
	)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000000)
    cerebro.broker.setcommission(commission=0.0)

    cerebro.addstrategy(SIU)
    cerebro.addobserver(AcctValue)
    cerebro.addanalyzer(AcctStats)
    cerebro.addsizer(PropSizer)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0, timeframe=bt.TimeFrame.Months)
    cerebro.addanalyzer(bt.analyzers.SQN)
    # Run over everything
    results = cerebro.run()
    strat = results[0]
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', strat.analyzers.sharperatio.get_analysis())
    print('DW:', strat.analyzers.DW.get_analysis()) 
    print("SQN:", strat.analyzers.sqn.get_analysis())
    # Plot the result
    cerebro.plot()
    print("--- %s seconds ---" % (time.time() - start_time))
    #cerebro.plot(iplot=True, volume=False)