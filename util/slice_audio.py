#Slice audio files based on start and end times in csv files
from pydub import AudioSegment
import os
import pandas as pd

def split_files(item, wav_item):
    song = AudioSegment.from_wav(wav_item)
    df = pd.read_csv(item)

    def audio_split(df):
        split = song[df['start_times']:df['end_times']]
        split.export('./sliced_audio/' + df['id'] + '.wav', format ='wav')

    df.apply(audio_split, axis=1)
