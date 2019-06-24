import pandas as pd
from git import *

df = pd.read_csv('all_refactorings.csv', sep='#')
df.drop(df.index[df['RefactoringType'] != 'Extract Method'], inplace=True)
del df['RefactoringType']
df = df.rename(columns={'BeforeClass': 'Class', 'BeforeMethod': 'Method'})

df['parent'] = df['CommitId']
df['1prev'] = df['CommitId']
df['2prev'] = df['CommitId']
df['3prev'] = df['CommitId']
df['4prev'] = df['CommitId']
df['5prev'] = df['CommitId']


def parent_commit(now, prev):
  for i, id in df.iterrows():
    # print(i)
    for j in repo.iter_commits(id[now], max_count=1):
      df.at[i,prev] = j.parents[0].hexsha


repo = Repo('ant/')
parent_commit('CommitId', 'parent')
parent_commit('parent', '1prev')
parent_commit('1prev', '2prev')
parent_commit('2prev', '3prev')
parent_commit('3prev', '4prev')
parent_commit('4prev', '5prev')

del df['2prev']
del df['4prev']


df.to_csv('Extract.csv',sep='#',index=False)