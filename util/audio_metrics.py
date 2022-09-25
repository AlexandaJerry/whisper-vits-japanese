#After running SRT_to_CSV_and_audio_split.py this script will return basic metrics of the pre-processed dataset.

import pandas as pd
from glob import glob
import wave
import contextlib
import datetime
import time
import os

def audio_metrics():
    data = pd.read_csv('./merged_csv/Filepath_Filesize.csv')
    print('------------------------------------------------------------------------------------------------------')
    print('COUNT OF FILES PER DATSET-SUBSET')
    print('------------------------------------------------------------------------------------------------------')

    #calculate length of subsets of dataset
    dev = pd.read_csv('./final_csv/dev.csv')
    test = pd.read_csv('./final_csv/test.csv')
    train = pd.read_csv('./final_csv/train.csv')
    df_all = pd.concat([dev,test,train])
    print('Length of dev-set: {} \nLength of test-set: {} \nLength of train-set: {}\
    \nLength of full-set: {}'.format(len(dev), len(test), len(train), len(df_all)))

    #prepare files for merge with audio length
    df_all = df_all.drop(['wav_filesize', 'transcript'], axis=1)

    #now individually merge with data df to catch audio length
    new_df = df_all.merge(data, on='wav_filename')


    #sum and avg of audio length for complete dataset
    avg_length = new_df['duration'].mean()
    sum = new_df['duration'].sum()
    length_of_audio = str(datetime.timedelta(seconds=sum))
    print('------------------------------------------------------------------------------------------------------')
    print('AUDIO METRICS FOR FULL DATASET')
    print('------------------------------------------------------------------------------------------------------')
    print('Average length of audio is: {} seconds.'.format(round(avg_length, 1)))
    print('Total length of audio in seconds is: {} seconds.'.format(round(sum, 1)))
    print('Total length of audio is: {}'.format(length_of_audio))
    print('------------------------------------------------------------------------------------------------------')

    #Calculate audio metrics per subset of the dataset:
    def calculate_audio_metrics_subset(subset):
        #prepare ch files for merge with audio length
        df = pd.read_csv('./final_csv/'+subset+'.csv')
        df = df.drop(['wav_filesize', 'transcript'], axis=1)

        data = pd.read_csv('./merged_csv/Filepath_Filesize.csv')
        #now individually merge with data df to catch audio length
        new_df = df.merge(data, on='wav_filename')
        #check to see that for every file a corresponding audio length was found in data df
        print('Length of dataframe {} that matches with the count of files in deepspeech csvs: {}'.format(subset,len(new_df)))

        #CH sum and avg of audio length
        avg_length = new_df['duration'].mean()
        sum_meteo = new_df['duration'].sum()
        length_of_audio = str(datetime.timedelta(seconds=sum))
        print('Average length of {} audio is: {}'.format(subset,round(avg_length, 1)))
        print('Total length of {} audio in seconds is: {} seconds'.format(subset,round(sum, 1)))
        print('Total length of {} audio is: {} '.format(subset, length_of_audio))

    print('AUDIO METRICS PER SUBSET:')
    print('------------------------------------------------------------------------------------------------------')
    print('TRAIN')
    print('-------')
    calculate_audio_metrics_subset('train')
    print('-------')
    print('DEV')
    print('-------')
    calculate_audio_metrics_subset('dev')
    print('-------')
    print('TEST')
    print('-------')
    calculate_audio_metrics_subset('test')
    print('------------------------------------------------------------------------------------------------------')
