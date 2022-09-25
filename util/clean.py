from pickle import FALSE, TRUE
import string
import pandas as pd

def clean_unwanted_characters(final_csv_path):

    df_ds_final = pd.read_csv('./merged_csv/'+final_csv_path)

    #some srt files contain font codes which are removed hereby
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#91FFFF>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#72FD59>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#E8E858>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#FFFFFF>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('</font>', '', regex=True)


    #Characters to be removed

    df_ds_final = df_ds_final.dropna()
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('\s+', '、', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].str.strip()

    df_ds_final['transcript'] = df_ds_final['transcript']

    #Save cleaned files
    final_path = final_csv_path[:-4]
    print('Length of ds_final: {}'.format(len(df_ds_final)))
    df_ds_final.to_csv('./merged_csv/'+final_path + '_merged.csv', header=True, index=False, encoding='utf-8')

    print('Final Files cleaned of unwanted characters')
