import datetime
import matplotlib

class date_dict(object):
    
    # initializes the function by defining a start date varialbe, and then breaking it up into Y,M, and D.
    def __init__(self, start_date):
        self.start_date = start_date
        Y = int(self.start_date[:4])
        M = int(self.start_date[4:6])
        D = int(self.start_date[6:8])
        self.base = datetime.datetime(Y,M,D)
        self.base2 = self.base
        
        self.date_list = []
        self.date_dict = {}
    
        #makes a list of dates, from the one given, to today
        while self.base < datetime.datetime.today():
            date_and_time = self.base.isoformat()
            date = date_and_time[:10]
            date = date.replace('-', '')
            self.date_list.append(date)
            self.base += datetime.timedelta(days = 1)
    
   #makes a dictionay from the list with keys returing a numerical conversion of the datetime objects
   #this propperly alligns the information with the dates axis
    def make_dict(self):
        for item in self.date_list:
            self.date_dict[item] = matplotlib.dates.date2num(self.base2)
            self.base2 += datetime.timedelta(days = 1)
        return self.date_dict
        
    def date_alligner(self,date_list):
        new_date_list = []
        for item in date_list:
            new_date_list.append(self.date_dict[item])
        return new_date_list

#some_list = date_dict("20090808")
#print some_list.make_dict()