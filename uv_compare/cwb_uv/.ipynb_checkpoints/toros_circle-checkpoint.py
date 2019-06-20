# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:29:15 2019

@author: apple
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from datetime import datetime,timedelta
from netCDF4 import Dataset
import cmocean as cm

from scipy.stats import pearsonr




from astropy.stats import circcorrcoef
from astropy import units as u


directory='./cor'
if not os.path.exists(directory):
    os.makedirs(directory)


data=Dataset('corspd.nc')
alldata=Dataset('ocm2.cdf')
toros=Dataset('tor2.cdf')




u_ocm=alldata['U_OCM'][:,:,:].data
v_ocm=alldata['V_OCM'][:,:,:].data
dir_ocm=alldata['DIR_OCM'][:,:,:].data
spd_ocm=alldata['SPD_OCM'][:,:,:].data
dir_ocm[dir_ocm==-1.e+34]=np.nan
spd_ocm[spd_ocm==-1.e+34]=np.nan
dir_ocm[dir_ocm==-999]=np.nan
spd_ocm[spd_ocm==-999]=np.nan
u_tor=toros['U_TOR'][:,:,:].data
v_tor=toros['V_TOR'][:,:,:].data
dir_tor=toros['DIR_TOR'][:,:,:].data
spd_tor=toros['SPD_TOR'][:,:,:].data
u_ocm[u_ocm==-1.e+34]=np.nan
v_ocm[v_ocm==-1.e+34]=np.nan
dir_ocm[dir_ocm==-1.e+34]=np.nan
spd_ocm[spd_ocm==-1.e+34]=np.nan
u_tor[u_tor==-999]=np.nan
v_tor[v_tor==-999]=np.nan
dir_tor[dir_tor==-999]=np.nan
spd_tor[spd_tor==-999]=np.nan
u_tor[u_tor==-1.e+34]=np.nan
v_tor[v_tor==-1.e+34]=np.nan
dir_tor[dir_tor==-1.e+34]=np.nan
spd_tor[spd_tor==-1.e+34]=np.nan


lon=data['MX2'][:]
lat=data['MY2'][:]

m=Basemap(projection='merc',llcrnrlat=21,urcrnrlat=27,\
            llcrnrlon=118,urcrnrlon=124) #resolution='h'



time=[0,31,59,90,120,151,181,212,243,273,304,334,362]
month=['01','02','03','04','05','06','07','08','09','10','11','12']
month_name=[]
month_name.append('Jan')
month_name.append('Feb')
month_name.append('Mar')
month_name.append('Apr')
month_name.append('May')
month_name.append('Jun')
month_name.append('Jul')
month_name.append('Aug')
month_name.append('Sep')
month_name.append('Oct')
month_name.append('Nov')
month_name.append('Dec')



def pear_avg_dir(array1,array2,t1,t2):
    a=array1[t1:t2,:,:]
    b=array2[t1:t2,:,:]
    cor=np.zeros((60,49))
    for i in range(60):
        for j in range(49):
            bad = ~np.logical_or(np.isnan(a[:,i,j]), np.isnan(b[:,i,j]))
            x=np.compress(bad, a[:,i,j])
            y=np.compress(bad, b[:,i,j])
            alpha=x*u.deg
            beta=y*u.deg
            cor[i,j]=circcorrcoef(alpha, beta) 
    return cor


def go_circle(ocm,tor,st,name):
    test2=pear_avg_dir(ocm,tor,time[st]*24,time[st+1]*24)
#    test2[test2>=0.7]=1
#    test2[(test2>=0.3) &  (test2<=0.7)]=0.5
#    test2[(test2<=0.3) &  (test2>=0)]=0
#    test2[test2<=-0.7]=-1
#    test2[(test2<=-0.3) &  (test2>=-0.7)]=-0.5
#    test2[(test2>=-0.3) &  (test2<=0)]=0  
    
    fig = plt.figure()
    m=Basemap(projection='merc',llcrnrlat=21,urcrnrlat=27,\
            llcrnrlon=118,urcrnrlon=124) #resolution='h'
    fig.set_size_inches(15, 12, forward=True)
    ax = plt.gca()
    x,y=np.meshgrid(lon,lat)
    x,y=m(x,y)
    cs=m.contourf(x,y,test2,np.linspace(-1,1,41),extend='both',cmap='seismic')
#color bar  pad is distance in colobar to pic
    cbar = m.colorbar(cs, location='right', pad="5%")
#set fontsize in color bar 
    cbar.ax.tick_params(labelsize=20)


    m.readshapefile('shape/ocm2','comarques',linewidth=1.5,drawbounds=True,color='k')    
    
#draw shape
    patches   = []
    for info, shape in zip(m.comarques_info, m.comarques):
        patches.append(Polygon(np.array(shape), True) )

    ax.add_collection(PatchCollection(patches, facecolor= '#AAAAAA', edgecolor='k', linewidths=1., zorder=2))

        
####################       label   ################################################  
      
#make ylabel
    m.drawparallels(np.arange(16,31,2),labels=[1,0,0,0],fontsize=20, linewidth=0.0)
#make xlabel
    m.drawmeridians(np.arange(110,130,2),labels=[0,0,0,1],fontsize=20, linewidth=0.0) 
    plt.xlabel('Longitude',fontsize=20, labelpad=35)
    plt.ylabel('Latitude',fontsize=20,  labelpad=55)  
    plt.title(month[st],fontsize=20)
    plt.savefig(os.path.join(directory,name+'_'+month[st])+'.png')




def pear_avg_spd(array1,array2,t1,t2):
    a=array1[t1:t2,:,:]
    b=array2[t1:t2,:,:]
    cor=np.zeros((60,49))
    for i in range(60):
        for j in range(49):
            bad = ~np.logical_or(np.isnan(a[:,i,j]), np.isnan(b[:,i,j]))
            x=np.compress(bad, a[:,i,j])
            y=np.compress(bad, b[:,i,j])
            cor[i,j]=pearsonr(x,y)[0]
    return cor

def go_spd(ocm,tor,st,name):
    test2=pear_avg_spd(ocm,tor,time[st]*24,time[st+1]*24)
#    test2[test2>=0.7]=1
#    test2[(test2>=0.3) &  (test2<=0.7)]=0.5
#    test2[(test2<=0.3) &  (test2>=0)]=0
#    test2[test2<=-0.7]=-1
#    test2[(test2<=-0.3) &  (test2>=-0.7)]=-0.5
#    test2[(test2>=-0.3) &  (test2<=0)]=0  
    
    fig = plt.figure()
    m=Basemap(projection='merc',llcrnrlat=21,urcrnrlat=27,\
            llcrnrlon=118,urcrnrlon=124) #resolution='h'
    fig.set_size_inches(15, 12, forward=True)
    ax = plt.gca()
    x,y=np.meshgrid(lon,lat)
    x,y=m(x,y)
    cs=m.contourf(x,y,test2,np.linspace(-1,1,41),extend='both',cmap='seismic')
#color bar  pad is distance in colobar to pic
    cbar = m.colorbar(cs, location='right', pad="5%")
#set fontsize in color bar 
    cbar.ax.tick_params(labelsize=20)


    m.readshapefile('shape/ocm2','comarques',linewidth=1.5,drawbounds=True,color='k')    
    
#draw shape
    patches   = []
    for info, shape in zip(m.comarques_info, m.comarques):
        patches.append(Polygon(np.array(shape), True) )

    ax.add_collection(PatchCollection(patches, facecolor= '#AAAAAA', edgecolor='k', linewidths=1., zorder=2))

        
####################       label   ################################################  
      
#make ylabel
    m.drawparallels(np.arange(16,31,2),labels=[1,0,0,0],fontsize=20, linewidth=0.0)
#make xlabel
    m.drawmeridians(np.arange(110,130,2),labels=[0,0,0,1],fontsize=20, linewidth=0.0) 
    plt.xlabel('Longitude',fontsize=20, labelpad=35)
    plt.ylabel('Latitude',fontsize=20,  labelpad=55)  
    plt.title(month[st],fontsize=20)
    plt.savefig(os.path.join(directory,name+'_'+month[st])+'.png')
    
    

for i in range(5):
    go_circle(dir_ocm,dir_tor,i,'dir')
    go_spd(spd_ocm,spd_tor,i,'spd')












