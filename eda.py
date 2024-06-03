#Questions to answer
#1. Which countries have the highest human freedom in 2021? What about over time? What is the highest score recorded?
#2. Which regions have the highest average human freedom, personal freedom, economic freedom?
#3. Which countries have a significalntly higher pf to ef or vice versa


#Import in necessary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns 

#Read in the cleaned dataframes
df_2023_f=pd.read_csv(r'C:\Users\chris\Desktop\Human Freedom Python\df_2023_f.csv')
hf_df=pd.read_csv(r'C:\Users\chris\Desktop\Human Freedom Python\hf_df.csv')
pf_df_f=pd.read_csv(r'C:\Users\chris\Desktop\Human Freedom Python\pf_df_f.csv')
ef_df_f=pd.read_csv(r'C:\Users\chris\Desktop\Human Freedom Python\ef_df_f.csv')


#/////////////////////////////////////////////////////////////////////////////
#1.
#Look at the highest scores recorded 
df_2023_f.sort_values(by='hf_score',ascending=False).head(10)
#The 10 higheset scores ever recorded all belong to Switzerland and New Zealand
#The highest score is from Switzerland in 2000 at 9.32, followed by them in 2002(9.30),2003(9.28), which is tied with New Zealand in 2000

#Look specifically at 2021
df_2023_f[df_2023_f['year']==2021].sort_values(by='hf_score',ascending=False).head(10)
#In 2021 specifically, the highest hf_score is Switzerland(9.01), New Zealand(8.88), Denmark(8.83)
#Intrestingly all of the top 10 are also in the top 10 of pf, but only the top 4 are in the top 10 of ef

#Create a horizontal bar chart for the countries with the top 20 highest hf
hf_2021_h=hf_df[hf_df['year']==2021][['countries','hf_score']].sort_values(by='hf_score',ascending=False).head(20)
hf_2021_h.set_index('countries',inplace=True)
hf_2021_h.plot(kind='barh')
plt.title('Top 20 Highest Human Freedom by Country in 2021')
plt.show()

#Bar chart for the 20 lowest hf countries
hf_2021_l=hf_df[hf_df['year']==2021][['countries','hf_score']].sort_values(by='hf_score').head(20)
hf_2021_l.set_index('countries',inplace=True)
hf_2021_l.plot(kind='barh')
plt.title('20 Countries with the Lowest Human Freedom in 2021')
plt.show()
#The lowest is the Syrian Arab Republic, followed by the Yemen Republic, Sudan, Myanmar, and Iran
#Almost all of the countries are either in Africa or the Middle East
#China is in the bottom 20 which is interesting considering they are the 2nd largest economy

#Look at the difference year over year of hf scores
#First invert the index so we can use diff then reinvert index
#Only take from year 2001 on since 2000 has no diff
hf_diff=hf_df.iloc[::-1]
hf_diff['hf_rot']=hf_diff.groupby('countries').hf_score.diff()
hf_diff=hf_diff.iloc[::-1]
hf_diff=hf_diff[hf_diff['hf_rot'].notna()]

#Look at the top 20 and bottom 20 differences in hf
hf_diff_h=hf_diff[['countries','year','hf_score','hf_rot']].sort_values(by='hf_rot', ascending=False).head(20)
hf_diff_h
#The country with the biggest change was Tunisia in 2011 with a change of 1.4(5.03 to 6.43), Gambia also had an increase over 1, with a 1.09 increase to 6.59 in 2017
#Most of these countries had a low score in the 4s or 5s so it makes sense they would be able to have a higher rate of change then a country that was already scored high


hf_diff_l=hf_diff[['countries','year','hf_score','hf_rot']].sort_values(by='hf_rot').head(20)
hf_diff_l
#The largest drop in hf came from Myanmar in 2021 with a drop of 1.55 to 3.88, Bahrain also had a drop of over 1 in 2011 by 1.02 to 5.30
#Interestingly, the United States comes into the top 20 with a drop of 0.47 to 8.32 in 2020
#Actually, 6 of the top 20 largest drops came in 2020 with another one coming in 2021


#Create bar charts for the top 20 and lowest 20 diff
#Set the index to country and year so that the bar chart has both of that info
hf_diff_h=hf_diff_h[['countries', 'year', 'hf_rot']]
hf_diff_hg=hf_diff_h.set_index(['countries', 'year'])
hf_diff_hg.plot(kind='barh')
plt.xlabel('Difference')
plt.ylabel(' ')
plt.title('20 Highest Difference in Human Freedom Over a Year')
plt.show()


hf_diff_l=hf_diff_l[['countries', 'year', 'hf_rot']]
hf_diff_lg=hf_diff_l.set_index(['countries','year'])
hf_diff_lg.plot(kind='barh')
plt.xlabel('Difference')
plt.ylabel(' ')
plt.title('20 Lowest Difference in Human Freedom Over a Year')
plt.show()


#/////////////////////////////////////////////////////////////////////////
#2 Regions


#Look at hf
hf_df['region_hf_mean']=round(hf_df.groupby(['region','year'])['hf_score'].transform('mean'),2)
region_hf_mean=hf_df.drop_duplicates(subset=['year','region'], keep='first')
region_hf_mean=region_hf_mean[['year','region','region_hf_mean']]
region_hf_mean[region_hf_mean['year']==2021].sort_values(by='region_hf_mean', ascending=False)
#The top 2 regions for hf are North America at 8.47 and Western Europe at 8.46 they are far and away the highest regions
#Middle East & North Africa is at the bottom by itself at 5.21, almost a whole point behind the Sub-Saharan Africa at 6.10

#Create a box plot for hf of 2021
sns.boxplot(x='hf_score', y='region', data=hf_df)
#There is a huge range for Middle East, Sub-Saharan Africa, and South Asia


plt.figure(figsize=(10,10))
for cat in region_hf_mean['region'].unique():
    sub=region_hf_mean[region_hf_mean['region']==cat]
    sns.lineplot(data=sub, x='year', y='region_hf_mean', label=f'{cat}')
plt.ylabel('hf_mean')
plt.title('Human Freedom by Region Over Time')
#The graph shows us what we aleady know with North America and Western Europe together at the top, but intersetingly they have fallen quite a bit around 2020
#There isn't really any movement of the rankings except that Eastern Europe is slightly above East Asian in 2021 when they were below them leadup to that point
#The gap between the Middle East & North Africa and everyone else is only getting wider with time, as they have been on a substancial down trend since 2010(Arab Spring started in 2010)



#Ef
#Look at the mean of ef for each region over time
ef_df_f['region_ef_mean']=round(ef_df_f.groupby(['region','year'])['ef_score'].transform('mean'),2)
region_ef_mean=ef_df_f.drop_duplicates(subset=['year','region'], keep='first')
region_ef_mean=region_ef_mean[['year','region','region_ef_mean']]
region_ef_mean[region_ef_mean['year']==2021].sort_values(by='region_ef_mean', ascending=False)
#In 2021, North America has the highest average economic freedom at 8.06, followed by Western Europe at 7.77
#Sub-Saharan Africa and Middle East & North Africa have the lowest EF at 5.94 and 5.95 respectively

#Create a box plot for each region to make it easier to compare across region
sns.boxplot(x='ef_score', y='region',data=ef_df_f)
#In the box-plot for 2021 ef we see that North America has the smallest range, with middle East & North Africa having the largest range, much larger than any other region


#Create a for loop to make a graph that plots the mean of each region over time
plt.figure(figsize=(12,12))
for cat in region_ef_mean['region'].unique():
    sub=region_ef_mean[region_ef_mean['region']==cat]
    sns.lineplot(data=sub, x='year', y='region_ef_mean', label=f'{cat}')
plt.ylabel('ef_mean')
plt.title('Economic Freedom by Region Over Time')
#By looking at the line chart, North America, Western Europe, and East Asia have all remained in the 1,2,3 spots respectively from 2000 to 2021
#A lot more movement here than in hf with all except the top 3 changing rank at somepoint
#The seemingly largest risers have been South Asia rising from ~6.0 ef to ~6.5, and Eastern Europe rising from ~6.5 ef to ~7.2(One point being 7th place to now ending in 4th)


#Make same graphs for pf
#Look at the mean of each regions pf
pf_df_f['region_pf_mean']=round(pf_df_f.groupby(['region','year'])['pf_score'].transform('mean'),2)
region_pf_mean=pf_df_f.drop_duplicates(subset=['year','region'], keep='first')
region_pf_mean=region_pf_mean[['year','region','region_pf_mean']]
region_pf_mean[region_pf_mean['year']==2021].sort_values(by='region_pf_mean', ascending=False)
#When looking at pf by region, Western Europe is atop at 8.95, followed by North America at 8.76, and then Oceania at 8.32 which was middle of the pack in ef
#The lowest regions are Middle East & North Africa at 4.67 and South Asia at 5.86
#Intrestingly Sub-Saharan Africa is only third from the bottom at 6.20, when it was the lowest for ef at 5.94 and the 2nd lowest for hf

#Create a box plot of pf of 2021
sns.boxplot(x='pf_score',y='region', data=pf_df_f)
#South Asia, Middle East, and Sub-Saharan Africa all have the largest ranges

#Create plot of pf score over time
plt.figure(figsize=(10,10))
for cat in region_pf_mean['region'].unique():
    sub=region_pf_mean[region_pf_mean['region']==cat]
    sns.lineplot(data=sub, x='year', y='region_pf_mean', label=f'{cat}')
plt.ylabel('pf_mean')
plt.title('Personal Freedom by Region Over Time')
#By looking at the graph we can see three distinct clusters of scores. 
#The top 6 regions(Western Europe, North America, Oceania, Eastern Europe, East Asia, and Latin America & the Caribbean)
#The middle 3 regions(Caucasus & Central Asia, Sub Saharan Africa, and South Asia)
#The bottom(Middle East & North Africa)
#The ranking in 2000 is the same as in 2021, but there was movement of rankings over the years, particularly in the middle regions
#There is a noticable drop in personal freedom around 2020 likely coinciding with the pandemic lockdowns
#In 2012-2013 the Middle East & North Africa which was already the lowest had an extreme drop that persists until 2021



#///////////////////////////////////////////////////////////////////////////
#3(High in one category but low in other in 2021)

#Create a scatterplot for pf vs ef in 2021
#Create a df that just has 2021 data
df_2021=df_2023_f[df_2023_f['year']==2021]
#Assign color to each individual region
region_colors={'Sub-Saharan Africa':'tab:green', 'Middle East & North Africa':'tab:orange', 'South Asia':'tab:grey',
       'Latin America & the Caribbean':'tab:red', 'North America':'tab:olive', 'Eastern Europe':'tab:blue',
       'East Asia':'tab:cyan', 'Caucasus & Central Asia':'tab:purple', 'Western Europe':'tab:pink',
       'Oceania':'tab:brown'}
#Create a color df to be put in as the color for the scatter plot
df_2021['Colors']=df_2021['region'].map(region_colors)

#Scatter plot of all countries in 2021 with color based on region
pf_ef_2021=df_2021.plot.scatter(x='pf_score',y='ef_score', c=df_2021['Colors'])
plt.title('Economic Freedom vs Personal Freedom in 2021')

#Create Data frame with countries based on difference between ef and pf(pf - ef)(+ means higher pf)(- mean higher ef)
ep_diff=df_2021
ep_diff['pf_ef_diff']=ep_diff['pf_score']-ep_diff['ef_score']

ep_diff[['countries', 'region','pf_ef_diff', 'pf_score', 'ef_score', 'hf_score' ]].sort_values(by='pf_ef_diff', ascending=False).head(10)
#The countries with a higher pf than ef are Argentina with a 3.57 difference, Suriname with a 2.65 difference and Timor-Leste with a 2.47 difference.
ep_diff[['countries', 'region','pf_ef_diff', 'pf_score', 'ef_score', 'hf_score' ]].sort_values(by='pf_ef_diff', ascending=False).tail(10)
#The countries with a higher ef than pf are Saudi Arabia with a 3.62 difference, Bahrain with a 3.39 difference and the UAE with a 2.78 difference.

#Create a scatter plot of the difference
ep_diff.plot.scatter(x='pf_ef_diff', y='region', c=ep_diff['Colors'])
#We see that having a difference of about 1.7 or greater puts you in the top 10.
#The Middle East & North Africa is skewed towards having a higher ef than pf with 5 of the top 10, but no country having a pf difference greater than 1
#Latin America & The Caribbean have almost the opposite story with 5 of the top 10 greater pf difference and only 1 ef difference of greater then 1
#Sub-Saharan Africa has difference in both high pf and ef, but has a slight skew towards having a higher pf difference
#Western Europe has a very close spread hovering in the 0 to 1.7 greater pf difference, despite having a large amount of countries


#/////////////////////////////////////////////////////////////////////////////////////////////
#Extra info to think about
#North America scores high in all of the categories but it is only the US and Canada
#Helpful code
df_2023_f[(df_2023_f['region']=='Oceania')&(df_2023_f['year']==2021)]
