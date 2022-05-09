import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import os, sys, subprocess
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Tk,IntVar,StringVar,Entry,OptionMenu,DoubleVar,messagebox
import csv
from datetime import date
plt.rcParams.update({'font.size': 16, 'figure.figsize': [12.0, 6.0]})

ponidir = '.' #'/home/mar345/data/LineUp'
if os.path.isdir(ponidir):
    root = Tk()
    ponifile = fd.askopenfile(parent=root, initialdir=ponidir, title='Select a poni file')
    root.destroy()
ponilines = ponifile.readlines()
ponifile.close()
for line in ponilines:
    if "Distance:" in line:
        a = line.split()
        distance = a[1]

gu = Tk()
rptlist = fd.askopenfilenames(parent=gu, title='Select rpt files', filetypes=[("rpt files", ".rpt")])
gu.destroy()
for file in rptlist:
    with open(file, 'a') as rpt:
        rpt.write('d = '+str(distance)+'\n')  
        rpt.close()