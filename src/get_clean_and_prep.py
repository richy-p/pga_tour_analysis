import os
import pandas as pd


def get_data(filename='pgaTourData.csv',path='~/Documents/dai/repos/pga_tour_analysis/data/'):
    return pd.read_csv(os.path.join(path,filename))

def change_nan_to_0(df,columns):
    '''
    INPUT:  df - data frame
            columns - string or list of strings
    OUTPUT: df - same data frame with NaNs in specified columns chaged to zeros
    '''
    df[columns] = df[columns].fillna(0)
    return df

def add_rank_column(df,column,is_ascending=False):
    '''
    Insert a column with the rank for the specified column, grouped by year
    '''
    df.insert(df.columns.get_loc(column)+1,f'{column} rank', df.groupby('Year')[column].rank(method="min",ascending=is_ascending))

def insert_rank_columns(df):
    for column in df.columns:
        if column == 'Player Name' or column == 'Year':
            continue
        elif column == 'Average Putts' or column == 'Average Score':
            add_rank_column(df,column,True)
        else:
            add_rank_column(df,column)
    return df
 

if __name__ == "__main__":
    df_original = get_data()
    columns_of_interest = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']

    df = df_original.loc[:,columns_of_interest]
    df = change_nan_to_0(df,['Wins','Top 10'])
    df = insert_rank_columns(df)

    
