#######################
#EconToolLab is an app that helps
#students majoring in economics
########################



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
import tkMessageBox
import sys
import os
import ttk
print matplotlib.__version__

#connecting to database
dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
global cursor 
cursor = dbConnection.cursor()

####################################################
#imports quandl csv data into sqlite
# df = pandas.read_csv('FRED-GDP.csv')
# df.to_sql('Gross Domestic Product (1947-2017)', dbConnection)
#####################################################



def nestedMenu(frame,row,var):
  econIndicators = {'GDP': ['Gross Domestic Product (1947-2017)', 
             'Potential GDP (1949-2027)', 'Lagging Index (1948 - 2017)',
             'Personal consumption expenditure (1959-2017)'],

             'Inflation and price': ['Annual Inflation Rate (1914-2017)', 
             'Chained CPI (1999-2017)',
             'Producer Price Index for Commodities (1994-2017)'
             ],
             'Labor': ['Labor force participation (1948-2017)','Employment rate(non-farm 1939-2017)', 
             'Employment rate for women (1964-2017)',
             'Unemployment rate (1948-2017)'],
             'Housing': ['Housing Market Index (1985-2017)',
             'House Price Index All States (1975-2016)',
             '30-year Fixed Mortgage Rates (1971-2017)',
             'Annual Rate for Total Construction (2002-2016)'],
             'Exports/Imports': ['Imports/Exports rates(1989-2016)'],
             'Industry': ['Manufacturing and Trade Inventories and Sales (1992-2017)'],
             'Investment':['Angel investment by sector (2002-2015)'],
             'Equity':['S&P 500 index (1950-2017)', 'US Treasury Long Term Rates (2000-2017)'
    
  ]}

  chosenIndicator.set('Gross Domestic Product (1947-2017)') #default indicator
  nestedMenu = Menubutton(frame, textvariable = var, font=('Helvetica', 16))
  mainMenu = Menu(nestedMenu, tearoff= False)
  nestedMenu.config(menu = mainMenu)

  for indicator in(econIndicators.keys()):
    option = Menu(mainMenu)
    mainMenu.add_cascade(label = indicator, menu = option)
    mainMenu.add_separator()
    for nestedIndicator in econIndicators[indicator]:
                  option.add_checkbutton(label=nestedIndicator, variable = var, onvalue=nestedIndicator, offvalue=0)
                  option.add_separator()
  nestedMenu.grid(row =row, columnspan = 2, sticky = 'EW', padx = (40,0), pady = (20, 0))
def correlation():
  checkedScatter = IntVar()
  checkedBivar = IntVar()
  corrFrame = Toplevel(root)
  corrFrame.geometry('700x800')
  corrLabel = Label(corrFrame, text = 'Bivariate Statistics', font=('Helvetica 23 underline'))
  corrLabel.grid(row = 0,column = 0, pady=(50,0), padx = (60,0), sticky = W)
  startLabel2 = Label(corrFrame, text = 'Start Year', font=('Helvetica', 17)).grid(row = 3, column = 0, padx = (60,0),sticky = NW, pady = (40,10))
  startYear2 = Entry(corrFrame)
  startYear2.grid(row = 3, column = 1, sticky = NW, pady =(40,10))
  endLabel2 = Label(corrFrame, text = 'End Year', font=('Helvetica', 17)).grid(row = 4, column = 0, padx = (60,0), sticky=NW)
  endYear2 = Entry(corrFrame)
  endYear2.grid(row = 4, column = 1, sticky = NW)
  plotLabel = Label(corrFrame, text = 'Plot Type:', font=('Helvetica 23 underline'))
  plotLabel.grid(row = 6,column = 0, pady=(30,0), padx = (40,0), sticky = W)
  plotValue = Checkbutton(corrFrame,  variable = checkedScatter, text = 'Scatter Plot', font=('Helvetica 15 underline')).grid(row = 7, column = 0, sticky = W, padx = (40,0), pady = (8,10))
  histValue = Checkbutton(corrFrame,  variable = checkedBivar, text = 'Bivariate Plot', font=('Helvetica 15 underline')).grid(row = 7, column = 1, sticky = W, pady = (8,10))

  values1=[]
  values2=[]
  dates1 =[]
  dates2 =[]
  x=[]
  y=[]
  chosenIndicator = StringVar()
  chosenIndicator2 = StringVar()
#########################################################
# plotting the scatterplot graph 
# to see positive/negative/no relation between variables
#########################################################
  def scatter():
    del dates1[:]
    del values1[:]
    del dates2[:]
    del values2[:]
    cursor.execute('SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator.get()+']')
    for column in cursor:
      minYear = int(column[0])
      maxYear = int(column[1])
    cursor.execute('SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator2.get()+']')
    for column in cursor:
      minYear2 = int(column[0])
      maxYear2 = int(column[1])
    maxLower = max(minYear, minYear2)
    maxUpper = min(maxYear, maxYear2)


    ###############################################################################
    # showing an error message if years are out of range and proceeding if in range
    ###############################################################################
    if startYear2.get() == '':
      tkMessageBox.showerror("Error", "Please input years")

    if startYear2.get() != '':
      if ((int(startYear2.get())<minYear or int(startYear2.get())<minYear2) or (int(startYear2.get())>maxYear or int(startYear2.get())>maxYear2 or (int(endYear2.get())<minYear or int(endYear2.get())>maxYear))):
        tkMessageBox.showerror("Error", "Input years are out of range. The correct range is "+ str(maxLower)+ ' - '+ str(maxUpper))
    
      else:
        cursor.execute('SELECT * from [' + chosenIndicator.get()+'] where strftime("%Y", date) between "' + startYear2.get() +'" and "' + endYear2.get() +'" order by date asc')
        for column in cursor:
          values1.append(column[2])
          dates1.append(column[1])
          x=values1
        cursor.execute('SELECT * from [' + chosenIndicator2.get()+'] where strftime("%Y", date) between "' + startYear2.get() +'" and "' + endYear2.get() +'" order by date asc')
        for column in cursor:
          values2.append(column[2])
          dates2.append(column[1])
          y=values2
      
  
  ################################################
  #finding correlation for two economic variables
  #################################################
    covariance = np.cov(x,y)[0][1]
    correlation = np.corrcoef(x,y)[1][0]
    corrList = Listbox(corrFrame, font=('Helvetica', 18), borderwidth=0, width =50)
    corrList.insert(END, 'Correlation coefficient   ' + str(correlation))
    corrList.insert(END, 'Covarience                    ' +str(covariance))
    corrList.grid(column = 0, row = 10, columnspan =2, sticky =W, padx=(60,0), pady = 30)

    if checkedScatter.get() == 1:
      fig, axes = plt.subplots()
      axes.set_title(chosenIndicator.get()+ ' and '+ chosenIndicator2.get())
      axes.set_xlabel(chosenIndicator.get())
      axes.set_ylabel(chosenIndicator2.get())
      axes.scatter(y,x,color='red')
    if checkedBivar.get() ==1:
      dates11 = mdates.datestr2num(dates1)
      dates22 = mdates.datestr2num(dates2)

      fig2, axes2 = plt.subplots()
      axes2.set_title(chosenIndicator.get()+ ' and '+ chosenIndicator2.get())
      axes2.set_xlabel(chosenIndicator.get()+'\n' +chosenIndicator2.get())
      plot1,=axes2.plot(dates11,values1,color='red')
      plot2,=axes2.plot(dates22,values2,color='green')
      fig2.legend([plot1,plot2],[chosenIndicator.get(), chosenIndicator2.get()], 'upper right')
      axes2.xaxis_date()
  
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()

  
  chosenIndicator.set('Gross Domestic Product (1947-2017)')
  chosenIndicator2.set('Annual Inflation Rate (1914-2017)')
  ##############################################################################################
  #creating two nested menus for choosing economic variables for calculating their correlation
  #and drawing a scatterplot
  ##############################################################################################
  nestedMenu(corrFrame,1,chosenIndicator)
  nestedMenu(corrFrame,2,chosenIndicator2)
  submitButton = Button(corrFrame, text = 'Plot', width= 10, command = scatter)
  submitButton.grid(row = 9, column = 1,  padx = (60,0), pady=(25,0), sticky=W)




root = Tk()
root.title('EconToolLab')
navFrame=Frame(root)
root.geometry('900x850')
# navFrame.grid_columnconfigure(0, weight=1)
# navFrame.grid_rowconfigure(0, weight=1)

#declaring variables
chosenIndicator = StringVar()
checkedMax = IntVar()
checkedMin = IntVar()
checkedMean = IntVar()
checkedStd = IntVar()
checkedVar = IntVar()
checkedRange = IntVar()
checkedMedian = IntVar()
checkedMed = IntVar()
checkedPlot = IntVar()
checkedHist = IntVar()
values = []
dates = []
maxim = IntVar()
label = StringVar()
color = StringVar()
plotTitle = StringVar()
minYear = IntVar()
maxYear = IntVar()
binNumber = IntVar()

def DescriptiveTools():
  toolsFrame = Toplevel(root)
  toolsFrame.geometry('900x850')
  toolsFrame.grid_rowconfigure(20, weight=1)
  toolsFrame.grid_columnconfigure(6, weight=1)
  var = StringVar()



  def query ():

    #################################################################################
    #function that plots histogram or time series or both using matplolib, as well as 
    #creates an output table consisiting of dates and values depending on the user's input
    #################################################################################

    def plot():
      valueCanvas = Canvas(toolsFrame)
      scrollbar = Scrollbar(valueCanvas)  
      valueCanvas.grid(row=0, rowspan= 15, column= 4, columnspan=2, padx = (100,0), pady=(20,0))
      listbox = Listbox(valueCanvas, height=20, width =25, font=('Helvetica', 16))
      listbox.grid(row=0, sticky=E)
      listbox.insert(END, 'Date                     Value')
      del dates[:]
      del values[:]
      for column in cursor:
        dates.append(str(column[1]))
        values.append(column[2])
        binNumber = len(values)
        index=0
      y = values

      for date in dates:
        listbox.insert(END, date+'               ' +str(values[index]))
        index+=1
      ##########################################################
      #creates a scrollbar for the listbox with dates and values  
      ##########################################################

      scrollbar.grid(row=0, column=7, sticky=N+S)
      listbox.config(yscrollcommand=scrollbar.set)
      scrollbar.config(command=listbox.yview)

      
      valueLabel = Label(valueCanvas, text = 'Statistics', font=('Helvetica 18 underline'))
      valueLabel.grid(row =10, sticky =W, pady = 21)
      statbox = Listbox(valueCanvas, font=('Helvetica', 17), borderwidth = 0, width = 25)
      if checkedMax.get():
        maxim = np.max(values)
        statbox.insert(END, 'Maximum  ' + str(maxim))
      

      if checkedMin.get() == 1:
        minim = np.min(values)
        statbox.insert(END,'Minimum  ' + str(minim))
  

      if checkedMean.get() == 1:
        mean = np.average(values)
        statbox.insert(END,'Mean  ' + str(mean))
       
        
      if checkedStd.get() == 1:
        stdDev = np.std(values)
        statbox.insert(END,'Standard deviation ' + str(stdDev))
        
      if checkedMed.get() == 1:
        median = np.median(values)
        statbox.insert(END,'Median value is ' + str(median))
        

      if checkedRange.get() == 1:
        rang = np.max(values) - np.min(values)
        statbox.insert(END,'Range ' + str(rang))
      statbox.grid(rowspan=20)  
     

      
      ###############################################################
      #plotting time series style graph using matplotlib method 'plot'
      ###############################################################
     
      
      # plot = Figure(figsize=(6,4))
      if checkedPlot.get() ==1:
        # axes = plot.add_subplot(111)
        fig, axes = plt.subplots()
        axes.xaxis_date()
        fig.autofmt_xdate() 
 
        axes.set_xlabel(xAxis.get() or 'year')
        axes.set_ylabel(yAxis.get() or 'value')
        x = mdates.datestr2num(dates)
        axes.set_title(plotTitle.get() or chosenIndicator.get())
        axes.plot(x, y, color = color.get())
        plt.show() 
        plt.clf()
        plt.cla()
        plt.close()
  
      ###############################################################
      #plotting histogram style graph using matplotlib method 'hist'
      ###############################################################
      if checkedHist.get() == 1:
        fig, axes = plt.subplots()
        axes.set_title(plotTitle.get() or chosenIndicator.get())
        axes.set_xlabel(xAxis.get() or 'value')
        axes.set_ylabel(yAxis.get() or 'percent')

        ####################################################################################################################
        #calculating default optimal number of bins(rounded to the nearest whole number) using 
        #Sturges Rule in case not provided by the user
        ####################################################################################################################

        k = int(round(1 + (3.322*np.log10(binNumber))))
        x = int(binEntry.get() or k)

        axes.hist(y, bins = x, rwidth=0.3, normed=True)
        plt.show() 
        plt.clf()
        plt.cla()
        plt.close()
          
      
      
      
      # def goBack():
      #   python = sys.executable
      #   os.execl(python, python, * sys.argv)
        

      # resetButton = Button(toolsFrame, text = "Restart to plot new graph", command=goBack).grid(row=20)
      
      

    #########################################
    #checking if input years are out of range
    #########################################

    cursor.execute('SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator.get()+']')
    for column in cursor:
      minYear = int(column[0])
      maxYear = int(column[1])

    ###############################################################################
    # showing an error message if years are out of range and proceeding if in range
    ###############################################################################

    if startYear.get() != '':
      if (int(startYear.get())<minYear or int(startYear.get())>maxYear) or (int(endYear.get())<minYear or int(endYear.get())>maxYear):
        tkMessageBox.showerror("Error", "Input years are out of range. The correct range is "+ str(minYear)+ ' - '+ str(maxYear))
    
      else:
        cursor.execute('SELECT * from [' + chosenIndicator.get()+'] where strftime("%Y", date) between "' + startYear.get() +'" and "' + endYear.get() +'" order by date asc')
        plot()
    if startYear.get() == '':
      cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date asc')
      plot()

  ######################################################
  # creating nested dropdown menu for economic variables
  # using Tkinter's Menu and Menubutton
  ######################################################



  nestedMenu(toolsFrame,0, chosenIndicator)

  ###############################################
  #checkbuttons for descriptive statistical tools
  ###############################################

  descStatLabel = Label(toolsFrame, text = 'Descriptive Statistics:', font=('Helvetica 15 underline'))
  descStatLabel.grid(row = 1,column = 0, pady=(20,0), padx = (40,0), sticky = W)
  variance = Checkbutton(toolsFrame,  onvalue=1, variable = checkedVar, offvalue=0, text = 'Variance').grid(row = 2,column = 0, pady=(10,0), padx = (40,0), sticky = W)
  std = Checkbutton(toolsFrame, variable = checkedStd, onvalue=1, offvalue=0, text = 'Std.Deviation').grid(row = 2, column = 1, columnspan = 1, pady=(10,0),  sticky= W)
  mean = Checkbutton(toolsFrame, variable = checkedMean, onvalue=1, offvalue=0, text = 'Mean').grid(row = 3, column = 0, sticky = W, padx = (40,0), pady=(8,0))
  median = Checkbutton(toolsFrame,  variable = checkedMed, onvalue=1, offvalue=0, text = 'Median').grid(row = 3, column = 1, sticky = W, pady=(8,0))
  minValue = Checkbutton(toolsFrame,  variable = checkedMin, onvalue=1, offvalue=0, text = 'Minimum').grid(row = 4, column = 0, sticky = W, padx = (40,0), pady=(8,0))
  maxValue = Checkbutton(toolsFrame, variable = checkedMax, onvalue=1, offvalue=0, text = 'Maximum').grid(row = 4, column = 1, sticky = W, pady=(8,0))

  ###############################################
  #checkbuttons for plot type choice
  ###############################################
  rangeValue = Checkbutton(toolsFrame,  variable = checkedRange, onvalue=1, offvalue=0, text = 'Range').grid(row = 5, column = 0, sticky = W, padx = (40,0), pady = (8,0))
  plotLabel = Label(toolsFrame, text = 'Plot Type:', font=('Helvetica 15 underline'))
  plotLabel.grid(row = 6,column = 0, pady=(30,0), padx = (40,0), sticky = W)
  plotValue = Checkbutton(toolsFrame,  variable = checkedPlot, text = 'Time Series Graph').grid(row = 7, column = 0, sticky = W, padx = (40,0), pady = (8,10))
  histValue = Checkbutton(toolsFrame,  variable = checkedHist, text = 'Histogram').grid(row = 7, column = 1, sticky = W, pady = (8,10))
  startLabel = Label(toolsFrame, text = 'Start Year').grid(row = 8, column = 0, padx = (40,0),sticky = NW)
  startYear = Entry(toolsFrame)
  startYear.grid(row = 8, column = 1, sticky = NW)
  endLabel = Label(toolsFrame, text = 'End Year').grid(row = 9, column = 0, padx = (40,0), sticky=NW)
  endYear = Entry(toolsFrame)
  endYear.grid(row = 9, column = 1, sticky = NW)

  ###############################################
  #checkbuttons for custom styling the plot
  ###############################################
  customLabel = Label(toolsFrame, text = 'Custom Styles:', font=('Helvetica 15 underline'))
  customLabel.grid(row = 11,column = 0, pady=(20,0), padx = (40,0), sticky = W)

  color.set('green')
  colorPick = OptionMenu(toolsFrame, color, 'red', 'green', 'black', 'blue', 'orange', 'grey').grid(row=12, pady=(20,0), padx = (40,0), sticky = W )
  plotTitleBox = Label(toolsFrame, text = 'Plot Title').grid(row=13, column =0, sticky = W, pady=(20,0), padx = (40,0))
  plotTitle= Entry(toolsFrame)
  plotTitle.grid(row=13, column = 1, pady=(20,0))

  yAxisTitleBox = Label(toolsFrame, text = 'Y-axis').grid(row=14, column =0, sticky = W, padx = (40,0))
  yAxis= Entry(toolsFrame)
  yAxis.grid(row=14, column = 1)

  xAxisTitleBox = Label(toolsFrame, text = 'X-axis').grid(row=15, column =0, sticky = W, padx = (40,0))
  xAxis= Entry(toolsFrame)
  xAxis.grid(row=15, column = 1)

  ###############################################
  #choosing the bin number for the histogram
  ###############################################
  binLabel = Label(toolsFrame, text = 'Number of bins').grid(row=16, column =0, sticky = W, padx = (40,0))
  binEntry= Entry(toolsFrame)
  binEntry.grid(row=16, column = 1)

  submitButton = Button(toolsFrame, text = 'Submit', width= 10, command = query)
  submitButton.grid(row = 17, column = 1,  padx = (75,0), pady=(20,0), sticky=W)

def about():
  aboutFrame = Toplevel(root)
  listbox = Text(aboutFrame, font=('Helvetica', 15), spacing1 = 1)
  listbox.pack(fill=BOTH, pady =(20,0), padx=20)
  listbox.insert(END, '    Econ Tool Lab is an application aimed at students majoring in Economics.\n \
    It is an easy-to-use tool for visualization and analysis of economic data.\n \
    Econ Tool Lab offers a  combination of economic data from the most widely used databases and some of the features of\
    statistical software packages for data analysis. The application provides a quick access to most common economic\
    variables and indicators, as well as statistical tools to analyze them.\n\n\n\
    Economic Indicators:\n\n\
    GDP(gross domestic product) - the total dollar value of all goods and services produced over a specific time period\n\n\
    Inflation - the rate at which the general level of prices for goods and services is rising\n\n\
    Consumer Price Index (CPI)  -  the weighted average of prices of a basket of consumer goods and services\n\n\
    Labor Force - subset of Americans who have jobs or are seeking a job, are at least 16 years old, are not serving in the military and are not institutionalized.\n\n\
    Unemployment Rate - the percentage of the labor force that is jobless\n\n\
    Equity - a stock or any other security representing an ownership interest\n\n\
    Statistical Tools"\n\n\
    Data Visualization:\n\n\
    Time Series\
    Histogram\
    Scatter Plot\
    ')
  listbox.config(state=DISABLED)
  

#displaying app logo. Logo is from logologo.com.
photo = PhotoImage(file='/Users/kimo/Desktop/project/graph-logo.gif')
appLogo = Label(navFrame, image = photo)

appLogo.image = photo
appLogo.pack(anchor='center',fill=BOTH, pady=(20,8))

appName = Label(navFrame, text ='Econ Tool Lab', font=('Helvetica', 45), fg='#4c4d4f')
appName.pack(anchor='center',fill=BOTH, pady=(0,10))
appSub = Label(navFrame, text ='Easy-to-use tool for visualization and analysis of economic data', font=('Helvetica', 20), fg = '#5e8e54')
appSub.pack(anchor='center')
button1 = Button(navFrame, text="Descriptive Statistics", command=DescriptiveTools, font=('Helvetica', 25))
button1.pack(anchor='center',fill=BOTH, pady =(60,0), expand=1)
button2= Button(navFrame, text="Bivariate Analysis",command=correlation, font=('Helvetica', 25))
button2.pack(anchor='center',fill=BOTH, pady=20)
button3= Button(navFrame, text="About/Help", command=about, font=('Helvetica', 25))
button3.pack(anchor='center',fill=BOTH)
navFrame.pack()
root.mainloop()








