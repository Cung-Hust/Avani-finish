import socket, sys, threading, time
from tkinter import*

#===== GUI =====
gui = Tk()
gui.title('Port scanner')
gui.geometry("400x600+20+20")

#===== Colors =====
m1c = '#00ee00'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground = m1c, activeBackground = fgc, activeForeground = bgc, highlightColor = m1c, highlightBackground = m1c)


#==== Lables ====
L11 = Label(gui, text = "Port Scanner", font = ("Helvetica", 16, 'underline'))
L11.place(x = 16, y = 10)

L21 = Label(gui, text = "Target")
L21.place(x = 16, y = 90)

L22 = Entry(gui, text = "localhost")
L22.place(x = 180, y = 90)
L22.insert(0, "localhost")

L23 = Label(gui, text = "Ports")
L23.place(x = 16, y = 158)

L24 = Entry(gui, text = "1")
L24.place(x = 180, y = 158, width = 95)
L24.insert(0, "1")

L25 = Entry(gui, text = "1024")
L25.place(x = 290, y = 158, width = 95)
L25.insert(0, "1024")

L26 = Label(gui, text = "Results: ")
L26.place(x = 16, y = 220)

L27 = Label(gui, text = "[...]")
L27.place(x = 180, y = 220)

#==== Ports list ====
frame = Frame(gui)
frame.place(x = 16, y = 275, width = 370, heigh = 215)
listbox = Listbox(frame, width = 59, heigh = 6)
listbox.place(x = 0, y = 0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
#==== Start GUI =====
gui.mainloop()