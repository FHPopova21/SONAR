import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit

def split_data_by_sourcefile(X:np.ndarray, Y:np.ndarray,
                            metadata:pd.DataFrame,
                            test_size: float =0.15,
                            val_size: float =0.15,
                            random_state =42):
    groups = metadata["source_file"].values

    splitter_test = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_val_idx, test_idx = next(splitter_test.split(X, Y, groups))

    X_temp = X[train_val_idx]
    Y_temp = Y[train_val_idx]
    X_test = X[test_idx]
    Y_test = Y[test_idx]

    remaining_size = 1.0 - test_size
    relative_val_size = val_size / remaining_size 

    spliiter_val = GroupShuffleSplit(n_splits=1, test_size = relative_val_size, random_state=random_state)
    train_idx, val_idx = next(spliiter_val.split(X_temp, Y_temp, groups[train_val_idx]))

    X_train = X_temp[train_idx]
    Y_train = Y_temp[train_idx]
    X_val = X_temp[val_idx]
    Y_val = Y_temp[val_idx]


    print(f"Train size: {len(X_train)} ({len(np.unique(groups[train_val_idx][train_idx]))} source files)")
    print(f"Validation size: {len(X_val)} ({len(np.unique(groups[val_idx]))} source files)")
    print(f"Test size: {len(X_test)} ({len(np.unique(groups[test_idx]))} source files)")

    return X_train, X_val, X_test, Y_train, Y_val, Y_test

x = np.load('/Users/filipapopova/source/repos/Ambient-Sound-Awareness-System-ASAS-/data/processed/X.npy')
y = np.load('/Users/filipapopova/source/repos/Ambient-Sound-Awareness-System-ASAS-/data/processed/y.npy')
df = pd.read_csv('/Users/filipapopova/source/repos/Ambient-Sound-Awareness-System-ASAS-/data/processed/master_metadata.csv')
# Split safely
X_train, X_val, X_test, y_train, y_val, y_test = split_data_by_sourcefile(x, y, df)