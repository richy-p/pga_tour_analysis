import get_clean_and_prep as gcp
import plotting as myplt
import pandas as pd


class StatisticsGroup(object):
    _columns_of_interest = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']
    _proper_column_names = ['Player Name','Year','Wins','Top 10 Finishes','Driving Accuracy','Driving Distance','GIR','Scrambling','Putts Per Round','Scoring Average    ','SG: Off-the-Tee    ','SG: Approach-the-Green','SG: Around-the-Green','SG: Putting','SG: Total']
    _proper_name_dict = dict(zip(_columns_of_interest,_proper_column_names))
    
    def __init__(self,name=None,statistics_column_names=[],units=None):
        self.name = name
        self.column_names = statistics_column_names
        self.proper_names = self.__get_proper_names()
        self.units = units
        
    def __len__(self):
        return len(self.column_names)
    
    def __get_proper_names(self):
        return [self._proper_name_dict[col] for col in self.column_names]
    


# class StatisticsCategory(object):
#     def __init__(self,name,statistics_column_name,units=None,is_ascending_improving=True):
#         self.name = name
#         self.column_names = statistics_column_name
#         self.units = units
#         self.is_ascending_improving = is_ascending_improving
    


if __name__ == "__main__":
    df_original = gcp.get_data()
    columns_of_interest = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']
    df = df_original.loc[:,columns_of_interest]
    
    df = gcp.change_nan_to_0(df,['Wins','Top 10'])
    df = gcp.insert_rank_columns(df)

    # group column names together to make calling easier
    traditional_stats = StatisticsGroup('Traditional Statistics',['Fairway Percentage', 'Avg Distance', 'gir', 'Average Putts', 'Average Scrambling'])
    strokes_gained_stats = StatisticsGroup('Strokes Gained Statistics',['SG:OTT', 'SG:APR', 'SG:ARG','Average SG Putts'],'Strokes Gained')
    fairway_green_scramble_pct_columns = StatisticsGroup('Fairways, Greens, and Scrambling',['Fairway Percentage', 'gir', 'Average Scrambling'],'Percent')
    distance_off_tee_column = StatisticsGroup('Distance off the Tee',['Avg Distance'],'Distance (yards)')
    avg_putts_column = StatisticsGroup('Average Putts per Round', ['Average Putts'],'Number of Putts')

    # I haven't made proper names for ranks so these will not work when object instantiated. Not sure I was going to use them anyway. May come back to them later.
    # traditional_stats_rank = StatisticsGroup('Traditional Statistic Rank',[stat + ' rank' for stat in traditional_stats.column_names])
    # strokes_gained_stats_rank = StatisticsGroup('Strokes Gained Ranks',[stat + ' rank' for stat in strokes_gained_stats.column_names])
    # quad_stat_groups = [traditional_stats,traditional_stats_rank, strokes_gained_stats, strokes_gained_stats_rank]
    # myplt.make_win_top10_quad_heatmaps(df,quad_stat_groups)
    # for year in df.Year.unique():
    #     myplt.make_win_top10_quad_heatmaps(df[df['Year']==year],quad_stat_groups)
    
    # Make a few scatter plots to show why Strokes Gained statistics are used.
    myplt.make_double_scatter_plot(df,['gir','Average Scrambling'],'Average Putts',alpha=.5,title='Dependency between Traditional Statistics',with_top_performers=False,save_path='/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/dependency_between_gir_scrambling_putts.png')    
    myplt.make_double_scatter_plot(df,['SG:APR','SG:ARG'],'Average SG Putts',alpha=.5,title='Dependency between Strokes Gained Statistics',with_top_performers=False,save_path='/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/dependency_between_SG_apr_arg_putting.png')    

    for group in [traditional_stats,strokes_gained_stats]:
        myplt.make_win_top10_heatmaps(df,group,just_top_performers=True)

    myplt.make_violin_top_performer_plots(df,strokes_gained_stats)
    myplt.make_violin_top_performer_plots(df,distance_off_tee_column,show_legend=True,orientation='h')
    myplt.make_violin_top_performer_plots(df,fairway_green_scramble_pct_columns)
    myplt.make_violin_top_performer_plots(df,avg_putts_column,show_legend=True,orientation='h')
