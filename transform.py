import pandas as pd
from git import *

df = pd.read_csv('refactoring.csv', sep='@|#')
del df['method']

df['parent'] = df['commitId']
df['1prev'] = df['commitId']
df['2prev'] = df['commitId']
df['3prev'] = df['commitId']
df['4prev'] = df['commitId']
df['5prev'] = df['commitId']


def parent_commit(now, prev):
  for i, id in df.iterrows():
    # print(i)
    for j in repo.iter_commits(id[now], max_count=1):
      df.at[i,prev] = j.parents[0].hexsha


repo = Repo('ant/')
parent_commit('commitId', 'parent')
parent_commit('parent', '1prev')
parent_commit('1prev', '2prev')
parent_commit('2prev', '3prev')
parent_commit('3prev', '4prev')
parent_commit('4prev', '5prev')

del df['2prev']
del df['4prev']


df.to_csv('Extract.csv',sep='#',index=False)
