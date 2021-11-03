import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import os
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import *
import csv
plt.rcParams.update({'font.size': 16, 'figure.figsize': [12.0, 6.0]})

# File selection
def filesel():
    global tr_file
    root = Tk()
    file_extensions = ['*.txt','*.dat']
    ftypes = [
        ('All files', '*'),
        ('txt and dat files (*.txt, *dat)', file_extensions),
    ]
    tr_file = fd.askopenfile(parent=root, title='Select a file')
    root.destroy()

filesel()

# Opens a window which asks for the experiment number
def close_window():
    gui.destroy()

gui = Tk()
tk.Label(gui, text="Scan number").grid(row=0)
a1 = IntVar()
e1 = tk.Entry(gui, textvariable=a1)
e1.grid(row=0, column=1)
button1 = tk.Button(text = "OK", command = close_window).grid(row=8)
gui.mainloop()
tr_expe_nr = a1.get()

# Scans the experiment data gets the x and transmission values
searchlines = tr_file.readlines()
tr_file.close()

xpos_list = []
tr_list = []
peak_pos = []
i=-1

for line in searchlines:
    i=i+1
    if ("#S "+str(tr_expe_nr)+" ") in line:
        a = line.split()
        b = a[6]          #counts the number of theoretically measured points (input for ascan)
        for j in np.arange(i+14, i+14+int(b)+1, 1):
            if ("#C") in searchlines[j]:      #'#C' means the end of measurement (even if aborted)
                break      #if there are not enough points (aborted), stops before the #C line anyway
            else:
                c = searchlines[j].split()
                xpos_list.append(float(c[0]))
                tr_list.append(float(c[9]))

# Plots the data and enables to click and unclick points on the plot, and numbers them
fig = plt.figure()
ax = fig.subplots()
ax.plot(xpos_list, tr_list, color = 'b')

cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)

coord = []   #list for coordinates
def onclick(event):
    global coord
    x = event.xdata
    y = event.ydata
    flipper=0
    if coord:    #if coord is not an empty list
        for ctuple in coord:
            if (abs(x-ctuple[0]) < 1.0) :   #because coord is a list of tuples:[(x1,y1), (x2,y2)...]
                flipper=flipper+1
                coord.remove(ctuple)
                break
            else:
                flipper=flipper
    else:   #if coord is empty, automatically add the first point
        flipper=flipper

    if flipper==0:
        coord.append((x,y))
        
    # Clear all markers and text (necessary for unclicking procedure)
    for aline in ax.lines:
        aline.set_marker(None)
    for txt in ax.texts:
        txt.set_visible(False)

    # Redraw with updated points
    nb = 0
    for ctuple2 in coord:
        nb = nb+1
        ax.plot(ctuple2[0],ctuple2[1], marker='o', color='r')
        ax.text(ctuple2[0],ctuple2[1]-4000, str(nb), color='r', weight='bold')
    fig.canvas.draw()    #redraw the figure
    
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

xlist = []
tlist = []

for ctuple3 in coord:
    xlist.append(ctuple3[0])
    tlist.append(ctuple3[1])

# Create a window with all samples and fillable boxes (name, time, etc.)
def close_window2():
    gu.destroy()

gu = Tk()

tk.Label(gu, text="Point nr.").grid(row=0, column=0)
tk.Label(gu, text="Name").grid(row=0, column=1)
tk.Label(gu, text="Sample group").grid(row=0, column=2)
tk.Label(gu, text="Meas. type").grid(row=0, column=3)
tk.Label(gu, text="x pos.").grid(row=0, column=4)
tk.Label(gu, text="z pos.").grid(row=0, column=5)
tk.Label(gu, text="Transmission").grid(row=0, column=6)
tk.Label(gu, text="Measurement time").grid(row=0, column=7)
tk.Label(gu, text="Thickness").grid(row=0, column=8)

name_refs = []
time_refs = []
x_refs = []
z_refs = []
number_refs = []
type_refs = []
transm_refs = []
thick_refs = []

for n in np.arange(1,len(coord)+1,1):
    tk.Label(gu, text=str(n)).grid(row=n, column=0)   #point

    s1 = StringVar(gu)  #name
    e1 = Entry(gu, textvariable=s1).grid(row=n, column=1)
    name_refs.append(s1)

    i2 = IntVar(gu)  #measurement number
    e2 = Entry(gu, textvariable=i2).grid(row=n, column=2)
    number_refs.append(i2)

    v3 = StringVar(gu)  #sample subtype
    v3.set("Sample")
    m3 = OptionMenu(gu, v3, "Sample", "Vacuum", "Lupo/PE").grid(row=n, column=3)
    type_refs.append(v3)

    tk.Label(gu, text=str(round(xlist[n-1], 1))).grid(row=n, column=4)  #x-pos
    x_refs.append(round(xlist[n-1], 1))

    d5 = StringVar(gu)  #z-pos (needs to be a string for later)
    e5 = Entry(gu, textvariable=d5).grid(row=n, column=5)
    z_refs.append(d5)

    tk.Label(gu, text=str(int(tlist[n-1]))).grid(row=n, column=6) #transmission
    transm_refs.append(int(tlist[n-1]))

    i7 = IntVar(gu)  #time
    e7 = Entry(gu, textvariable=i7).grid(row=n, column=7)
    time_refs.append(i7)

    d8 = DoubleVar(gu)  #thickness
    e8 = Entry(gu, textvariable=d8).grid(row=n, column=8)
    thick_refs.append(d8)

button2 = tk.Button(text = "OK", command = close_window2).grid(row=20)
gu.mainloop()

def foldersel():
    global pfx
    gu3 = Tk()
    pfx = fd.askdirectory(parent=gu3, title='Select a folder to save data')
    gu3.destroy()

foldersel()

# Create script
runpath = os.path.join(pfx,"run_script.txt")
parampath = os.path.join(pfx,"parameters.csv")
lupopath = os.path.join(pfx,"lupo.txt")
ztest = ''
with open(runpath, 'w') as f:
    f.write('sc'+'\n')
    f.write('\n')
    for n in np.arange(1,len(coord)+1,1):
        type_sample = type_refs[n-1].get()
        if type_sample != "Vacuum":
            time_sample = time_refs[n-1].get()       #### TO-DO: use pandas
            name_sample = name_refs[n-1].get()
            x_sample = x_refs[n-1]
            z_temp = z_refs[n-1].get()  #string
            z_str_list = z_temp.split(',')   #split z_temp in a list of strings using comma sep.
            f.write('umv sax '+str(x_sample)+'\n')
            for z_sample in z_str_list:
                if z_sample != '' and z_sample!= ztest:  #if z is the same or if z-pos field is not filled, we don't write umv saz again
                    f.write('umv saz '+str(z_sample)+'\n')
                if len(z_str_list) > 1:
                    f.write('startacq '+str(time_sample)+' '+str(name_sample)+'_z'+str(z_sample)+'\n')  #puts z value in file name if several
                else:
                    f.write('startacq '+str(time_sample)+' '+str(name_sample)+'\n')
                ztest = z_sample
    f.write('\n'+'sc'+'\n')
    f.write('\n')
f.close()
### TO-DO: input temperature ? (voir comment c'est ecrit)

# Recap everything in one csv file
with open(parampath, 'w', encoding='UTF8') as h:
    writer = csv.writer(h)
    header = ['Name', 'Sample group', 'Type', 'X position', 'Z positions', 'Transmission', 'Time (s)', 'Thickness']
    writer.writerow(header)
    for n in np.arange(0,len(coord),1):
        data = [name_refs[n].get(), number_refs[n].get(), type_refs[n].get(), x_refs[n], z_refs[n].get(), transm_refs[n], 
        time_refs[n].get(), thick_refs[n].get()]
        writer.writerow(data)
h.close()

# Save Lupo info for k calculation later
with open(lupopath, 'w') as p:
    p.write('Type'+'\t'+'Transmission'+'\t'+'Time (s)'+'\n')
    for n in np.arange(0,len(coord),1):
        if type_refs[n].get()=="Lupo/PE":
            num = number_refs[n].get()
            p.write(str(type_refs[n].get())+'\t'+str(transm_refs[n])+'\t'+str(time_refs[n].get())+'\n')
            for m in np.arange(0,len(coord),1):
                if type_refs[m].get()=="Vacuum" and number_refs[m].get()==num:
                    p.write(str(type_refs[m].get())+'\t'+str(transm_refs[m])+'\t'+str(time_refs[m].get())+'\n')
                    break
            break
p.close()