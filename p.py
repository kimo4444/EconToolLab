from Tkinter import *
import sqlite3
import pandas

dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
cursor = dbConnection.cursor()

df = pandas.read_csv('FRED-GDP.csv')
df.to_sql('gdp', dbConnection)

root = Tk()
root.title('EconToolLab')
root.geometry('900x600')
root['bg'] = '#E8E8E8'

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



toolsFrame = Frame(root)
var = StringVar()
toolChoice = OptionMenu(toolsFrame, var, 'GDP per capita','Inflation','Employment data', 'Housing Data', 'Population Data')
var.set('Inflation')
toolChoice.grid(columnspan=2,sticky="WE")


variance = Checkbutton(toolsFrame, text = 'Variance').grid(row = 1,column=0)

std = Checkbutton(toolsFrame, text = 'Std.Deviation').grid(row = 1, column=1)

mean = Checkbutton(toolsFrame, text = 'Mean').grid(row = 2, column = 0, sticky = W)
median = Checkbutton(toolsFrame, text = 'Median').grid(row = 2, column = 1, sticky = W)


min = Checkbutton(toolsFrame, text = 'Minimum').grid(row = 3, column = 0, sticky = W)
max = Checkbutton(toolsFrame, text = 'Maximum').grid(row = 3, column = 1, sticky = W)

range = Checkbutton(toolsFrame, text = 'Range').grid(row = 4, column = 0, sticky = W)
skewness = Checkbutton(toolsFrame, text = 'Skewness').grid(row = 4, column = 1, sticky = W)


toolsFrame.grid()
plotFrame = Frame(root).grid()

root.mainloop()


