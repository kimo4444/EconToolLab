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
x=[]
y=[]
chosenIndicator = StringVar()
chosenIndicator2 = StringVar()

# plotting the sctterplot for two variables
def correlation():
	cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date')
	for column in cursor:
		values1.append(column[2])
		x=values1[1:10]	
	cursor.execute('SELECT * from [' + chosenIndicator2.get()+'] order by date')
	for column in cursor:
		values2.append(column[2])
		y = values2[1:10]

#finding correlation for two economic variables
	correlation = np.corrcoef(x,y)[1][0]
	corrLabel = Label (corrFrame, text = 'Correlation coefficient is ' + str(correlation), fg = '#518242', font=('Helvetica', 20))
	corrLabel.grid(column = 0, row = 4)
	fig = Figure(figsize=(5,4))
	axes = fig.add_subplot(111)
	axes.set_title('scatter plot')
	axes.set_xlabel(chosenIndicator.get())
	axes.set_ylabel(chosenIndicator2.get())
	axes.scatter(y,x,color='blue')
	axes.invert_yaxis()
	canvas = FigureCanvasTkAgg(fig, master=corrFrame)
	canvas.get_tk_widget().grid(padx =(40,0))
	canvas.draw()
	corrLabel = Label (corrFrame, textvariable = correlation)
	corrLabel.grid(column = 1, row = 10, padx = (20,0))

chosenIndicator.set('Real Gross Domestic Product (1930-2016)')
chosenIndicator2.set('Annual Inflation Rate (1914-2017)')
#creating two nested menus for choosing economic variables for calculating their correlation 
nestedMenu(corrFrame,1,chosenIndicator)
nestedMenu(corrFrame,2,chosenIndicator2)
submitButton = Button(corrFrame, text = 'Plot', width= 10, command = correlation)
submitButton.grid(row = 3, column = 1,  padx = (20,0), pady=(25,0), sticky=W)






root.mainloop()
	