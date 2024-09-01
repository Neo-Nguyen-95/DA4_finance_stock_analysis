#%% LOAD DATA
# EDA package
import pandas as pd
pd.set_option('display.max_columns', None)
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

# my customized package
from module_data_cleaning import wrangle

df_income = wrangle('PNJ_income.csv')

#%% APP DESIGN
st.title("WEB APP FOR FINANCIAL ANALYSIS")

#%% PART I: TREND ANALYSIS
st.markdown("""
## PART I: INCOME STATEMENT ANALYSIS
Phân tích báo cáo doanh thu của công ty!
""")

#%% 1.1: GROWTH ANALYSIS
st.markdown("""
### 1.1 Phân tích tăng trưởng
""")

# box value
category = st.selectbox(
    "Chọn mục:",
    list(df_income.columns[1:])
    )

# plot
def growth_chart(category):
    year = df_income.iloc[:, 0]
    value = df_income.loc[:, category]
    fig = px.bar(x=year, y=value,
                 title='Tăng trưởng hàng năm')
    
    fig.update_yaxes(title_text='Income [VND]')
    fig.update_xaxes(title_text='Year')
    
    return fig

# connect
st.plotly_chart(
    growth_chart(category)
    )

# chart of percentage
col1, col2 = st.columns(2)

def growth_part(category):
    year = df_income.iloc[:, 0]
    value = df_income.iloc[:, 1:].loc[:, category]/df_income.iloc[:, 3] * 100
    fig = px.bar(x=year, y=value,
                 title='% so với doanh thu thuần')
    
    fig.update_yaxes(title_text='Biên lợi nhuận so với doanh thu thuần [%]')
    fig.update_xaxes(title_text='Year')
    
    return fig

with col1:
    st.plotly_chart(
        growth_part(category)
        )

def growth_percent(category):
    year = df_income.iloc[1:, 0]
    # growth in % in comparison to the previous year
    value = ((df_income.loc[1:, category].values - df_income.loc[:len(df_income)-2, category].values)/
              df_income.loc[:len(df_income)-2, category].values
              )*100
    
    fig = px.bar(x=year, y=value)
    
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Tăng trưởng so với năm trước [%]')
    
    return fig 

with col2:
    st.plotly_chart(
        growth_percent(category)
        )
    
#%% 1.2: MARGIN ANALYSIS
st.markdown("""
### 1.2 Phân tích biên (chi tiết))
""")

def margin_analysis():
    year = df_income.iloc[:, 0]
    for cat in df_income.columns:
        if 'doanh thu thuần' in cat.lower():
            income_col = cat
        
        if 'lợi nhuận gộp' in cat.lower():
            ebit = df_income.loc[:, cat] / df_income.loc[:, income_col] * 100
            
        if 'lợi nhuận sau thuế thu nhập doanh nghiệp' in cat.lower():
            ebitda = df_income.loc[:, cat] / df_income.loc[:, income_col] * 100
            
    fig = go.Figure(data=[
        go.Bar(name='EBIT', x=year, y=ebit),
        go.Bar(name='EBITDA', x=year, y=ebitda)  
        ])
    
    fig.update_layout(title_text='Báo cáo biên lợi nhuận!')
    fig.update_layout(barmode='group')
    fig.show()
    
    return fig
    
st.plotly_chart(
    margin_analysis()
    )
            







