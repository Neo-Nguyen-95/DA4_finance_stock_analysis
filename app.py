#%% LOAD DATA
# EDA package
import pandas as pd
pd.set_option('display.max_columns', None)

import streamlit as st

# my customized package
from module_data_cleaning import wrangle
from module_income_analysis import show_income_report, show_growth_analysis, show_margin_analysis
from module_bsheet_analysis import show_bsheet_report, show_balancesheet_analysis
from module_cashflow_analysis import show_cashflow_report, show_cashflow_analysis

company_name = "FPT"

folder_path = 'data/'

df_income = wrangle(folder_path + company_name + '_income.csv')
df_cashflow = wrangle(folder_path + company_name + '_cashflow.csv')
df_bsheet = wrangle(folder_path + company_name + '_bsheet.csv')
#%% APP DESIGN
st.title("WEB APP FOR FINANCIAL ANALYSIS")
st.sidebar.title("VALUE CONFIRM")

st.markdown("""
### Case study: {}""".format(company_name))

#%% PART I: TREND ANALYSIS WITH INCOME STATEMENT
st.markdown("""
## PART I: INCOME STATEMENT ANALYSIS
**Income Statement report**
""")
st.sidebar.markdown("""
                    ## PART I: FOR INCOME STATEMENT
                    """)

show_income_report(df_income)

#%% 1.1: GROWTH ANALYSIS
st.markdown("""
### 1.1 Phân tích tăng trưởng
""")

show_growth_analysis(df_income)
    
#%% 1.2: MARGIN ANALYSIS
st.markdown("""
### 1.2 Phân tích biên (chi tiết)
Chọn đúng các chỉ số để xác định các chỉ số biên chính xác.

EBIT (Earning Before Interst and Taxes) = Lợi nhuận thuần + lãi vay

EBITDA (Earning before Interest, Taxes, Depreciation and Amortization) = EBIT + khấu hao

""")

show_margin_analysis(df_income, df_cashflow, df_bsheet)

#%% PART II: BALANCE SHEET ANALYSIS
st.markdown("""
## PART II: BALANCE SHEET ANALYSIS
**Balance Sheet report**
""")
st.sidebar.markdown("""
## PART II: FOR BALANCE SHEET
""")

show_bsheet_report(df_bsheet)

show_balancesheet_analysis(df_bsheet)

#%% PART III: CASHFLOW ANALYSIS
st.markdown("""
## PART III: CASHFLOW ANALYSIS
**Cash flow report**
""")

st.sidebar.markdown("""
## PART III: FOR CASH FLOW STATEMENT
""")

show_cashflow_report(df_cashflow)

show_cashflow_analysis(df_cashflow)


