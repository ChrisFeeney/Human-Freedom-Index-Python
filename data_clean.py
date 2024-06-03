import pandas as pd
import numpy as np
#Read in the csv for 2023
df_2023 = pd.read_csv(r'C:\Users\chris\Desktop\Human Freedom Python\2023-Human-Freedom-Index-Data.csv')
df_2023

#Take a look at high level information
#There is 146 columns with 3630 rows
#This includes data from 2000-2021
df_2023.info()
df_2023.describe()
#Drop duplicates if they exist
df_2023.drop_duplicates()

#Set the amount of columns displayed to 146
pd.set_option('display.max.columns', 146)
pd.set_option('display.max.rows', 200)
df_2023
#look at how many NULL values there are per column
df_2023.isnull().sum()
df_2023.columns

#Create dfs for each group of values
#Create a variable that has the columns that all the new tables should have
#Create new dfs that only have columns that begin with pf,hf,ef
#Concat the add_columns to each df
add_columns=['year', 'iso', 'countries','region']

hf_df=df_2023.filter(regex='^hf_')
hf_df=pd.concat([df_2023[add_columns], hf_df], axis=1)

pf_df=df_2023.filter(regex='^pf_')
pf_df=pd.concat([df_2023[add_columns], pf_df], axis=1)

#filter down the pf_df to only include the encompassing columns instead of everysingle one
#This just makes the data simpler to deal with
pf_df_f=pf_df[['year','iso','countries','region','pf_score','pf_rank','pf_rol','pf_ss','pf_movement','pf_religion','pf_assembly','pf_expression','pf_identity']]
pf_df_f

ef_df=df_2023.filter(regex='^ef_')
ef_df=pd.concat([df_2023[add_columns], ef_df], axis=1)

#Filtered down the ef_df to only enclude encompassing columns
ef_df_f=ef_df[['year','iso','countries','region','ef_score','ef_rank','ef_government','ef_legal','ef_money','ef_trade','ef_regulation']]
ef_df_f


#/////////////////////////////////////
#Look at each df individually to decide how to best clean

#There are 350 rows of nan values in all hf categories
#All of the countries with nan for hf_score have nan for all hf categories
no_hf=pd.isnull(hf_df['hf_score'])
hf_df[no_hf]

#Look at where there are nan values for pf_score
#Not all countries that have nan for pf_score have nan for all pf columns
no_pf=pd.isnull(pf_df_f['pf_score'])
pf_df_f[no_hf]

#Look at where there are nan values for ef_score
#Not all countries that have nan for ef_score have nan for all ef columns
no_ef=pd.isnull(ef_df_f['ef_score'])
ef_df_f[no_ef]


#/////////////////////////////////////////////////////////////////////////////////////////////
#Fill in each column of the ef_df with a mean value grouped by the country
def fill_na(ef_df_f, group_countries, var_col):
    for col in var_col:
        country_mean=ef_df_f.groupby(group_countries)[col].transform('mean')
        ef_df_f[col]=ef_df_f[col].fillna(country_mean)
    return ef_df_f

columns=['ef_government','ef_legal','ef_money','ef_trade','ef_regulation']
ef_df_f=fill_na(ef_df_f, 'countries', columns)


#Fill in the null variables for pf which is only pf_identity
country_mean_pf=pf_df_f.groupby('countries')['pf_identity'].transform('mean')
pf_df_f['pf_identity']=pf_df_f['pf_identity'].fillna(country_mean_pf)


#Check to see if there any null values in the pf and ef df other than score and rank
pf_df_f.isnull().sum()
ef_df_f.isnull().sum()
#/////////////////////////////////////////////////////////////////////////////////

#It seems as though if a country does not have ef and pf scores then it also won't have an hf score

#Look at the specific countries where there are nan values
spec_count=['Canada']
pf_df_f[pf_df_f['countries'].isin(spec_count)]
#By exploring Canada it appears that the pf_score and ef_score is just the average of all the main indicators
#Can try to fit scores for all countries that don't have by using means in the columns that don't have values


#Now we will calculate the score for pf and ef which is just the average of the main variables
#Create a variable that calculates the mean of the main variables of ef and then replace na of score with it
#Then round the score so that is back to 2 decimals
mean_ef=ef_df_f.loc[:,['ef_government','ef_legal','ef_money','ef_trade','ef_regulation']].mean(axis=1)
ef_df_f['ef_score']=ef_df_f['ef_score'].fillna(mean_ef)
ef_df_f['ef_score']=round(ef_df_f['ef_score'],2)
ef_df_f

#Do the same thing for pf
mean_pf=pf_df_f.loc[:,['pf_rol','pf_ss','pf_movement','pf_religion','pf_assembly','pf_expression','pf_identity']].mean(axis=1)
pf_df_f['pf_score']=pf_df_f['pf_score'].fillna(mean_pf)
pf_df_f['pf_score']=round(pf_df_f['pf_score'],2)
pf_df_f

#Now that we have the pf_score and ef_score for all countries for every year we can fill in all of the null hf scores
sum_hf=ef_df_f['ef_score'].add(pf_df_f['pf_score'])
mean_hf=sum_hf/2
hf_df['hf_score']=hf_df['hf_score'].fillna(mean_hf)
hf_df

#Check to make sure there is only null values for rank and quartile
hf_df.isnull().sum()
pf_df_f.isnull().sum()
ef_df_f.isnull().sum()
#///////////////////////////////////////////////////////////////////////////
#Merge all the seperate dfs into one main, through outer joins
#Inverse the index so that it is filtered by year desc
df_2023_f=hf_df.merge(pf_df_f, how='outer', on=['year','iso','countries','region'])
df_2023_f=df_2023_f.merge(ef_df_f, how='outer', on=['year','iso','countries','region'])
df_2023_f[:]=df_2023_f[::-1]
df_2023_f


#////////////////////////////////////////////////////////////////////////////////
#Cleaned data sets containing each countries main indicators and score
ef_df_f
pf_df_f
hf_df
df_2023_f

#Create csvs for each df so the progress is not lost
ef_df_f.to_csv(r'C:\Users\chris\Desktop\Human Freedom Python\ef_df_f.csv', index=False)
pf_df_f.to_csv(r'C:\Users\chris\Desktop\Human Freedom Python\pf_df_f.csv', index=False)
hf_df.to_csv(r'C:\Users\chris\Desktop\Human Freedom Python\hf_df.csv', index=False)
df_2023_f.to_csv(r'C:\Users\chris\Desktop\Human Freedom Python\df_2023_f.csv', index=False)