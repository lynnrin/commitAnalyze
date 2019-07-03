import csv
import xml.etree.ElementTree as ET
import glob
import pandas as pd
import requests

FILE_INPUT = ''
target_file = './ant_data/xml/'
save_csv_file = './ant_data/csv/'

def send_line(message):
    line_token = 'nU7wXOhxtTSvpZI0HENbOJEIPAGXh4rp1oJufBt98GQ'
    endpoint = 'https://notify-api.line.me/api/notify'
    message = "\n{}".format(message)
    payload = {'message': message}
    header = {'Authorization': 'Bearer {}'.format(line_token)}
    requests.post(endpoint, data=payload, headers=header)

def change_dict_key(d, old_key, new_key, default_value=None):
    d[new_key] = d.pop(old_key, default_value)

def parseXML(InputFileName):
    tree = ET.parse(target_file + InputFileName + '.xml')
    root = tree.getroot()
    df_parse = pd.DataFrame()
    s_all = []
    
    for node in root:
        for package_name in node:
            s_v = {}
            s1 = {}
            m1 = {}
            m2 = {}
            for class_name in package_name:
                if class_name.tag == 'method':
                    s1 = class_name.attrib
                if class_name.tag == 'metrics':
                    m1 = class_name.attrib
                    keys = m1.keys()
                    for k in keys:
                        if 'class' not in k:
                            change_dict_key(m1, k, 'class' + k)
                    # m1_n = m1.rename(index=lambda x: 'class_' + str(x))
                for method in class_name:
                    if method.tag != 'metrics':
                        continue
                    m2 = method.attrib
                    s_v = {}
                    s_v.update(s1)
                    s_v.update(m1)
                    s_v.update(m2)
                    s_all.append(s_v)
                        # s_v = pd.concat([s1, m1, m2])
                        # df_parse = df_parse.append(s_v, ignore_index=True)

    df_parse = pd.io.json.json_normalize(s_all)
    df_parse.dropna(how='any', axis=0)
    df_parse.to_csv('./ant_data/csv/' + InputFileName + '.csv', index=False, sep='@')
    del df_parse


def allFileChangeCSV():
    import os
    num = 0
    try:
        f_n = glob.glob('./ant_data/xml/*.xml')
    
    except:
        print("err")
        return False
   
    for f in f_n:
        parseXML(os.path.splitext(f)[0].split('/')[-1])
        num += 1
        print("Done " + str(num) + " files")
    
    print("Done all file")
        


if __name__ == '__main__':
    # try:
        # send_line('start')
        allFileChangeCSV()
        # send_line('all clear')
    # except:
        # send_line('error')
