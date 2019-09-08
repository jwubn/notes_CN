# Taiwan Stock Market Equities

The backtesting system framework is programmed by GAO Chang, my co-worker in the project. I am responsible for any errors.
<br />
The core ideas of the backtesting system is that using the signals generated from strategies function to implement intra-day trading, i.e., clear all the positions every day before market closes.
I consider 4 kinds of CTA trading strategies here, the Bollinger Band, Price Rate-of-Change, Williams %R, and Parabolic Stop-and-Reverse.
<br />
### Bollinger Band
A Bollinger Band is a technical analysis tool defined by a set of lines plotted two standard deviations (positively and negatively) away from a simple moving average (SMA) of the security's price, but can be adjusted to user preferences. The core idea of Bollinger band is to use the combination of the standard deviation and SMA to evaluate the overbought or oversold status of the market. In the Taiwan stock market, the momentum version of Bollinger band has better performance.
<br />
### Price Rate-of-Change
The Price Rate of Change (ROC) is a momentum-based technical indicator that measures the percentage change in price between the current price and the price a certain number of periods ago. The ROC indicator is plotted against zero, with the indicator moving upwards into positive territory if price changes are to the upside, and moving into negative territory if price changes are to the downside.
<br />
### Williams %R
Williams %R, also known as the Williams Percent Range, is a type of momentum indicator that moves between 0 and -100 and measures overbought and oversold levels. The Williams %R may be used to find entry and exit points in the market. The indicator is very similar to the Stochastic oscillator and is used in the same way. It was developed by Larry Williams and it compares a stock’s closing price to the high-low range over a specific period, typically 14 days or periods.
<br />
### Parabolic SAR
The parabolic SAR attempts to give traders an edge by highlighting the direction an asset is moving, as well as providing entry and exit points. In this article, we'll look at the basics of this indicator and show you how you can incorporate it into your trading strategy.
