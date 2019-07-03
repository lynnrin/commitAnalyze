# -*- coding: utf-8 -*-
from git import *

repo = Repo("~/commitAnalyze/ant")
with open("antSha.csv", mode='w') as f:
  for item in repo.iter_commits('master', max_count=1000000):
    if len(item.parents) == 1:
      f.write(item.hexsha+"\n")
