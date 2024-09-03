import streamlit as st
from utils import format_number
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_cashflow_report(df_cashflow):
    st.write('Current Unit: VND')
    df_show = df_cashflow.set_index('0. Year').applymap(format_number).T
    
    st.write(df_show)

def show_cashflow_analysis(df_cashflow):
    ###--- GET VALUE
    cash_from_operation_name = st.sidebar.selectbox(
        "Chọn lưu chuyển tiền từ kinh doanh:", 
        df_cashflow.columns, index=24)
    cash_from_investing_name = st.sidebar.selectbox(
        "Chọn lưu chuyển tiền từ đầu tư:",
        df_cashflow.columns, index=36)
    cash_from_financing_name = st.sidebar.selectbox(
        "Chọn lưu chuyển tiền từ tài chính:",
        df_cashflow.columns, index=47)
    cashflow_total_name = st.sidebar.selectbox(
        "Chọn lưu chuyển tiền thuần trong kì:",
        df_cashflow.columns, index=48)
    cash_beginning_name = st.sidebar.selectbox(
        "Chọn tiền đầu kì:",
        df_cashflow.columns, index=49)
    cash_ending_name = st.sidebar.selectbox(
        "Chọn tiền cuối kì:",
        df_cashflow.columns, index=51)
    
    
    ###--- CALCULATION
    cash_from_operation = df_cashflow[cash_from_operation_name]
    cash_from_investing = df_cashflow[cash_from_investing_name]
    cash_from_financing = df_cashflow[cash_from_financing_name]
    cashflow_total = df_cashflow[cashflow_total_name]
    year = df_cashflow['0. Year']
    cash_beginning = df_cashflow[cash_beginning_name]
    cash_ending = df_cashflow[cash_ending_name]
    
    ###--- PLOT
    # total cash flow
    fig2 = go.Figure(data=[
        go.Bar(name='Đầu kì', x=year, y=cash_beginning),
        ])
    fig2.add_trace(go.Bar(
        x=year, y=cashflow_total, name='Dòng tiền',
        marker=dict(
            color = 'rgba(0,0,0,0)',
            pattern=dict(
                shape='/',
                fgcolor='#E95793',
                bgcolor='rgba(0,0,0,0)'
                ),
            line=dict(color='#E95793', width=1)
            )
        ))
    fig2.update_layout(title_text='Cơ cấu lưu chuyển tiền tệ', barmode='stack')
    
    st.plotly_chart(fig2)
    
    # compare cash flows
    fig = go.Figure(data=[
        go.Line(name='Từ kinh doanh', x=year, y=cash_from_operation),
        go.Line(name='Từ đầu tư', x=year, y=cash_from_investing),
        go.Line(name='Từ tài chính', x=year, y=cash_from_financing)
        ])
    fig.update_layout(title_text='Lưu chuyển tiền tệ')
    fig.update_xaxes(title_text='Năm', showgrid=True)
    fig.update_yaxes(title_text='Tiền [VND]')
    
    st.plotly_chart(fig)
    
    
    
    
    
    
    
    