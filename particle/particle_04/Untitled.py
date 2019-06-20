
# coding: utf-8

# In[1]:


import os
os.environ['PROJ_LIB'] = '/opt/conda/share/proj'


# In[187]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.font_manager import FontProperties
import math
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


# In[7]:


data=pd.read_csv('particle.pth',header=None)


# In[108]:


# how many particle
ball=25
#get the run time space
time=int(data[0][1])
# your cpp lon and lat
#lon
rlambda0 = 120.4 
#lat
phi0 =  22.34


# In[109]:


pi=math.pi
rlambda0=rlambda0*pi/180
phi0=phi0*pi/180


# In[110]:


def cpp(ifl,xin,yin,rlambda0,phi0):
    r=6378206.4
    pi=3.1415926
    if(ifl==1):
        xin=xin*pi/180
        yin=yin*pi/180
        xout=r*(xin-rlambda0)*np.cos(phi0)
        yout=yin*r
    elif(ifl==-1):
        xout=rlambda0+xin/r/np.cos(phi0)
        yout=yin/r
        xout=xout/pi*180
        yout=yout/pi*180
    return xout,yout


# In[128]:


all_xy=pd.DataFrame()
for i in range(ball):
    lon=[ float(j.split()[1])  for st,j in enumerate(data[0])  if(st-3)%(ball+1)==i  if(st-3)>=0 ]
    lat=[ float(j.split()[2])  for st,j in enumerate(data[0])  if(st-3)%(ball+1)==i  if(st-3)>=0 ]
#    df=pd.DataFrame({'lon_'+str(i):lon,'lat_'+str(i):lat})
    cpp_lon=[cpp(-1,i,j,rlambda0,phi0)[0]   for i,j in zip(lon,lat)]
    cpp_lat=[cpp(-1,i,j,rlambda0,phi0)[1]   for i,j in zip(lon,lat)]
    all_xy['lon_'+str(i)]=cpp_lon
    all_xy['lat_'+str(i)]=cpp_lat


# In[159]:


import random
def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color


# In[198]:


m=Basemap(projection='merc',llcrnrlat=22.42,urcrnrlat=22.47,            llcrnrlon=120.38,urcrnrlon=120.49) #resolution='h'


# In[201]:


fig = plt.figure()
fig.set_size_inches(12, 8, forward=True)
ax = plt.gca()


for i in range(25):
    x,y=m(all_xy['lon_'+str(i)].values,all_xy['lat_'+str(i)].values)
    m.plot(x,y,color=randomcolor())
    m.plot(x[0],y[0],'k', marker='X')

#read shape file
m.readshapefile('shape/DPB','comarques',linewidth=1.5,drawbounds=True,color='k')      
#draw shape
patches   = []
for info, shape in zip(m.comarques_info, m.comarques):
    patches.append(Polygon(np.array(shape), True) )
ax.add_collection(PatchCollection(patches, facecolor= '#AAAAAA', edgecolor='k', linewidths=1., zorder=2))


# In[202]:


import pandas as pd
import simplekml
from datetime import datetime,timedelta


# In[219]:


date="20190118"  # start date
hr="0"  # start hour
skip=2  # jump buoy
splite=ball # how many buoy


# In[220]:


time=datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(hr))


# In[225]:


kml = simplekml.Kml()
cood=[]
start_hr_index=23
A=False
for j in range(ball):
    for st,i in enumerate(range(int(len(all_xy)))):
        if (st ==(start_hr_index)):
            A=True
            pnt =kml.newpoint(name="First", coords=[(all_xy['lon_'+str(j)][st],all_xy['lat_'+str(j)][st])],description = time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
            pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/A.png'
        elif ((st >(start_hr_index)) & (st%skip==0)):
            pnt =kml.newpoint(name="", coords=[(all_xy['lon_'+str(j)][st],all_xy['lat_'+str(j)][st])],description = time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
        if(A):
            cood.append((all_xy['lon_'+str(j)][st],all_xy['lat_'+str(j)][st]))
        time=time+timedelta(hours=1)

    time=time+timedelta(hours=-1)
    pnt =kml.newpoint(name="", coords=[(all_xy['lon_'+str(j)][st],all_xy['lat_'+str(j)][st])],description = time.strftime("%Y-%m-%d %H:00"))  # lon, lat, optional height
    lin = kml.newlinestring(name="", coords=cood)
    lin.style.linestyle.width= 4  # 10 pixels
    lin.style.linestyle.color = simplekml.Color.yellow
    kml.save("test"+str(j)+".kml")

