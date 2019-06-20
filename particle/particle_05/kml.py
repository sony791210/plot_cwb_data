# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:02:37 2019

@author: apple
"""

import pandas as pd
import simplekml
from datetime import datetime,timedelta


data=pd.read_csv('particle.track.lonlat',header=None,sep='\s+')


date="20190118"  # start date
hr="06"  # start hour
skip=2  # jump buoy
splite=5 # how many buoy





#mk the time in UTC+0 ~UTC+8
utc_8=datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(hr))
utc_0=utc_8+timedelta(hours=-8)
begin=utc_0.strftime("%Y%m%d")
start_hr_index=int(utc_0.strftime("%H"))-1
starttime=datetime(int(begin[0:4]),int(begin[4:6]),int(begin[6:8]))
time=[]
for i in range(96):
    starttime=starttime+timedelta(hours=1)
    time.append(starttime)
#back to utc+8    
times=[i+timedelta(hours=8) for i in time]



#y=int(str(date)[0:4])
#m=int(str(date)[4:6])
#d=int(str(date)[6:8])
#h=start
#time=datetime(y,m,d,0)




kml = simplekml.Kml()
for j in range(5):
    fol = kml.newfolder(name=str(i)+' Folder')
    cood=[]
    A=False
    time=times[0]
    for st,i in enumerate(range(int(len(data)/splite))):
        sit=st+int(len(data)/splite)*j
        if (st ==(start_hr_index)):
            A=True
            pnt =fol.newpoint(name="First", coords=[(data[0][sit],data[1][sit])],description = 'point is '+str(j)+' \n'+time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
            pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
            pnt.style.labelstyle.scale = 1
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png'
        elif ((st >(start_hr_index)) & (st%skip==0)):
            pnt =fol.newpoint(name="", coords=[(data[0][sit],data[1][sit])],description = 'point is '+str(j)+' \n'+time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
            pnt.style.iconstyle.scale = 0.5
        if(A):
            cood.append((data[0][sit],data[1][sit]))
        time=time+timedelta(hours=1)

    time=time+timedelta(hours=-1)               
    pnt =fol.newpoint(name="", coords=[(data[0][sit],data[1][sit])],description = 'point is '+str(j)+' \n'+time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
    pnt.style.iconstyle.scale = 0.5
    lin = fol.newlinestring(name="", coords=cood)
    lin.style.linestyle.width= 3   # 10 pixels
    if(j ==0):
        lin.style.linestyle.color = simplekml.Color.yellow        
    elif(j==1):
        lin.style.linestyle.color = simplekml.Color.purple
    elif(j==2):
        lin.style.linestyle.color = simplekml.Color.orange   
    elif(j==3):
        lin.style.linestyle.color = simplekml.Color.green   
    elif(j==4):
        lin.style.linestyle.color = simplekml.Color.blue   
    else:
        lin.style.linestyle.color = simplekml.Color.royalblue   
        
kml.save("botanicalgarden.kml")