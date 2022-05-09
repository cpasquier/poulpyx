import matplotlib.pyplot as plt
import os
import tkinter.filedialog as fd
from tkinter import Tk
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
