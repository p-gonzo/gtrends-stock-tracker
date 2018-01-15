import urllib
from pyGTrends import pyGTrends
import ystockquote
from datetime import date
#my module to convert dates into a numerical string in the YMD format
from date_converter import date_converter

#this will need to be changed as it currently uses my information
connector = pyGTrends("USERNAME","PASSWORD")

today = str(date.today())
today = today.replace('-','')

#prompts the user for a stock and converts it to upper case
#prompt = ">>> "
#print "Stock Symbol?"
#stock_symbol = raw_input(prompt)
#stock_symbol = stock_symbol.upper()

#print "Data type?"
#metric_type = raw_input(prompt)


class ychart_data(object):
    
    #sets up the initial varibles
    #defines the chart type, and sets up the URL
    def __init__(self, symbol, data_type):
        self.url = 'http://ycharts.com/companies/%s/%s' % (symbol, data_type) 
        self.raw_url = urllib.urlopen(self.url).read()
        self.raw_url = self.raw_url.split('\n')

    # gather dates according to their embeded code within the URL
    def date_fetcher(self):
        self.dates = []
        self.date_index = []
        for line in self.raw_url:
            
            #looks for the first sign of a date
            #and removes emptpy spaces on either side
            if """<td class="col1">""" in line:
                date = line.strip(" ")
                
                #ensures it is a date with a simple number check at an index
                #appends the final dates to a list
                #also records the index of each date for finding the related metric
                if line[-6] == "0" or line[-6] == "1" or line[-6] == "2" or line[-6] == "3" or line[-6] == "4" or line[-6] == "5" or line[-6] == "6" or line[-6] == "7" or line[-6] == "8" or line[-6] == "9":  
                    date = date[17:]
                    date = date.strip("</td>")
                    self.dates.append(date)
                    self.date_index.append(self.raw_url.index(line))
                else:
                    pass
            else:
                pass
        
        self.dates =  self.dates[0:35]
        return self.dates
    
    #preps dates for translation by other functions
    def date_modder(self):
        modded_dates = []
        for date in self.dates:
            MDY = date.split(' ')
            month = MDY[0]
            month = month[0:3]
            day = MDY[1]
            day = day.strip(',')
            year = MDY[2]
            value = month + ' ' + day + ' ' + year
            modded_dates.append(value)
        modded_dates = date_converter(modded_dates)
        print len(modded_dates)
        return modded_dates
        
    def metric_fetcher(self):
        self.metric_list = []
        for number in self.date_index:
            metric = (self.raw_url[number + 5])
            metric = metric.strip(" ")
            self.metric_list.append(metric)
        self.metric_list = self.metric_list[0:35]
        return self.metric_list
    
    def metric_modder(self):
        modded_metrics = []
        for metric in self.metric_list:
            
            #convert billions abbr to number
            if metric[-1] == 'B':
                metric = metric.strip('B')
                metric = float(metric)
                metric = metric * 1000000000
                metric = int(metric)
            
            #convert millions abbr to number
            elif metric[-1] == 'M':
                metric = metric.strip('M')
                metric = float(metric)
                metric = metric * 1000000
                metric = int(metric)
            
            #else:
                #metric = int(metric)
            
            modded_metrics.append(metric)
        
        print modded_metrics
        print len(modded_metrics)
        return modded_metrics


        
            


ten_Q = ychart_data("AAPL", "pe_ratio")

ten_Q.date_fetcher()
date_list = ten_Q.date_modder()

print date_list

ten_Q.metric_fetcher()
metrics = ten_Q.metric_modder()

class yahoo_stock_data(object):
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.daily_averages = []
        self.dates = []
        self.date_hash = {}
        day = 0
        raw_list = ystockquote.get_historical_prices(self.symbol, "20040104", today)
        raw_list = raw_list[1:]
        raw_list.reverse()
        
        #creates a two lists:  one for the daily averages, and one for the dates
        while len(raw_list) > day:
            day_number = raw_list[day]
            date = day_number[0]
            date = date.replace('-','')
            high = day_number[2]
            low = day_number[3]
            high = float(high)
            low = float(low)
            daily_average = (high + low)/2
            self.daily_averages.append(daily_average)
            self.dates.append(date)
            day = day + 1
    
    def stock_value(self):
        return self.daily_averages
    
    def dates_list(self):
        return self.dates



class google_data(object):
    
    def __init__(self, search_term):
        self.search_term = search_term
        connector.download_report((self.search_term), geo = "all", scale = 0)
        self.raw_data = connector.csv()
        self.raw_data = self.raw_data.split('\n')
        self.raw_data = self.raw_data[2:]
        self.dates = []
    
    def date_fetcher(self):
        line_number = 0
        while line_number < len(self.raw_data):
            one_line = self.raw_data[line_number]
            one_line = one_line.split(', ')
            data_point = (one_line[0])
            self.dates.append(data_point)
            line_number = line_number + 1
        del self.dates[-1]
        self.dates = date_converter(self.dates)
        print self.dates
        return self.dates
    
    def term_trend(self):
        line_number = 0
        trend_data = []
        while line_number < len(self.raw_data):
            one_line = self.raw_data[line_number]
            one_line = one_line.split(', ')
            data_point = (one_line[1])
            trend_data.append(data_point)
            line_number = line_number + 1
        del trend_data[-1]
        return trend_data
        print terend_data 
            


#some_data = google_data("iphone")
#some_data.date_fetcher()

#y_chart = ychart_data("AAPL", "revenues")
#y_chart.date_fetcher()
#print y_chart.date_modder()
