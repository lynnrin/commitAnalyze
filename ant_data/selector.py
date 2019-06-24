import pandas as pd
l = []
df = pd.read_csv('../Extract.csv',sep='#')
for i, row in df.iterrows():
    if (row['parent'] in l) == False:
        l.append(row['parent'])
    if (row['3prev'] in l) == False:
        l.append(row['3prev'])
    if (row['5prev'] in l) == False:
        l.append(row['5prev'])

import subprocess

for i in l:
   subprocess.run("mv ./xml/" + i + ".xml ./true_xml/", shell=True) 
