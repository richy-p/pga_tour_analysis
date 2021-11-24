import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style='darkgrid')
plt.rcParams.update({'font.size': 12, 'font.family': 'sans'})

def make_double_scatter_plot(df,xcols,ycol,alpha=1,with_top_performers=True,title=None,show_legend=True,save_path=None):
    '''
    Makes figure with two subplots, each scatter plots that share a y axis.
    INPUT:  df      - data frame
            xcols   - list length 2 - contains the column names of the df to use for each x axis
            ycols   - str   - column name of df to use for the y axis
            alpha   - set transparency - defualt=1
            with_top_performers - bool  - when True will overlay the top performers on the scatter plot
            title   - str   - optional title for the plot
            show_legend - bool - only applicable if with_top_performers=True - if false no legend will be added to plot
            save_path   -   str - path and filename for figure to be saved
    OUTPUT: fig,axs handles
    '''
    # map df column names to proper names to be used on the figure
    column_names = ['Player Name', 'Year', 'Wins', 'Top 10', 'Fairway Percentage', 'Avg Distance', 'gir', 'Average Scrambling', 'Average Putts', 'Average Score', 'SG:OTT', 'SG:APR', 'SG:ARG', 'Average SG Putts', 'Average SG Total']
    proper_column_names = ['Player Name','Year','Wins','Top 10 Finishes','Driving Accuracy','Driving Distance','GIR','Scrambling','Putts Per Round','Scoring Average    ','SG: Off-the-Tee    ','SG: Approach-the-Green','SG: Around-the-Green','SG: Putting','SG: Total']
    proper_name_dict = dict(zip(column_names,proper_column_names))
    fig,axs = plt.subplots(1,2,sharey=True,figsize=(10,5))
    for i in range(2):
        df.plot.scatter(xcols[i],ycol,ax=axs[i],alpha=alpha)
        if with_top_performers:
            top_wins_mask = df['Wins rank']<=3
            top_top10s_mask = df['Top 10 rank']<=3
            df[top_top10s_mask].plot.scatter(xcols[i],ycol,ax=axs[i],alpha=alpha,color='darkblue',edgecolor='black',label='Most Top 10s')
            df[top_wins_mask].plot.scatter(xcols[i],ycol,ax=axs[i],alpha=alpha,color='gold',edgecolor='black',label='Most Wins')
        axs[i].set_xlabel(proper_name_dict[xcols[i]])
    axs[0].set_ylabel(proper_name_dict[ycol])
    if with_top_performers:
        axs[0].legend().set_visible(False)
        axs[1].legend().set_visible(show_legend)
        if show_legend:
            axs[1].legend(loc='upper left')
    fig.suptitle(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path)
    return fig,axs
    

def make_win_top10_heatmaps(df,group,just_top_performers=False,top_performer_rank_limit=3):
    '''
    Make win and top 10 heatmaps of the specified statistical group
    INPUT - df - data frame, group - statistics group class obj
            just_top_performers - bool - if true then the correlation will only be between players ranked in the top X(set by top_performer_rank_limit) for wins or top 10s in a year
            top_performer_rank_limit - int - rank to include up to for top performers - default is 3 (players ranked 3rd or higher)
    '''
    if just_top_performers:
        df = df[(df['Wins rank']<=top_performer_rank_limit) | (df['Top 10 rank']<=top_performer_rank_limit)]
        title_str = f'{group.name} Correlation of Finishes for Top Performers'
        save_path_name = f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/win_top10_heatmap_top_performers_{group.name.replace(" ","_")}.png'
    else:
        title_str = group.name
        save_path_name = f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/win_top10_heatmap_{group.name.replace(" ","_")}.png'
    corr = df[['Wins','Top 10']+group.column_names].corr()
    fig,ax = plt.subplots(figsize=(4.5,3))
    sns.heatmap(corr.iloc[2:,:2], annot=True,ax=ax)
    ax.set_title(title_str)
    ax.set_yticklabels(group.proper_names)
    fig.tight_layout()      
    fig.savefig(save_path_name,bbox_inches='tight')

def make_win_top10_quad_heatmaps(df,stat_groups):
    '''
    Makes a figure with 4 subplots of heat maps showing the correlation between wins/top 10s and the Traditional and Strokes Gained statistics as well as the ranks for each. Used for EDA.
    INPUT:  df - data frame
            stat_groups - list of 4 statistics_group objects
    '''
    fig,axs = plt.subplots(2,2,figsize=(10,10))
    for i,ax in enumerate(axs.flatten()):
        corr = df[['Wins','Top 10']+stat_groups[i].column_names].corr()
        sns.heatmap(corr.iloc[:2,2:], annot=True,ax=ax)
        ax.set_title(stat_groups[i].name)
        ax.set_xticklabels(stat_groups.proper_names)
    fig.suptitle(f'{df.Year.unique()[0]}' if len(df.Year.unique()) == 1 else f'{df.Year.unique().min()} - {df.Year.unique().max()}')
    fig.tight_layout()
    year_string = f'{df.Year.unique()[0]}' if len(df.Year.unique()) == 1 else f'{df.Year.unique().min()}_{df.Year.unique().max()}'
    fig.savefig(f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/win_top10_quad_heatmaps_{year_string}.png')   

def make_violin_top_performer_plots(df,group,orientation='v',show_legend=True):
    '''
    Make violin plot of the specified statistic group to show the distribution of all players, and overlay the top performers.
    INPUT:  df - data frame
            group - statistics_group object - indicates what columns to use for figure
            orientation - str - 'v' or 'h' 
            show_legend - bool 
    '''
    if orientation == 'v':
        figsize=(12,10)
    else:
        figsize=(12,3*len(group))
    fig,ax = plt.subplots(figsize=figsize)
    sns.violinplot(data=df[group.column_names],inner='quartile',cut=0,scale='count',ax=ax,color='forestgreen',orient=orientation)
    sns.swarmplot(data=df[df['Top 10 rank']<=3][group.column_names],ax=ax,color='blue',edgecolor='black',linewidth=1,size=4,label='Golfer ranked in Top 3 for most Top 10 finishes in a year',orient=orientation)
    sns.swarmplot(data=df[df['Wins rank']<=3][group.column_names],ax=ax,color='gold',edgecolor='black',linewidth=1,size=4,label='Golfer ranked in Top 3 for most Wins in a year',orient=orientation)
    if orientation =='v':
        ax.set_xticklabels(group.proper_names)
        ax.set_ylabel(group.units)
    else:
        ax.set_yticklabels(group.proper_names)
        ax.set_xlabel(group.units)
    ax.set_title(f"Distribution of Golfers' {group.name}")
    if show_legend:
        handles,labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels,handles))
        ax.legend(by_label.values(),by_label.keys())
    fig.tight_layout()
    fig.savefig(f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/violins_with_top_players_overlaid_{group.name.replace(" ","_")}.png')

def make_player_overview_plot(df,player):
    '''
    Plots the strokes gained statistics and number of wins and top 10s for each year for an individual player.
    INPUT: df - data frame
           player -  str 
    '''
    fig,axs = plt.subplots(2,1,sharex=True)
    df[df['Player Name']==player].plot(x='Year',y=['SG:OTT','SG:APR','SG:ARG','Average SG Putts'],ax=axs[0])
    axs[0].set_ylabel('Strokes Gained')
    axs[0].legend(['SG:OTT','SG:APP','SG:ARG','SG:Putting'],bbox_to_anchor=(1,0.5),loc='center left')
    df[df['Player Name']==player].plot(x='Year',y=['Top 10','Wins'],ax=axs[1])
    axs[1].set_ylabel('Wins/Top 10s')
    axs[1].legend(['Top 10s','Wins'],bbox_to_anchor=(1,0.5),loc='center left')
    fig.suptitle(f'{player} Overview')
    fig.tight_layout()
    fig.savefig(f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/player_overview_{player.replace(" ","_")}.png')

def make_player_overview_plot(df,player,ranks=False):
    '''
    Plots the strokes gained statistics and number of wins and top 10s for each year for an individual player.
    INPUT: df - data frame
           player -  str 
    '''
    stat_columns = ['SG:OTT','SG:APR','SG:ARG','Average SG Putts']
    title_string = f'{player} Overview'
    filename_string = f'player_overview_{player.replace(" ","_")}'
    if ranks:
        stat_columns = [stat + ' rank' for stat in stat_columns]
        title_string = f'{player} Overview - Rank Based'
        filename_string = f'player_overview_rank_based_{player.replace(" ","_")}'
    fig,axs = plt.subplots(2,1,sharex=True)
    df[df['Player Name']==player].plot(x='Year',y=stat_columns,ax=axs[0])
    axs[0].set_ylabel('Strokes Gained')
    axs[0].legend(['SG:OTT','SG:APP','SG:ARG','SG:Putting'],bbox_to_anchor=(1,0.5),loc='center left')
    df[df['Player Name']==player].plot(x='Year',y=['Top 10','Wins'],ax=axs[1])
    axs[1].set_ylabel('Wins/Top 10s')
    axs[1].legend(['Top 10s','Wins'],bbox_to_anchor=(1,0.5),loc='center left')
    fig.suptitle(title_string)
    fig.tight_layout()
    fig.savefig(f'/home/rpeterson/Documents/dai/repos/pga_tour_analysis/images/{filename_string}.png')


if __name__ == "__main__":
    pass