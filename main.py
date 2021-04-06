from tkinter import *
from source import finalDownload
import matplotlib.pyplot as plt
import numpy as np

def downloadData():
    loadedData = inputData()
    days, currency = int(loadedData[0]), str(loadedData[1])
    currencyLow = currency.lower()
    database = finalDownload(days, currencyLow, currency)
    drawPlot(database, currency)
    myLabel = Label(root, text="Data has been downloaded succesfully!")
    myLabel.grid(row=2, column=0)


def drawPlot(data, currency):
    size = data.shape[0]
    x = np.arange(0, size)
    plt.plot(x, data[currency][::-1])
    xlabel = " ".join((str(data['Data'].values[-1]), ' to ', str(data['Data'][0])))
    plt.xlabel(xlabel)
    plt.ylabel('PLN')
    plt.legend([currency])
    plt.xticks([])
    plt.show()

def inputData():
    days = inputBox.get()
    currency = inputBox_2.get()
    return [days, currency]

root = Tk()
root.title("NBP - API")
root.iconbitmap('cash.jpg')
root.geometry('400x400')

daysLabel = Label(root, text="Enter desired numbers of days", width=30)
currencyLabel = Label(root, text='Enter desired currency', width=30)
daysLabel.grid(row=0, column=1)
currencyLabel.grid(row=1, column=1)

inputBox = Entry(root, width=10)
inputBox_2 = Entry(root, width=10)   
inputBox.grid(row=0, column=2, padx=10)
inputBox_2.grid(row=1, column=2, padx=10)

myButton = Button(root, text="Click Me!", command=downloadData)
myButton.grid(row=2, column=2)


root.mainloop()
