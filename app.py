from sankg_helper import *
#from circle_network import *
from dash import Dash, dcc, html, Input, Output
#import dash_bootstrap_components as dbc
import os
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import string
import math


#%%
tvl_df = pd.read_csv('/Users/aorawancraprayoon/Desktop/7_12-TVLDEI-Visualizations_DF.csv')
ps_df = pd.read_csv('/Users/aorawancraprayoon/Desktop/7_22-ProxyDEI-Visualizations_DF.csv.gz')

#%%
tvl_options = {
    'Practice Subtopic': tvl_df['Practice Subtopic'].unique(),
    'Practice Topic': tvl_df['Practice Topic'].unique(),
    'Practice-Protected Group/DEI Context Category': tvl_df['Practice-DEI Term Category'].unique(),
    'Industry (abbv)': tvl_df['INDUSTRY'].unique(),
    'Country of operation': tvl_df['COUNTRY-Text'].unique(),
    'Indicator Term' : tvl_df['Indicator Term'].unique(),
    'Year': tvl_df['year'].unique(),
    'Practice Theme': tvl_df['Practice Theme'].unique(),
    'Practice Subtopic Sentiment': ['Positive', 'Neutral', 'Negative'],
    'Practice-Protected Group/DEI Context Term': tvl_df['Practice-DEI Term'].unique(),
    'Country of Company': tvl_df['COUNTRY-Company'].unique(),
    'Country of Publication': tvl_df['COUNTRY-Publication'].unique(),
    'Company': tvl_df['Company'].unique(),
    'Publication': tvl_df['Primary Article Source'].unique(),
    'Indicator Category': tvl_df['Indicator Term Category'].unique(),
    'Outcome Subtopic': tvl_df['Outcome Subtopic'].unique(),
    'Outcome Topic': tvl_df['Outcome Topic'].unique(),
    'Outcome Theme': tvl_df['Outcome Theme'].unique(),
    'Outcome-Protected Group/DEI Context Term': tvl_df['Outcome-DEI Term'].unique(),
    'Outcome-Protected Group/DEI Context Category': tvl_df['Outcome-DEI Term Category'].unique(),
    'Outcome Subtopic Sentiment': ['Positive', 'Neutral', 'Negative']
}

ps_options = {
    'Practice Subtopic': ps_df['Practice Subtopic'].unique(),
    'Practice Topic': ps_df['Practice Topic'].unique(),
    'Practice-Protected Group/DEI Context Category': ps_df['Practice-DEI Term Category'].unique(),
    'Industry (abbv)': ps_df['INDUSTRY'].unique(),
    'Country of operation': ps_df['COUNTRY-Text'].unique(),
    'Indicator Term' : ps_df['Indicator Term'].unique(),
    'Year': ps_df['year'].unique(),
    'Practice Theme': ps_df['Practice Theme'].unique(),
    'Practice Subtopic Sentiment': ['Positive', 'Neutral', 'Negative'],
    'Practice-Protected Group/DEI Context Term': ps_df['Practice-DEI Term'].unique(),
    'Company': ps_df['company_name'].unique(),
    'Indicator Category': ps_df['Indicator Term Category'].unique(),
    'Outcome Subtopic': ps_df['Outcome Subtopic'].unique(),
    'Outcome Topic': ps_df['Outcome Topic'].unique(),
    'Outcome Theme': ps_df['Outcome Theme'].unique(),
    'Outcome-Protected Group/DEI Context Term': ps_df['Outcome-DEI Term'].unique(),
    'Outcome-Protected Group/DEI Context Category': ps_df['Outcome-DEI Term Category'].unique(),
    'Outcome Subtopic Sentiment': ['Positive', 'Neutral', 'Negative']
}
#%%
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
'''
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
'''

app = Dash(__name__, external_stylesheets=external_stylesheets, title='Rights CoLab - Dashboard', update_title='Loading...')
#app = Dash(external_stylesheets = [dcc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

#%%

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src='/assets/rights colab logo blue.png', className="header-logo"),
                #html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="DEI Data Visualization Dashboard", className="header-title"
                ),
                html.P(
                    children="Interactive data visualizations to inform metrics formation.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                
                # Sankey Diagram Header
                html.Div(
                    children=[
                        html.H1(children="Multi-feature Sankey Diagram", className="graph-header-title"),
                        html.P(
                            children="description",
                            className="graph-header-description",
                        ),
                    ],
                    className="graph-header",
                ),
                
                html.Div([
                    html.Div(
                        children=[
                            html.Div(children="Step 1a: Choose a dataset ", className="menu-title"),
                            
                            dcc.Dropdown(['TVL News Articles', 'Proxy Statements'],
                                           value = 'TVL News Articles',
                                           className="dropdown",
                                           id='cc-dataset',
                                           ),
                            html.Div(children="Step 1b: Choose your number of features ", className="menu-title"),
                            dcc.Slider(3, 5, value=3, step = 1, id='cc-dim'),
                            html.Hr(),
                            html.Div(children="Step 2a: Choose the feature of your focus ", className="menu-title"),
                            
                            dcc.Dropdown(#list(all_options.keys()),
                                           value = 'Practice-Protected Group/DEI Context Category',
                                           clearable=True,
                                           searchable=True,
                                           className="dropdown",
                                           id='cc-00',
                                           ),
                            
                            html.Div(children="Step 2b: Choose your focus ", className="menu-title"),
                            dcc.Dropdown(id='cc-01',
                                 value='age',
                                 clearable=True,
                                 searchable=True,
                                 className="dropdown",
                                 ),
                            
                            html.Hr(),
                            
                            html.Div(children="Step 3: Choose your 2nd feature", className="menu-title"),
                            dcc.Dropdown(
                                id="cc-1",
                                #options=[
                                #    {"label": f, "value": f}
                                #    for f in list(all_options.keys())
                                #],
                                value="Practice Subtopic",
                                clearable=True,
                                searchable=True,
                                className="dropdown",
                            ),
                            
                            html.Div(children="Step 4: Choose your 3rd feature", className="menu-title"),
                            dcc.Dropdown(
                                id="cc-2",
                                #options=[
                                #    {"label": f, "value": f}
                                #    for f in list(all_options.keys())
                                #],
                                value="Country of operation",
                                clearable=True,
                                searchable=True,
                                className="dropdown",
                            ),
                            
                            html.Div(children="Step 4: Choose your 4th feature", className="menu-title", style= {'display': 'none'}, id = 'cc-3-head'),
                            dcc.Dropdown(
                                id="cc-3",
                                #options=[
                                #    {"label": f, "value": f}
                                #    for f in list(all_options.keys())
                                #],
                                value="Industry (abbv)",
                                clearable=True,
                                searchable=True,
                                className="dropdown",
                                style= {'display': 'none'}
                            ),
                            
                            html.Div(children="Step 4: Choose your 5th feature", className="menu-title", style= {'display': 'none'}, id = 'cc-4-head'),
                            dcc.Dropdown(
                                id="cc-4",
                                #options=[
                                #    {"label": f, "value": f}
                                #    for f in list(all_options.keys())
                                #],
                                value='Outcome Subtopic',
                                clearable=True,
                                searchable=True,
                                className="dropdown",
                                style= {'display': 'none'}
                            ),
                            
                            html.Hr(),
                            
                            html.Div(children="Step 5: Choose by counts of articles/documents or counts of companies", className="menu-title"),
                            dcc.RadioItems(#['Article', 'Company'],
                                           value = 'Company', id = 'count-by', inline=True)
            
                            
                        ], style = {'padding':30, 'flex': 1}),
                    html.Div(
                        children=[
                            html.Div(dcc.Graph(id="sankey-diagram")#, style={"height": 400, 'width': 1000}
                                     )
                            ], style = {'padding':10, "height": 400, 'width': 1000}
                        ),
                    #html.Div(dbc.Alert("Note that all chosen features must be different for the diagram to be updated to reflect your selections.", color="info")),
                    html.Hr(),
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                
                html.Div(
                        children=[

                    html.Div(children="Step 6a: Display the top __% of the 2nd feature only", className="menu-title"),
                    #dcc.Slider(, min=0, step=1),
                    
                    dcc.Slider(10, 100, value=40, step = 10, id='top-1',
                        marks={
                            10: {'label': '10%'},
                            20: {'label': '20%'},
                            30: {'label': '30%'},
                            40: {'label': '40%'},
                            50: {'label': '50%'},
                            60: {'label': '60%'},
                            70: {'label': '70%'},
                            80: {'label': '80%'},
                            90: {'label': '90%'},
                            100: {'label': '100%','style': {'font-weight': 'bold'}}
                        }
                    ),
                                
                    html.Div(children="Step 6b: Display the top __% of the 3rd feature only", className="menu-title"),
                    #dcc.Slider(id='top-3', min=0, step=1),
                    dcc.Slider(10, 100, value=100, step = 10, id='top-2',
                        marks={
                            10: {'label': '10%'},
                            20: {'label': '20%'},
                            30: {'label': '30%'},
                            40: {'label': '40%'},
                            50: {'label': '50%'},
                            60: {'label': '60%'},
                            70: {'label': '70%'},
                            80: {'label': '80%'},
                            90: {'label': '90%'},
                            100: {'label': '100%','style': {'font-weight': 'bold'}}
                        }
                    ),
                    
                    html.Div(id='top-3-show', children=[
                        html.Div(children="Step 6c: Display the top __% of the 4th feature only", className="menu-title"),
                        dcc.Slider(10, 100, value=50, id='top-3', step = 10,
                            marks={
                                10: {'label': '10%'},
                                20: {'label': '20%'},
                                30: {'label': '30%'},
                                40: {'label': '40%'},
                                50: {'label': '50%'},
                                60: {'label': '60%'},
                                70: {'label': '70%'},
                                80: {'label': '80%'},
                                90: {'label': '90%'},
                                100: {'label': '100%','style': {'font-weight': 'bold'}}
                        })], style= {'display': 'none'}
                    ),
                    
                    
                    
                    html.Div(id='top-4-show', children= [ 
                        html.Div(children="Step 6d: Display the top __% of the 5th feature only", className="menu-title"),
                        dcc.Slider(10, 100, value=50, id='top-4', step = 10, 
                            marks={
                                10: {'label': '10%'},
                                20: {'label': '20%'},
                                30: {'label': '30%'},
                                40: {'label': '40%'},
                                50: {'label': '50%'},
                                60: {'label': '60%'},
                                70: {'label': '70%'},
                                80: {'label': '80%'},
                                90: {'label': '90%'},
                                100: {'label': '100%','style': {'font-weight': 'bold'}}
                        })], style= {'display': 'none'}
                    ) 
                
                ], style = {'padding':30, 'flex': 1})
                #html.Hr(),
            
                #html.Hr(),
            
                #html.Div(id='display-selected-values')
            ],
            className="sankey-card",

        ),
        '''
        html.Div(
            children=[
                
                # Sankey Diagram Header
                html.Div(
                    children=[
                        html.H1(children="Inter-feature Circle Diagram", className="graph-header-title"),
                        html.P(
                            children="description",
                            className="graph-header-description",
                        ),
                    ],
                    className="graph-header",
                ),
                
                html.Div([
                    html.Div(
                        children=[
                            html.Div(children="Step 1: Choose a dataset ", className="menu-title"),
                            
                            dcc.Dropdown(['TVL News Articles', 'Proxy Statements'],
                                           value = 'TVL News Articles',
                                           className="dropdown",
                                           id='cc-dataset-circle',
                                           ),
                            html.Div(children="Step 2: Choose your feature ", className="menu-title"),
                            
                            dcc.Dropdown(['Practice Subtopic', 'Outcome Subtopic', 'Practice-Protected Group/DEI Context Term', 'Outcome-Protected Group/DEI Context Term'],
                                           value = 'Practice Subtopic',
                                           clearable=True,
                                           searchable=True,
                                           className="dropdown",
                                           id='circle-choice',
                                           ),
                            
                            html.Div(children="Step 3: Choose by counts of articles/documents or counts of companies", className="menu-title"),
                            dcc.RadioItems(#['Article', 'Company'],
                                           value = 'Company', id = 'count-by-circle', inline=True)
            
                            
                        ], style = {'padding':30, 'flex': 1}),
                    html.Div(
                        children=[
                            html.Div(dcc.Graph(id="circle-diagram")#, style={"height": 400, 'width': 1000}
                                     )
                            ], style = {'padding':10, "height": 900, 'width': 900}
                        ),
                    #html.Div(dbc.Alert("Note that all chosen features must be different for the diagram to be updated to reflect your selections.", color="info")),
                    html.Hr(),
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                
            ],
            className="sankey-card",

        ),
        '''
        
    ],
    
    #className="menu",
)

@app.callback(
   Output(component_id='top-3-show', component_property='style'),
   Output(component_id='top-4-show', component_property='style'),
   Output(component_id='cc-3', component_property='style'),
   Output(component_id='cc-4', component_property='style'),
   Output(component_id='cc-3-head', component_property='style'),
   Output(component_id='cc-4-head', component_property='style'),
   Input(component_id='cc-dim', component_property='value'))
def show_hide_element(dim):
    if dim == 3:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'},{'display': 'none'}, {'display': 'none'},{'display': 'none'}#, 'Practice Subtopic', 'flexible work', "Practice-Protected Group/DEI Context Category", "Country of operation", 'Practice Theme', 'Industry (abbv)'
    elif dim == 4:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}#, 'Practice-Protected Group/DEI Context Category', 'migrant', 'Industry (abbv)', 'Practice Theme', 'Country of operation', 'Year'
    elif dim == 5:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}#, 'Year', 2022, 'Industry (abbv)', 'Practice-Protected Group/DEI Context Category', 'Practice Subtopic', 'Indicator Term'
   
@app.callback(
    Output('cc-00', 'options'),
    Output('cc-1', 'options'),
    Output('cc-2', 'options'),
    Output('cc-3', 'options'),
    Output('cc-4', 'options'),
    Output('count-by', 'options'),
    Input('cc-dataset', 'value'))
def set_dataset_options(dataset):
    if dataset == 'TVL News Articles':
        drop_options = [{"label": f, "value": f} for f in list(tvl_options.keys())]
        count_options = ['Article', 'Company']
    elif dataset == 'Proxy Statements':
        drop_options = [{"label": f, "value": f} for f in list(ps_options.keys())]
        count_options = ['Proxy Statement', 'Company']
    return drop_options, drop_options, drop_options, drop_options, drop_options, count_options

'''
@app.callback(
    Output('cc-00', 'value'),
    Input('cc-00', 'options'))
def set_choice(choice):
    return choice[19]['value'] #migrant
'''

@app.callback(
    Output('cc-01', 'options'),
    Input('cc-dataset', 'value'),
    Input('cc-00', 'value'))
def set_choice_options(dataset, choice):
    if dataset == 'TVL News Articles':
        return [{'label': i, 'value': i} for i in tvl_options[choice]]
    elif dataset == 'Proxy Statements':
        return [{'label': i, 'value': i} for i in ps_options[choice]]

@app.callback(
    Output('cc-01', 'value'),
    Input('cc-01', 'options'))
def set_choice(choice):
    return choice[19]['value'] #migrant

@app.callback(
    Output("sankey-diagram", "figure"),
    Input("cc-dataset", "value"),
    Input("cc-dim", "value"),
    Input("cc-00", "value"),
    Input("cc-01", "value"),
    Input("cc-1", "value"),
    Input("cc-2", "value"),
    Input("cc-3", "value"),
    Input("cc-4", "value"),
    Input("count-by", "value"),
    Input("top-1", "value"),
    Input("top-2", "value"),
    Input("top-3", "value"),
    Input("top-4", "value"))
def update_sankg(dataset, dim, dt_0, dim_choice, dt_1, dt_2, dt_3, dt_4, count_by_choice, top_percent_1, top_percent_2, top_percent_3, top_percent_4):
    
    labels, source_1, target_1, value_1, dt_list, dataset_dict = update_sankg_helper(dataset, tvl_df, ps_df, tvl_options, ps_options, dim, dt_0, dim_choice, dt_1, dt_2, dt_3, dt_4, count_by_choice, top_percent_1, top_percent_2, top_percent_3, top_percent_4)
    
    nodes_list = []
    highlight_color_list = []
    other_position = []
    normal_color_node = 'blue'
    normal_color_link = 'rgba(0,0,0,0.1)' 
    
    highlight_list = make_highlight_list(nodes_list, highlight_color_list, other_position)
    
    sankg = make_sankey(labels, source_1, target_1, value_1, dt_list, dataset_dict, highlight_list, normal_color_node, normal_color_link)
    
    return sankg

@app.callback(
    Output('count-by-cirlce', 'options'),
    Input('cc-dataset-circle', 'value'))
def set_dataset_options_circle(dataset):
    if dataset == 'TVL News Articles':
        count_options = ['Article', 'Company']
    elif dataset == 'Proxy Statements':
        count_options = ['Proxy Statement', 'Company']
    return count_options
'''
@app.callback(
    Output("circle-diagram", "figure"),
    Input("cc-dataset-circle", "value"),
    Input("circle-choice", "value"),
    Input("count-by-circle", "value"))
def update_circlex(dataset, choice, count_by_choice):
    if choice == 'Practice Subtopic':
        color_by = 'Practice Theme'
    elif choice == 'Outcome Subtopic': 
        color_by = 'Outcome Theme'
    elif choice == 'Practice-Protected Group/DEI Context Term': 
        color_by = 'Practice-Protected Group/DEI Context Category'
    elif choice == 'Outcome-Protected Group/DEI Context Term':
        color_by = 'Outcome-Protected Group/DEI Context Category'
        
    if dataset == 'TVL News Articles':
        combo_df = tvl_df
        if count_by_choice == 'Company':
            count_by = 'TVL ID'
        elif count_by_choice == 'Article':
            count_by = 'Primary Article Bullet Points'
    elif dataset =='Proxy Statements':
        combo_df = ps_df
        if count_by_choice == 'Company':
          count_by = 'company_name'
        elif count_by_choice == 'Proxy Statement':
          count_by = 'label'
    
    fig = make_circle_network(combo_df, client_back_map[choice], client_back_map[color_by], count_by)
    return fig
'''
if __name__ == '__main__':
    app.run_server(debug=True)



