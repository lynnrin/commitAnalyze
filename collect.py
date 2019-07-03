from git import *
import os
import csv
import subprocess
import glob
import pandas as pd

target = "ant/"

def rename(home, target, target_file):
    try:
        f_n = glob.glob(home + target_file + "/metric*")
        file_name = home + target_file + "_data/xml/" + target + ".xml"
        rename = "mv " + f_n[0] + " " + file_name
        subprocess.run(rename, shell=True)
        return True
    except:
        return False

def play_jar():
    l = []
    num=1
    target_file = "commitAnalyze/ant"
    currentFileList = os.listdir('/home/lynnrin/' + target_file+'_data/xml/')
    home = "/home/lynnrin/"
    jar_cmd = ["java", "-jar", home + "jxmetrics/org.jtool.jxmetrics/build/libs/jxmetrics-1.0-all.jar", "-target", home + target_file  + "/", "-name", "metric"]
    df = pd.read_csv('Extract.csv',usecols=['parent', '3prev', '5prev'],sep='#')
    repo = Repo(target)
    for i, row in df.iterrows():
        if (row['parent'] in l) == False:
            l.append(row['parent'])
        if (row['3prev'] in l) == False:
            l.append(row['3prev'])
        if (row['5prev'] in l) == False:
            l.append(row['5prev'])

    print(len(l))
    for i in l:
        if (i in currentFileList) == True:
            continue
        repo.git.reset('--hard', i)
        subprocess.run(jar_cmd)
        if rename(home, i, target_file):
            print("Done, " + str(num) + "files")
            num = num + 1

play_jar()
