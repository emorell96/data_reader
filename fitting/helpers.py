import numpy as np
import os

def find_maximum(tab):
    dim=np.size(tab)
    indice=np.array([])
    for i in range (1,dim-1):
        if tab[i]>tab[i-1] and tab[i]>tab[i+1] and tab[i]>4:
            indice=np.append(indice, i)
        
    return indice

def load_data(filename):

    a=np.genfromtxt(filename,delimiter='\t')
    x=a[:,0]
    y=a[:,1]
    return x,y
    
# Ici find_file me permet de sortir les noms de chzque fichier de donnée. Par exemple si j'ai pris des données à differentes valeurs de courant. ça va juste me sortir chaque valeur de courant. Ensuite j'utilise ces valeurs de courant pour 
    #pour appeler uniquement les données de chaque courant (il peur y avoir plusieurs traces à meme courant pour moyenner)

#TODO:modify to avoid depending on the path of installation https://stackoverflow.com/questions/44977227/how-to-configure-main-py-init-py-and-setup-py-for-a-basic-package
import sys
sys.path.append(r'F:\Onedrive\Academic Files\LKB\rabi_fitting')
#sys.path.append(r'F:\Onedrive\Academic Files\LKB\rabi_fitting')
from fitting import VERBOSE_LVL   #permet l'acces aux constantes


def find_file(root,start,end, folder = 'D:\\Users\\atomchips\\Desktop\\Cavity_protection_20181206\\2018-12-12\\'): #folder est mqintenant un argument optionel
    '''
        This function is deprecated use the class which reads the files and provides all the info contained in the files
    '''
    
    os.chdir(folder+root)
    filenames = os.listdir(folder+root) #use variable with meaning, list could be anything, filenames is obviously a list with filenames in it.
    if(VERBOSE_LVL > 0): #prints only if the user wants it
        print(filenames)
    #dim_list=np.size(list) #not used??
    filenames_filtered=[]
    #goes through all the files in the list gotten
    for i in range (0,np.size(filenames)-1): #pourquoi le dernier fichier est ignore?
        if filenames[i][start:end] != filenames[i+1][start:end]:
            filenames_filtered=np.append(filenames_filtered,filenames[i][start:end])
    filenames_filtered=np.append(filenames_filtered,filenames[np.size(filenames)-1][start:end])
    return filenames_filtered
#function which takes a pattern and gives the strings in those placeholders
    
    

        


if (__name__ == '__main__'):
    print('Executing as standalone script')
    #mettre ici du code pour tester le module