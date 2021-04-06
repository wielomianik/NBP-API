import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

#### dict_keys(['table', 'currency', 'code', 'rates'])

def getCurrencyLow(days, currency, currencyName):
    today = dt.datetime.today()
    for i in range(days + 1):
        last = today - dt.timedelta(days = i)

    startDate = today.strftime('%Y-%m-%d')
    endDate = last.strftime('%Y-%m-%d')

    connect = 'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + endDate + '/' + startDate
    connectResult = requests.get(connect)
    response = connectResult.json()

    data = pd.DataFrame(response['rates'], columns=['effectiveDate', 'mid'], index=None)
    NewNames = {'effectiveDate': 'Data', 'mid': currencyName}
    data.rename(columns=NewNames, inplace=True)
    return data

def getCurrency(numberofDays, currency, currencyName):
    
    if numberofDays < 350:
        
        result = getCurrencyLow(numberofDays, currency, currencyName)
        return result
    
    else:
        
        results = []
        condition = round(numberofDays / 350)
        currentDays = 350
        start = dt.datetime.today()
        #print("condition:", condition)
        
        for section in range(condition + 1):
            #print("section:", section)
            for i in range(currentDays + 1):
                last = start - dt.timedelta(days=i)

            startDate = start.strftime('%Y-%m-%d')
            endDate = last.strftime('%Y-%m-%d')

            connect = 'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + endDate + '/' + startDate
            #print(connect)
            connectResult = requests.get(connect)
            response = connectResult.json()

            data = pd.DataFrame(response['rates'], columns=['effectiveDate', 'mid'], index=None)
            NewNames = {'effectiveDate': 'Data', 'mid': currencyName}
            data.rename(columns=NewNames, inplace=True)
            data.sort_values(by='Data', inplace=True, ascending=False)
            data = data.reset_index(drop=True)
            
            results.append(data)
            start = last
            numberofDays -= 350
            
            if numberofDays < 350:
                currentDays = numberofDays
                
        return results


def finalDownload(finalDays, finalCurrencyCode, finalCurrencyName):
    
    tempCurrency = getCurrency(finalDays, finalCurrencyCode, finalCurrencyName)
    downloadedCurrency = tempCurrency[0]
    
    
    for i in range(len(tempCurrency) - 1):
        downloadedCurrency = downloadedCurrency.append(tempCurrency[i + 1])
        
    downloadedCurrency.drop_duplicates(subset='Data', inplace=True)
    downloadedCurrency = downloadedCurrency.reset_index(drop=True)
    downloadedCurrency = downloadedCurrency.astype({'Data': 'datetime64'})

    daysResult = []
    Results = []
    for i in range(downloadedCurrency.shape[0] - 1):
        result = (downloadedCurrency['Data'][i] - downloadedCurrency['Data'][i + 1]).days
        
        if result != 1:
            Results.append(result)
            daysResult.append([downloadedCurrency['Data'][i], downloadedCurrency['Data'][i + 1],
                                   downloadedCurrency[finalCurrencyName][i + 1]])

    for i in range(len(daysResult)):

        checkFinal = downloadedCurrency['Data'].isin([daysResult[i][1]])
        checkFinalindex = checkFinal[checkFinal == True].index
        slicePart = checkFinalindex[0]
        
        for j in range(Results[i] - 1):
            line = pd.DataFrame({'Data': 'Dzień wolny', finalCurrencyName: daysResult[i][2]}, index=[slicePart])
            downloadedCurrency = downloadedCurrency.append(line, ignore_index=False)
            downloadedCurrency = downloadedCurrency.sort_index().reset_index(drop=True)
    
    del downloadedCurrency['Data']
    newDates = []
    toDay = dt.datetime.today()
    for k in range(downloadedCurrency.shape[0]):
        lastDay = toDay - dt.timedelta(days=k)
        newDates.append(lastDay.strftime('%Y-%m-%d'))
        
        
    downloadedCurrency.insert(0, 'Data', newDates)
    downloadedCurrency.sort_values(by='Data', inplace=True, ascending=False)
    downloadedCurrency = downloadedCurrency.reset_index(drop=True)
    
    return downloadedCurrency


usd = finalDownload(1702, 'usd', 'USD')
euro = finalDownload(1702, 'eur', 'EURO')

finalCurrency = usd
finalCurrency = finalCurrency.assign(EURO=pd.Series(euro['EURO']).values)


size = finalCurrency.shape[0]
x = np.arange(0, size)
plt.plot(x, finalCurrency['USD'][::-1], finalCurrency['EURO'][::-1])
xlabel = " ".join((str(finalCurrency['Data'].values[-1]), ' to ', str(finalCurrency['Data'][0])))
plt.xlabel(xlabel)
plt.ylabel('Wartość w zł')
plt.legend(['USD', 'EURO'])
plt.xticks([])
plt.show()
    