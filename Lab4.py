### Lab 4 Ary Suri ###
from datetime import datetime
import requests, json


#1. Get stock ticker from user

stockTicker = input("Enter a stock ticker: ")
stockUrl = "https://query1.finance.yahoo.com/v11/finance/quoteSummary/" + stockTicker


#check if stockTicker is valid and handle error
financialData = requests.get(stockUrl  + "?modules=financialData", headers={'User-agent': 'Mozilla/5.0'})
while financialData.status_code != 200:
    stockTicker = input("Error with previously entered ticker. Please enter a valid stock ticker: ")
    stockUrl = "https://query1.finance.yahoo.com/v11/finance/quoteSummary/" + stockTicker
    financialData = requests.get(stockUrl  + "?modules=financialData", headers={'User-agent': 'Mozilla/5.0'})


#Api requests
financialData = financialData.json()
nameData = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + stockTicker, headers={'User-agent': 'Mozilla/5.0'}).json()
dateData = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/" + stockTicker + "?metrics=high?&interval=1d&range=1d", headers={'User-agent': 'Mozilla/5.0'}).json()

#get desired data
fullName = nameData['quoteResponse']['result'][0]['longName']
currPrice = financialData['quoteSummary']['result'][0]['financialData']['currentPrice']['fmt']
targetMeanPrice = financialData['quoteSummary']['result'][0]['financialData']['targetMeanPrice']['fmt']
cashOnHand = financialData['quoteSummary']['result'][0]['financialData']['totalCash']['fmt']
profMarg = financialData['quoteSummary']['result'][0]['financialData']['profitMargins']['fmt']
date = datetime.fromtimestamp(dateData['chart']['result'][0]['meta']['regularMarketTime']).date().strftime('%m/%d/%Y')

#return as json
results = {"stockTicker":stockTicker, "fullStockName":fullName, "currentPrice":currPrice, "targetMeanPrice":targetMeanPrice, "cashOnHand":cashOnHand, "profitMargin":profMarg, "date":date}

resultsJson = json.dumps(results)
with open("results.json", "w") as outfile:
    outfile.write(resultsJson)
