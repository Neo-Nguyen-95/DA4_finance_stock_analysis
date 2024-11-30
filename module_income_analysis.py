import streamlit as st
from utils import format_number
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_income_report(df_income):
    income_unit_percent = st.checkbox('Unit: %')

    if income_unit_percent:
        st.write('Current Unit: % Doanh thu thuần')
        df_show = df_income.set_index('0. Year')
        # find doanh thu thuần chính xác
        for i in df_income.columns:
            if 'doanh thu thuần' in i.lower():
                doanh_thu_thuan_col = i
        
        df_show = df_show.div(df_show.loc[:, doanh_thu_thuan_col], axis=0)*100
        st.write(df_show.round(1).T)
    else:
        st.write('Current Unit: VND')
        st.write(df_income.set_index('0. Year').applymap(format_number).T)
        
        
def show_growth_analysis(df_income):
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
    col111, col112 = st.columns(2)

    def growth_part(category):
        year = df_income.iloc[:, 0]
        value = df_income.iloc[:, 1:].loc[:, category]/df_income.iloc[:, 3] * 100
        fig = px.bar(x=year, y=value, title='% so với doanh thu thuần')
        
        fig.update_yaxes(title_text='Biên lợi nhuận so với doanh thu thuần [%]')
        fig.update_xaxes(title_text='Year')
        
        return fig

    with col111:
        st.plotly_chart(
            growth_part(category)
            )

    def growth_percent(category):
        year = df_income.iloc[1:, 0]
        # growth in % in comparison to the previous year
        value = ((df_income.loc[1:, category].values - df_income.loc[:len(df_income)-2, category].values)/
                  df_income.loc[:len(df_income)-2, category].values
                  )*100
        
        fig = px.bar(x=year, y=value, title='% tăng trưởng so với năm trước')
        
        fig.update_xaxes(title_text='Year')
        fig.update_yaxes(title_text='Tăng trưởng so với năm trước [%]')
        
        return fig 

    with col112:
        st.plotly_chart(
            growth_percent(category)
            )
        
        
def show_margin_analysis(df_income, df_cashflow, df_bsheet):
    ###----- CONFIRM VALUES 
    doanh_thu_thuan = st.sidebar.selectbox(
        "Chọn doanh thu thuần", list(df_income.columns[1:]), index=2
        )
    loi_nhuan_gop = st.sidebar.selectbox(
        "Chọn lợi nhuận gộp:", list(df_income.columns[1:]), index=4
        )
    lai_vay = st.sidebar.selectbox(
        "Chọn lãi vay:", list(df_income.columns[1:]), index=7
        )
    loi_nhuan_truoc_thue = st.sidebar.selectbox(
        "Chọn lợi nhuận trước thuế:", list(df_income.columns[1:]), index=15
        )
    loi_nhuan_rong = st.sidebar.selectbox(
        "Chọn lợi nhuận sau thuế:", list(df_income.columns[1:]), index=19
        ) 
    khau_hao = st.sidebar.selectbox(
        "Chọn khấu hao:", list(df_cashflow.columns), index=3
        )
    tong_tai_san = st.sidebar.selectbox(
        "Chọn tổng tài sản:", list(df_bsheet.columns), index=15)
    
    von_chu_so_huu = st.sidebar.selectbox(
        "Chọn vốn chủ sở hữu: ", df_bsheet.columns,index=19, key=0
        )
    gia_von_hang_ban = st.sidebar.selectbox(
        "Chọn giá vốn hàng bán: ", df_income.columns, index=4
        )
    average_total_asset = st.sidebar.selectbox(
        "Chọn trung bình vốn năm: ", df_bsheet.columns, index=23
        )
    average_inventory = st.sidebar.selectbox(
        "Chọn trung tồn kho năm: ", df_bsheet.columns, index=24
        )
     
    ###----- GET VALUES
    
    bien_gop = df_income[loi_nhuan_gop] / df_income[doanh_thu_thuan] * 100
    
    ebit = df_income[loi_nhuan_truoc_thue] + df_income[lai_vay]
    bien_ebit = ebit / df_income[doanh_thu_thuan] * 100
    
    df_temp = pd.merge(df_income, df_cashflow, on='0. Year')
    ebitda = (
        df_temp[loi_nhuan_truoc_thue] + df_temp[lai_vay] 
        + df_temp[khau_hao]
        )
    bien_ebitda = ebitda / df_temp[doanh_thu_thuan] * 100
    
    bien_rong = df_income[loi_nhuan_rong] / df_income[doanh_thu_thuan] * 100
    
    roa = df_income[loi_nhuan_rong] / df_bsheet[tong_tai_san] * 100
    roe = df_income[loi_nhuan_rong] / df_bsheet[von_chu_so_huu] * 100
    
    asset_turnover = df_income[doanh_thu_thuan] / df_bsheet[average_total_asset]
    inventory_turnover = df_income[gia_von_hang_ban] / df_bsheet[average_inventory]
    
    ###----- PLOT MARGIN ANALYSIS       
    fig = go.Figure(data=[
        go.Line(name='Biên lợi nhuận gộp', x=df_income['0. Year'], y=bien_gop),
        go.Line(name='EBIT', x=df_income['0. Year'], y=bien_ebit),
        go.Line(name='EBITDA', x=df_temp['0. Year'], y=bien_ebitda),
        go.Line(name='Biên lợi nhuận ròng', x=df_income['0. Year'], y=bien_rong)
        ])
    
    fig.update_layout(title_text='Chỉ số biên lợi nhuận',
                      barmode='group')
    fig.update_yaxes(title_text='% Doanh thu thuần')
    fig.update_xaxes(title_text='Year', showgrid=True)
        
    st.plotly_chart(fig)
    
    ###----- PROFITABILITY RATIO
    # PLOT ROA
    roa_chart, roa_note = st.columns([3, 1])
    
    with roa_chart:
        fig2 = go.Figure(data=[
            go.Line(name='ROA', x=df_income['0. Year'], y=roa)
            ])
        
        fig2.update_layout(title_text='ROA analysis',
                          xaxis_title='Năm',
                          yaxis_title='[%]')
        
        st.plotly_chart(fig2)
    
    with roa_note:
        st.markdown("""
                **Explain:**
                
                Return on Asset:
                    
                - ROA = Lợi nhuận sau thuế / Tổng tài sản
                - Good: > 5%; Great > 20%
                 """)

    # PLOT ROE
    roe_chart, roe_note = st.columns([3, 1])
    
    with roe_chart:
        fig3 = go.Figure(data=[
            go.Line(name='ROE', x=df_income['0. Year'], y=roe)
            ])
        
        fig3.update_layout(title_text='ROE analysis',
                          xaxis_title='Năm',
                          yaxis_title='[%]')
        
        st.plotly_chart(fig3)
        
    with roe_note:
        st.markdown("""
                **Explain:**
                 
                Return on Equity:
                - ROE = Lợi nhuận sau thuế / Tổng vốn chủ sở hữu
                - Good: > 15%
                 """)
                 
    ###--- PLOT EFFICIENCY RATIOS
    # PLOT ASSET TURNOVER
    asset_turnover_chart, asset_turnover_note = st.columns([3, 1])
    
    with asset_turnover_chart:
        fig4 = go.Figure(data=[
            go.Line(name='Asset turnover', x=df_income['0. Year'], y=asset_turnover)
            ])
        
        fig4.update_layout(title_text='Asset turnover',
                          xaxis_title='Năm',
                          yaxis_title='Tỉ lệ')
        
        st.plotly_chart(fig4)
        
        
    with asset_turnover_note:
        st.markdown("""
                    **Explain:**
                    
                    - Asset turnover = Doanh thu thuần / Trung bình tổng tài sản
                    - Trung bình tổng tài sản = Trung bình tổng tài sản đầu và cuối kì
                    
                    """)
    
    
    # PLOT INVENTORY TURNOVER
    inventory_turnover_chart, inventory_turnover_note = st.columns([3, 1])
    
    with inventory_turnover_chart:
        fig5 = go.Figure(data=[
            go.Line(name='Inventory turnover', x=df_income['0. Year'], y=inventory_turnover)
            ])
        
        fig5.update_layout(title_text='Inventory turnover',
                          xaxis_title='Năm',
                          yaxis_title='Tỉ lệ')
        
        st.plotly_chart(fig5)
        
        
    with inventory_turnover_note:
        st.markdown("""
                    **Explain:**
                    
                    - Inventory turnover = Giá vốn hàng bán / Trung bình tồn kho
                    - Trung bình tồn kho = Trung bình tồn kho đầu và cuối kì
                
                    """)
    



