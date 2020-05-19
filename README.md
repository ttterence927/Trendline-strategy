# Trendline-strategy(valid from 2017 to 2019) 

# Description
Strategy logic:

if exit bullish trend or take profit or stop loss

  then close long
  
if stop loss or take profit

  then close short
  
if bullish trend(VBMO>threshold) and trendline signal

  then long
  
else if short signal

  then short


Results:

Product:HSI future

Max position:3

Final Portfolio Value: 100023653.00

SR: OrderedDict([('sharperatio', 1.1787277686933937)])

DW: AutoOrderedDict([('len', 14787), ('drawdown', 0.0010557391374165358), ('moneydown', 1056.0), ('max', AutoOrderedDict([('len', 

27089), ('drawdown', 0.002463847438566604), ('moneydown', 2464.0)]))])

SQN: AutoOrderedDict([('sqn', 3.5344221568969414), ('trades', 875)])


# Reference:
https://www.tradingview.com/script/mpeEgn5J-Trendlines-JD/

https://www.tradingview.com/script/F5BJcmtO-Volatility-Based-Momentum-Oscillator-VBMO/
![image alt text](image_0.png)
