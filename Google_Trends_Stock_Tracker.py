#------------------------------------------------------------------------------------------------------------------------------------------#
#Imports:
#------------------------------------------------------------------------------------------------------------------------------------------#

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import *
from matplotlib import pyplot as plt
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyGTrends import pyGTrends
import ystockquote
from datetime import *
import datetime

from Tkinter import *
import Tkinter as Tk
import sys


# a module which converts dates into a numerical string in the YMD format
from date_converter import date_converter
# a module to make a dictionary for plotting the values against dates
from dict_maker import date_dict
# a module to pull data from ycharts.com, yahoo finace, and google analitics
from data_miner import ychart_data, yahoo_stock_data, google_data


#------------------------------------------------------------------------------------------------------------------------------------------#
#setup:
#------------------------------------------------------------------------------------------------------------------------------------------#

#finds today's date for graphing purposes
today = str(date.today())
today = today.replace('-','')

#------------------------------------------------------------------------------------------------------------------------------------------#
#Graphing:
#------------------------------------------------------------------------------------------------------------------------------------------#

fig = Figure(figsize=(8,6.2), dpi=100)

class graph_plot(object):
    
    def __init__(self, stock_symbol, metric):
        fig.clear()
        # Jan 4, 2004 is the oldest date in any of the lists
        #it is from the google trends data
        self.dictionary_class = date_dict("20040104")
        self.date_dictionary = self.dictionary_class.make_dict()
        self.stock_symbol = stock_symbol
        self.metric = metric
        fig.clear()
        fig.suptitle(self.stock_symbol + " " + metric +" VS Term Search Volume", fontsize=12, x = 0.5, y = .95)

    def plot_trend_info(self, term):
        google_information = google_data(term)
        self.ax1 = fig.add_subplot(111)
        self.lns1 = self.ax1.plot(self.dictionary_class.date_alligner(google_information.date_fetcher()),google_information.term_trend(), 'g-', label = "Search volume for " + "'" + term + "'")
        self.ax1.set_xlabel('Date')
        # Make the y-axis label and tick labels match the line color.
        self.ax1.set_ylabel("Search Volume", color='g')
        for tl in self.ax1.get_yticklabels():
            tl.set_color('g')
        #this rotates the dates and shifts them to the right
        #allows for more dates to be put into a smaller space
        fig.autofmt_xdate()
        
    def plot_ychart_info(self):
        stock_information = yahoo_stock_data(self.stock_symbol)

        ychart_information = ychart_data(self.stock_symbol, self.metric)
        ychart_information.date_fetcher()
        ychart_information.metric_fetcher()

        ax2 = self.ax1.twinx()

        #these format the x axis to display dates
        datemin = datetime.date(2004,01,04)
        datemax = datetime.date.today()
        ax2.set_xlim(datemin, datemax)

        if self.metric == "price":
            lns2 = ax2.plot(self.dictionary_class.date_alligner(stock_information.dates_list()),stock_information.stock_value(), 'b-', label = self.stock_symbol + " " + self.metric)
        else:
            lns2 = ax2.plot(self.dictionary_class.date_alligner(ychart_information.date_modder()), ychart_information.metric_modder(), 'b-', label = self.stock_symbol + " " + self.metric)
        
        
        ax2.set_ylabel(self.stock_symbol + " " + self.metric, color='b')
        for tl in ax2.get_yticklabels():
            tl.set_color('b')

        def price(x): return '$%1.2f'%x
        ax2.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax2.format_ydata = price
        ax2.grid(True)

        #places the line names into a legend
        lns = self.lns1+lns2
        labs = [l.get_label() for l in lns]
        ax2.legend(lns, labs, loc=2, prop={'size':8})

        fig.subplots_adjust(left = 0.08, bottom = 0.15, right = 0.89, top = 0.9)

#------------------------------------------------------------------------------------------------------------------------------------------#
#TK GUI Setup
#------------------------------------------------------------------------------------------------------------------------------------------#

class Tk_gui(object):
    
    def __init__(self):
        self.root = Tk.Tk()
        self.root.wm_title("Trend Metrics Beta V0.6")
        self.root.grid()
        self.symbol = StringVar()
        self.term = StringVar()
        self.metric = StringVar()
        self.metric.set("Choose a Metric")
        self.metrics = ("accounts_payable", "accounts_receivable", "asset_utilization", "book_value_of_equity", "book_value_per_share",
                        "cash_and_equivalents", "cash_on_hand", "cash_financing", "cash_financing_ttm", "cash_investing", "cash_investing_ttm",
                        "cash_operations", "cash_operations_ttm", "current_ratio", "debt_equity_ratio", "dividend", "dividend_yield", "eps", 
                        "eps_growth", "eps_ttm", "earning_yield", "enterprise_value", "expenses", "expenses_ttm", "free_cash_flow", 
                        "free_cash_flow", "gross_profit_margin", "gross_profit_margin", "interest_expense", "interest_income", "inventories_net",
                        "liabilities", "long_term_debt", "market_cap", "net_income", "net_income_ttm", "net_ppe", "pe_ratio", "peg_ratio", 
                        "price", "price_to_book_value", "ps_ratio", "profit_margin", "r_and_d_expense", "retained_earnings", "retained_earnings_growth",
                        "return_on_assets", "return_on_equity", "revenues", "revenue_growth", "revenues_ttm", "sga_expense", "shareholders_equity",
                        "assets")
    
    def start_gui(self):
        Tk.mainloop()
    
    def pop_out(self):
        pass
        
    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    
    def caps(self, event): # converts the symbol variable to upper case on the fly
        self.symbol.set(self.symbol.get().upper())
        
    def update_graph(self):
        self.grapher = graph_plot(self.symbol.get(), self.metric.get())
        self.grapher.plot_trend_info(self.term.get())
        self.grapher.plot_ychart_info()
        #self.canvas.clear()
        self.canvas.draw()
        self.root.update()
    
    def main_gui(self):
        control_column = 0
        graph_column = 3
        
        explaination = Tk.Label(self.root, text = "This text is only for filler.  Please pay it no attention...")
        explaination.grid(column = control_column, row = 0, columnspan = 3)
        
        symbol_label = Tk.Label(self.root, text = "Stock Symbol:")
        symbol_label.grid(column = control_column, row = 1)
        
        symbol_entry = Entry(self.root, width = 20, textvariable = self.symbol)
        symbol_entry.grid(column = control_column + 1, row = 1)
        symbol_entry.bind("<KeyRelease>", self.caps)
        
        term_label = Tk.Label(self.root, text = "Search Term:")
        term_label.grid(column = control_column, row = 2)
        
        term_entry = Entry(self.root, width = 20, textvariable = self.term)
        term_entry.grid(column = control_column + 1, row = 2)
        
        metric_option = OptionMenu(self.root, self.metric, *self.metrics)
        metric_option.grid(column = control_column, row = 3)
        
        update_button = Tk.Button(master=self.root, text='Graph', command=self.update_graph)
        update_button.grid(row=4, column = control_column)
        
        #creates a frame for the graph, and plops it inside
        #for the 'sunken' asthetics
        graph_frame = Tk.Frame(self.root, borderwidth=5, relief="sunken", width=500, height=500)
        graph_frame.grid(column = graph_column, row=1, columnspan = 6, rowspan = 10)
        self.canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        self.canvas.show()
        graph = self.canvas.get_tk_widget()
        graph.pack()

        #I must create a seperate frame for the graph to live in
        #otherwise it will not show up properlly. 
        control_frame = Tk.Frame(self.root, borderwidth=5, relief="sunken", width=500, height=50)
        control_frame.grid(column = graph_column, row=0, columnspan = 4, sticky = 'ew')
        toolbar = NavigationToolbar2TkAgg(self.canvas,control_frame)
        toolbar.update()

        expand_button = Tk.Button(master=self.root, text = "Expand Graph \n", command = self.pop_out)
        expand_button.grid(row = 0, column = graph_column + 4, columnspan = 2)

        for child in self.root.winfo_children(): child.grid_configure(padx=5, pady=5)

#------------------------------------------------------------------------------------------------------------------------------------------#
#TK GUI Execution
#------------------------------------------------------------------------------------------------------------------------------------------#

main_screen = Tk_gui()
main_screen.main_gui()
main_screen.start_gui()




