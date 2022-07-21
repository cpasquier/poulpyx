import matplotlib.pyplot as plt
import os
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Tk,DoubleVar,Entry,Button
plt.rcParams.update({'font.size': 16, 'figure.figsize': [12.0, 6.0]})

ponidir = '.'
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

def close_window():       #function to close the window
    gu1.destroy()

gu1 = Tk()      #to get the K value previously determinated
tk.Label(gu1, text="K =").grid(row=0, column=0)
d1 = DoubleVar(gu1)  
e1 = Entry(gu1, textvariable=d1).grid(row=0, column=1)
button1 = tk.Button(text = "OK", command = close_window, width=6, height=2).grid(row=1,column=1, pady=15)
gu1.mainloop()

kset = d1.get()

gu2 = Tk()     #modify rpt file (add K,d)
rptlist = fd.askopenfilenames(parent=gu2, title='Select rpt files', filetypes=[("rpt files", ".rpt")])
gu2.destroy()
for file in rptlist:
    with open(file, 'a') as rpt:
        rpt.write('d = '+str(distance)+'\n')
        rpt.write('k = '+str(kset)+'\n')  
        rpt.close()
