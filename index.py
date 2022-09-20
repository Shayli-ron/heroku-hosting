from distutils.log import debug
from gc import callbacks
from inspect import trace
from time import strftime
from timeit import main
from turtle import color
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input , Output, State
import plotly.graph_objs as go
import pandas as pd
import datetime
import numpy as np



#Preper data:

#read the file
data = pd.read_csv('PLTK_Revenue_Download - Sheet 1 (1).csv')
#convert to 1 date column 
df = data.set_index('Grouping').T
#preper before replacing 
df[df.columns] = df[df.columns].fillna(0)
df[df.columns] = df[df.columns].astype(str)
#replacing the ','
cols = ['1v1.LOL', 'Best Fiends', 'Best Fiends Stars', 'Bingo Blitz',
       'Board Kings', 'Caesars Slots', 'House of Fun', "June's Journey",
       'JustBuild.LOL', 'JustFall.LOL', "Pearl's Peril", "Pirate Kings",
       'Poker Heat', 'Redecor', 'Slotomania', 'Solitaire Grand Harvest',
       'Switchcraft', 'Tropicats', 'Vegas Downtown Slots & Words',
       'World Series of Poker']
for col in cols:
    df[col] = df[col].str.replace(',','')
df['sum_products'] = df['sum_products'].str.replace(',','')

df[df.columns] = df[df.columns].astype(int)

df['sum_products'] = df['sum_products'] * 1.2
# Converting the index as date
df.index = pd.to_datetime(df.index)
# df = df.T


traces = []
for col in cols:
    traces.append(go.Bar(
                    x= df.index,
                    y = df[col],
                    name=col))


#Read Revenue file
rev_data = pd.read_csv('PLTK REVENUE(Q) - גיליון1 (1).csv')
rev_data['Date'] = pd.to_datetime(rev_data['Date'])


traces.append(go.Scatter(
                    x= rev_data['Date'],
                    y = rev_data['Revenue'],
                    name='Overall_Revenue',
                    mode = 'markers+lines',
                    line=dict(width = 3,color = '#FF00FF')
                    ))
traces.append(go.Scatter(
                    x= df.index,
                    y = df['sum_products'],
                    name='Overall_Products',
                    mode = 'markers+lines',
                    line=dict(width = 1,color = '#7882f5')
                    ))


#Check Correlation
# corr_df = rev_data.join(df)
rev_data['Date_index'] = rev_data['Date']
rev_data = rev_data.set_index('Date')
corr_df = pd.merge(rev_data, df, left_index=True, right_index=True)
# print("corrrrrrr")
# print(corr_df)




#read year over year revenue
revenue_YoverY = pd.read_csv('PLTK - Y_Y - Sheet 1.csv')
revenue_YoverY = revenue_YoverY.set_index('Grouping').T
cols = ['1v1.LOL', 'Best Fiends', 'Best Fiends Stars', 'Bingo Blitz',
       'Board Kings', 'Caesars Slots', 'House of Fun', "June's Journey",
       'JustBuild.LOL', 'JustFall.LOL', "Pearl's Peril", "Pirate Kings",
       'Poker Heat', 'Redecor', 'Slotomania', 'Solitaire Grand Harvest',
       'Switchcraft', 'Tropicats', 'Vegas Downtown Slots & Words',
       'World Series of Poker']
revenue_YoverY[revenue_YoverY.columns] = revenue_YoverY[revenue_YoverY.columns].fillna(0)
revenue_YoverY = revenue_YoverY*100

for col in cols:
    revenue_YoverY[col] = revenue_YoverY[col].replace(0,np.nan)

revenue_YoverY.index = pd.to_datetime(revenue_YoverY.index)

rev_perc_traces = []
for col in cols:
    rev_perc_traces.append(go.Bar(
                    x= revenue_YoverY.index,
                    y = revenue_YoverY[col],
                    name=col
    ))

#Read Users file:
users_data = pd.read_excel('Users_ Industry.xlsx')
#Preper Users file:
users_df = users_data.set_index('Publisher').T
users_df.index = pd.to_datetime(users_df.index)
users_df['Playtika'] = users_df['Playtika'].astype(float)
users_df['YoY'] = users_df['YoY'].astype(float)*100


#Read users per product file  - value
users_product_value = pd.read_csv('Users per Product - value - Sheet 1.csv')
users_product_value = users_product_value.fillna(0)
users_product_value = users_product_value.set_index('Game').T
users_product_value.index = pd.to_datetime(users_product_value.index)
cols  = ['1v1.LOL', 'Best Fiends', 'Best Fiends Stars', 'Bingo Blitz',
       'Board Kings', 'Caesars Slots', 'House of Fun', "June's Journey",
       'JustBuild.LOL', 'JustFall.LOL', "Pearl's Peril", 'Pirate Kings',
       'Poker Heat', 'Redecor', 'Slotomania', 'Solitaire Grand Harvest',
       'Switchcraft', 'Tropicats', 'Vegas Downtown Slots & Words',
       'World Series of Poker']
for col in cols:
    users_product_value[col] = users_product_value[col].str.replace(',','')
users_product_value = users_product_value.fillna(0)
users_product_value[users_product_value.columns] = users_product_value[users_product_value.columns].astype(int)

traces_users_per_product_value = []
for col in cols:
    traces_users_per_product_value.append(go.Bar(
                    x= users_product_value.index,
                    y = users_product_value[col],
                    name=col))

#Read usrs per product Percentage file:

users_product_percent = pd.read_csv('Users per Product - Percentage - Sheet 1.csv')
users_product_percent = users_product_percent.fillna(0)
users_product_percent = users_product_percent.set_index('Game').T
users_product_percent.index = pd.to_datetime(users_product_percent.index)
cols  = ['1v1.LOL', 'Best Fiends', 'Best Fiends Stars', 'Bingo Blitz',
       'Board Kings', 'Caesars Slots', 'House of Fun', "June's Journey",
       'JustBuild.LOL', 'JustFall.LOL', "Pearl's Peril", 'Pirate Kings',
       'Poker Heat', 'Redecor', 'Slotomania', 'Solitaire Grand Harvest',
       'Switchcraft', 'Tropicats', 'Vegas Downtown Slots & Words',
       'World Series of Poker']
users_product_percent = users_product_percent.fillna(0)
users_product_percent[users_product_percent.columns] = users_product_percent[users_product_percent.columns].astype(float)
users_product_percent = users_product_percent*100

traces_users_per_product_percentage = []
for col in cols:
    traces_users_per_product_percentage.append(go.Bar(
                    x= users_product_percent.index,
                    y = users_product_percent[col],
                    name=col))


app = dash.Dash(__name__ )

server = app.server

app.layout = html.Div([
    html.H4('PLTK Stock Dashboard', style={'color' : 'white'}, className='title'),
    html.Div([
        html.H6('The Correlation between The Reported Revenue & The Sum-Revenue from all Products is : ' + (corr_df['Revenue'].astype(float).corr(corr_df["sum_products"].astype(float))*100).astype(str) + '%',
        style={'color': '#22b3e3'} , className='corr_title'),
        dcc.Graph(
             id='my_graph',
         figure={
            'data': 
                
                   traces
                   
            ,
            'layout':go.Layout(
            barmode='stack',
            # height = 1300,
            title = {'text': 'Revenue from each product', 
                    #  'y':1,
                    #  'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linecolor = 'white',
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True
                        ),
            yaxis = dict(title = '<b>Value</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True)
            )
           
            }
            ,style={'width': '100%', 'height': '80vh'})
    ], className= 'create_container twelve columns'),


    html.Div([
        dcc.Graph(
             id='yearoveryear_rev',
         figure={
            'data': 
                
                   rev_perc_traces
                   
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Revenue Y/Y (Per Product) (Percentage %)', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        # linecolor = 'pink',
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        )),
            yaxis = dict(title = '<b>Percentage</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True)
            )
           
            }
            ,style={'width': '100%', 'height': '80vh'})
    ], className= 'create_container twelve columns'),
    html.Div([ 
        html.Div([
            dcc.Graph(
             id='user_graph',
         figure={
            'data': 
                [go.Scatter(
                    x= users_df.index,
                    y = users_df['Playtika'],
                    name='Users Value',
                    mode = 'markers+lines',
                    line=dict(width = 3,color = '#8308ff')
                    )]
                   
                   
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Users Value', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Value</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
           
            }
            ,style={'width': '100%', 'height': '80vh'})
    ], className= 'create_container six columns'),
    html.Div([ 
        dcc.Graph(
             id='user_perc_graph',
         figure={
            'data': 
                [go.Scatter(
                    x= users_df.index,
                    y = users_df['YoY'],
                    name='Users Value',
                    mode = 'markers+lines',
                    line=dict(width = 3,color = '#08c9ff')
                    )]
                   
                   
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Users Value Y/Y (Percentage %)', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Percentage</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
           
            }
            ,style={'width': '100%', 'height': '80vh'})
    ], className= 'create_container six columns')
        ]),
        html.Div([ 
            html.Div([ 
                dcc.Graph(
             id='user_per_product_value',
         figure={
            'data': 
                traces_users_per_product_value
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Users Per Product', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Value</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'})
            ], className= 'create_container six columns'),
            html.Div([ 
                dcc.Graph(
             id='user_per_product_percentage',
         figure={
            'data': 
                traces_users_per_product_percentage
            ,
            'layout':go.Layout(
            barmode='stack',
            title = {'text': 'Users Per Product Y/Y (Percentage %)', 
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont= dict(color='white',
                            size = 20), 
            font=dict(color='white',
                    size = 12), 
            
            hovermode='closest',
            paper_bgcolor = '#1f2c56', 
            plot_bgcolor='#1f2c56',
            legend={
                'orientation' : 'h',
                'bgcolor' : '#1f2c56',
                'xanchor': 'center', 'x' : 0.5, 'y' : -0.7
            },
            margin= dict(r = 0),
            xaxis = dict(
                # title = '<b>Date</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linewidth = 2,
                        ticks = 'outside',
                        tickfont = dict(
                            color = 'white',
                            size = 12
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        showspikes = True),
            yaxis = dict(title = '<b>Percentage</b>',
                        color = 'white',
                        showline = True,
                        showgrid = True,
                        showspikes = True)
            )
            }
            ,style={'width': '100%', 'height': '80vh'})
            ], className= 'create_container six columns')
        ])
        
        
],id = 'mainContainer', style={'display':'flex', 'flex-direction': 'colum'})



if __name__ =='__main__':
    app.run_server(debug=True)

