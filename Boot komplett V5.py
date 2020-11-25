# Made by Dominik Powell
#-------MODULES--------
#   time
#   serial
#   senseHat
import time
import serial
import math
from sense_hat import SenseHat
#------VARIABLES-------
#   max gps accuracy [int]
#   round GPS decimals
DECIMALROUND=5
#   compass inaccuracy in degrees [+- int]
DEGREEINACCURACY=3
#   aimto angle [int]
aimto=0
#   list of coords [list of lists]
waypoints=[[48.199533, 11.416428], [48.199582, 11.415361]]
#   closeenough [int]
gpsdist=0.000170
mingpacc=12
loopcnt=0
vmax=18
vmin=-10
speeds=[0, 0]
maxserialmessages=3
offsetangle=180
dehnungsfaktor=1.5
GPSPORT="/dev/ttyUSB0"
ARDUINOPORT='/dev/ttyACM1'
#------FUNCTIONS-------
#   get coords from GPS+decode [return coords or false if inaccuracy > maximum acceptance]
def ParseNmea(sentence):
    bits=sentence.split("$")
    lalat=False
    lalon=False
    lautc=False
    gpacs=9999
    for thingy in bits:
        fn=thingy.decode().split(",")
        if fn[0]=="$GNGGA":
            try:
                lat=fn[2]
                long=fn[4]
                if fn[3]=="S":
                    N=-1
                else:
                    N=1
                if fn[5]=="W":
                    E=-1
                else:
                    E=1
                longbd=long[0]+long[1]+long[2]
                longad=long[3:len(long)-1]
                lalon=round((int(longbd)+(float(longad)/60))*N, DECIMALROUND)
                latbd=lat[0]+lat[1]
                latad=lat[2:len(lat)-1]
                lalat=round((int(latbd)+(float(latad)/60))*E, DECIMALROUND)
                lautc=fn[1][0]+fn[1][1]+":"+fn[1][2]+fn[1][3]+":"+fn[1][4]+fn[1][5]
            except:
                print(sentence)
                lalat=False
                lalon=False
        if fn[0]=="$GPACCURACY":
            try:
                gpacs=float(fn[1].split("*")[0])
            except:
                gpacs=99999
        if fn[0]=='$GLGSV':
            pass
        if fn[0]=='$GPGSV':
            pass
        if fn[0]=='$GNRMC':
            pass
        if fn[0]=='$GPGSA':
            pass
        if fn[0]=='$GLGSA':
            pass

    return [lalat, lalon, lautc, gpacs]

#   point to coords [take currentcoords and aimto coords] [return angle for compass]
def anglefromcoords(current, aimat):
    current[1]=dehnungsfaktor*current[1]
    aimat[1]=dehnungsfaktor*aimat[1]
    angle=math.degrees(math.atan(abs(current[1]-aimat[1])/abs(current[0]-aimat[0])))
    if current[0]>aimat[0] and current[1]>aimat[1]:
        angle=angle+180
    if current[0]>aimat[0] and current[1]<aimat[1]:
        angle=180-angle
    if current[0]<aimat[0] and current[1]>aimat[1]:
        angle=360-angle
    if current[0]<aimat[0] and current[1]<aimat[1]:
        angle=angle
    return angle
#   rotate to angle [take aimto angle] [return true if close enough]
def pointtoangle(boat_or, target_or):
    boat_or+=offsetangle
    if boat_or>=360:
        boat_or-=360
    prov_or=target_or-boat_or
    if prov_or>-180 and prov_or<=180:
        turn_or=prov_or
    if prov_or>180:
        turn_or=prov_or-360
    if prov_or<=-180:
        turn_or=prov_or+360
    return turn_or
#tell arduino to go to angle
def talktoino(newspeed, speeds):
    counter=0
    while speeds[0]!=newspeed[0] or speeds[1]!=newspeed[1]:
        if counter<maxserialmessages:
            counter+=1
            if speeds[0]>newspeed[0]:
                serialARDUINO.write(b'1')
                speeds[0]-=1
            if speeds[0]<newspeed[0]:
                serialARDUINO.write(b'2')
                speeds[0]+=1
            if speeds[1]>newspeed[1]:
                serialARDUINO.write(b'3')
                speeds[1]-=1
            if speeds[1]<newspeed[1]:
                serialARDUINO.write(b'4')
                speeds[1]+=1
        else:
            break
    return speeds
#links rechts speed berechnen
def calc_v(deltaangle):
    v=(-vmax/100*abs(deltaangle))+vmax
    if v<0:
        v=0
    pm=(vmax/100*abs(deltaangle))/3
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
    return [round(l), round(r)]
#amicloseenough
def distance(x1, y1, x2, y2):
    y1=dehnungsfaktor*y1
    y2=dehnungsfaktor*y2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
def debugpt(lat, lon, tarlat, tarlon, utc, gpacc, lspeed, rspeed, heading, deltaangle, gpsdist):
    print(str(utc)+16*'-')
    print(str(lat)+'    ,    '+str(lon)+'  ('+str(gpacc)+')')
    print(str(tarlat)+'    ,    '+str(tarlon))
    print('Dist: '+str(gpsdist))
    print("L    R")
    print(str(lspeed)+'    '+str(rspeed))
    print(str(heading)+'  '+str(deltaangle))
    print('\n\n')
    
#------__INIT__--------
#senseHAT
sense = SenseHat()
#   serial gps (115200)
serialGPS=serial.Serial(GPSPORT, 115200, timeout=0.5)
#   serial arduino (9600)
serialARDUINO=serial.Serial(ARDUINOPORT, 9600)
#   recieve Coords from Laptop

#   save coords
serialGPS.write(b'AT+CGNSPWR=1\n')
serialGPS.write(b'AT+CGNSTST=1\n')
#   talk to arduino
#   show boot pic on sensehat
r=[255, 0, 0]
b=[0, 0, 255]
w=[255, 255, 255]
flag=[
    r, b, b, r, r, b, b, r,
    b, r, b, r, r, b, r, b,
    b, b, r, r, r, r, b, b,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    b, b, r, r, r, r, b, b,
    b, r, b, r, r, b, r, b,
    r, b, b, r, r, b, b, r]
sense.set_pixels(flag)
time.sleep(10)
sense.clear()
print("waiting for joystick")
while True:
    if len(sense.stick.get_events())!=0:
        break
sense.show_letter("S")
time.sleep(3)
sense.clear()
print("Waypoints")
for wp in waypoints:
    print(wp)
print(str(vmin)+' '+str(vmax))
print(gpsdist)
print(dehnungsfaktor)
print("getting GPS")
selfpos=ParseNmea(serialGPS.readlines())
print("got GPS")
print(selfpos)

#------MAINLOOP--------
while len(waypoints)>0:
    nextcoords=waypoints[0]
    print("going to "+str(nextcoords[0])+', '+str(nextcoords[1]))
    tardst=distance(nextcoords[0], nextcoords[1], selfpos[0], selfpos[1])
    while tardst>gpsdist:
        tardst=distance(nextcoords[0], nextcoords[1], selfpos[0], selfpos[1])
        loopcnt+=1
        if loopcnt>=4:
            selfnewpos=ParseNmea(serialGPS.readlines())
            loopcnt=0
            debugpt(selfnewpos[0], selfnewpos[1], nextcoords[0], nextcoords[1], selfnewpos[2], selfnewpos[3], motorspeeds[0], motorspeeds[1], self_or, deltaangle, tardst)
            selfpos=selfnewpos
        tar_ang=anglefromcoords([selfpos[0], selfpos[1]], [nextcoords[0], nextcoords[1]])
        self_or=sense.get_orientation()["yaw"]
        deltaangle=pointtoangle(self_or, tar_ang)
        motorspeeds=calc_v(deltaangle)
        if selfpos[3] >= mingpacc:
            motorspeeds=[0, 0]
        speeds=talktoino(motorspeeds, speeds)
        time.sleep(0.2)
    print('reached coords'+str(nextcoords[0])+' '+str(nextcoords[1])+'\n\n')
    waypoints.pop(0)
for f in range(0, 10):
    talktoino([0, 0], speeds)
sense.clear(120, 120, 120)
serialGPS.write(b'AT+CGNSTST=0')
serialGPS.write(b'AT+CGNSPWR=0')
