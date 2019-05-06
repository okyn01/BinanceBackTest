import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np

def formatNum(num):
	return "{:.8f}".format(num)

def percentage(new, old):
	return round(((new / old) - 1 ) * 100)

def createdf(symbol, timeframe):
	df = pd.read_json('data\\Binance_{}_{}_1 Jan, 2018-30 Apr, 2019.json'.format(symbol, timeframe))
	df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'timeClose', 'QAS', 'NoT', 'TBA', 'TBQ', 'ignore']
	del df['QAS'], df['NoT'], df['TBA'], df['TBQ'], df['ignore'], df['timeClose']
	df['Date'] = pd.to_datetime(df['Date'],unit='ms')
	df.set_index('Date', inplace=True)
	return df



symbols = ['LTCBTC', 'GASBTC', 'NEOBTC', 'BNBBTC', 'MCOBTC', 'ETHBTC', 'LRCBTC', 'WTCBTC']

envolopePercentage = 6

for symbol in symbols:
	df = createdf(symbol, "1h")
	df['EMA_26'] = ta.EMA(df.Close.values, timeperiod=26)
	df['EMA_26_UP'] = df['EMA_26'] * (1 + (envolopePercentage / 100))
	df['EMA_26_DOWN'] = df['EMA_26'] * (1 - (envolopePercentage / 100))
	
	df['EMA_13'] = ta.EMA(df.Close.values, timeperiod=13)
	df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df.Close.values, fastperiod=12, slowperiod=26, signalperiod=9)

	df['WMA_MACD'] = ta.EMA(df.macdhist.values, timeperiod=4)
	df['WMA_LOW'] = ta.EMA(df.Low.values, timeperiod=4)

	df['MACD_SAVGOL'] = scipy.signal.savgol_filter(df.macdhist.values, 21, 5)
	df['LOW_SAVGOL'] = scipy.signal.savgol_filter(df.Low.values, 21, 5)

	df = df.dropna()

	df['macdmin'] = df.MACD_SAVGOL[(df.MACD_SAVGOL.shift(1) > df.MACD_SAVGOL) & (df.MACD_SAVGOL.shift(-1) > df.MACD_SAVGOL) & (df.MACD_SAVGOL < 0)]
	df['macdmax'] = df.MACD_SAVGOL[(df.MACD_SAVGOL.shift(1) < df.MACD_SAVGOL) & (df.MACD_SAVGOL.shift(-1) < df.MACD_SAVGOL) & (df.MACD_SAVGOL > 0)]

	df['lowmin'] = df.LOW_SAVGOL[(df.LOW_SAVGOL.shift(1) > df.LOW_SAVGOL) & (df.LOW_SAVGOL.shift(-1) > df.LOW_SAVGOL)]
	df['lowmax'] = df.LOW_SAVGOL[(df.LOW_SAVGOL.shift(1) < df.LOW_SAVGOL) & (df.LOW_SAVGOL.shift(-1) < df.LOW_SAVGOL)]

	
	macdmax = 0
	oldmacdmax = 0
	macdmin = 0
	oldmacdmin = 0

	print (symbol)

	for index, row in df.iterrows():

		if(row['macdmax'] > 0):
			macdmax = row['macdmax']

		if(row['macdmin'] < 0):
			macdmin = row['macdmin']

		if(oldmacdmin < macdmin):
			print(index, format(float(oldmacdmin), '0.8f'), format(float(macdmax), '0.8f'), format(float(macdmin), '0.8f'))


		oldmacdmin = macdmin
		oldmacdmax = macdmax


		#~np.isnan(df.loc[index, 'macdmin'])
		#previoushaopen = df.loc[index, 'HA_Open']
		#previoushaclose = df.loc[index, 'HA_Close']



fig, axes = plt.subplots(nrows=2, ncols=1)

df[['LOW_SAVGOL']].plot(ax=axes[0])
df[['Low']].plot(ax=axes[0])
axes[0].scatter(df.index, df['lowmin'], c='g')
axes[0].scatter(df.index, df['lowmax'], c='r')


df[['MACD_SAVGOL']].plot(ax=axes[1])
df[['macdhist']].plot(ax=axes[1])
axes[1].scatter(df.index, df['macdmin'], c='g')
axes[1].scatter(df.index, df['macdmax'], c='r')

plt.show()
