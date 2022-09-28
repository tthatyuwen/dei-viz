#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 00:04:27 2022

@author: sabrinashih
"""
import math
import plotly.graph_objects as go

client_back_map = {
    'Practice Subtopic': 'Practice Subtopic',
    'Practice Topic': 'Practice Topic',
    'Practice-Protected Group/DEI Context Category': 'Practice-DEI Term Category',
    'Industry (abbv)': 'INDUSTRY',
    'Country of operation': 'COUNTRY-Text',
    'Indicator Term' : 'Indicator Term',
    'Year': 'year',
    'Practice Theme': 'Practice Theme',
    'Practice Subtopic Sentiment': 'Practice Term Sentiment Score',
    'Practice-Protected Group/DEI Context Term': 'Practice-DEI Term',
    'Country of Company': 'COUNTRY-Company',
    'Country of Publication': 'COUNTRY-Publication',
    'Company': 'Company',
    'Publication': 'Primary Article Source',
    'Indicator Category': 'Indicator Term Category',
    'Outcome Subtopic': 'Outcome Subtopic',
    'Outcome Topic': 'Outcome Topic',
    'Outcome Theme': 'Outcome Theme',
    'Outcome-Protected Group/DEI Context Term': 'Outcome-DEI Term',
    'Outcome-Protected Group/DEI Context Category': 'Outcome-DEI Term Category',
    'Outcome Subtopic Sentiment': 'Outcome Term Sentiment Score'
}

def subchoice_by_one(df, count_by):
  column_choice = df.shape[1]-3

  new_df = df.copy()
  new_df['Total'] = new_df.groupby([new_df.columns[i] for i in range(column_choice+1)])[count_by].transform('sum')
  new_df.drop(count_by, axis=1, inplace=True)
  new_df.rename(columns={new_df.columns[new_df.shape[1]-1]:count_by}, inplace=True)
  new_df.drop(new_df.columns[new_df.shape[1]-2], axis=1, inplace=True)
  new_df = new_df.drop_duplicates(subset=[new_df.columns[i] for i in range(new_df.shape[1]-1)])
  new_df = new_df.sort_values(count_by, ascending=False)

  return new_df

def get_unique_N(iterable, N):
    """Yields (in order) the first N unique elements of iterable. 
    Might yield less if data too short."""
    seen = set()
    for e in iterable:
        if e in seen:
            continue
        seen.add(e)
        yield e
        if len(seen) == N:
            return


def top_percent_filter(df, top_percent, count_by):

    # Make consolidated df
    val_df = df.copy()
    val_df['Total'] = val_df.groupby([df.columns[df.shape[1]-3],df.columns[df.shape[1]-2]])[count_by].transform('sum')
    val_df.drop(count_by, axis=1, inplace=True)
    val_df.rename(columns={val_df.columns[val_df.shape[1]-1]:count_by}, inplace=True)
    val_df.drop([val_df.columns[c] for c in range(df.shape[1]-3)], axis=1, inplace=True)
    val_df = val_df.drop_duplicates()
    val_df = val_df.sort_values(count_by, ascending=False)
    
    # Filter consolidated df
    max = len(set(val_df.iloc[:,1].values))
    top_filter=int(math.ceil(max/10) * (top_percent/10))

    keep_woo  = list(get_unique_N(val_df.iloc[:,1].values, top_filter))
    make_other  = [option for option in set(val_df.iloc[:,1].values) if option not in keep_woo]
    d = {**{o: 'Other' for o in make_other}, **{k: k for k in keep_woo}}
    val_df.iloc[:, 1] = val_df.iloc[:, 1].map(d)
    graph_df = val_df

    graph_df['Total'] = graph_df.groupby([graph_df.columns[0], graph_df.columns[1]])[graph_df.columns[2]].transform('sum')
    graph_df.drop(count_by, axis=1, inplace=True)
    graph_df.rename(columns={graph_df.columns[2]:count_by}, inplace=True)
    graph_df = graph_df.drop_duplicates(subset=[graph_df.columns[0], graph_df.columns[1]])

    return graph_df

def rename_source_other(df_prior, df_post, count_by):
  keep_woo = [v for v in df_prior.iloc[:, 1].values if v != 'Other']
  make_other = [option for option in df_post.iloc[:, df_post.shape[1]-3].values if option not in keep_woo]
  d = {**{o: 'Other' for o in make_other}, **{k: k for k in keep_woo}}
  df_post.iloc[:, df_post.shape[1]-3] = df_post.iloc[:, df_post.shape[1]-3].map(d)

  df_post['Total'] = df_post.groupby([df_post.columns[0], df_post.columns[1]])[df_post.columns[2]].transform('sum')
  df_post.drop(count_by, axis=1, inplace=True)
  df_post.rename(columns={df_post.columns[2]:count_by}, inplace=True)
  df_post = df_post.drop_duplicates()
  
  return df_post

def update_sankg_helper(dataset, tvl_df, ps_df, tvl_options, ps_options, dim, dt_0, dim_choice, dt_1, dt_2, dt_3, dt_4, count_by_choice, top_percent_1, top_percent_2, top_percent_3, top_percent_4):
    
    full_dt_list = [dt_0, dt_1, dt_2, dt_3, dt_4]
    dt_list = full_dt_list[:dim]
    
    if dataset == 'TVL News Articles':
        combo_df = tvl_df
        dataset_dict = tvl_options
        if count_by_choice == 'Company':
            count_by = 'TVL ID'
        elif count_by_choice == 'Article':
            count_by = 'Primary Article Bullet Points'
    elif dataset =='Proxy Statements':
        combo_df = ps_df
        dataset_dict = ps_options
        if count_by_choice == 'Company':
          count_by = 'company_name'
        elif count_by_choice == 'Proxy Statement':
          count_by = 'label'


    full_percent_list = [top_percent_1,top_percent_2,top_percent_3,top_percent_4]
    top_percent_list = full_percent_list[:dim-1]
    
    
    dim_type = [client_back_map[d] for d in dt_list]
    keep = [dim_choice,'\''+str(dim_choice)+'\'']
    
    # Set initial dataframes of counts
    filtered_df_0 = combo_df.groupby(dim_type)[count_by].nunique().reset_index()

    # Create sub-dataframes by level
    choice_full_df = filtered_df_0.loc[filtered_df_0[dim_type[0]].isin(keep)]
    choice_full_df  = choice_full_df.sort_values(count_by, ascending=False)
    
    sub_df_list = [choice_full_df]
    input_df = choice_full_df
    for i in range(dim-2):
      input_df = subchoice_by_one(input_df, count_by)
      sub_df_list.append(input_df)
    
    sub_df_list.reverse()
    filtered_dfs = []
    for j in range(len(top_percent_list)):
      filtered_dfs.append(top_percent_filter(sub_df_list[j], top_percent_list[j], count_by))

    other_filterd_dfs = []
    for f in range(len(filtered_dfs)):
      if f != 0:
        other_filterd_dfs.append(rename_source_other(filtered_dfs[f-1], filtered_dfs[f], count_by))
      else:
        other_filterd_dfs.append(filtered_dfs[f])
    
    # Initializations for graph
    source_1 = []
    target_1 = []
    value_1 = []
    
    category_unique_list = []
    category_unique_list.append(filtered_dfs[0][dim_type[0]].unique())
    
    for f in other_filterd_dfs:
      category_unique_list.append(f.iloc[:,1].unique())
      
    for d in range(len(other_filterd_dfs)):
      source_offset = sum([len(category_unique_list[e]) for e in range(d)])
      target_offset = sum([len(category_unique_list[e]) for e in range(d+1)])
      for i in range(other_filterd_dfs[d].shape[0]):
        source_1.append(list(category_unique_list[d]).index(other_filterd_dfs[d].iat[i, 0]) + source_offset)
        target_1.append(list(category_unique_list[d+1]).index(other_filterd_dfs[d].iat[i, 1])+ target_offset)
        value_1.append(other_filterd_dfs[d].iat[i, 2])

    labels = [c_i for c in category_unique_list for c_i in c]
    
    return labels, source_1, target_1, value_1, dt_list, dataset_dict


def make_node_colors(normal_color_node, highlight_list, labels):
  colors = [normal_color_node]*len(labels) # adjust based on how many nodes
  
  for n in highlight_list:
    if n[0] == 'Other':
      index_other_list = [i for i in range(len(labels)) if labels[i] == 'Other']
      position = index_other_list[n[2]-1]
    else:
      position = labels.index(n[0])

    colors[position] = n[1]
  return colors

def make_link_colors(normal_color_link, highlight_list, labels, value_1, source_1, target_1):
  colors = [normal_color_link]*len(value_1) # adjust based on how many links
  
  for n in highlight_list:
    if n[0] == 'Other':
      index_other_list = [i for i in range(len(labels)) if labels[i] == 'Other']
      position = index_other_list[n[2]-1]
    else:
      position = labels.index(n[0])
    
    pos_source = None
    pos_target = None

    pos_source = [i for i, x in enumerate(source_1) if x == position]
    pos_target = [i for i, x in enumerate(target_1) if x == position]

    for index in pos_source:
      colors[index] = n[1]

    for index in pos_target:
      colors[index] = n[1]

  return colors

def get_flow_summaries(labels, dt_list, dataset_dict, source_1, target_1):
  all_str = []
  for item_idx in range(len(labels)):
    position = item_idx
    item = labels[item_idx]
    #last_item_cat_idx = -1
    #index_other_list = [i for i in range(len(labels)) if labels[i] == 'Other']

    string = ""
    if item in dataset_dict[dt_list[0]]:
      
        #string = "(%s)<br />" %dt_list[0]
        string = "<br />"
        targets = [labels[target_1[i]] for i, x in enumerate(source_1) if x == position]
        #string = string + "From: None<br />" + "To " + dt_list[1] + " (" + str(len(targets)) + "): "+ ', \n'.join(targets)
        string = string + "From: N/A<br />" + "To: " + str(len(targets))
        #last_item_cat_idx = 0
    elif item in dataset_dict[dt_list[len(dt_list)-1]]:
        string = "<br />"
        #string = "(%s)<br />" %dt_list[len(dt_list)-1]
        sources = [labels[source_1[i]] for i, x in enumerate(target_1) if x == position]
        #string = string #+ "From " + dt_list[len(dt_list)-2] + " (" + str(len(sources)) +"): "+', \n'.join(sources) + "<br />To: None"
        string = string + "From: " + str(len(sources)) + "<br />To: N/A"
        #last_item_cat_idx = len(dt_list)-1
    elif item == 'Other':
        #index_pos = index_other_list.index(position)
        string = "<br />"
        targets = [labels[target_1[i]] for i, x in enumerate(source_1) if x == position] # enumerate through source_1 and find where the source is diverse
        sources = [labels[source_1[i]] for i, x in enumerate(target_1) if x == position]
        #string = string + "From " + dt_list[index_pos] +" (" + str(len(sources)) + "): " + ', \n'.join(sources) + "<br />" + "To " + dt_list[index_pos+2] +" (" + str(len(targets)) + "): " +', \n'.join(targets)
        string = string + "From: " + str(len(sources)) + "<br />" + "To: "+ str(len(targets))
    else:
        for d in range(1,len(dt_list)-1):
            if item in dataset_dict[dt_list[d]]:
              string = "<br />"
              #string = "(%s)<br />" %dt_list[d]
              targets = [labels[target_1[i]] for i, x in enumerate(source_1) if x == position] # enumerate through source_1 and find where the source is diverse
              sources = [labels[source_1[i]] for i, x in enumerate(target_1) if x == position]
              #string = string #+ "From " + dt_list[d-1] +" (" + str(len(sources)) + "): " + ', \n'.join(sources) + "<br />" + "To " + dt_list[d+1] +" (" + str(len(targets)) + "): " +', \n'.join(targets)
              string = string + "From: "  + str(len(sources)) + "<br />" + "To: "  + str(len(targets))
              #last_item_cat_idx = d
    all_str.append(string)
  return all_str

def make_highlight_list(nodes_list, highlight_color_list, other_position):
  highlight_list = []
  for i in range(len(nodes_list)):
    highlight_list.append([nodes_list[i], highlight_color_list[i], other_position[i]])
  return highlight_list

def make_sankey(labels, source_1, target_1, value_1, dt_list, dataset_dict, highlight_list, normal_color_node, normal_color_link):
  fig = go.Figure(data=[go.Sankey(
      node = dict(
        pad = 50,
        thickness = 10,
        line = dict(color = "black", width = 0.5),
        label = labels,
        color = make_node_colors(normal_color_node, highlight_list, labels), # make_node_color(highlight_node, normal_color, highlight_color)
        customdata = get_flow_summaries(labels, dt_list, dataset_dict, source_1, target_1),
        hovertemplate = '%{label} %{customdata}'
      ),
      link = dict(
        source = source_1, # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = target_1,
        value = value_1,
        # Jane edit
        color = make_link_colors(normal_color_link, highlight_list, labels, value_1, source_1, target_1),
        #color = make_link_color(highlight_node, 'rgba(0,0,0,0.2)', 'limegreen'), # make_node_color(highlight_node, normal_color, highlight_color)
        #hovertemplate = "[Article/Company] counts of: <br />"
        #+ "Practice Subtopic: 'hiring/recruitment' <br />"
        #+ get_category("'hiring/recruitment'") + "%{source.label}"
      ),
      )])
  fig.update_layout(height=900)
  return fig