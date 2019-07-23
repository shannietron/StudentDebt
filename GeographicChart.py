
# coding: utf-8

# In[201]:


import pandas as pd
from bokeh.io import show, output_file,output_notebook
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure, show
import bokeh.palettes
from bokeh.transform import linear_cmap

import math
from pyproj import Proj, transform
output_notebook()


# In[205]:


df = pd.read_csv('data/ProgramDebt1415_1516PP.csv',na_values = ['PrivacySuppressed'])
df = df[pd.notnull(df['DEBTMEAN'])]

uni = pd.read_csv('data/hd2017.csv',encoding = "ISO-8859-1")

df['OPEID'] = df['OPEID'].apply(str)
df["OPEID"]=df["OPEID"].apply('{0:0>6}'.format) #pad leading zeros to make 6 digits
uni["OPEID"]=uni["OPEID"].str[:-2] #drop the last two digits which code for branch locations
df["radius"]=(df["COUNT"]/df["COUNT"].mean())*1000


# In[206]:


df = df.merge(uni,on="OPEID")
# convert to web mercater. long,lat
df["LONGITUD"],df["LATITUDE"] = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), df["LONGITUD"].tolist(),df["LATITUDE"].tolist())


# In[211]:


from bokeh.tile_providers import get_provider, Vendors

tile_provider = get_provider(Vendors.CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-13868734, -7502569), y_range=(3214024, 6467184),
           x_axis_type="mercator", y_axis_type="mercator",plot_width=1200,plot_height=800)
p.add_tile(tile_provider)
mapper = linear_cmap(field_name="DEBTMEAN", palette='Plasma256' ,low=df["DEBTMEAN"].quantile(q=0.25) ,high=df["DEBTMEAN"].quantile(0.75))

p.circle(x="LONGITUD", y="LATITUDE",line_color=mapper ,radius="radius", fill_color=mapper, fill_alpha=0.8, source=df)

show(p)


# In[209]:


df["DEBTMEAN"].quartile()

