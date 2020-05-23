# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:07:36 2020

@author: atcag
"""

#%% Import Libraries

import pandas as pd
import plotly.graph_objects as go
import sankeyutilities as sankeyutilities

#%%

df_test = pd.read_csv('./examples/data/fakeloandata.csv')

#%%

df_test.head()

#%%

sankey_data_obj = sankeyutilities.sankeybackend(df_groupby=df_test,
                                                columnname_sources='source',
                                                columnname_targets='target',
                                                columnname_weights='rows')


#%%

sankey_data_obj.nodelabels

#%%


fig = go.Figure(data=[go.Sankey(node=sankey_data_obj.dict_nodes,
		                            link=sankey_data_obj.dict_links)])

fig.update_layout(title_text = "", font_size=12)
fig.write_html('./examples/examplesankey_image.html', auto_open=True)

#%%

