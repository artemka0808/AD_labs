import os
import pandas as pd

def read_csv_files_to_df(directory):
    data_frames = []

    for filename in os.listdir(directory):
        reg = filename.split("_")[1]
        file_path = os.path.join(directory, filename)

        try:
            df = pd.read_csv(file_path, index_col=False, header=1)
            df.columns = [col.strip().lower().replace("<br>", "") for col in df.columns]
            df = df.replace(to_replace=r'<.*?>', value='', regex=True)
            df["oblast"] = reg
            data_frames.append(df)

        except Exception as e:
            print(f"Не вдалося зчитати файл {file_path}: {e}")

    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)

    else:
        combined_df = pd.DataFrame()

    return combined_df

df = read_csv_files_to_df("data")


while (df[['vci', 'tci', 'vhi']] == -1).any().any():
    df = df.mask(df == -1, df.shift())

df = df.dropna(subset=['vci', 'tci', 'vhi'])
df.to_csv('data/lab_3.csv', index=False)
