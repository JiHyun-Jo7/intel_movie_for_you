import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_review.csv')
df.dropna(inplace=True)
df.info()
print(df.head(10))
print(df['title'].unique())

one_sentences = []
for title in df['title'].unique():
    temp = df[df['title'] == title]
    one_sentence = ' '.join(temp['cleaned_sentences'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'title':df['title'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.info()
df_one.to_csv('./crawling_data/cleaned_one_review.csv', index=False)