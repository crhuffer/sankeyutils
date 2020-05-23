import pandas as pd

class sankeybackend():

	def __init__(self, df_groupby=None, columnname_sources=None, columnname_targets=None, columnname_weights=None,
				 alpha=0.5,
				 colorlinks=False,
				 colornodes=True,
				 node_pad=10, node_thickess=20, node_line=dict(color='black', width=0.25),
				 node_colors='rgba(120, 120, 120, 0.8)'):


		##TODO: add listofsources as an input data format.
		##TODO: add df_long as an input data format.
		self.df_groupby = df_groupby
		self.columnname_sources = columnname_sources
		self.columnname_targets = columnname_targets
		self.columnname_weights = columnname_weights
		self.alpha = alpha

		self.colorlinks = colorlinks
		self.colornodes = colornodes

		self.node_pad = node_pad
		self.node_thickess = node_thickess
		self.node_line = node_line
		self.node_colors = node_colors

		# if self.colorlinks == 'sources':
		# 	self.getlink_colors()

		if self.colornodes == False and self.node_colors == None:
			self.node_colors = 'rgba(120, 120, 120, 0.8)'
		elif self.colornodes == True:
			self.getnode_colors()



		self.setup_indextonameconversiondicts()

	@property
	def uniquesources(self):
		return sorted(list(self.df_groupby[self.columnname_sources].unique()))

	@property
	def uniquetargets(self):
		return sorted(list(self.df_groupby[self.columnname_targets].unique()))

	@property
	def uniquenodes(self):
		return sorted(list(set(self.uniquesources+self.uniquetargets)))

	@property
	def numberofnodes(self):
		return len(self.uniquenodes)

	def setup_indextonameconversiondicts(self):

		self.dict_indextoname = {}
		self.dict_nametoindex = {}
		for index, node in enumerate(self.uniquenodes):
			self.dict_indextoname[index] = node
			self.dict_nametoindex[node] = index

	@property
	def nodelabels(self):
		return [self.dict_indextoname[index] for index in range(self.numberofnodes)]

	@property
	def dict_links(self):
		self.listofsourceindexes = []
		self.listoftargetindexes = []
		self.listofweightindexes = []

		# we have to index based on position, so enforce that the columns are in the correct order
		for row_index, row in self.df_groupby.iterrows():
			self.listofsourceindexes.append(self.dict_nametoindex[row[self.columnname_sources]])
			self.listoftargetindexes.append(self.dict_nametoindex[row[self.columnname_targets]])

			self.listofweightindexes.append(row[self.columnname_weights])

		temp_dict = {'source': self.listofsourceindexes,
					 'target': self.listoftargetindexes,
					 'value': self.listofweightindexes}

		if self.colorlinks != False:
			self.getlink_colors()
			temp_dict['color'] = self.link_colors

		return temp_dict



	@property
	def dict_nodes(self):
		dict_temp = {'pad': self.node_pad,
					 'thickness': self.node_thickess,
					 'line': self.node_line,
					 'label': self.nodelabels,
					 'color': self.node_colors}

		return dict_temp

	@property
	def colorlist(self):
		colorlist = ["rgba(31, 119, 180, alpha)",
                     "rgba(255, 127, 14, alpha)",
                     "rgba(44, 160, 44, alpha)",
                     "rgba(214, 39, 40, alpha)",
                     "rgba(148, 103, 189, alpha)",
                     "rgba(140, 86, 75, alpha)",
                     "rgba(227, 119, 194, alpha)",
                     "rgba(127, 127, 127, alpha)",
                     "rgba(188, 189, 34, alpha)",
                     "rgba(23, 190, 207, alpha)",
                     "rgba(31, 119, 180, alpha)",
                     "rgba(255, 127, 14, alpha)",
                     "rgba(44, 160, 44, alpha)",
                     "rgba(214, 39, 40, alpha)",
                     "rgba(148, 103, 189, alpha)",
                     "rgba(140, 86, 75, alpha)",
                     "rgba(227, 119, 194, alpha)",
                     "rgba(127, 127, 127, alpha)",
                     "rgba(188, 189, 34, alpha)",
                     "rgba(23, 190, 207, alpha)",
                     "rgba(31, 119, 180, alpha)",
                     "rgba(255, 127, 14, alpha)",
                     "rgba(44, 160, 44, alpha)",
                     "rgba(214, 39, 40, alpha)",
                     "rgba(148, 103, 189, alpha)",
                     "rgba(140, 86, 75, alpha)",
                     "rgba(227, 119, 194, alpha)",
                     "rgba(127, 127, 127, alpha)",
                     "rgba(188, 189, 34, alpha)",
                     "rgba(23, 190, 207, alpha)",
                     "rgba(31, 119, 180, alpha)",
                     "rgba(255, 127, 14, alpha)",
                     "rgba(44, 160, 44, alpha)",
                     "rgba(214, 39, 40, alpha)",
                     "rgba(148, 103, 189, alpha)",
                     "rgba(227, 119, 194, alpha)",
                     "rgba(127, 127, 127, alpha)",
                     "rgba(188, 189, 34, alpha)",
                     "rgba(23, 190, 207, alpha)",
                     "rgba(31, 119, 180, alpha)",
                     "rgba(255, 127, 14, alpha)",
                     "rgba(44, 160, 44, alpha)",
                     "rgba(214, 39, 40, alpha)",
                     "rgba(148, 103, 189, alpha)",
                     "rgba(140, 86, 75, alpha)",
                     "rgba(227, 119, 194, alpha)",
                     "rgba(127, 127, 127, alpha)"]
		return [colorstr.replace('alpha', str(self.alpha)) for colorstr in colorlist]

	def getlink_colors(self):
		if self.colorlinks == 'sources':
			listofindexes = self.listofsourceindexes
			uniquenames = self.uniquesources

		dict_nametocolor = {}
		for index, name in enumerate(uniquenames):
			dict_nametocolor[name] = self.colorlist[index]

		# we have a dict with keys as names and values as color.
		# we need to iterate through the list of link indexes, convert them to names, and pass that to colors.

		self.link_colors = [dict_nametocolor[self.dict_indextoname[index]] for index in listofindexes]

	def getnode_colors(self):
		# grab the first numberofnodes worth of values from the colorlist.
		self.node_colors = self.colorlist[:self.numberofnodes]

	def evalute_ifincomingequalsoutgoing(self, list_internalnodes):
		df_groupby_sources = self.df_groupby.groupby(by=['source']).agg({'rows': 'sum'})
		df_groupby_targets = self.df_groupby.groupby(by=['target']).agg({'rows': 'sum'})


		for internalnode in list_internalnodes:
			count_sources = df_groupby_sources.loc[internalnode, 'rows']
			count_targets = df_groupby_targets.loc[internalnode, 'rows']
			if count_sources == count_targets:
				print('passed: {}, number of rows: {}'.format(internalnode, count_sources))
			else:
				print('failed: {}, number of source rows: {}, number of target rows: {}, difference: {}'.format(internalnode,
					      count_sources, count_targets,
						  count_sources-count_targets))

#%%

if __name__ == '__main__':

	import plotly.graph_objects as go

	df_test = pd.read_csv('./examples/data/fakeloandata.csv')

	# %%

	df_test.head()

	# %%

	sankey_data_obj = sankeybackend(df_groupby=df_test,
									columnname_sources='source',
									columnname_targets='target',
									columnname_weights='rows')

	# %%

	sankey_data_obj.dict_links

	# %%

	sankey_data_obj.nodelabels

	# %%

	fig = go.Figure(data=[go.Sankey(node=sankey_data_obj.dict_nodes,
		                            link=sankey_data_obj.dict_links)
						  ]
					)

	fig.update_layout(title_text="", font_size=12)
	fig.write_html('testsankey_image.html', auto_open=True)

	sankey_data_obj = sankeybackend(df_groupby=df_test,
									columnname_sources='source',
									columnname_targets='target',
									columnname_weights='rows',
									colornodes=False,
									colorlinks='sources')

	sankey_data_obj.dict_links

	fig = go.Figure(data=[go.Sankey(node=sankey_data_obj.dict_nodes,
		                            link=sankey_data_obj.dict_links)
						  ]
					)

	fig.update_layout(title_text="", font_size=12)
	fig.write_html('testsankey_image.html', auto_open=True)

	sankey_data_obj.evalute_ifincomingequalsoutgoing(['folder', 'cond', 'signoff', 'suspense'])


#%%

