import streamlit as st
from utils import format_number
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pandas as pd

def show_bsheet_report(df_bsheet):
    unit = st.checkbox('Change balance sheet unit: %')
    
    if unit:
        st.write('Current Unit: %')
        df_show = df_bsheet.set_index('0. Year').T
        df_show = df_show.div(df_show.loc['TỔNG CỘNG TÀI SẢN', :], axis=1)*100
        df_show = df_show.round(1)
        
    else:
        st.write('Current Unit: VND')
        df_show = df_bsheet.set_index('0. Year').applymap(format_number).T
    
    st.write(df_show)


def show_balancesheet_analysis(df_bsheet):
    ###--- GET VALUES
    # verify columns
    short_term_asset_name = st.sidebar.selectbox(
        "Chọn tài sản ngắn hạn:", df_bsheet.columns, index=1)
    long_term_asset_name = st.sidebar.selectbox(
        "Chọn tài sản dài hạn:", df_bsheet.columns,index=7)
    total_asset_name = st.sidebar.selectbox(
        "Chọn tổng tài sản:", df_bsheet.columns,index=15, key='bsheet_total_asset')
    # verify columns
    debt_name = st.sidebar.selectbox(
        "Chọn nợ phải trả:", df_bsheet.columns, index=16)
    equity_name = st.sidebar.selectbox(
        "Chọn vốn chủ sở hữu:", df_bsheet.columns,index=19)
    total_equity_name = st.sidebar.selectbox(
        "Chọn tổng nguồn vốn:", df_bsheet.columns,index=22)
    inventory_name = st.sidebar.selectbox(
        "Chọn hàng tồn kho:", df_bsheet.columns, index=5)
    
    # get values
    short_term_asset = df_bsheet[short_term_asset_name]
    long_term_asset = df_bsheet[long_term_asset_name]
    total_asset = df_bsheet[total_asset_name]
    debt = df_bsheet[debt_name]
    equity = df_bsheet[equity_name]
    total_equity = df_bsheet[total_equity_name]
    year = df_bsheet['0. Year']
    inventory = df_bsheet[inventory_name]
    
    ###--- ASSET STRUCTURE
    short_term_asset_percent = short_term_asset / total_asset * 100
    long_term_asset_percent = long_term_asset / total_asset * 100
    
    # plot
    fig1 = go.Figure(data=[
        go.Bar(name='Tài sản ngắn hạn', x=year, y=short_term_asset_percent),
        go.Bar(name='Tài sản dài hạn', x=year, y=long_term_asset_percent)
        ])
    
    fig1.update_layout(barmode='stack',
                      title_text='Cơ cấu tài sản')
    fig1.update_xaxes(title_text='Năm')
    fig1.update_yaxes(title_text='Cơ cấu tài sản')
    
    st.plotly_chart(fig1)
    
    ###--- EQUITY STRUCTURE
    debt_percent = debt / total_equity * 100
    equity_percent = equity / total_equity * 100
    
    # plot
    fig2 = go.Figure(data=[
        go.Bar(name='Nợ', x=year, y=debt_percent),
        go.Bar(name='Vốn chủ sở hữu', x=year, y=equity_percent)
        ])
    
    fig2.update_layout(barmode='stack',
                      title_text='Cơ cấu vốn')
    fig2.update_xaxes(title_text='Năm')
    fig2.update_yaxes(title_text='Cơ cấu vốn')
    
    st.plotly_chart(fig2)
    
    ###--- LIQUIDITY RATIO
    liquid_chart, liquid_note = st.columns([3, 1]) 
    
    with liquid_chart:
        quick_ratio = (short_term_asset - inventory) / debt
        current_ratio = short_term_asset / debt
        
        fig3 = go.Figure(data=[
            go.Line(name='Quick ratio', x=year, y=quick_ratio),
            go.Line(name='Current Ratio', x=year, y=current_ratio)
            ])
        
        fig3.update_layout(title_text='Balance sheet ratio analysis')
        
        st.plotly_chart(fig3)
        
    with liquid_note:
        st.markdown("""
        **Important liquidity ratios:**
        
        The quick ratio: ability to meet its short-term obligations with 
        its most liquid assets.

        quick_ratio = (current - inventory) / current debt
        
        The current ratio: ability to pay short-term obligations or those due 
        within one year.
            
        current ratio = current asset / current debt
        """)
        
def update_annual_average(df_bsheet, col: str) -> pd.Series:
    value_shift = df_bsheet[[col]].iloc[0].tolist()
    (value_shift
     .extend([asset for asset in df_bsheet[col][:-1]])
     )
    value_shift = pd.Series(value_shift)

    value_origin = df_bsheet[col]

    value_average = (value_shift + value_origin)/2
    
    return value_average