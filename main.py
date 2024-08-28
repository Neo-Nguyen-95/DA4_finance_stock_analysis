#%% LOAD DATA
# EDA package
import pandas as pd
pd.set_option('display.max_columns', None)
import seaborn as sns
import matplotlib.pyplot as plt

from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px

# for spyder display
import plotly.io as pio
pio.renderers.default='browser'


# my customized package
# from data_processing.cafef_scraping import FinanceStat
from data_processing.data_cleaning import wrangle
# from fin_analysis.income_statement import ...

# export data to .csv file, only use once to download data
# data = FinanceStat('pnj')
# data.export_findata(form='csv')

df_income = wrangle('pnj_incsta.csv')
df_income.columns

#%% I. ANALYZE INCOME DATA
intro_part_i = """
## PART I: INCOME STATEMENT ANALYSIS
This part is to analyze income statement of the company
"""

# data for part i
# 1. Analyze revenue growth
# def annual_growth_currency(col):
#     year = df_income.iloc[:, 0]
#     value = df_income.iloc[:, col]
#     fig = px.line(x=year, y=value)
    
#     return fig
# annual_growth_currency(3)
    
# def annual_growth_percent(col):
#     year = df_income.iloc[1:, 0]
#     # growth in % in comparison to the previous year
#     value = ((df_income.iloc[1:, col].values - df_income.iloc[:-1, col].values)/
#              df_income.iloc[:-1, col].values
#              )*100
    
#     fig = px.bar(x=year, y=value)
    
#     return fig 
# annual_growth_percent(3)

#%% APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    html.H1("WEB APP FOR FINANCIAL ANALYSIS",
            style={'text-align':'center'}),
    
    # PART I
    dcc.Markdown(children=intro_part_i),
    
    dcc.Dropdown(df_income.columns, '0. Year', id='income_stat_items'),
    dcc.Graph(id='annual_growth_currency', figure={}),
    
    ])

#%% APP PART I
@callback(
    Output('annual_growth_currency', 'figure'),
    Input('income_stat_items', 'value')
    )
def annual_growth(item):
    year = df_income.iloc[:, 0]
    value = df_income.loc[:, item]
    fig = px.line(x=year, y=value)
    
    return fig

#%% --- RUN: http://127.0.0.1:8050/
app.run(debug=True)






