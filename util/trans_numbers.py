from num2words import num2words  #num2words(42, lang='de')
from nltk import word_tokenize
import string
import pandas as pd


def translate_numbers(cleaned_csv_path):
    #read csv
    df_ds_final = pd.read_csv('./merged_csv/' + cleaned_csv_path)

    def convert_numbers(line):
        line = word_tokenize(line)
        a = line
        a = [int(x) if x.isdigit()== True else x for x in a]
        b = [num2words(x, lang='de') if type(x)==int else x for x in a]
        c = ' '.join(b)
        #d = c.replace(' £££ ', '\n')
        return c

    df_ds_final['transcript'] = df_ds_final['transcript'].apply(convert_numbers)

    #if numbers are not tokens alone, they can't be converted. e.g. 2L; therefore those will be removed here

    def clean_csv(df_ds_final):
        remove_char = '0123456789'

        table = str.maketrans('','', remove_char)
        df_ds_final['transcript'] = [w.translate(table) for w in df_ds_final['transcript']]

    clean_csv(df_ds_final)

    #once more remove certain characters because they are created by num2words
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ä','ae', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ö','oe', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ü','ue', regex=True)
    df_ds_final['transcript'] = df_ds_final['transcript'].replace('ß','ss', regex=True)

    #Save cleaned files
    final_path = cleaned_csv_path[:-4]
    print('Length of ds_final: {}'.format(len(df_ds_final)))
    df_ds_final.to_csv('./merged_csv/'+final_path + '_cleaned.csv', header=True, index=False, encoding='utf-8-sig')

    print('Final Files with converted and removed numbers')
