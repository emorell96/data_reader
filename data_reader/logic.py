import os
import data_reader.helpers as aux
import sys
#here the file structure is rabi_fitting
#                                    | ---  data_reader
##                                   |----  fitting
#                                       etc
#adapt to your own system. You need to do sys.path.append("path\to\module") so module is the main folder where the package resides.
sys.path.append(r'F:\Onedrive\Academic Files\LKB\rabi_fitting')
import data_reader as dr



#class to read the files and include the info for easy access:
class DataFile:
    filename = ""
    directory = ""
    value = ""
    unit = ""
    datetime = ""
    extension = ""
    prefix = ""
    def __init__(self, fname, folder = "", pattern = "%Y-%m-%d-%H.%M.%S"): #https://docs.python.org/2/library/re.html
        if folder == "": #fname == full folder location
            self.directory, self.filename = os.path.split(fname)
        else:
            self.filename = fname
            self.directory = folder
        #pattern defines the pattern for the date time, the rest is fixed such as [decimal-numbers][unit(a set of non blank characters)]_[DATETIME].[EXTENSION]
        #You could add more advanced patterns in the helpers.py
        self.prefix, self.value, self.unit, self.datetime, self.extension = aux.basic_read_string(fname, pattern)
    def isvalidselection(self, **kargs):
        """
        This function does all the logic behind the filtering decision.
        If takes the key parameters such as 'ext' or 'value' or 'unit' and tells me if those values are matched.
        All the key parameters are treated as AND. (ext = '.csv') AND value = '0800ma' AND unit = 'ma'
        """
        valid = True
        if("ext" in kargs):
            extensions = kargs.get("ext")
            extensions = [x.strip().lower() for x in extensions]
            valid *= (("."+self.extension) in extensions)
        if("value" in kargs):
            values = kargs.get("value")
            values = [x.strip().lower() for x in values]
            valid *= (self.value in values)
        if("unit" in kargs):
            units = kargs.get("unit")
            units = [x.strip().lower() for x in units] #makes sure that the lower or capitalletter wont affect a comparison
            valid *= (self.unit in units) 
        if("prefix" in kargs):
            prefixes = kargs.get("prefix")
            prefixes = [x.strip().lower() for x in prefixes]
            valid *= self.prefix != "" and (self.prefix in prefixes)
        #as you can see you can add many more criteria in a very general way.
        #you just have to define put arg1 = value1 and create the code here to deal
        #with this case. You would write something like 
        # --------------
        #if("arg1" in kargs):
        #   values = kargs.get("values")
        #   #ALL THE LOGIC TO DEAL WITH THE VALUES IF NEEDED
        #   valid *= (self.arg1 in values)
        # ---------------------
        # Now of course, you need to define a way of setting the attribute arg1
        # in the class, as the class doesnt come by default with that value. If for
        # example you wanted to filter by size of the file. You could create
        # a method inside the class which def weighfile(self) which would use os to get
        # the size, and then store it in self.size. Once this is done, you simply do,
        # self.size to get the size (inside of the class), or once outside, when being
        # used by an end user, you could just datafile.size (ofcourse he must have called
        # the weigh function before).
        # so the last line would be now valid *= (self.size in values)
        # Or if the weigh function outputs the size, valid *= (self.weigh() in values)   
        #     

        return valid
    def path(self):
        """
        returns the full path of the file
        """
        return os.path.join(self.directory, self.filename)
    

# class IterDataSet:
#     def __iter__(cls):
#         return iter(cls.DataFiles)

class DataSet:
    #idea: to have a class which contains multiple DataSet and having multiple ways of populating this.
    #you could have multiple DataSet for different values, or a large DataSet with all the measurements of one day.
    #you could include sorting, and attribute listing capabilities (i.e. print all the DataFile.value in the DataSet)
    
    #To store the DataFiles I want to use a list of DataFiles

    #note: the advantage of a class structure is that all of the logic and inner complications are hidden to the end user
    #the user doesn't have to know what a dictionnary is, he will just have to do:
    #DataSet.get_all_by_key("08000ma") or something similar.

    #note: the key will probably have to be a tuple (value, unit, datetime) as to ensure the uniquity of the keys
    #Allows for using it in a for loop, as for datafile in dataset
    
    #list containing all objects
    DataFiles = []
    Note = ""
    '''
    Idea:
        Initializes a DataSet class. The list files is by default empty, as such,
        DataSet() will create an empty DataSet. If instead files is given then depending on the type of the list:
        
        
        If files is a list of DataFiles then the list will replace the empty internal list of DataFiles. You can disable this, and force the constructor to ignore empty filenames by setting ignore_empty_fn = True
        If instead files is just a string, if the filename is empty, then the whole folder will be imported. If not, then only one file will be imported.

        You can set extension = "csv" for example, such as only the files with "csv" as extension will be imported into the DataSet.
        You can also set value = "0800" and only the files with said values will be imported.
        Same for unit = "ma".
        You may also select by year, month, or day, or even hour, such as only the files taken on said year, month year or hour will be imported.

        Finally, all the sorting parameters can be given as a list (e.g. value = ["0800", "0900", "1000"]), it will then import the files with the values listed.
    Problem: Python is not a strongly typed language, as such no idea of what ty
    pes I give in files. And as it is very error prone.
    Solution:

    Use classmethods. Check: https://stackoverflow.com/questions/44765482/multiple-constructors-the-pythonic-way

    '''
    #how to initialize (create) a set by calling DataSet(arguments)
    def __init__(self, _DataFiles = None, type = DataFile, **kargs):
        '''
        Initializes the DataFiles directly. It needs then a list of DataFile.
        DO NOT USE DataSet([path1, path2, ...]) directly instead use the class methods defined below.
        Each class method corresponds to different input parameters.
        '''
        self.DataFiles = list() if _DataFiles == None else _DataFiles
        if "note" in kargs:
            self.Note = kargs.get("note")
    
    @classmethod
    def frompathlist(cls, pathlist, type = DataFile, ignore_empty_fn = False, **kargs):
        """ 
        Add a note by using note = "This is my note" as argument when calling it.
        If files is a list of strings where each string represents a 
        PATH (Folder + filename), then the DataSet will create a DataSet
        based on those files, if the filename in one of the PATHs is ''
        (i.e. empty string) (i.e. PATH = 'C:\\Users\\AtomChips\\Data\\' ) then
        the whole directory while be imported.
        set ignore_empty_fn = True to disable this default behaviour.
        Filter by extensions using ext = ('.csv', '.txt') or ext = '.csv' for example. 
        Filter by value using values = ('0800', '0900') for example.
        Filter by unit using unit = 'ma'.

        Use type to use classes which are derivated from DataFile through inheritance.
        """
        data = []
        for path in pathlist:
            #check if path has filename:
            if dr.VERBOSE_LVL > 1:
                print("Checking if path has a filename.")
                print("Current path is '" + path + "'.")
            directory, filename = os.path.split(path)
            if dr.VERBOSE_LVL > 0:
                print("Current directory is '"+directory+"'.")
                print("Current filename is '"+filename+"'.")
            if filename: #in Python "" == False, so not "" == True.
                #Filename is not empty:
                #use append:
                path = os.path.join(directory, filename)
                cls.__append(path, data, type, **kargs)#we try adding the file. If not succesful, we raise an error.
                    
                continue #move on to the next path.
            #import all files in directory unless ignore_empty_fn = True:
            if ignore_empty_fn:
                continue #move on to the next path in the list WITHOUT executing the rest.
            #continue was not trigerred, so continue:
            #import all documents in directory:
            #iterate through all files in the directory:

            #Python3.6+
            try:
                for entry in os.scandir(directory): #apparently quicker than list dir
                    extensions = kargs.get('ext') if ('ext' in kargs) else ""
                    if entry.path.endswith(extensions):
                        #if kargs["ext"] is empty it's ok, as extensions = "" and all strings end with ""
                        cls.__append(entry.path, data, type, **kargs)
            #python 2 way of scaning a dir
            except:
                #default to the Python 2 way:
                for filename in os.listdir(directory):
                    extensions = kargs.get('ext') if ('ext' in kargs) else ""
                if filename.endswith(extensions):
                        #if kargs["ext"] is empty it's ok, as extensions = "" and all strings end with ""
                        cls.__append(os.path.join(directory, filename), data, type, **kargs)
        if len(data) == 0:
            print("Returning empty DataSet, no file matched your filters.")
        return cls(data, **kargs)
    
    
    #this function is charged of adding a DataFile to the internal list. Here is all the filtering    
    @staticmethod
    def __append(path, prev_list, _type, **kargs):
        """
        The function adds a datafile to the internal list.
        It does the validation, i.e. right extension, value, unit, etc.
        The main reason for its existance is to avoid copy pasting code.
        returns true if succesful, false if not (validation not passed)
        """
        if dr.VERBOSE_LVL > 0:
            print("Adding file '"+path+"'.")
        
        tmpFile = DataFile(path)
        if tmpFile.isvalidselection(**kargs):
            prev_list.append(_type(path))
        else:
            print("-------------------------")
            print("Current file: "+path)
            print("The specified file was not found or it did not match the filtering criteria. Make sure the path is well wirtten or/and expand the filter criteria.")
    def __len__(self):
        return len(self.DataFiles)

    def append(self, dataset):
        return None

    def __iter__(self):
        return iter(self.DataFiles)

    def values(self, **kwargs):
        """
        Gives the values contained in the dataset. By default it gives a value + unit. Such as "0800ma".
        disable it by providing unit = False.
        """
        vals = []
        for file in self:
            if len(vals)== 0:
                vals.append((file.value, file.unit))
                continue
            if not ((file.value, file.unit) in vals):
                vals.append((file.value, file.unit))
                continue
        return vals
    
    def filter(self, **kwargs):
        """
        You can add filter_note = "" which will be used as note on the new DataSet.
        If no filter_note is given, then the note of the old dataset will be used.
        Same filtering idea as in the construction of the object.
        By extension: ext = ('.csv', '.txt')
        By value: value = "0800"
        By unit: unit = "mA"
        Returns NEW dataset. It doesnt modify the old dataset.
        """
        #Clean list
        FilteredDataFiles = []
        #iterate trhough all files:
        for file in self:
            #make sure the current file is a valid file:
            if file.isvalidselection(**kwargs):
                FilteredDataFiles.append(file)
        if len(FilteredDataFiles) == 0:
            print("Warning: New DataSet is empty")
        note = self.Note if not ("filter_note" in kwargs) else kwargs.get("note").strip()
        return DataSet(FilteredDataFiles, note = note)


    


                
                



if (__name__ == '__main__'):
    path = r"F:\Onedrive\Academic Files\LKB\rabi_fitting\data\0800ma_2018-12-19-10.44.36.csv"
    # file = DataFile(path)
    # print(file.directory)
    # print(file.filename)
    # print(file.extension)
    # print(file.value)
    # print(file.unit)
    # print(file.datetime)
    # print(file.isvalidselection(ext = ".csv")) #1
    # print(file.isvalidselection(ext = (".txt", ".csv"))) #1
    # print(file.isvalidselection(value = "0900")) #0
    # print(file.isvalidselection(value = "0800")) #1
    # print(file.isvalidselection(value = "0900", ext = ".csv")) #0
    # print(file.isvalidselection(value = "0800", ext = ".csv")) #1
    # print(file.isvalidselection(value = "0800", ext = ".py")) #0
    # #Test a non empty filename
    # print("--------------------------------------------")
    # print("Testing a non empty filename")
    # files = DataSet.frompathlist([path])
    # file = files.DataFiles[0]
    # print(file.directory)
    # print(file.filename)
    # print(file.extension)
    # print(file.value)
    # print(file.unit)
    # print(file.datetime)
    print("--------------------------------------------")
    print("Testing an empty filename, aka uploading the whole directory")
    directory = r"F:\Onedrive\Academic Files\LKB\rabi_fitting\data\\"
    files = DataSet.frompathlist([directory])
    print(files.values())
    # file = files.DataFiles[0]
    # print(file.directory)
    # print(file.filename)
    # print(file.extension)
    # print(file.value)
    # print(file.unit)
    # print(file.datetime)

    # print("--------------------------------------------")
    # print("Testing a filter by extension")
    # extension = ".csv"
    # files = DataSet.frompathlist([directory], ext = extension)
    # file = files.DataFiles[0]
    # print(file.directory)
    # print(file.filename)
    # print(file.extension)
    # print(file.value)
    # print(file.unit)
    # print(file.datetime)

    print("test iteration through dataset:")
    for file in files:
        print(file.value)
    print(len(files))
