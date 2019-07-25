
# coding: utf-8

# In[9]:


import pandas as pd
from bokeh.io import show, output_file,output_notebook
from bokeh.models import NumeralTickFormatter,ColorBar,LinearColorMapper,BasicTicker,HoverTool
from bokeh.plotting import figure, show
import bokeh.palettes
from bokeh.transform import linear_cmap
from bokeh.tile_providers import get_provider, Vendors


import math
from pyproj import Proj, transform
output_notebook()


# In[22]:


df = pd.read_csv('data/ProgramDebt1415_1516PP.csv',na_values = ['PrivacySuppressed'])
df = df[pd.notnull(df['DEBTMEAN'])]

uni = pd.read_csv('data/hd2017.csv',encoding = "ISO-8859-1")

df['OPEID'] = df['OPEID'].apply(str)
df["OPEID"]=df["OPEID"].apply('{0:0>6}'.format) #pad leading zeros to make 6 digits
uni["OPEID"]=uni["OPEID"].str[:-2] #drop the last two digits which code for branch locations
df["radius"]=(df["COUNT"]/df["COUNT"].max())*100


# In[23]:


df = df.merge(uni,on="OPEID")
# convert to web mercater. long,lat
df["LONGITUD"],df["LATITUDE"] = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), df["LONGITUD"].tolist(),df["LATITUDE"].tolist())


# In[24]:


output_file("InteractiveGeographicChart.html")
tile_provider = get_provider(Vendors.CARTODBPOSITRON)

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("Institute","@INSTNM"),
    ("State","@STABBR"),
    ("Course","@CIPDESC"),
    ("Mean Debt US$", "@DEBTMEAN"),
    ("Count","@COUNT")
])

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-13868734, -7502569), y_range=(3214024, 6467184),
           x_axis_type="mercator", y_axis_type="mercator",plot_width=1200,plot_height=800)
p.tools.append(hover)
p.add_tile(tile_provider)

mapper = LinearColorMapper(palette='RdBu11', low=df["DEBTMEAN"].quantile(q=0.25) ,high=df["DEBTMEAN"].quantile(0.75))


p.circle(x="LONGITUD", y="LATITUDE",line_color={'field': 'DEBTMEAN', 'transform': mapper} ,size="radius", fill_color={'field': 'DEBTMEAN', 'transform': mapper}, fill_alpha=0.8, source=df)

color_bar = ColorBar(color_mapper=mapper,ticker=BasicTicker(desired_num_ticks=11),
                     label_standoff=12, border_line_color=None, location=(0,0))

p.add_layout(color_bar, 'right')
show(p)


# In[5]:


df.iloc[75157]

