# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
df_ipl = pd.read_csv(path)


df_ipl['year'] = df_ipl['date'].apply(lambda x: x[:4])
df_ipl.head(5)
# Plot the wins gained by teams across all seasons
match_data = df_ipl.drop_duplicates(subset='match_code').reset_index(drop=True)
wins = match_data['winner'].value_counts()

wins.plot(kind='bar')
plt.title('Total Wins for all seasons')
plt.xlabel('Teams')
plt.ylabel('Win Count')
# Plot Number of matches played by each team through all seasons
temp = pd.melt(match_data, id_vars = ['match_code'],value_vars = ['team1','team2'])
temp.sort_values(by=['match_code','variable'])
played = temp.value.value_counts()
played.plot.bar(title='No. of matches')
# Top bowlers through all seasons
wick_filter = (df_ipl['wicket_kind'] == 'caught') | (df_ipl['wicket_kind'] =='bowled') | (df_ipl['wicket_kind'] =='lbw') | (df_ipl['wicket_kind'] =='stumped') | (df_ipl['wicket_kind'] =='caught and bowled')

wickets = df_ipl[wick_filter]
wickets['bowler'].value_counts()[:10].plot(kind = 'bar')
# How did the different pitches behave? What was the average score for each stadium?
score_per_venue = df_ipl.loc[:,['match_code','venue','inning','total']]

total_score = score_per_venue.groupby(['match_code','venue','inning']).agg({'total':'sum'}).reset_index()
avg_score = total_score.groupby(['venue','inning'])['total'].mean().reset_index()
avg_score.head(5)

plt.figure(figsize=(19,8))
plt.plot(avg_score[avg_score['inning']==1]['venue'],
        avg_score[avg_score['inning']==1]['total'],'*-b',
        label = 'inning1')
plt.plot(avg_score[avg_score['inning']==2]['venue'],
        avg_score[avg_score['inning']==2]['total'],'o-r',
        label = 'inning2')
plt.xticks(rotation = 90)
plt.legend(loc='upper right')
plt.show()
# Types of Dismissal and how often they occur
diss = df_ipl.groupby(['wicket_kind']).count().reset_index()[['wicket_kind','year']].rename(columns={'year':'count'})
plt.figure(figsize=(10,10))
plt.pie(diss['count'],autopct='%1.0f%%')
plt.legend(labels=diss['wicket_kind'],loc='upper right')
plt.show()
# Plot no. of boundaries across IPL seasons
boundary = df_ipl.loc[:,['runs','year']]
fours = boundary[boundary['runs']==4].groupby(['year'])['runs'].count()
sixes = boundary[boundary['runs']==6].groupby(['year'])['runs'].count()

#print(type(fours))
#sixes.value_counts()

plt.figure(figsize=(10,8))

plt.plot(fours.index,fours,'-b',label='fours')
plt.plot(sixes.index,sixes,'-r',label='sixes')
plt.show()
# Average statistics across all seasons

matches_played = match_data.groupby(['year'])['total'].sum()
avg_data = pd.DataFrame([matches_played,fours,sixes])
avg_data.index=['No of matches','Fours','Sixes']
avg_data.T.plot(kind='bar',figsize = (5,5)) #transpose by using T



