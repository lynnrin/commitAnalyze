import csv
import lxml.etree as ET
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

def parseXML(InputFileName):
    tree = ET.parse(target_file + InputFileName + '.xml')
    root = tree.getroot()
    df_parse = pd.DataFrame()
    
    for node in root:
        print('next')
        for package_name in node:
            s1 = pd.Series()
            # m1 = pd.Series()
            m1_n = pd.Series()
            m2 = pd.Series()
            for class_name in package_name:
                if class_name.tag == 'method':
                    s1 = pd.Series(class_name.attrib.values(), index=class_name.attrib.keys())
                if class_name.tag == 'metrics':
                    m1 = pd.Series(class_name.attrib.values(), index=class_name.attrib.keys())
                    m1_n = m1.rename(index=lambda x: 'class_' + str(x))
                for method in class_name:
                    if method.tag == 'metrics':
                        m2 = pd.Series(method.attrib.values(), index=method.attrib.keys())
                        s_v = pd.concat([s1, m1_n, m2])
                        df_parse = df_parse.append(s_v, ignore_index=True)
    df_parse.dropna(how='any', axis=1)
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
        break
    
    print("Done all file")
        


if __name__ == '__main__':
    # try:
        # send_line('start')
        allFileChangeCSV()
        # send_line('all clear')
    # except:
        # send_line('error')