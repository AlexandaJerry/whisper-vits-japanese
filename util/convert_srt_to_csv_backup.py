## This script will first change the encoding of srt files and then convert it to a csv

import pandas as pd
import os
import io
from glob import glob
import re
import numpy as np
import sys

# Create csv directory

csv_path = './csv'

if not os.path.exists(csv_path):
    try:
        os.mkdir(csv_path)
    except OSError:
        print('Creation of directory %s failed' %csv_path)

#Check if srt_files directory exists and contains srt files

srt_path = './srt_files'

if os.path.exists(srt_path):
    print('Folder %s exists.. continuing processing..' %srt_path)
else:
    print('Folder "srt_files" is missing')
    try:
        os.mkdir(srt_path)
    except OSError:
        print('Creation of directory %s failed' %srt_path)
    else:
        print('Successfully created the directory %s' %srt_path)
    print('--> Please add srt files to folder %s' %srt_path)
    sys.exit()

#First change encoding from cp1252 to utf8 to keep Umlaute (e.g. ä, ö, ü)
def change_encoding(srt):
    with io.open(srt, 'r', encoding='cp1252') as f:
        text = f.read()
        # process Unicode text
    with io.open(srt, 'w', encoding='utf8') as f:
        f.write(text)

def convert_srt_to_csv(file):
    with open(file, 'r') as h:
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
    file_extension = id_extension.replace('o_', 'o')
    file_extension = file_extension.replace('_.', '.')
    df_text['id'] = id_extension +  df_text['id'].map(str)

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

    df_text['start_times'] = df_text['start_times'].apply(convert_to_ms) * 0.975 #subtracting 2.5% of start_time because of scarce splitting
    df_text['end_times'] = df_text['end_times'].apply(convert_to_ms)

    df_text['start_times'] = df_text['start_times'].apply(conv_int)

    df_text.to_csv('./csv/' + file_extension + '.csv', index=False, header=True, encoding='utf-8-sig')

srt_counter = len(glob('./srt_files/' + '*.srt'))

if srt_counter == 0:
    print('!!! Please add srt_file(s) to %s-folder' %srt_path)
    sys.exit()

print('Encoding srt_file(s) to utf8...')
for srt in glob('./srt_files/*.srt'):
    change_encoding(srt)
print('Encoding of %s-files changed' %srt_counter)

print('Extracting information from srt_file(s) to csv_files')
for file in glob('./srt_files/*.srt'):
    convert_srt_to_csv(file)
print('%s-file(s) converted and saved as csv-files to ./csv' %srt_counter)
