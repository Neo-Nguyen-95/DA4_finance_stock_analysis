import pandas as pd

def wrangle(datapath):
    df = pd.read_csv(datapath)
    df = df.astype(int)
    df.rename(columns={'Unnamed: 0': '0. Year'}, inplace=True)
    # format year column
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y')
    df.iloc[:, 0] = df.iloc[:, 0].dt.year
    
    return df

#%% TEST SITE

# df = wrangle('PNJ_income.csv') 