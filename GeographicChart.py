
# coding: utf-8

# In[64]:


import pandas as pd
from bokeh.io import show, output_file,output_notebook
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
import math
output_notebook()


# In[65]:


df = pd.read_csv('data/ProgramDebt1415_1516PP.csv',na_values = ['PrivacySuppressed'])
uni = pd.read_csv('data/hd2017.csv',encoding = "ISO-8859-1")
df['OPEID'] = df['OPEID'].apply(str)

df["OPEID"]=df["OPEID"].apply('{0:0>6}'.format) #pad leading zeros to make 6 digits
uni["OPEID"]=uni["OPEID"].str[:-2]


# In[71]:


df.merge(uni,on="OPEID")

