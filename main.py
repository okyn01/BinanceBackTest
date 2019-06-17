import pandas as pd
import talib as ta
import numpy as np
import helpers as hlp
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from binance.client import Client

client = Client("", "")

symbols = hlp.getAllSymbols()
filteredSymbols = []

envolopePercentage = 6

for symbol in symbols:
	if(hlp.getVolume(symbol) >= 1000.0):

		df = hlp.getOHLChistory(symbol, '30m', 500)

		#df['EMA_26'] = ta.EMA(df.Close.values, timeperiod=26)
		#df['EMA_26_UP'] = df['EMA_26'] * (1 + (envolopePercentage / 100))
		#df['EMA_26_DOWN'] = df['EMA_26'] * (1 - (envolopePercentage / 100))
		
		df['EMA_13'] = ta.EMA(df.Close.values, timeperiod=13)
		df['EMA_26'] = ta.EMA(df.Close.values, timeperiod=26)


		#DETERMINE THE TREND 
		if(df['EMA_13'].tail(1).sum() >= (df['EMA_13'].tail(5).sum() / 5)):
			print(symbol, 'UPTREND')
			filteredSymbols.append(symbol)

		else:
			print(symbol, 'DOWNTREND')



for filteredSymbol in filteredSymbols:

	df = hlp.getOHLChistory(filteredSymbol, '5m', 500)

	df['EMA_13'] = ta.EMA(df.Close.values, timeperiod=13)
	df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df.Close.values, fastperiod=12, slowperiod=26, signalperiod=9)

	df['maxima-macd'] = df.iloc[argrelextrema(df.macdhist.values, np.greater, order=2)[0]]['macdhist']
	df['minima-macd'] = df.iloc[argrelextrema(df.macdhist.values, np.less, order=2)[0]]['macdhist']

	df['maxima-low'] = df.iloc[argrelextrema(df.Low.values, np.greater, order=2)[0]]['Low']
	df['minima-low'] = df.iloc[argrelextrema(df.Low.values, np.less, order=2)[0]]['Low']


	fig, axes = plt.subplots(nrows=2, ncols=1)

	df['zeroline'] = 0

	df[['EMA_13']].plot(ax=axes[0])
	df[['Low']].plot(ax=axes[0])
	df[['macdhist', 'zeroline']].plot(ax=axes[1])

	axes[0].scatter(df.index, df['maxima-low'], c='g')
	axes[0].scatter(df.index, df['minima-low'], c='r')

	axes[1].scatter(df.index, df['maxima-macd'], c='g')
	axes[1].scatter(df.index, df['minima-macd'], c='r')

	plt.show()



'''
fig, axes = plt.subplots(nrows=2, ncols=1)

df['zeroline'] = 0

df[['EMA_13']].plot(ax=axes[0])
df[['Low']].plot(ax=axes[0])
df[['macdhist', 'zeroline']].plot(ax=axes[1])

axes[0].scatter(df.index, df['maxima-low'], c='g')
axes[0].scatter(df.index, df['minima-low'], c='r')

axes[1].scatter(df.index, df['maxima-macd'], c='g')
axes[1].scatter(df.index, df['minima-macd'], c='r')

plt.show()
'''





