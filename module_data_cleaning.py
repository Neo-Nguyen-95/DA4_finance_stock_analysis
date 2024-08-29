import pandas as pd

def wrangle(datapath):
    df = pd.read_csv(datapath)
    df.rename(columns={'Unnamed: 0': '0. Year'}, inplace=True)
    # format year column
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y')
    
    return df
    