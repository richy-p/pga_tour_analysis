
## TO DO:
X change nans to 0 for wins and top 10s  
X for each year rank each statistical category - this will nearly double the number of columns - how will ties be handled?    
x Look at the distribution of the statistics, how much do they vary between the players?  
x make heat map of just wins/top 10s vs the traditional statistics,   another with strokes gained statistics, and two more with the ranks for each  
_ Look at the player with the most wins/top 10s each year, where did they rank?  
_ violin plots with top players plotted - swarmplot or stripplot  
X organize/strucutre py files for execution  
X scatter plot of gir and putts (show why strokes gained is used)  
[ ] adjust plots for README.md - check on GitHub to make sure they look good  
[ ] clean up code
_ cumulative distibution (what percent of top performers are in the top X of each statistic)

**Accomplished yesterday:**
_ function for creating win and top 10 heat maps  
_ made violin plots of statistical categories overlaid with players with the most wins and top 10s  
X organize/strucutre py files for execution  
x build function for making the violin plots - or alternative plots  
X scatter plot of gir and putts (show why strokes gained is used)
-[x] redo heatmap with the correlation between just top performers    
-[x] started draft of readme

**Plan today: **   
-[ ] finish draft of read me   
-[ ] pretty some of figures

**MVP**
- two small heat maps of traditional and strokes gained statistics
- violin plots with top performers overlaid


Notes:   
Scatter plot of interesting points  
Could look at changes throught years


## Elevator pitch
"Drive for show, putt for dough"
Investigate PGA tour data from 2010-2018 - determin if one aspect of golf is more prevelant in top performers.


## Initial look

correlation heat map 
* traditional statistics between   .21-.31 except fairway %
* SG: .22-.27 except APR is .35 for wins and .46 top10, and OTT is .35 for top10  

Winners
* 157 out of 526 unique players

Top 10  
* 391 players  

Max wins in a year - 5 by Tiger in 2013  
Max top 10 in year - 14 by Spieth in 2015  

Overall
Dustin Johnson 13 Wins 59 top 10s


Ranked in the top 3 wins or top 10s
42 unique players, 73 data points


Column Name             

Player Name             Player Name
Year                    Year
Wins                    Wins
Top 10                  Top 10 Finishes
Fairway Percentage      Driving Accuracy
Avg Distance            Driving Distance
gir                     GIR
Average Scrambling      Scrambling
Average Putts           Putts Per Round
Average Score           Scoring Average    
SG:OTT                  SG: Off-the-Tee    
SG:APR                  SG: Approach-the-Green
SG:ARG                  SG: Around-the-Green
Average SG Putts        SG: Putting
Average SG Total        SG: Total

'Player Name','Year','Wins','Top 10 Finishes','Driving Accuracy','Driving Distance','GIR','Scrambling','Putts Per Round','Scoring Average    ','SG: Off-the-Tee    ','SG: Approach-the-Green','SG: Around-the-Green','SG: Putting','SG: Total'