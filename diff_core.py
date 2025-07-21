import pandas as pd

def compare_csv(file1_path, file2_path, key_column=None):
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    sort_col = key_column if key_column else df1.columns[0]

    if sort_col in df1.columns:
        df1 = df1.sort_values(by=sort_col)
    if sort_col in df2.columns:
        df2 = df2.sort_values(by=sort_col)

    if key_column and key_column in df1.columns and key_column in df2.columns:
        merged = df1.merge(df2, on=key_column, how='outer', indicator=True)
    else:
        merged = df1.merge(df2, how='outer', indicator=True)

    only_in_file1 = merged[merged['_merge'] == 'left_only']
    only_in_file2 = merged[merged['_merge'] == 'right_only']

    return only_in_file1, only_in_file2
