import pandas as pd


def merge_transcripts_and_wav_files(transcript_path, DS_csv):
    df_final = pd.DataFrame()

    df_transcripts = pd.read_csv(transcript_path)
    df_files = pd.read_csv(DS_csv)

    #by splitting the path at / and then choosing -1, the filename can be extracted
    def remove_path(path):
        path = path.split('/')[-1]
        return path

    df_files['id'] = df_files['wav_filename'].apply(remove_path)

    #filter out duration of less than 10 seconds
    def convert(duration):
        time = float(duration)
        return time
    df_files['duration'] = df_files['duration'].apply(convert)
    df_files = df_files[df_files['duration']<10.00]

    #drop unnecessary columns
    df_transcripts.drop(['start_times','end_times'], axis=1, inplace=True)
    df_files.drop(['duration'], axis=1, inplace=True)

    df_files['id'] = df_files['id'].replace('.wav', '', regex=True)

    #merge on column id
    df_final = pd.merge(df_transcripts, df_files, on='id')
    df_final.drop(['id'], axis=1, inplace=True)
    #rearrange columns
    df_final = df_final[['wav_filename', 'wav_filesize', 'transcript']]

    df_final.to_csv('./merged_csv/DS_training_final.csv', header=True, index=False, encoding='utf-8-sig')
