import numpy as np
import pandas as pd


def split_dataset(to_split_path):

    df = pd.read_csv('./merged_csv/' + to_split_path)

    def train_validate_test_split_CV(df, train_percent=.75, validate_percent=.1, seed=None):
        np.random.seed(seed)
        perm = np.random.permutation(df.index)
        m = len(df.index)
        train_end = int(train_percent * m)
        validate_end = int(validate_percent * m) + train_end
        train = df.iloc[perm[:train_end]]
        validate = df.iloc[perm[train_end:validate_end]]
        test = df.iloc[perm[validate_end:]]
        return train, validate, test

    train, validate, test = train_validate_test_split_CV(df)
    out_path = './final_csv/'

    train.to_csv(out_path + 'train.csv', header=True, index=False, encoding='utf-8-sig')
    validate.to_csv(out_path + 'dev.csv', header=True, index=False, encoding='utf-8-sig')
    test.to_csv(out_path + 'test.csv', header=True, index=False, encoding='utf-8-sig')
