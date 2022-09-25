import pandas as pd
from glob import glob


def merge_csv(path):
    print('Merging csv-files with transcriptions')
    csv_combined = pd.DataFrame()
    for entry in glob (path+'*.csv'):
        df = pd.read_csv(entry)
        csv_combined = csv_combined.append(df)

    csv_combined.to_csv('./merged_csv/Full_Transcript.csv', header=True, index=False, encoding='utf-8-sig')
    print('All csv-files merged')
