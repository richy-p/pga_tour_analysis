import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

class statistics_group(object):
    def __init__(self,name=None,statistics_column_names=[]):
        self.name = name
        self.column_names = statistics_column_names

def make_win_top10_heatmaps(df,group):
    '''
    Make win and top 10 heatmaps of the specified statistical group
    INPUT - df - data frame, group - statistics group class obj
    '''
    corr = df[['Wins','Top 10']+group.column_names].corr()
    fig,ax = plt.subplots()
    sns.heatmap(corr.iloc[:2,2:], annot=True,ax=ax)
    ax.set_title(group.name)
    fig.savefig(f'images/win_top10_heatmap_{group.name.replace(" ","_")}.png')

def make_win_top10_quad_heatmaps(df):
    '''
    Makes a figure with 4 subplots of heat maps showing the correlation between wins/top 10s and the Traditional and Strokes Gained statistics as well as the ranks for each.
    '''
    fig,axs = plt.subplots(2,2,figsize=(10,10))
    stat_groups = [traditional_stats,traditional_stats_rank, strokes_gained_stats, strokes_gained_stats_rank]
    for i,ax in enumerate(axs.flatten()):
        corr = df[['Wins','Top 10']+stat_groups[i].column_names].corr()
        sns.heatmap(corr.iloc[:2,2:], annot=True,ax=ax)
        ax.set_title(stat_groups[i].name)
    fig.suptitle(f'{df.Year.unique()[0]}' if len(df.Year.unique()) == 1 else f'{df.Year.unique().min()} - {df.Year.unique().max()}')
    fig.tight_layout()
    year_string = f'{df.Year.unique()[0]}' if len(df.Year.unique()) == 1 else f'{df.Year.unique().min()}_{df.Year.unique().max()}'
    fig.savefig(f'images/win_top10_quad_heatmaps_{year_string}.png')    

if __name__ == "__main__":
    df_original = pd.read_csv('data/pgaTourData.csv')
    columns_of_interest = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']

    df = df_original.loc[:,columns_of_interest]
    df = change_nan_to_0(df,['Wins','Top 10'])
    # insert rank columns
    for column in df.columns:
        if column == 'Player Name' or column == 'Year':
            continue
        elif column == 'Average Putts' or column == 'Average Score':
            add_rank_column(df,column,True)
        else:
            add_rank_column(df,column)

    # group column names together to make calling easiernu99
    # fairway_green_scramble_pct_columns = ['Fairway Percentage', 'gir', 'Average Scrambling']
    # traditional_stats = ['Fairway Percentage', 'Avg Distance', 'gir', 'Average Putts', 'Average Scrambling']
    # strokes_gained_stats = ['SG:OTT', 'SG:APR', 'SG:ARG','Average SG Putts']
    # traditional_stats_rank = [stat + ' rank' for stat in traditional_stats]
    # strokes_gained_stats_rank = [stat + ' rank' for stat in strokes_gained_stats]
    
    traditional_stats = statistics_group('Traditional Statistics',['Fairway Percentage', 'Avg Distance', 'gir', 'Average Putts', 'Average Scrambling'])
    strokes_gained_stats = statistics_group('Strokes Gained Statistics',['SG:OTT', 'SG:APR', 'SG:ARG','Average SG Putts'])
    traditional_stats_rank = statistics_group('Traditional Statistic Rank',[stat + ' rank' for stat in traditional_stats.column_names])
    strokes_gained_stats_rank = statistics_group('Strokes Gained Ranks',[stat + ' rank' for stat in strokes_gained_stats.column_names])
    # need to break up some traditional ones for plotting 
    fairway_green_scramble_pct_columns = statistics_group('Fairways, Greens, and Scrambling',['Fairway Percentage', 'gir', 'Average Scrambling'])
    distance_off_tee_column = statistics_group('Distance off the Tee',['Avg Distance'])
    avg_putts_column = statistics_group('Average Putts per Round', ['Average Putts'])

    stat_groups = [traditional_stats,traditional_stats_rank, strokes_gained_stats, strokes_gained_stats_rank]

    make_win_top10_quad_heatmaps(df)
    for year in df.Year.unique():
        make_win_top10_quad_heatmaps(df[df['Year']==year])

    for group in stat_groups:
        make_win_top10_heatmaps(df,group)