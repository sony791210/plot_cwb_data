# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:31:01 2019

@author: apple
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings('ignore')


data=pd.read_csv('RMSE.asc',header=None,sep='\s+')

data[0]=pd.to_datetime(data[0],format='%Y%m%d')

fig = plt.figure()

fig.set_size_inches(8, 4, forward=True)
plt.plot(data[0],data[1])
plt.title('OCM2NEW VS TOROS')
plt.xlabel('MONTH(2019)')
plt.savefig('err.png')