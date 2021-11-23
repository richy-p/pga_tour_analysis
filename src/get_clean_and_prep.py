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

def insert_rank_columns(df):
    '''
    Add rank columns to each statistical column in the data frame, df. (All columns except name and year)
    '''
    for column in df.columns:
        if column == 'Player Name' or column == 'Year':
            continue
        elif column == 'Average Putts' or column == 'Average Score':
            add_rank_column(df,column,True)
        else:
            add_rank_column(df,column)
    return df

def add_rank_column(df,column,is_ascending=False):
    '''
    Insert a column with the rank for the specified column, grouped by year. New rank column is inserted directly after applicable column
    INPUT:  df - data frame
            column - str - Name of column in df to use to compute the rank
            is_ascending - bool - option to be passed to rank method. Default is False - set to true if lower is better rank
    '''
    df.insert(df.columns.get_loc(column)+1,f'{column} rank', df.groupby('Year')[column].rank(method="min",ascending=is_ascending))

 

if __name__ == "__main__":
    pass

    
