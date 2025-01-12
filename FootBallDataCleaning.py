''' International football results from 1872 to 2024 data cleaning
Source : https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017'''

import zipfile
import math
import collections
import openpyxl


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as pp

#import csv datafile
goalscorers = pd.read_csv('goalscorers.csv')
matchResults = pd.read_csv('results.csv')
shootouts = pd.read_csv('shootouts.csv')

#split data into two tables
franceMatchResults = matchResults[(matchResults.home_team == 'France') | (matchResults.away_team == 'France')]
franceMatchResultsHome = matchResults[(matchResults.home_team == 'France')]
franceMatchResultsAway = matchResults[(matchResults.away_team == 'France')]

'''creating a new column called result in the franceMatchResultsHome DataFrame, 
based on the scores of home and away matches '''

franceMatchResultsHome.loc[:, 'result'] = franceMatchResultsHome[['home_score', 'away_score']].apply(
    lambda row: 'draw' if row['home_score'] == row['away_score']
    else 'lose' if row['home_score'] < row['away_score']
    else 'win', axis=1
)
franceMatchResultsAway.loc[:, 'result'] = franceMatchResultsAway[['home_score', 'away_score']].apply(
    lambda row: 'draw' if row['home_score'] == row['away_score']
    else 'lose' if row['home_score'] > row['away_score']
    else 'win', axis=1
)

#rewrite franceMatchResults with the new data
franceMatchResults = pd.concat([franceMatchResultsHome, franceMatchResultsAway], axis=0).reset_index(drop=True)

#removes the column city 'cause we already have the column country
franceMatchResults.drop(columns=['city'], inplace=True)

print(franceMatchResults.head(10))

#Checking for the Neutral variable values 
print(set(franceMatchResults.neutral))

'''The neutral column has only two values, True and False. we might need it later in the dashboard'''

#Goal Scorers Data
#split data into two tables
'''Extracting france goal scorers from the goalscorers DataFrame'''
franceGoalScorers = goalscorers[(goalscorers.home_team == 'France') | (goalscorers.away_team == 'France')]

franceMatchResults = franceMatchResults.groupby(['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'country', 'neutral', 'result']).size().sort_values(ascending=False).reset_index(name='count')
print(franceMatchResults.head(10))

franceMatchResults.drop(columns=['count'], inplace=True)
print(franceMatchResults.head(10))

franceMatchResults = franceMatchResults.groupby(['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'country', 'neutral', 'result']).size().sort_values(ascending=False).reset_index(name='count')
print(franceMatchResults.head(10))

#Exporting the cleaned data to a new excel file
franceMatchResults.to_excel('franceMatchResults.xlsx', index=False)
franceGoalScorers.to_excel('franceGoalScorers.xlsx', index=False)