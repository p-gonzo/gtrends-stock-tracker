def date_converter(list_of_dates):
    month_number = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03',
                    'Apr' : '04', 'May' : '05', 'Jun' : '06',
                    'Jul' : '07', 'Aug' : '08', 'Sep' : '09',
                    'Oct' : '10', 'Nov' : '11', 'Dec' : '12'} 
    
    day_number = {'1' : '01', '2' : '02', '3' : '03', '4' : '04',
                    '5' : '05', '6' : '06', '7' : '07', '8' : '08',
                    '9' : '09','10' : '10','11' : '11','12' : '12',
                    '13' : '13','14' : '14','15' : '15','16' : '16',
                    '17' : '17','18' : '18','19' : '19','20' : '20',
                    '21' : '21','22' : '22','23' : '23','24' : '24',
                    '25' : '25','26' : '26','27' : '27','28' : '28',
                    '29' : '29','30' : '30','31' : '31','32' : '32'}
    
    new_list_of_dates = []
    
    for date in list_of_dates:
        MDY = date.split(' ')
        
        M = MDY[0]
        M = month_number[M]
        
        D = MDY[1]
        D = day_number[D]
        
        Y = MDY[2]
        
        YMD = Y+M+D
        new_list_of_dates.append(YMD)
    return new_list_of_dates