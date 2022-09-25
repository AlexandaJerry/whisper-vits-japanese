#Create csv with filepath and -size in preparation for final DS training-csv

import pandas as pd
import os
from glob import glob
import wave
import contextlib


def create_DS_csv (path):
    #this function holds the code to extract the filepath and filesize of all audio in the respective directory
    print('Extracting filepath and -size for every .wav file in ./sliced_audio')
    data = pd.DataFrame(columns=['wav_filename', 'wav_filesize', 'duration'])
    df = pd.DataFrame(columns=['wav_filename', 'wav_filesize', 'duration'])

    for entry in glob(path +'*.wav'):
        filepath = os.path.abspath(entry) #主要需要文件名
        filesize = os.path.getsize(entry)
        with contextlib.closing(wave.open(entry, 'rb')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        df['wav_filename'] = [filepath]
        df['wav_filesize'] = [filesize]
        df['duration'] = [duration]
        data = data.append(df)
    data.to_csv('./merged_csv/Filepath_Filesize.csv', header=True, index=False, encoding='utf-8-sig')
