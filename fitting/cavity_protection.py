# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 10:22:51 2018

@author: atomchips/Enrique Morell
"""

import numpy as np
import matplotlib.pyplot as plt
#python3:
import pickle #cPickle is now included in the pickle module. If the C version of pickle (aka cPickle) is available, pickle will automatically use it no need to call cPickle anymore
#pyhton2:
''' try:
    import cPickle
except:
    import pickle
 '''
import sys, os, inspect, time, glob
from scipy.optimize import curve_fit
from scipy.stats import norm
from scipy.special import jv as jv
import csv
import shutil, os

import data_reader as dr
#''''''''LIRE''''''''':
#creation d'un fichier auxiliaire qui a toutes les fonctions qui sont utilles au code mais ne sont pas l'objectif du fichier.
#utiliser from file import function1, function2 permet d'utiliser les fonctions sans ecrire file.function1 mais simplement function1
from helpers import find_maximum
#os.chdir('D:\\Users\\atomchips\\Desktop\\Data_loading_MOT_3')
#basename='D:\\Users\\atomchips\\Desktop\\Data_loading_MOT_3'
from fit_functions import * #l'asterisque veux dire importer tout
plt.close('all')
#Ici c'est pour tout remettre en phase à partir du calcul de la position max de chaque trace     



def group(dataset, start=0, end=98):
    """
    Dataset from the module data_reader.
    It should have been properly filtered using the right filters.
    """
    maxlist_1 = []
    maxlist_2 = []
    for file in dataset:
        x, y = np.loadtxt(file.path, unpack=True)
        x, y = x[start:end], y[start:end]
        x1=x[start:int(end/2)]
        y1=b[start:int(end/2)]
        x2=a[int(end/2):end]
        y2=b[int(end/2):end] #will not work in python 3 as end/2 may be a float
        max_1=np.argmax(y1)
        max_2=np.argmax(y2)
        Max_1=np.append(Max_1, max_1)
        Max_2=np.append(Max_2, max_2)
    
    return Max_1, Max_2
    
    
def group_2(basename,start,end):
    tab_name=find_file(basename,start,end)

    Max=np.array([])
    
    os.chdir(Folder+basename)
    pathlist = os.listdir(Folder+basename)
    for k in range(0,np.size(tab_name)):#goes through all files. Will be replaced by iterating through a dataset
        for i in range(0,np.size(pathlist)):
            #filtering which will be done with a data set
            if pathlist[i][0:16]=='power'+tab_name[k]+pathlist[i][9:11]+'_2018': #14 pathlist[i][0:14]=='2dmot'+tab_name[k]  pathlist[i][0:10]==tab_name[k]
                #this is what really is done to one file.
                a,b=load_data(pathlist[i])
                maxi=np.argmax(b)
        
        Max=np.append(Max, maxi)
        
    
    return Max
                
            
                
    
    
    
    
#☺ça c'est la fonction principale    

def Data_Rabi(basename,start,end):
    plt.close('all')
    #for 2ms
    #slope=1200/0.0002851
    #for 10ms
    slope=1200/0.00155
    os.chdir(Folder+basename)
    pathlist = os.listdir(Folder+basename)
    print(pathlist)
    t=300/16 #all of these outside general functions
    
    splitting=[]
    width_1=[]
    width_2=[]
    Sigma_1=np.array([])
    Sigma_2=np.array([])
    
    depth=[]
   #Ici je cherche tous les fichiers ayant par exemple la meme profondeur de piege
    Natoms= find_file(basename,start,end) #filtering done through data set #list all "prefixes" of the files
    print('Natom est')
    print(Natoms) #creation d'un __str__ done
    Current_mot=[] #selection of mot files
    
    #   
    print('max vaut')
    #Max_1, Max_2=group(basename,start,end)  
    
    
    
    #ici je cherche les max de chaque trace
    #Max=group_2(basename,start,end) #    print Max_2
    #print(Max_1)
    #I feel like this part will have to be implemented in RabiFile.
    for k in range (0,np.size(Natoms)):#np.size(Natoms) #iteration through all files in Natoms preselected in the dataset in the new version
        count=0
        a,b=load_data(pathlist[0]) #outsourced to RabiFile
        
        
        res_x=np.zeros(np.size(a))[0:98] #array with zeros for x
        
        res_y=np.zeros(np.size(b))[0:98] #array with zeros for y
     
        
        depth=np.append(depth,(1600/100)*int(basename[0:2]))
        
        for i in range (0,np.size(pathlist)):


            #filtering done previously or creation of different data sets to handle different files.
            if pathlist[i][0:16]=='power'+Natoms[k]+pathlist[i][9:11]+'_2018': #pathlist[i][0:16]=='power'+Natoms[k]+pathlist[i][9:11]+'_2018' //pathlist[i][0:11]==Natoms[k]+'_2018'// #pathlist[i][0:14]=='2dmot'+Natoms[k]  pathlist[i][0:10]==Natoms[k]
                print(Natoms[k])
                x,y=load_data(pathlist[i])
                x=x[0:98]
                y=y[0:98]
                # fig=plt.figure()
                # plt.plot(x,y)
                # plt.show()
                
                
                #ici je remets tout en phase. Delta c'est la distance en indice entre les max
                #Sivant la valeur de delta, j'ajoute ou je retire des cases
                delta=np.argmax(y)-Max[k]
                if delta>0:
                    y=y[delta:98]
                    tab=np.zeros(delta)
                    y=np.append(y,tab)
                    
                if delta<0:
                
                    tab=np.zeros(-delta)
                    y=np.append(tab,y)
                    y=y[0:98]
                
        
                print('x est')
                print(np.size(x))
                print(np.size(y)) #ALWAYS write print(variable) to ensure compatibiltiy betwwen python 3 and 2
                
                #ici c'est quand j'avais des traces presentant le doublet de Rabi, je coupais le tableau en deux pour calculer dans chaque partie le max
               
                
            #    x1=x[0:98/2]
            #    y1=y[0:98/2]
            #    x2=x[98/2:98]
            #    y2=y[98/2:98]
            #    delta_1=np.argmax(y1)-Max_1[k]
            #    delta_2=np.argmax(y2)-Max_2[k]

           
            #    if delta_1>0:
            #        y1=y1[delta_1:98/2]
            #        tab=np.zeros(delta_1)
            #        y1=np.append(y1,tab)
               
               
               
            #    if delta_1<0:
               
            #        tab=np.zeros(-delta_1)
            #        y1=np.append(tab,y1)
            #        y1=y1[0:184]
               
               
               
            #    if delta_2>0:
            #        y2=y2[delta_2:98/2]
            #        tab=np.zeros(delta_2)
            #        y2=np.append(y2,tab)
               
               
               
            #    if delta_2<0:
               
            #        tab=np.zeros(-delta_2)
            #        y2=np.append(tab,y2)
            #        y2=y2[0:184]
               
            #    Y=np.append(y1,y2)
              
               
            #    X=np.append(x1,x2)
          
                
                
                
                res_x=x
                res_y=res_y+y
                count=count+1
            
        res_x=res_x
       
        res_y=res_y/count
        maxs=find_maximum(res_y)
        print(maxs)
    #    Max=find_maximum(res_y)
    #    print('le max vaut')
    #    print(Max)
    #    print(res_x[Max[2]]-res_x[Max[1]])
    #    fig1=plt.figure()
    #    plt.plot(res_x,res_y)
    #    plt.title(Natoms[k])
    #    plt.show()
      
        
        
        
        ############################################
        #sauver trace remise en phase
        Photon=y[np.argmax(res_y)]
        number_photon=2*2*(Photon/0.0001)
        fig1=plt.figure()
        plt.plot(res_x,res_y)
        plt.title(Natoms[k]+'flux_photon/s='+str(number_photon))
        plt.show()
        os.chdir('D:\\Users\\atomchips\\Desktop\\Cavity_protection_20181206\\curve_20181218\\pic_gauche')
#        np.savetxt(Natoms[k][0:4]+'mv'+basename+'.txt', np.transpose([res_x, res_y]),delimiter='\t',header='\t'.join(['temps','ampltiude']))
        #np.savetxt('data'+Natoms[k][0:4]+'mv'+'.txt', np.transpose([res_x, res_y]),delimiter='\t',header='\t'.join(['temps','ampltiude']))
        fig1.savefig(Natoms[k][0:4]+'uW'+'.png')
        os.chdir(Folder+basename)
#        print(Natoms[k])
        ################################################
        
        
        
        
        
        
        #################################################
        ## Fit reduit en prenant les max locaux et en fitant ces quelques points
        ## Ici je remets en phase, je garde que les max locaux. Ensuite je trace que les max locaux que je fit à l'aide d'une lorentzienne
        
#        datax_1=np.array([])
#        datax_2=np.array([])
#        datay_1=np.array([])
#        datay_2=np.array([])
       
#        Testx_1=res_x[0:184]
#        Testx_2=res_x[184:368]
       
#        Testy_1=res_y[0:184]
#        Testy_2=res_y[184:368]
#        indice_1=find_maximum(Testy_1)
#        indice_2=find_maximum(Testy_2)
#        print(indice_2)
       
#        for i in range (0,np.size(indice_1)):
#            datax_1=np.append(datax_1,Testx_1[indice_1[i]])
#            datay_1=np.append(datay_1,Testy_1[indice_1[i]])
# #            print ('valeur ma est')
# #            print(Testy_1[indice_1[i]])
       
#        for i in range (0,np.size(indice_2)):
#            datax_2=np.append(datax_2,Testx_2[indice_2[i]])
#            datay_2=np.append(datay_2,Testy_2[indice_2[i]])
       
       

#        pp_1=[datay_1[np.argmax(datay_1)],datax_1[np.argmax(datay_1)],datax_1[np.argmax(datay_1)+1]-datax_1[np.argmax(datay_1)-1],0]
#        pp_2=[datay_2[np.argmax(datay_2)],datax_2[np.argmax(datay_2)],datax_1[np.argmax(datay_1)+1]-datax_1[np.argmax(datay_1)-1],0]
#        print (datay_2)
#        ind_1=np.argmax(datay_1)
#        ind_2=np.argmax(datay_2)
#        datay_1=np.delete(datay_1,ind_1)
#        datax_1=np.delete(datax_1,ind_1)
#        datay_2=np.delete(datay_2,ind_2)
#        datax_2=np.delete(datax_2,ind_2)
       
#        poppt2, pcov2 = curve_fit(lorentz, datax_2, datay_2, pp_2)
#        poppt1, pcov1 = curve_fit(lorentz, datax_1, datay_1, pp_1)
#        splitting=np.append(splitting,slope*(poppt2[1]-poppt1[1])/2)
#        #splitting=np.append(splitting,slope*(datax_2[np.argmax(datay_2)]-datax_1[np.argmax(datay_1)])/2)
#        Current_mot=np.append(Current_mot,int(Natoms[k][0:3]))
#        width_1=np.append(width_1, slope*poppt1[2])
#        width_2=np.append(width_2, slope*poppt2[2])
       
       
#        print(datay_2)
#        delta=slope*(datax_2[1]-datax_2[0])
#        print(Natoms[k])
#        print('delta vaut')
#        print(delta)
#        fig=plt.figure()
#        plt.plot(res_x,res_y)
#        plt.plot(datax_1,lorentz(datax_1,*poppt1))
#        plt.plot(datax_2,lorentz(datax_2,*poppt2))
#        plt.title(Natoms[k][0:4]+'mA'+basename)
            
#         ################################################################################################
        
        
        
#         ######### Fit sans prendre les max locaux. Ici c'est le fit normal des traces. Je coupe les données en deux car j'ai une doublet de rabi. Je fitte independamment l'un et l'autre. Je pourrais utliser la double lorentzienne ici mais bon^^
        

#        x_1=res_x[0:184]
#        y_1=res_y[0:184]
#        x_2=res_x[184:368]
#        y_2=res_y[184:368]
      
#        p_1=[y_1[np.argmax(y_1)],x_1[np.argmax(y_1)],0.0001,0]
#        p_2=[y_2[np.argmax(y_2)],x_2[np.argmax(y_2)],0.0001,0]
#        popt1, pcov1 = curve_fit(lorentz, x_1, y_1,p_1)
#        popt2, pcov2 = curve_fit(lorentz, x_2, y_2,p_2)
#        fig=plt.figure()
       
#        plt.plot(res_x,res_y)
#        plt.plot(x_1,lorentz(x_1,*popt1))
#        plt.plot(x_2,lorentz(x_2,*poppt2))
#        plt.title(Natoms[k][0:4]+'mA'+basename)
#        splitting=np.append(splitting,slope*(popt2[1]-popt1[1])/2)
#        Current_mot=np.append(Current_mot,int(Natoms[k][0:4]))
#        width_1=np.append(width_1, slope*popt1[2])
#        width_2=np.append(width_2, slope*popt2[2])
      
        
    return splitting, width_1, Current_mot


def Rabi_point_by_point(basename):
    os.chdir('C:\\homes\\Manip\\Data\\Labview\\2018\\2018-11-11\\'+basename)
    pathlist = os.listdir('C:\\homes\\Manip\\Data\\Labview\\2018\\2018-11-11\\'+basename)


    count=0
    shot=[]
    Moyenne=[]
    for i in range (0,np.size(pathlist)):
        if len(pathlist[i])<33:
            a,b=load_data(pathlist[i])
            Moy=np.average(b)
            shot=np.append(shot, count)
            Moyenne=np.append(Moyenne, Moy)
            count=count+1
        
    
    return shot, Moyenne
    
    


            
        
        
        
    
    
    


              
    
    
#data=os.listdir('D:\\Users\\atomchips\\Desktop\\Cavity_protection_20181206\\2018-12-07')
#
#for i in range(0,np.size(data)):
#    splitting, width_1, width_2,depth, Current_mot=Data_Rabi(data[i])
#    os.chdir('D:\\Users\\atomchips\\Desktop\\Cavity_protection_20181206\\Data_20181207')
#    np.savetxt(data[i]+'.txt', np.transpose([splitting, width_1, width_2,depth, Current_mot]),delimiter='\t',header='\t'.join(['splitting in MHz','width_1 in MHz','width_2 in MHz','depth in uK','Current_mot in mA'])) 
#
#   

    
    





#splitting, width, depth, trap_depth=Data_Rabi()
##plt.plot(trap_depth,width)
#fig2=plt.figure()
##plt.plot(trap_depth,splitting)
#index=np.argsort(trap_depth)
#x=width[index]
#y=splitting[index]
#t=np.sort(trap_depth)
#fig1=plt.figure()
#plt.plot(t,x,'--g')
#plt.ylabel('width of the first peak in MHz')
#plt.xlabel('Trap depth in uK')
#plt.title('Width of the first peak function of the trap depth')
#fig2=plt.figure()
#plt.ylabel('Rabi Splitting in MHz')
#plt.xlabel('Trap depth in uk')
#plt.title('Rabi Splitting function of the trap depth')
#plt.plot(t,y,'--b')
#
#os.chdir('D:\\Users\\atomchips\\Desktop\\Reste_number_toms')
#z_1=zip(t,x)
#np.savetxt('width.txt',z_1, delimiter='\t',newline='\n')
#z_2=zip(t,y)
#np.savetxt('Rabi_splitting.txt',z_2, delimiter='\t',newline='\n')
#with open('width_2.csv', 'w') as f:
#    writer = csv.writer(f, delimiter='\t')
#    writer.writerows(z_1)
#    
#with open('Rabi_splitting_2.csv', 'w') as f:
#    writer = csv.writer(f, delimiter='\t')
#    writer.writerows(z_2)
#


#splitting,width=Data_Rabi_atom()
#current=[1.6,1.4,0.9,0.75,0.65]
#index=np.argsort(current)
#x=width[index]
#y=splitting[index]
#t=np.sort(current)
#fig1=plt.figure()
#ax = plt.subplot(111)
#plt.plot(t[1:5], y[1:5],'--r')
#plt.ylabel('Rabi Splitting in MHz')
#plt.xlabel('current in A of the 2D MOT Coils')
#plt.title('Rabi Splitting function of current of the 2D MOT coils')
#plt.xlim(0.75, None)
#ax.plot(t[1:5], y[1:5], label='300uK trap depth')
#ax.legend()
#fig2=plt.figure()
#ax_2 = plt.subplot(111)
#plt.plot(t[1:5], x[1:5],'--b')
#plt.ylabel('Width in MHz')
#plt.xlabel('current in A of the 2D MOT Coils')
#plt.title('Width function of current of the 2D MOT coils')
#plt.xlim(0.75, None)
#ax_2.plot(t[1:5], x[1:5], label='300uK trap depth')
#ax_2.legend()


#
#
#basename='52mv'
#splitting, width_1, Current_mot=Data_Rabi(basename)
#os.chdir('D:\\Users\\atomchips\\Desktop\\Cavity_protection_20181206\\Data_20181212')
#np.savetxt(basename+'.txt', np.transpose([splitting, width_1, Current_mot]),delimiter='\t',header='\t'.join(['splitting','width_1','Current_mot'])) 
#
#





##os.chdir('D:\\Users\\atomchips\\Desktop\\Reste_number_toms')
#z=zip(t,y)

#with open('Atoms_2.csv', 'w') as f:
#    writer = csv.writer(f, delimiter='\t')
#    writer.writerows(z)
    















