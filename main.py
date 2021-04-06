from tkinter import *
from source import finalDownload
import matplotlib.pyplot as plt
import numpy as np

root = Tk()

def downloadData():
    days, currency = 500, 'USD'
    currencyLow = currency.lower()
    database = finalDownload(days, currencyLow, currency)
    drawPlot(database)
    myLabel = Label(root, text="Data has been downloaded succesfully!")
    myLabel.grid(row=2, column=0)


def drawPlot(data):
    size = data.shape[0]
    x = np.arange(0, size)
    plt.plot(x, data[currency][::-1])
    xlabel = " ".join((str(data['Data'].values[-1]), ' to ', str(data['Data'][0])))
    plt.xlabel(xlabel)
    plt.ylabel('PLN')
    plt.legend([currency])
    plt.xticks([])
    plt.show()


myButton = Button(root, text="Click Me!", command=downloadData)
myButton.grid(row=0, column=0)

root.mainloop()


