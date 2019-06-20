# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:06:49 2019

@author: apple
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.font_manager import FontProperties
from datetime import datetime,timedelta
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

data=pd.read_csv('particle.track.lonlat', sep='\s+',header=None)


# define   point=5 runday=20   
# plot jump 20 plot once


points=5
days=4
jump=4


date="20190118"
hr="06"



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
time=[i+timedelta(hours=8) for i in time]



#mk the max lon
lon_max=max(data[0])
lon_min=min(data[0])
lon_diff=(lon_max-lon_min)/6

#mk the max lat
lat_max=max(data[1])
lat_min=min(data[1])
lat_diff=(lat_max-lat_min)/6

#set plot range
max_lon=round(lon_max+lon_diff,2)
min_lon=round(lon_min-lon_diff,2)
max_lat=round(lat_max+lat_diff,2)
min_lat=round(lat_min-lat_diff,2)

#set the plot label
xlab_laeb=[min_lon,round((min_lon+max_lon)/2,2) ,max_lon]
ylab_laeb=[round(min_lat+lat_diff,2),round((min_lat+max_lat)/2,2) ,round(max_lat-lat_diff,2)]


# define lon lat
lon=data[0]
lat=data[1]

xlon=lon
ylat=lat

row_5=len(data)
row=row_5/points
lon_data=pd.DataFrame()
lat_data=pd.DataFrame()
# get 5 point lon lat
for i in range(points):
    lon_data[i]=xlon[0+24*i*days:24*days*(i+1)].reset_index(drop=True)
    lat_data[i]=ylat[0+24*i*days:24*days*(i+1)].reset_index(drop=True)
    
    

m=Basemap(projection='merc',llcrnrlat=min_lat,urcrnrlat=max_lat,\
            llcrnrlon=min_lon,urcrnrlon=max_lon)


# plot all
fig = plt.figure()
fig.set_size_inches(12, 8, forward=True)
ax = plt.gca()

xg,yg=m(lon_data[0].values,lat_data[0].values)
m.plot(xg,yg,'g')

ct=0
bt=0
st=1
out_x=[]
out_y=[]
out_t=[]
for i,j,k in zip(lon_data[0].values,lat_data[0].values,time):
    if(bt>=start_hr_index):
        if(ct==0):  
            xp,yp=m(i,j)
            m.plot(xp,yp,'r', marker='D')
            plt.text(xp, yp, str(st), fontsize=12);
            st=st+1
            out_x.append(i)
            out_y.append(j)
            out_t.append(k)
        ct=ct+1
        if(ct>=jump):
            ct=0
    bt=bt+1
out_x.append(i)
out_y.append(j)
out_t.append(k)

xp,yp=m(i,j)
m.plot(xp,yp,'r', marker='D')
plt.text(xp, yp, str(st), fontsize=12);
    

#make xlabel
m.drawmeridians(xlab_laeb,labels=[0,0,0,1],fontsize=15, linewidth=0.0)
#make ylabel
m.drawparallels(ylab_laeb,labels=[1,0,0,0],fontsize=15, linewidth=0.0)

m.readshapefile('shape/ocm2','comarques',linewidth=1.5,drawbounds=True,color='k')     
#draw shape
patches   = []
for info, shape in zip(m.comarques_info, m.comarques):
    patches.append(Polygon(np.array(shape), True) )
ax.add_collection(PatchCollection(patches, facecolor= '#DDDDDD', edgecolor='k', linewidths=1., zorder=2))

plt.xlabel('Longitude',fontsize=15, labelpad=30)
plt.ylabel('Latitude',fontsize=15 ,  labelpad=100)
plt.title('track  ',fontsize=15,weight='bold')
table=[]
st=1
for i,j,k in zip(out_x,out_y,out_t):
    i="{:.6f}".format(i)
    j="{:.6f}".format(j)
    k=k.strftime("%m/%d %H:00")
    table.append([st,i,j,k])
    st=st+1
table=np.array(table) 
rows=['num','lon','lat','time']
the_table = plt.table(cellText=table,cellLoc='center',
                      colLabels=rows,bbox=(0,-1.2,1,1))

for (row, col), cell in the_table.get_celld().items():
    if (row == 0):
        cell.set_text_props(fontproperties=FontProperties(weight='bold'))
the_table.set_fontsize(14)
plt.savefig('test.png',dpi=150,bbox_inches='tight')

















