from pickle import FALSE, TRUE
import string
import pandas as pd
from unidecode import unidecode

def clean_unwanted_characters(final_csv_path):

    df_ds_final = pd.read_csv('./merged_csv/'+final_csv_path)

    #some srt files contain font codes which are removed hereby
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#91FFFF>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#72FD59>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#E8E858>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('<font color=#FFFFFF>', '', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('</font>', '', regex=True)


    #Characters to be removed
    punct = str(['.!"#$%&\'()*+,-/:;<–=>?@[\\]^_°`{}~ ̀ ̆ ̃ ́'])
    transtab = str.maketrans(dict.fromkeys(punct, ' '))
    df_ds_final = df_ds_final.dropna()

    df_ds_final['transcript'] = '£'.join(df_ds_final['transcript'].tolist()).translate(transtab).split('£')

    df_ds_final['transcript'] = df_ds_final['transcript'].str.lower()
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('\s+', ' ', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].str.strip()

    #Further remove unwanted characters
    remove_char = '鄚氏鐷顤鐰鄣酹輐霵鐼羦鄜酲酺酺礫飉舣δφℳˁｶᛠᛏˁːɣ\ʿʻʾŋ\ʹªьʺъˀˇʼʔˊˈ!"#$%&\()*+,-./:;<=>?@[]^_`{|}~'

    table_2 = str.maketrans('','', remove_char)
    df_ds_final['transcript'] = [w.translate(table_2) for w in df_ds_final['transcript']]

    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ä','ae', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ö','oe', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ü','ue', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('α','alpha', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ə','e', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ё','e', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('γ','gamma', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('µ','mikro', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('π','pi', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('β','beta', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ζ','zeta', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ß','ss', regex=True)

    #to get rid of final unwanted characters transform characters to strictly unicode
    def to_ASCII(text):
        text = unidecode(text)
        return text

    df_ds_final['transcript'] = df_ds_final['transcript']

    #Save cleaned files
    final_path = final_csv_path[:-4]
    print('Length of ds_final: {}'.format(len(df_ds_final)))
    df_ds_final.to_csv('./merged_csv/'+final_path + '_merged.csv', header=True, index=False, encoding='utf-8')

    print('Final Files cleaned of unwanted characters')
