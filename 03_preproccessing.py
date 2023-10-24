import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/movie_reviews_total.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

count = 0
cleaned_sentences = []
# 진행 상황 확인용
for review in df.review:
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 100 == 0:
        print()
    if count % 1000 == 0:
        print(count / 1000)
    review = re.sub('[^가-힣]', ' ', review)
    tokened_review = okt.pos(review, stem=True)


    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])  # word = 단어, class = 품사
    # 명사, 동사, 형용사만 keep
    df_token = df_token[((df_token['class']=='Noun')|
                         (df_token['class']=='Verb')|
                         (df_token['class']=='Adjective'))]             # 조건 인덱싱

    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]       # review 항목 제거
print(df.head(10))

df.to_csv('./crawling_data/cleaned_review.csv', index=False)