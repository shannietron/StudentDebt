
# coding: utf-8

# In[71]:


import pandas as pd
from bokeh.io import show, output_file,output_notebook
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure, show
import math
from pyproj import Proj, transform
output_notebook()


# In[72]:


df = pd.read_csv('data/ProgramDebt1415_1516PP.csv',na_values = ['PrivacySuppressed'])
df = df[pd.notnull(df['DEBTMEAN'])]

uni = pd.read_csv('data/hd2017.csv',encoding = "ISO-8859-1")

df['OPEID'] = df['OPEID'].apply(str)
df["OPEID"]=df["OPEID"].apply('{0:0>6}'.format) #pad leading zeros to make 6 digits
uni["OPEID"]=uni["OPEID"].str[:-2] #drop the last two digits which code for branch locations


# In[73]:


df = df.merge(uni,on="OPEID")
# convert to web mercater. long,lat
df["LONGITUD"],df["LATITUDE"] = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), df["LONGITUD"].tolist(),df["LATITUDE"].tolist())


# In[74]:


from bokeh.tile_providers import get_provider, Vendors

tile_provider = get_provider(Vendors.CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-13868734, -7502569), y_range=(3214024, 6467184),
           x_axis_type="mercator", y_axis_type="mercator",plot_width=1200,plot_height=800)
p.add_tile(tile_provider)
p.circle(x="LONGITUD", y="LATITUDE", size=15, fill_color="blue", fill_alpha=0.8, source=df)

show(p)

