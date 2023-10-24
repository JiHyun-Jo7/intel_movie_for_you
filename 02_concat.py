import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/*')

df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)                # Nan 제거
    df_temp.drop_duplicates(inplace=True)       # 중복 제거
    df = pd.concat([df, df_temp], ignore_index=True)

df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/movie_reviews_total.csv', index = False)