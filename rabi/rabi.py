import sys
import numpy as np
sys.path.append(r'F:\Onedrive\Academic Files\LKB\rabi_fitting')
import data_reader as dr

class RabiFile(dr.logic.DataFile):
    """
    A DataFile but with more scientific oriented functions towards cold atom physics
    
    2 column file, x, y.
    """
    def set_delimeter(self, delimeter):
        self._delimeter = delimeter
    def set_x_y_columns(self, x_column, y_column, **kargs):
        """
        sets the columns of the x and y in the file. first column is the zeroth column (0).
        you can also set ranges of columns by providing x_range = (first_row, last_row) and
        y_range = (first_row, last_row)
        """
        self.x_col = x_column
        self.y_col = y_column
        if "x_range" in kargs:
            self.x_range = kargs.get("x_range")
        if "y_range" in kargs:
            self.y_range = kargs.get("y_range")

    def rabi_peaks_very_coarse(self, x_y_mode = False):
        """
        Data needs to have both peaks in different halfs of the files.
        If x_y_mode true the function returns the peaks not in terms of row number # but in x coordinates. 
        """
        xcol, ycol = 0, 1
        if(hasattr(self, "x_col")):
            xcol, ycol = self.x_col, self.y_col
        else:
            print("WARNING: x and y columns are not set. The program will continue by assuming the 0 column to be x, and the 1st column to be y.")
        x, y = np.loadtxt(self.path(), delimiter=self._delimeter,usecols=(xcol, ycol), unpack=True)
        if(hasattr(self, "x_range")):
            x = x[self.x_range[0]:self.x_range[1]]
        if(hasattr(self, "y_range")):
            y = y[self.y_range[0]:self.y_range[1]]
        #cut the arrays in half:
        x1, x2 = np.array_split(x, 2) #check np.split. As x and y are np.arrays doing x.split is thr same as np.split(x, 2)
        y1, y2 = np.array_split(y, 2)
        max_1=np.argmax(y1)
        max_2=np.argmax(y2) 

        out_max_1 = (max_1, y1[max_1]) if not x_y_mode else (x1[max_1], y1[max_1])
        out_max_2 = (max_2, y2[max_2]) if not x_y_mode else (x2[max_2], y2[max_2])

        return out_max_1, out_max_2


if(__name__ == "__main__"):
    dr.logic.DataFile(r"F:\Onedrive\Academic Files\LKB\rabi_fitting\data\power0009µW_2018-12-18-16.27.44.csv")
    #test of the rabifile:
    rabifile = RabiFile(r"F:\Onedrive\Academic Files\LKB\rabi_fitting\data\power0009µW_2018-12-18-16.27.44.csv")
    rabifile.set_delimeter("\t")
    print(rabifile.rabi_peaks_very_coarse(x_y_mode=True))