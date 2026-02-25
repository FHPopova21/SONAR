import pandas as pd

def split_data_by_folds(csv_path, output_dir="data/"):
    df = pd.read_csv(csv_path)
    
    # Train: 60% (Folds 1 до 6 включително)
    train_df = df[df['fold'].isin([1, 2, 3, 4, 5, 6])]
    
    # Validation: 20% (Folds 7 и 8)
    val_df = df[df['fold'].isin([7, 8])]
    
    # Test: 20% (Folds 9 и 10)
    test_df = df[df['fold'].isin([9, 10])]
    
    # Запазваме ги като отделни CSV файлове
    train_df.to_csv(f'{output_dir}/train_split.csv', index=False)
    val_df.to_csv(f'{output_dir}/val_split.csv', index=False)
    test_df.to_csv(f'{output_dir}/test_split.csv', index=False)
    
    print(f"Train: {len(train_df)} записа")
    print(f"Val: {len(val_df)} записа")
    print(f"Test: {len(test_df)} записа")