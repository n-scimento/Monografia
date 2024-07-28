"""
import sys         
sys.path.append('D:/projects/base/app/modules') 

see more at https://realpython.com/python-import/ or https://www.geeksforgeeks.org/python-import-module-outside-directory/
"""
import os

folder_name = 'Py'
for root, dirs, files in os.walk(os.getcwd()):
    if folder_name in dirs:
        new_path = os.path.join(root, folder_name)
        os.chdir(new_path)
        
import pandas as pd 
from bmf import real, nominal, update

