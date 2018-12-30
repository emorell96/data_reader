import re
from datetime import datetime
def basic_read_string(str, date_time_patern):
    '''
        Reads and returns the information contained in a string.
        The code supposes that the string is in the following format:
        [decimal-numbers][unit(a set of non blank characters)]_[DATETIME].[EXTENSION]
        The [DATETIME] format is to be provided in the date_time_patern argument.
        The patern needs to follow the syntax used in python. 
        For example YYYY-MM-DD-HH.MM.SS would be %Y-%m-%d-%H.%M.%S
        Check: https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        PS: Stop using python 2.7, upgrade to 3.7 already pls.
    '''
    #use regular expressions to get the value, unit, and datetime and extension
    regex = re.compile(r"(\d+)(\S+)_(\S+)\.([a-z]+)")
    results = []
    try:
        results = list(regex.findall(str)[0])
    except:
        print("The string provided is badly formatted. We couldn't match the pattern on the string. Make sure \
        it follows [decimal-numbers][unit(a set of non blank characters)]_[DATETIME].[EXTENSION]")
        quit()
    results[2] = datetime.strptime(results[2], date_time_patern)
    return results

    
    
if (__name__ == '__main__'):
    print('Executing as standalone script')
    #mettre ici du code pour tester le module
    print(basic_read_string(r"./0800ma_2018-12-19-10.44.36.csv", "%Y-%m-%d-%H.%M.%S"))
