import pandas as pd
import glob

data_path = glob.glob('./crawling_data/*')

df = pd.DataFrame()
for path in data_path:
    print(path)
    df_review = pd.read_csv(path, index_col=0)
    titles = set(df_review.index.to_list())

    for title in titles:
        try:
            total_review = ''
            reviews = df_review.loc[title]
            reviews = reviews['review'].to_list()
            for review in reviews:
                if review == '':
                    continue
                total_review += review
            dict = {'title':[title],'review':[total_review]}
            df_movie = pd.DataFrame(dict)
            df = pd.concat([df, df_movie], ignore_index=True)
        except:
            continue


df.to_csv('./crawling_data/movie_reviews_202101_202310.csv',index=False)
