import numpy as np

import sys
sys.path.append(r'F:\Onedrive\Academic Files\LKB\rabi_fitting')
import data_reader as dr #new general tool set including DataSet
import rabi.rabi as rb #new RabiFile which is based on DataFile but adds a few extra mor focused functions


directory = r"F:\Onedrive\Academic Files\LKB\rabi_fitting\data\\" #r'D:\Users\atomchips\Desktop\\Cavity_protection_20181206\\2018-12-12\\'
#creation of the datasets which are of interest using data_reader
#data for 0800mA
NAtomsData = dr.logic.DataSet.frompathlist([directory], type = rb.RabiFile, value = ("0800",), unit = ("ma",))
for file in NAtomsData:
    print(file.filename)

