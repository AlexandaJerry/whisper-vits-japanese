import pandas as pd
import os
import io
from glob import glob
import re
import numpy as np
import sys


#First change encoding from cp1252 to utf8 to keep Umlaute (e.g. ä, ö, ü)
def change_encoding(srt):
    with io.open(srt, 'r', encoding= "utf-8") as f:
        text = f.read()
        # process Unicode text
    with io.open(srt, 'w', encoding= 'utf-8-sig') as f:
        f.write(text)

def convert_srt_to_csv(file):
    with open(file, 'r',encoding= 'utf-8-sig') as h:
        sub = h.readlines()   #returns list of all lines

    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
    regex = re.compile(re_pattern)
    # Get start times
    times = list(filter(regex.search, sub))
    end_times = [time.split('--> ')[1] for time in times] #returns a list
    start_times = [time.split(' ')[0] for time in times]  #returns a list

    # Get lines
    lines = [[]]
    for sentence in sub:
        if re.match(re_pattern, sentence):
            lines[-1].pop()
            lines.append([])
        else:
            lines[-1].append(sentence)

    lines = lines[1:]   #all text in lists

    column_names = ['id','start_times', 'end_times', 'transcript']
    df_text = pd.DataFrame(columns=column_names)

    df_text['start_times'] = start_times
    df_text['end_times'] = end_times
    df_text['transcript'] = [" ".join(i).replace('\n', '') for i in lines]
    df_text['end_times'] = df_text['end_times'].replace(r'\n', '', regex=True)

    df_text['id'] = np.arange(len(df_text))
    id_extension = os.path.basename(file).replace('.srt', '_')
    id_extension = id_extension.replace(' ', '_')
    id_extension = id_extension.replace('-', '_')
    id_extension = id_extension.replace('.', '_')
    id_extension = id_extension.replace('__', '_')
    id_extension = id_extension.replace('___', '_')
    df_text['id'] = id_extension +  df_text['id'].map(str)

    file_extension = id_extension[:-1]

    #converting the times to milliseconds
    def convert_to_ms(time):
        h_ms = int(time[:2])*3600000
        m_ms = int(time[3:5])*60000
        s_ms = int(time[6:8])*1000
        ms = int(time[9:12])
        ms_total = h_ms + m_ms + s_ms + ms
        return(ms_total)

    def conv_int(start):
        new_start = int(start)
        return(new_start)

    df_text['start_times'] = df_text['start_times'].apply(convert_to_ms)
    df_text['end_times'] = df_text['end_times'].apply(convert_to_ms)

    df_text['start_times'] = df_text['start_times'].apply(conv_int)

    df_text.to_csv('./ready_for_slice/' + file_extension + '.csv', index=False, header=True, encoding='utf-8-sig')
