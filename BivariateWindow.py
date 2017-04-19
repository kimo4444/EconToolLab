from Tkinter import *
import sqlite3
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from p import nestedMenu, dbConnection, root


#establishing database connection
def dbConnection():
  
  dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
  global cursor 
  cursor = dbConnection.cursor()
dbConnection()

corrFrame = Toplevel(root)
corrFrame.geometry('700x800')
values1=[]
values2=[]
dates1 =[]
dates2 =[]
x=[]
y=[]
chosenIndicator = StringVar()
chosenIndicator2 = StringVar()

# plotting the scatterplot for two variables
def correlation():
	cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date')
	for column in cursor:
		values1.append(column[2])
		dates1.append(column[1])
		x=values1[1:10]	
	cursor.execute('SELECT * from [' + chosenIndicator2.get()+'] order by date')
	for column in cursor:
		values2.append(column[2])
		dates2.append(column[1])
		y = values2[1:10]


#finding correlation for two economic variables
	correlation = np.corrcoef(x,y)[1][0]
	corrLabel = Label (corrFrame, text = 'Correlation coefficient is ' + str(correlation), fg = '#518242', font=('Helvetica', 20))
	corrLabel.grid(column = 0, row = 4, sticky =W)
	covariance = np.cov(x,y)[0][1]
	covarLabel = Label (corrFrame, text = 'Covariance is ' + str(covariance), fg = '#518242', font=('Helvetica', 20))
	covarLabel.grid(column = 0, row = 5, sticky = W)
	fig = Figure(figsize=(5,4))
	axes = fig.add_subplot(111)
	axes.set_title('scatter plot')
	axes.set_xlabel(chosenIndicator.get())
	axes.set_ylabel(chosenIndicator2.get())
	axes.scatter(y,x,color='red')
	canvas = FigureCanvasTkAgg(fig, master=corrFrame)
	canvas.get_tk_widget().grid(padx =(45,0))
	canvas.draw()

	# fig2 = Figure(figsize=(5,4))
	# dates11 = mdates.datestr2num(dates1)
	# dates22 = mdates.datestr2num(dates2)

	# axes2 = fig2.add_subplot(111)
	# axes2.set_title('multiple plot')
	# axes2.set_xlabel(chosenIndicator.get()+'\n' +chosenIndicator2.get())
	# plot1,=axes2.plot(dates11,values1,color='red')
	# plot2,=axes2.plot(dates22,values2,color='green')
	# fig2.legend([plot1,plot2],[chosenIndicator.get(), chosenIndicator2.get()], 'upper right')
	# axes2.xaxis_date()
	# canvas2 = FigureCanvasTkAgg(fig2, master=corrFrame)
	# canvas2.get_tk_widget().grid(padx =(50,0))
	# canvas2.draw()
	

chosenIndicator.set('Real Gross Domestic Product (1930-2016)')
chosenIndicator2.set('Annual Inflation Rate (1914-2017)')

#creating two nested menus for choosing economic variables for calculating their correlation
nestedMenu(corrFrame,1,chosenIndicator)
nestedMenu(corrFrame,2,chosenIndicator2)
submitButton = Button(corrFrame, text = 'Plot', width= 10, command = correlation)
submitButton.grid(row = 3, column = 1,  padx = (20,0), pady=(25,0), sticky=W)

root.mainloop()
	