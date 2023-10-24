import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/movie_reviews_total.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
cleaned_sentences = []

for review in df.review[:10]:
    review = re.sub('[^가-힣]', ' ', review)
    tokened_review = okt.pos(review, stem=True)
    print(tokened_review)

    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])  # word = 단어, class = 품사
    # 명사, 동사, 형용사만 keep
    df_token = df_token[((df_token['class']=='Noun')|
                         (df_token['class']=='Verb')|
                         (df_token['class']=='Adjective'))]             # 조건 인덱싱
    print(df_token.head())

    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df_test = df.iloc[:10, :]
df_test['cleaned_sentences'] = cleaned_sentences
print(df_test.head(10))