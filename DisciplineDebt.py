
# coding: utf-8

# In[1]:


import pandas as pd
from bokeh.io import show, output_file,output_notebook
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
import math
output_notebook()


# In[2]:


df = pd.read_csv('data/ProgramDebt1415_1516PP.csv',na_values = ['PrivacySuppressed'])
df = df[pd.notnull(df['DEBTMEAN'])]


# In[3]:


n = 30 # plot the largest n disciplines
p = figure(x_range=meanDebt['CIPDESC'].head(n),title="Top {} Disciplines By Their Average Student Debt in 2015/16 ".format(n))
p.vbar(x='CIPDESC', top='DEBTMEAN', source=meanDebt.head(n), width=0.7)

p.xaxis.major_label_orientation =  math.pi/3
p.left[0].formatter.use_scientific = False
p.yaxis[0].formatter = NumeralTickFormatter(format="$000,.")

p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.05

p.ygrid.band_fill_alpha = 0.1
p.ygrid.band_fill_color = "navy"
p.min_border_left = 80
show(p)


# In[ ]:


df = pd.read_csv('data/ProgramDebt1516_1617PP.csv',na_values = ['PrivacySuppressed'])
df = df[pd.notnull(df['DEBTMEAN'])]

meanDebt = df.groupby('CIPDESC')['DEBTMEAN'].mean().reset_index()
meanDebt = meanDebt.sort_values('DEBTMEAN',ascending=False)
cipdesc=df['CIPDESC'].unique()


# In[ ]:


n = 30 # plot the largest n disciplines
p = figure(x_range=meanDebt['CIPDESC'].head(n),title="Top {} Disciplines By Their Average Student Debt in 2016/17 ".format(n))
p.vbar(x='CIPDESC', top='DEBTMEAN', source=meanDebt.head(n), width=0.7)

p.xaxis.major_label_orientation =  math.pi/3
p.left[0].formatter.use_scientific = False
p.yaxis[0].formatter = NumeralTickFormatter(format="$000,.")

p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.05

p.ygrid.band_fill_alpha = 0.1
p.ygrid.band_fill_color = "navy"
p.min_border_left = 80
show(p)

