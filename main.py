from tkinter import *
from tkdocviewer import *
from source import finalDownload
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def downloadData():  #Downloading data by using finalDownload function
    loadedData = inputData()
    days, currency = int(loadedData[0]), str(loadedData[1])
    currencyLow = currency.lower()
    downloadData.database = finalDownload(days, currencyLow, currency)
    drawPlot(downloadData.database, currency)


def drawPlot(data, currency):  #Plotting data
    size = data.shape[0]
    x = np.arange(0, size)
    plt.plot(x, data[currency][::-1])
    xlabel = " ".join((str(data['Data'].values[-1]), ' to ', str(data['Data'][0])))
    plt.xlabel(xlabel)
    plt.ylabel('PLN')
    plt.legend([currency])
    plt.xticks([])
    plt.show()

def inputData(): # Getting data from user input
    days = inputBox.get()
    currency = inputBox_2.get()
    return [days, currency]

def saveCSV():
    saveTo = downloadData.database
    saveTo.to_csv('saved_data.csv')

def anotherDownload():
    inputBox.delete(0, END)
    inputBox_2.delete(0, END)

def openFile():  # Build - in txt file with currency codes
    top = Toplevel()
    top.title('Currency codes')
    top.geometry('500x700')
    openTXT = DocViewer(top)
    openTXT.pack(side='top', expand=1, fill='both')
    openTXT.display_file("list.txt")

#################################################################################
############################## Tkinter section ##################################

root = Tk()
root.title("NBP - API")
root.iconbitmap('cash.ico')
root.geometry('715x260')

daysLabel = Label(root, text="Enter desired numbers of days:", width=30, pady=10)
currencyLabel = Label(root, text='Enter desired currency:', width=30)
daysLabel.grid(row=0, column=1)
currencyLabel.grid(row=1, column=1)

inputBox = Entry(root, width=10)
inputBox_2 = Entry(root, width=10)   
inputBox.grid(row=0, column=2, padx=10)
inputBox_2.grid(row=1, column=2, padx=10)


myButton = Button(root, text="Download", command=downloadData)
infoButton = Button(root, text="Click for help", command=openFile)
csvButton = Button(root, text="Save data as csv!", command=saveCSV)
anotherDownload = Button(root, text="Download another currency", command=anotherDownload)

myButton.grid(row=2, column=2, pady=10)
infoButton.grid(row=2, column=1, pady=10)
csvButton.grid(row=4, column=1, pady=10)
anotherDownload.grid(row=5, column=1, pady=10)


frame = LabelFrame(root, text="How to?")
frame.grid(row=1, column=4, padx=50)
frameLabel = Label(frame, text="Into the first box input the ammount of the days e.g. 1000 days \n Second box is for the currency code e.g. 'USD'"
                                    "\n Click the (Click for help) button for all currency codes")
frameLabel.pack()

root.mainloop()
