import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import os
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Tk,IntVar,StringVar,Entry,OptionMenu,DoubleVar
import csv
from datetime import date
plt.rcParams.update({'font.size': 16, 'figure.figsize': [12.0, 6.0]})

# File selection
root = Tk()
tr_file = fd.askopenfile(parent=root, title='Select a lineup file')
root.destroy()

# Opens a window which asks for the experiment number
def close_window():
    gui.destroy()

gui = Tk()
tk.Label(gui, text="Scan number").grid(row=0)
a1 = IntVar()
e1 = tk.Entry(gui, textvariable=a1)
e1.grid(row=0, column=1)
button1 = tk.Button(text = "OK", command = close_window).grid(row=1,pady=10)
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

tr_max = max(tr_list)   #will help for place of numbers
tr_min = min(tr_list)

# Plots the data and enables to click and unclick points on the plot, and numbers them
fig = plt.figure()
ax = fig.subplots()
ax.plot(xpos_list, tr_list, color = 'b')

cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)

coord=[]   #list for coordinates

def onclick(event):
    global coord
    x = event.xdata
    y = event.ydata
    flipper=0
    if coord:    #if coord is not an empty list
        for ctuple in coord:
            if (abs(x-ctuple[0]) < 0.5) :   #because coord is a list of tuples:[(x1,y1), (x2,y2)...]
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
        ax.text(ctuple2[0]-0.4,ctuple2[1]-(tr_max-tr_min)/12, str(nb), color='r', weight='bold')
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
tk.Label(gu, text="Measurement time (s)").grid(row=0, column=7)
tk.Label(gu, text="Thickness (cm)").grid(row=0, column=8)
tk.Label(gu, text="Temperature (°C)").grid(row=0, column=9)

name_refs = []
time_refs = []
x_refs = []
z_refs = []
number_refs = []
type_refs = []
transm_refs = []
thick_refs = []
temp_refs = []

for n in np.arange(1,len(coord)+1,1):
    tk.Label(gu, text=str(n)).grid(row=n, column=0)   #point number

    s1 = StringVar(gu)  #name
    e1 = Entry(gu, textvariable=s1).grid(row=n, column=1, padx=5, pady=2)
    name_refs.append(s1)

    i2 = IntVar(gu)  #measurement number
    e2 = Entry(gu, textvariable=i2).grid(row=n, column=2, padx=5, pady=2)
    number_refs.append(i2)

    v3 = StringVar(gu)  #sample subtype
    v3.set("Sample")
    m3 = OptionMenu(gu, v3, "Sample", "Vacuum", "Lupo/PE").grid(row=n, column=3, padx=5, pady=2)
    type_refs.append(v3)

    tk.Label(gu, text=str(round(xlist[n-1], 1))).grid(row=n, column=4, padx=5, pady=2)  #x-pos
    x_refs.append(round(xlist[n-1], 1))

    d5 = StringVar(gu)  #z-pos (needs to be a string for later)
    e5 = Entry(gu, textvariable=d5).grid(row=n, column=5, padx=5, pady=2)
    z_refs.append(d5)

    tk.Label(gu, text=str(int(tlist[n-1]))).grid(row=n, column=6, padx=5, pady=2) #transmission
    transm_refs.append(int(tlist[n-1]))

    i7 = IntVar(gu)  #time
    e7 = Entry(gu, textvariable=i7).grid(row=n, column=7, padx=5, pady=2)
    time_refs.append(i7)

    d8 = DoubleVar(gu)  #thickness
    e8 = Entry(gu, textvariable=d8).grid(row=n, column=8, padx=5, pady=2)
    thick_refs.append(d8)

    d9 = StringVar(gu)  #temperature
    e9 = Entry(gu, textvariable=d9).grid(row=n, column=9, padx=5, pady=2)
    temp_refs.append(d9)

tk.Label(gu, text="Initials of experimenter").grid(row=len(coord)+1,column=1, pady=15)
d10 = StringVar(gu)
e10 = Entry(gu, textvariable=d10).grid(row=len(coord)+1,column=2, pady=15)
button2 = tk.Button(text = "OK", command = close_window2, width=6, height=2).grid(row=len(coord)+1,column=5, pady=15)
gu.mainloop()

# Select folder to save the generated files
gu3 = Tk()
pfx = fd.askdirectory(parent=gu3, title='Select a folder to save data')
gu3.destroy()

# Get the date of the day for file numbering
today = date.today()
d1 = today.strftime("%y%m%d")

initiales = d10.get()

# Create script
runpath = os.path.join(pfx,str(d1)+'_'+str(initiales)+"_macro.mac")
parampath = os.path.join(pfx,str(d1)+'_'+str(initiales)+"_parameters.csv")
lupopath = os.path.join(pfx,str(d1)+'_'+str(initiales)+"_lupo.txt")
ztest = ''
temptest = ''
heat = False
cool = False
tempreg = False  #checks if the temperature regulation has been used
with open(runpath, 'w') as f:
    f.write('sc'+'\n')
    f.write('\n')
    for n in np.arange(1,len(coord)+1,1):
        type_sample = type_refs[n-1].get()
        if type_sample != "Vacuum":
            time_sample = time_refs[n-1].get()      
            name_sample = name_refs[n-1].get()
            x_sample = x_refs[n-1]
            z_tempor = z_refs[n-1].get()  #string
            z_str_list = z_tempor.split(',')   #split z_temp in a list of strings using comma sep.
            temp_tempor = temp_refs[n-1].get()  #string
            temp_str_list = temp_tempor.split(',')   #split z_temp in a list of strings using comma sep.

            f.write('umv sax '+str(x_sample)+'\n')   #move to x pos.

            for temp_sample in temp_str_list:
                if temp_sample != '' and temp_sample!= temptest:  #if temp is the same or if temp field is not filled, we don't write set_temp again
                    tempreg = True
                    if 40 >= float(temp_sample) >= 10:    #loops for conditions on turning on/off heating and cooling
                        if heat==False:
                            f.write('heat_on'+'\n')
                            heat=True
                        if cool==False:
                            f.write('cool_on'+'\n')
                            cool=True
                    if float(temp_sample) > 40:
                        if heat==False:
                            f.write('heat_on'+'\n')
                            heat=True
                        if cool==True:
                            f.write('cool_off'+'\n')
                            cool = False
                    if float(temp_sample) < 10:
                        if heat==True:
                            f.write('heat_off'+'\n')
                            heat=False
                        if cool==False:
                            f.write('cool_on'+'\n')
                            cool = True
                    sleep_time = 900     #standard 15 min for equilibration
                    f.write('set_temp '+str(temp_sample)+'\n')
                    f.write('sleep('+str(sleep_time)+')'+'\n')
                if len(temp_str_list) > 1:
                    templine = '_T'+str(temp_sample)
                else:
                    templine=''
                temptest = temp_sample

                for z_sample in z_str_list:
                    if z_sample != '' and z_sample!= ztest:  #if z is the same or if z-pos field is not filled, we don't write umv saz again
                        f.write('umv saz '+str(z_sample)+'\n')
                    if len(z_str_list) > 1:
                        acqline ='startacq '+str(time_sample)+' '+str(d1)+'_'+str(initiales)+'_'+str(name_sample)+'_z'+str(z_sample)  #puts z value in file name if several
                    else:
                        acqline = 'startacq '+str(time_sample)+' '+str(d1)+'_'+str(initiales)+'_'+str(name_sample)
                    ztest = z_sample

                    f.write(acqline+templine+'\n')   #start acquisition
    if tempreg==True:
        f.write('\n'+'power_off'+'\n')    #if the temperature regulation has been activated, we shut it down at the end
    f.write('\n'+'camin'+'\n')
    f.write('\n')
f.close()

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
                    p.write(str(type_refs[m].get())+'\t'+str(transm_refs[m])+'\n')
                    break
            break
p.close()
