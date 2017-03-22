from Tkinter import *
import sqlite3
import pandas
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#connects to database
dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
cursor = dbConnection.cursor()



#imports quandl csv data into sqlite
# df = pandas.read_csv('30_year_fixed_mortgage_rates.csv')
# df.to_sql('30-year Fixed Mortgage Rates (1971-2017)', dbConnection)


#main frame
root = Tk()
root.title('EconToolLab')
root.geometry('1000x800')



#top level menu for the main window
navBar = Menu(root)

statisticsMenu = Menu(navBar)
statisticsMenu.add_command(label = 'Univariate Analysis')
statisticsMenu.add_command(label='Bivariate Analysis')
navBar.add_cascade(label = 'Descriptive Statistics', menu = statisticsMenu)

regressionMenu = Menu(navBar)
regressionMenu.add_command(label = 'Import Data')
regressionMenu.add_command(label= 'Linear Regression')
navBar.add_cascade(label = 'Regression Analysis', menu = regressionMenu)

helpMenu = Menu(navBar)
helpMenu.add_command(label = 'Getting started')
helpMenu.add_command(label = 'Help')
navBar.add_cascade(label = 'About the EconToolLab', menu = helpMenu)
root.config(menu=navBar)

chosenIndicator = StringVar()
checkedMax  = IntVar()
checkedMin = IntVar()
checkedMean = IntVar()
checkedStd = IntVar()
checkedVar = IntVar()
checkedRange = IntVar()
checkedMedian = IntVar()
checkedMed = IntVar()
values = []
dates = []
maxim = IntVar()
label = StringVar()
start = IntVar()
end = IntVar()


toolsFrame = Frame(root)
var = StringVar()


def query ():
  cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date asc')
  for column in cursor:
    print column[0],column[1], column[2], '\n'
    dates.append(str(column[1]))
    values.append(column[2])
    datesValues = np.column_stack((dates, values))
    print datesValues
    label = StringVar()
    for date in dates:
      label.set(date)
    dataLabel = Label(toolsFrame, text = datesValues).grid()

  x = mdates.datestr2num(dates)
  y = values
  axes = plot.add_subplot(111)
  axes.plot(x, y)
  axes.xaxis_date()
  canvas.show() 
  
  if checkedMax.get() == 1:
    maxim = np.max(values)
    print 'Maximum value is', maxim

  if checkedMin.get() == 1:
    minim = np.min(values)
    print 'Minimum value is', minim
  

  if checkedMean.get() == 1:
    mean = np.average(values)
    print 'Average is', mean
  
  if checkedStd.get() == 1:
    stdDev = np.std(values)
    print 'Standard deviation is ', stdDev
  
  if checkedMed.get() == 1:
    median = np.median(values)
    print 'Median is ', median

  if checkedRange.get() == 1:
    rang = np.max(values) - np.min(values)
    print 'Range is ', rang



# nested dropdown menu for economic variables
econIndicators = {'GDP': ['Real Gross Domestic Product (1930-2016)', 
           'Potential GDP (1949-2027)', 'Lagging Index (1948 - 2017)'],
				   'Inflation and price': ['Annual Inflation Rate (1914-2017)', 
				   'Chained CPI (1999-2017)', 'Misery Index (1914-2017)',
           'Producer Price Index for Commodities (1994-2017)'
				   ],
				   'Labor': ['Labor force participation (1948-2017)','Employment rate(non-farm 1939-2017)', 
           'Employment rate for women (1964-2017)',
           'Unemployment rate (1948-2017)'],
				   'Housing': ['Housing Market Index (1985-2017)',
           '30-year Fixed Mortgage Rates (1971-2017)',
           'Annual Rate for Total Construction (2002-2016)'],
				   'Exports/Imports': ['Imports/Exports rates(1989-2016)'],
				   'Monetary Data': ['M1 Money stock (1975-2017)'],
				   'Industry': ['Manufacturing and Trade Inventories and Sales (1992-2017)'],
				   'Investment':['Angel investment by sector (2002-2015)'],
				   'Equity':['S&P 500 index (1950-2017)', 'US Treasury Long Term Rates (2000-2017)']

	
}
 


chosenIndicator.set('Real Gross Domestic Product (1930-2016)') #default indicator
nestedMenu = Menubutton(toolsFrame, textvariable = chosenIndicator)
mainMenu = Menu(nestedMenu, tearoff= False)
nestedMenu.config(menu = mainMenu)

for indicator in(econIndicators.keys()):
	option = Menu(mainMenu)
	mainMenu.add_cascade(label = indicator, menu = option)
	mainMenu.add_separator()
	for nestedIndicator in econIndicators[indicator]:
                option.add_checkbutton(label=nestedIndicator, variable = chosenIndicator, onvalue=nestedIndicator, offvalue=0)
                option.add_separator()
nestedMenu.grid(columnspan = 2, sticky = W, padx = (4,10), pady = (18, 0))



#checkbuttons for statistical tools
variance = Checkbutton(toolsFrame,  onvalue=1, variable = checkedVar, offvalue=0, text = 'Variance').grid(row = 2,column = 0, pady=(5,0), padx = (8,0), sticky = W)

std = Checkbutton(toolsFrame, variable = checkedStd, onvalue=1, offvalue=0, text = 'Std.Deviation').grid(row = 2, column = 1, pady=(5,0), padx = (8,0), sticky= W)

mean = Checkbutton(toolsFrame, variable = checkedMean, onvalue=1, offvalue=0, text = 'Mean').grid(row = 3, column = 0, sticky = W, padx = (8,0))
median = Checkbutton(toolsFrame,  variable = checkedMed, onvalue=1, offvalue=0, text = 'Median').grid(row = 3, column = 1, sticky = W, padx = (8,0))


minValue = Checkbutton(toolsFrame,  variable = checkedMin, onvalue=1, offvalue=0, text = 'Minimum').grid(row = 4, column = 0, sticky = W, padx = (8,0))
maxValue = Checkbutton(toolsFrame, variable = checkedMax, onvalue=1, offvalue=0, text = 'Maximum').grid(row = 4, column = 1, sticky = W, padx = (8,0))

rangeValue = Checkbutton(toolsFrame,  variable = checkedRange, onvalue=1, offvalue=0, text = 'Range').grid(row = 5, column = 0, sticky = W, padx = (8,0), pady = (0,20))

startLabel = Label(toolsFrame, text = 'Start Year').grid(row = 6, column = 0)
startYear = Entry(toolsFrame).grid(row = 6, column = 1)
endLabel = Label(toolsFrame, text = 'End Year').grid(row = 7, column = 0)
endYear = Entry(toolsFrame).grid(row = 7, column = 1)
submitButton = Button(toolsFrame, text = 'Submit', command = query)
submitButton.grid(row = 8, column = 1)





plot = Figure(figsize=(6,4))

canvas = FigureCanvasTkAgg(plot, master=toolsFrame)

canvas.get_tk_widget().grid(row = 0, column = 4, columnspan=10, rowspan=8, sticky = W)


calcStat = Label(toolsFrame, textvariable = values).grid(row = 7, column = 0, sticky =W)


toolsFrame.grid()

root.mainloop()


