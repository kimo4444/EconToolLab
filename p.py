from Tkinter import *
import sqlite3
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#connects to database
dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
cursor = dbConnection.cursor()



#imports quandl csv data into sqlite
# df = pandas.read_csv('Gross_national _product.csv')
# df.to_sql('Gross National Product (1930-2015)', dbConnection)


#main frame
root = Tk()
root.title('EconToolLab')
root.geometry('900x600')
# root['bg'] = '#E8E8E8'


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




# dropdown menu for economic variables
toolsFrame = Frame(root)
var = StringVar()


econIndicators = {'GDP': ['Real Gross Domestic Product (1947-2016)', 'Potential GDP (1949-2027)', 'Lagging Index (1948 - 2017)'],
				   'Inflation and price': ['Annual Inflation Rate (1914-2017)', 
				   'Chained CPI (1999-2017)', 'Misery Index (1914-2017)'
				   ],
				   'Labor': ['Natural rate of Unemployement','Unemployemnet rate by gender','Labor force participation rate','Employment rate(non-farm 1939-2017)'],
				   'Housing': ['Housing Market Index (1985-2017)', 'Fixed 30 year mortage rates','Historical ARM Indexes: 3 Year CMT'],
				   'Exports/Imports': ['Imports/Exports rates(1989-2016)'],
				   'Monetary Data': ['Share of Household Consumption'],
				   'Industry': ['Industry index by sector'],
				   'Investment':['Angel Investment', 'Angel Investment by sector'],
				   'Interest Rates': ['Interest Rate'],
				   'Equity':[ 'NASDAQ index']

	
}
 
#declaring query variables
chosenIndicator = StringVar()
checkedMax  = IntVar()
checkedMin = IntVar()
checkedMean = IntVar()
checkedStd = IntVar()
values = []
dates = []



chosenIndicator.set('Real Gross Domestic Product (1947-2016)')
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


#creates a database query depending on the chosen economic indicator
def query ():
  cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date asc')
  for column in cursor:
  	print column[0],column[1], column[2], '\n'
  	dates.append(str(column[1]))
  	values.append(int(column[2]))
  	print dates
  	print values
  x = mdates.datestr2num(dates)
  y = values
  fig, axes = plt.subplots()
  axes.plot(x, y)
  axes.xaxis_date()
  fig.autofmt_xdate() 
  
  if checkedMax.get() == 1:
  	cursor.execute('SELECT max(value), date from [' + chosenIndicator.get()+']')
  	for column in cursor:
  		print 'maximum value is ', column[0], 'in ', column[1], '\n'

  if checkedMin.get() == 1:
  	cursor.execute('SELECT min(value), date from [' + chosenIndicator.get()+']')
  	for column in cursor:
  		print 'minimum value is ', column[0], 'in ', column[1], '\n'
  

  if checkedMean.get() == 1:
  	cursor.execute('SELECT AVG(value), date from [' + chosenIndicator.get()+']')
  	for column in cursor:
  		print 'Average value is ', column[0], '\n'


  
  plt.show() 





#checkbuttons for statistical tools
variance = Checkbutton(toolsFrame,  onvalue=1, offvalue=0, text = 'Variance').grid(row = 2,column = 0, pady=(15,0), padx = (8,0), sticky = W)

std = Checkbutton(toolsFrame, variable = checkedStd, onvalue=1, offvalue=0, text = 'Std.Deviation').grid(row = 2, column = 1, pady=(15,0), padx = (8,0), sticky= W)

mean = Checkbutton(toolsFrame, variable = checkedMean, onvalue=1, offvalue=0, text = 'Mean').grid(row = 3, column = 0, sticky = W, padx = (8,0))
median = Checkbutton(toolsFrame,  onvalue=1, offvalue=0, text = 'Median').grid(row = 3, column = 1, sticky = W, padx = (8,0))


minValue = Checkbutton(toolsFrame,  variable = checkedMin, onvalue=1, offvalue=0, text = 'Minimum').grid(row = 4, column = 0, sticky = W, padx = (8,0))
maxValue = Checkbutton(toolsFrame, variable = checkedMax, onvalue=1, offvalue=0, text = 'Maximum').grid(row = 4, column = 1, sticky = W, padx = (8,0))

rangeValue = Checkbutton(toolsFrame,  onvalue=1, offvalue=0, text = 'Range').grid(row = 5, column = 0, sticky = W, padx = (8,0), pady = (0,20))

submitButton = Button(toolsFrame, text = 'Submit', command = query)
submitButton.grid(row = 6, column = 1)


toolsFrame.grid()
plotFrame = Frame(root)
# plot = Figure()
# plotCanvas = FigureCanvasTkAgg()



plotFrame.grid()

root.mainloop()


