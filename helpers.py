from datetime import datetime
import urllib.parse
import pandas as pd
from binance.client import Client

client = Client("", "")

def formatNum(num):
	return "{:.8f}".format(num)

def printTime():
	return datetime.now().strftime("[%H:%M:%S]")

def percentage(new, old):
	return round(((new / old) - 1 ) * 100)

def getAllSymbols(quoteAsset='BTC'):
	"""
		Get all symbols from binance using a quoteasset, default is BTC.
		Possible to exclude certain base assets such as TUSD
	"""
	exinfo = client.get_exchange_info()
	symbolList = []
	for symbol in exinfo['symbols']:
		if symbol['baseAsset'] != 'GXS': # EXCLUDE A SYMBOL IF NEEDED (ex. TUSD)
			if(symbol['quoteAsset'] == quoteAsset and symbol['status'] == 'TRADING'):
				symbolList.append(symbol['symbol'])

	return symbolList

def getOHLChistory(symbol='XLMBTC', interval='5m', limit=500):
	# Make API URL
	mainUrl = "https://www.binance.com/api/v1/klines?"
	url = mainUrl + urllib.parse.urlencode({"symbol": symbol, "interval": interval, "limit": limit})
	# Set pandas to 8 decimal places
	pd.set_option('precision', 8)
	# Read the url with pandas json
	df = pd.read_json(url)
	# Rename the columns
	df.columns = ['TimeOpen', 'Open', 'High', 'Low', 'Close', 'Volume', 'timeClose', 'QAV', 'trades', 'TBB', 'TBQ', 'ignore']
	# Change ms unix time stamp to normale date and time + 2 hours for local time
	df['TimeOpen'] = pd.to_datetime(df['TimeOpen'],unit='ms') + pd.Timedelta(hours=2)
	# Set TimeOpen as the index for the dataframe
	df.set_index('TimeOpen', inplace=True)
	# Delete all the clutter columns that we don't need
	del df['timeClose']; del df['QAV']; del df['trades']; del df['TBB']; del df['TBQ']; del df['ignore']

	return df

def getVolume(symbol):
	tickerData = client.get_ticker(symbol=symbol)
	tickerDataVolume = tickerData['quoteVolume']
	return float(tickerDataVolume)



