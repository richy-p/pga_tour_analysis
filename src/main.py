from matplotlib.pyplot import get
import get_clean_and_prep as gcp
import plotting as myplt
import pandas as pd


class StatisticsGroup(object):
    # _columns_in_df = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total',]
    _columns_in_df = ['Player Name', 'Year', 'Wins', 'Wins rank', 'Top 10', 'Top 10 rank',
       'Fairway Percentage', 'Fairway Percentage rank', 'Avg Distance',
       'Avg Distance rank', 'gir', 'gir rank', 'Average Scrambling',
       'Average Scrambling rank', 'Average Putts', 'Average Putts rank',
       'Average Score', 'Average Score rank', 'SG:OTT', 'SG:OTT rank',
       'SG:APR', 'SG:APR rank', 'SG:ARG', 'SG:ARG rank', 'Average SG Putts',
       'Average SG Putts rank', 'Average SG Total', 'Average SG Total rank']
    # _proper_column_names = ['Player Name','Year','Wins','Top 10 Finishes','Driving Accuracy','Driving Distance','GIR','Scrambling','Putts Per Round','Scoring Average    ','SG: Off-the-Tee    ','SG: Approach-the-Green','SG: Around-the-Green','SG: Putting','SG: Total']
    _proper_column_names = ['Player Name','Year','Wins','Wins Rank','Top 10 Finishes','Top 10 Finishes Rank','Driving Accuracy','Driving Accuracy Rank','Driving Distance','Driving Distance Rank','GIR','GIR Rank','Scrambling','Scrambling Rank','Putts Per Round','Putts Per Round Rank','Scoring Average','Scoring Average Rank','SG: Off-the-Tee','SG: Off-the-Tee Rank','SG: Approach-the-Green','SG: Approach-the-Green Rank','SG: Around-the-Green','SG: Around-the-Green Rank','SG: Putting','SG: Putting Rank','SG: Total','SG: Total Rank']
    _proper_name_dict = dict(zip(_columns_in_df,_proper_column_names))
    
    def __init__(self,name=None,statistics_column_names=[],units=None):
        self.name = name
        self.column_names = statistics_column_names
        self.proper_names = self.__get_proper_names()
        self.units = units
        
    def __len__(self):
        return len(self.column_names)
    
    def __get_proper_names(self):
        return [self._proper_name_dict[col] for col in self.column_names]
    
def get_top_individuals(df):
    '''
    Get the player with the most total wins, most total top 10s, and the most yearly top performances
    INPUT: df - data frame
    OUTPUT: individual_track_list - list of unique player names
    '''
    individual_track_list = []
    for col in ['Wins','Top 10']:
        individual_track_list.append(df.groupby('Player Name').sum()[[col]].idxmax()[0])
    top_performers = df[(df['Wins rank']<=3) | (df['Top 10 rank']<=3)]
    top_performers_name_list = list(top_performers['Player Name'])
    num_yearly_top_performances = {name: top_performers_name_list.count(name) for name in top_performers_name_list}
    individual_track_list.append(max(num_yearly_top_performances, key=num_yearly_top_performances.get))
    return list(set(individual_track_list))


if __name__ == "__main__":
    df_original = gcp.get_data()
    columns_of_interest = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']
    df = df_original.loc[:,columns_of_interest]
    
    df = gcp.change_nan_to_0(df,['Wins','Top 10'])
    df = gcp.insert_rank_columns(df)

    # group column names together to make calling easier for making figures
    traditional_stats = StatisticsGroup('Traditional Statistics',['Fairway Percentage', 'Avg Distance', 'gir',  'Average Scrambling', 'Average Putts'])
    strokes_gained_stats = StatisticsGroup('Strokes Gained Statistics',['SG:OTT', 'SG:APR', 'SG:ARG','Average SG Putts'],'Strokes Gained')
    fairway_green_scramble_pct_columns = StatisticsGroup('Fairways, Greens, and Scrambling',['Fairway Percentage', 'gir', 'Average Scrambling'],'Percent')
    distance_off_tee_column = StatisticsGroup('Distance off the Tee',['Avg Distance'],'Distance (yards)')
    avg_putts_column = StatisticsGroup('Average Putts per Round', ['Average Putts'],'Number of Putts')
    traditional_stats_rank = StatisticsGroup('Traditional Statistic Ranks',[stat + ' rank' for stat in traditional_stats.column_names])
    strokes_gained_stats_rank = StatisticsGroup('Strokes Gained Ranks',[stat + ' rank' for stat in strokes_gained_stats.column_names])
    quad_stat_groups = [traditional_stats,traditional_stats_rank, strokes_gained_stats, strokes_gained_stats_rank]
    
    # Make a side by side scatter plots showing statistic category dependencies.
    myplt.make_double_scatter_plot(df,['gir','Average Scrambling'],'Average Putts',alpha=.5,title='Dependency between Traditional Statistics',with_top_performers=False,save_path='/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/dependency_between_gir_scrambling_putts.png')    
    myplt.make_double_scatter_plot(df,['SG:APR','SG:ARG'],'Average SG Putts',alpha=.5,title='Dependency between Strokes Gained Statistics',with_top_performers=False,save_path='/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/dependency_between_SG_apr_arg_putting.png')    

    # make correlation maps
    for group in [traditional_stats,strokes_gained_stats,traditional_stats_rank,strokes_gained_stats_rank]:
        myplt.make_win_top10_heatmaps(df,group,just_top_performers=True)

    # make distrobution plots
    myplt.make_violin_top_performer_plots(df,strokes_gained_stats)
    myplt.make_violin_top_performer_plots(df,distance_off_tee_column,show_legend=True,orientation='h')
    myplt.make_violin_top_performer_plots(df,fairway_green_scramble_pct_columns)
    myplt.make_violin_top_performer_plots(df,avg_putts_column,show_legend=True,orientation='h')

    individual_track_list = get_top_individuals(df)
    for player in individual_track_list:
        myplt.make_player_overview_plot(df,player)