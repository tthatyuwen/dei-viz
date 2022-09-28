#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 06:13:43 2022

@author: sabrinashih
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import plotly.plotly as py

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges, LabelSet, Label
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8, Turbo256, all_palettes, viridis, turbo
from bokeh.transform import factor_cmap
from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges
from bokeh.models import Legend, LegendItem
from networkx.algorithms import community

def make_circle_network(df, node_type, node_color_type, node_size_type):
    node_type = 'Practice Subtopic'
    node_color_type = 'Practice Theme'
    node_size_type = 'TVL ID'
    
    nodes_df = df.groupby([node_type,node_color_type])[node_size_type].nunique().reset_index()
    nodes_df.columns = [node_type,node_color_type, node_size_type]
    nodes_df = nodes_df.sort_values(node_color_type).reset_index()
    nodes_df.drop('index', axis=1, inplace=True)
    
    # insert all edges - df of source, target, color is the same, thickness is number of occurrences
    all_pairs = []
    for c in df[node_size_type].unique():
      single_count_df = df[df[node_size_type] == c] 
      for pair in itertools.combinations(single_count_df[node_type].unique(),2):
        all_pairs.append(sorted(pair))
        
    edges_df = pd.DataFrame(all_pairs, columns =['Source', 'Target'])
    edges_df['Count']=1
    edges_df['Weight'] = edges_df.groupby(['Source', 'Target'])['Count'].transform('sum')
    edges_df.drop('Count', axis=1, inplace=True)
    edges_df = edges_df.drop_duplicates()
    edges_df.sort_values('Source').head(30)


    G = nx.Graph()
    G.add_nodes_from(nodes_df[node_type].values)
    for e in range(edges_df.shape[0]):
      G.add_edge(edges_df.iat[e,0], edges_df.iat[e,1], weight= edges_df.iat[e,2], width= math.pow(edges_df.iat[e,2],0.7))
      node_size_adjust_dict = {}
    node_size_dict = {}
    node_color_dict = {}
    number_to_adjust_by = 15
    
    edge_width_dict = {}
    
    node_color_dict = pd.Series(nodes_df.iloc[:,1].values,index=nodes_df.iloc[:,0]).to_dict()
    node_size_dict = pd.Series(nodes_df.iloc[:,2].values,index=nodes_df.iloc[:,0]).to_dict()
    node_size_adjust_dict = pd.Series([1.5*math.pow((x + number_to_adjust_by),0.5) for x in nodes_df.iloc[:,2].values],index=nodes_df.iloc[:,0]).to_dict()
    
    nx.set_node_attributes(G, name='node_size', values=node_size_dict)
    nx.set_node_attributes(G, name='node_size_adjusted', values=node_size_adjust_dict)
    nx.set_node_attributes(G, name='node_color_name', values=node_color_dict)
    
    color_to_color_num = {}
    color_list = turbo(len(set(node_color_dict.values())))
    #color_list = all_palettes['Viridis'][len(set(node_color_dict.values()))]
    for count, ele in enumerate(set(node_color_dict.values())):
      color_to_color_num[ele] = color_list[count]
    
    node_color_hex_dict = {}
    for n in G.nodes:
      node_color_hex_dict[n] = color_to_color_num[node_color_dict[n]]
    nx.set_node_attributes(G, name='node_color_number', values=node_color_hex_dict)
    
    #Choose colors for node and edge highlighting
    node_highlight_color = 'chartreuse'
    edge_highlight_color = 'green'
    
    #Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'node_size_adjusted'
    color_by_this_attribute = 'node_color_number'
    
    #Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    #color_palette = Category20
    
    #Choose a title!
    title = 'title'
    
    #Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
           ("Name", "@index"),
            ("Count", "@node_size"),
            ("Co-occurances", "@node_label") # Jane's Update
    ]
    
    #Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips = HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                x_range=Range1d(-810, 810), y_range=Range1d(-810, 810), title=title, height = 800, width = 800)
    
    #Create a network graph object with spring layout
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(G, nx.circular_layout, scale=500, center=(0,0))
    
    #Set node sizes and colors according to node degree (color as spectrum of color palette)
    #minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    #maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    #network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=linear_cmap(color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color))
    #index_cmap = factor_cmap('node_color', palette=color_palette, factors=sorted(nodes_df.iloc[:, 1].unique()), start=1)
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
    
    #Set node highlight colors
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    
    #Set edge opacity and width
    #weights = [G[u][v][weight] for u,v in G.edges()]
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.03, line_width='width')
    
    #Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width='width')
    
    #Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()
    
    plot.renderers.append(network_graph)
    
    #Add Labels
    x, y = zip(*network_graph.layout_provider.graph_layout.values())
    
    node_labels = list(G.nodes())
    
    # Rotary labels - Jane's updates
    angle_list = []
    align_list = []
    x_offset_list = []
    y_offset_list = []
    
    for item in network_graph.layout_provider.graph_layout.values():
      a, b = item[0], item[1]
      if a > 0 and b > 0:
        angle_list.append(math.degrees(math.atan(b/a)))
      elif a < 0 and b > 0:
        angle_list.append(math.degrees(math.atan(b/a))+180)
      elif a < 0 and b < 0:
        angle_list.append(math.degrees(math.atan(b/a))+180)
      elif a > 0 and b < 0:
        angle_list.append(math.degrees(math.atan(b/a)))
    
    for i in range(len(network_graph.layout_provider.graph_layout)):
      if angle_list[i] < 0:
        align_list.append('left')
        x_offset_list.append(abs(18*math.cos(angle_list[i])))
        y_offset_list.append(-abs(18*math.sin(angle_list[i])))
      if angle_list[i] >= 0 and angle_list[i] < 90:
        align_list.append('left')
        x_offset_list.append(abs(18*math.cos(angle_list[i])))
        y_offset_list.append(abs(18*math.sin(angle_list[i])))
    
      elif angle_list[i] >= 90 and angle_list[i] < 180:
        angle_list[i] += 180 # flip text
        align_list.append('right')
        x_offset_list.append(-abs(18*math.cos(angle_list[i])))
        y_offset_list.append(abs(18*math.sin(angle_list[i])))
    
      elif angle_list[i] >= 180 and angle_list[i] < 270:
        angle_list[i] += 180 # flip text
        align_list.append('right')
        x_offset_list.append(-abs(18*math.cos(angle_list[i])))
        y_offset_list.append(-abs(18*math.sin(angle_list[i])))
      elif angle_list[i] >= 270 and angle_list[i] < 360:
        align_list.append('left')
        x_offset_list.append(abs(18*math.cos(angle_list[i])))
        y_offset_list.append(-abs(18*math.sin(angle_list[i])))
    
    angle_tuple = tuple(angle_list)
    align_tuple = tuple(align_list)
    x_offset_tuple = tuple(x_offset_list)
    y_offset_tuple = tuple(y_offset_list)
    group = tuple(nodes_df['Practice Theme'])
    color = tuple(node_color_hex_dict.values())
    
    source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))], 'angle': angle_tuple, 'align': align_tuple, 'x_offset': x_offset_tuple, 'y_offset': y_offset_tuple, 'group': group ,'color':color})
    
    labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7, text_align='align', angle='angle', angle_units='deg', x_offset='x_offset', y_offset='y_offset')
    # End of Update
    
    
    plot.renderers.append(labels)
    

    unique_url = py.plot_mpl(mpl_fig, filename="my first plotly plot")
    
    return plot