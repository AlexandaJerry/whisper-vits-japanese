from unittest import skip
import pandas as pd
import os, io, re, sys, time, datetime
from glob import glob
import numpy as np

from util.creating_directories import create_directories
from util.convert_srt_to_csv import change_encoding
from util.convert_srt_to_csv import convert_srt_to_csv
from util.change_sample_rate import pre_process_audio
#from util.extract_audio import wmv_to_wav
#from util.extract_audio import mp4_to_wav
from util.slice_audio import split_files
from util.create_DS_csv import create_DS_csv
from util.merge_csv import merge_csv
from util.merge_transcripts_and_files import merge_transcripts_and_wav_files
from util.clean import clean_unwanted_characters
from util.split import split_dataset
from util.audio_metrics import audio_metrics
#from util.trans_numbers import translate_numbers

start_time = time.time()
#Check if srt_files directory exists and contains srt files
srt_path = './srt_files/'

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

#Check if audio directory exists and contains wmv or wav files

audio_path = './audio/'

if os.path.exists(audio_path):
    print('Folder %s exists.. continuing processing..' %audio_path)
else:
    print('Folder "audio" is missing')
    try:
        os.mkdir(audio_path)
    except OSError:
        print('Creation of directory %s failed' %audio_path)
    else:
        print('Successfully created the directory %s' %audio_path)
    print('--> Please add wav or wmv files to folder %s' %audio_path)

srt_counter = len(glob('./srt_files/' + '*.srt'))

if srt_counter == 0:
    print('!!! Please add srt_file(s) to %s-folder' %srt_path)

create_directories()
#Changing encoding from "cp1252" (a.k.a Windows 1252)to "utf-8-sig"
print('Encoding srt_file(s) to utf8...')
for srt in glob('./srt_files/*.srt'):
    change_encoding(srt)
print('Encoding of %s-file(s) changed' %srt_counter)
print('---------------------------------------------------------------------')

print('Extracting information from srt_file(s) to csv_files')
for file in glob('./srt_files/*.srt'):
    convert_srt_to_csv(file)
print('%s-file(s) converted and saved as csv-files to ./csv' %srt_counter)
print('---------------------------------------------------------------------')

pre_process_audio(audio_path)
print('Pre-processing of audio files is complete.')
print('---------------------------------------------------------------------')

#now slice audio according to start- and end-times in csv
print('Slicing audio according to start- and end_times of transcript_csvs...')
for item in glob('./ready_for_slice/*.csv'):
    wav_item = item.replace('.csv','.wav')
    if os.path.exists(wav_item):
        split_files(item, wav_item)
    else:
        next
wav_counter = len(glob('./sliced_audio/' + '*.wav'))
print('Slicing complete. {} files in dir "sliced_audio"'.format(wav_counter))
print('---------------------------------------------------------------------')

create_DS_csv('./sliced_audio/')
print('DS_csv with Filenames - and sizes created.')
print('---------------------------------------------------------------------')

#now join all seperate csv files
merge_csv('./ready_for_slice/')
print('Merged csv with all transcriptions created.')

print('---------------------------------------------------------------------')
transcript_path = './merged_csv/Full_Transcript.csv'
DS_csv = './merged_csv/Filepath_Filesize.csv'
df_final = pd.DataFrame()
df_transcripts = pd.read_csv(transcript_path)
df_files = pd.read_csv(DS_csv)

#by splitting the path at / and then choosing -1, the filename can be extracted
def remove_path(path):
    path = path.split('\\')[-1]
    return path

df_files['id'] = df_files['wav_filename'].apply(remove_path)

#filter out duration of less than 10 seconds
def convert(duration):
    time = float(duration)
    return time
df_files['duration'] = df_files['duration'].apply(convert)
df_files = df_files[df_files['duration']<12.00]
df_files = df_files[df_files['duration']>2.00]

#drop unnecessary columns
df_transcripts.drop(['start_times','end_times'], axis=1, inplace=True)

df_files['id'] = df_files['id'].replace('.wav', '', regex=True)

#merge on column id
df_final = pd.merge(df_transcripts, df_files, on='id')
df_final.drop(['id'], axis=1, inplace=True)
#rearrange columns
df_final = df_final[['wav_filename', 'duration', 'transcript']]

df_final.to_csv('./merged_csv/DS_training_final.csv', header=True, index=False, encoding='utf-8-sig')
print('Final DS csv generated.')
print('---------------------------------------------------------------------')

final_csv_path = 'DS_training_final.csv'
clean_unwanted_characters(final_csv_path)
print('Unwanted characters cleaned.')
print('---------------------------------------------------------------------')

#write transcript to text-file for language model
df_text = pd.read_csv('./merged_csv/DS_training_final_merged.csv')
df_text[['wav_filename','transcript']].to_csv('./filelists/train_filelist.txt', header=None, index=None, mode='a', sep='|')
df_text[['wav_filename','transcript']].to_csv('./filelists/val_filelist.txt', header=None, index=None, mode='a', sep='|')

import shutil,os,re
slice_path = './ready_for_slice'
merged_csv_files = './merged_csv'
final_csv_path = './final_csv'

# #shutil.rmtree(slice_path)
if os.path.exists(slice_path):
    try:
        shutil.rmtree(slice_path)
    except:
        skip

if os.path.exists(final_csv_path):
    try:
        shutil.rmtree(final_csv_path)
    except:
        skip
if os.path.exists(merged_csv_files):
    try:
        shutil.rmtree(merged_csv_files)
    except:
        skip        

#evaluate the scripts execution time
end_time = time.time()
exec_time = str(datetime.timedelta(seconds=end_time-start_time))

print('The script took {} to run'.format(exec_time))
print('********************************************************************************************************')


'''
Sources:
 - Downsampling wav-files: https://stackoverflow.com/questions/30619740/python-downsampling-wav-audio-file
 - Converting to 16-bit files: https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
 - Extract audio (wav) from wmv or mp4: https://zulko.github.io/moviepy/
 - Extract audio (wav) from wmv or mp4: https://medium.com/@steadylearner/how-to-extract-audio-from-the-video-with-python-aea325f434b6
 - Dataset-split: https://stackoverflow.com/questions/38250710/how-to-split-data-into-3-sets-train-validation-and-test

Further information:
 - README.md (https://github.com/tobiasrordorf/SRT-to-CSV-and-audio-split)
'''
