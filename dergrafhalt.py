import tkinter
import math
import time
main=tkinter.Tk()
canv=tkinter.Canvas(main, height=500, width=500)
canv.pack()
vmax=30
def calc_v(deltaangle):
    v=(-vmax/110*abs(deltaangle))+vmax
    if v<0:
        v=0
    pm=1/9*abs(deltaangle)
    if pm>10:
        pm=10
    if deltaangle<0:
        #wir müssen nach links
        l=v-pm
        r=v+pm
    if deltaangle>0:
        #rechts
        l=v+pm
        r=v-pm
    if deltaangle==0:
        l=vmax
        r=vmax
    return [l, r, pm, v]
def create_point(dist, ang, col):
    dist*=8
    x=250+dist*math.cos(math.radians(angle))
    y=250+dist*math.sin(math.radians(angle))
    canv.create_oval(x+2, y+2, x-2, y-2, fill=col)
canv.update()
for angle in range(-180, 180, 1):
    canv.create_rectangle(252, 252, 248, 248, fill='black')
    create_point(calc_v(angle)[0], angle, 'blue')
    create_point(calc_v(angle)[1], angle, 'red')
    create_point(calc_v(angle)[2], angle, 'green')
    create_point(calc_v(angle)[3], angle, 'yellow')
    canv.update()
    time.sleep(0.03)
canv.update()
    
