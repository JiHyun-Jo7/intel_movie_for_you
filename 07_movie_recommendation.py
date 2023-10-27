import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getReccomendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key = lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList

# 이전에 저장한 파일 로드
df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# print(df_reviews.iloc[0, 0])
# cosine_sim = linear_kernel(Tfidf_matrix[0], Tfidf_matrix)         # 0번째 영화와 전체 영화의 cosine 유사도
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# recommendation = getReccomendation(cosine_sim)
# print(recommendation)


embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')    # keyword 기반 영화 추천
keyword = ''
try:
    sim_word = embedding_model.wv.most_similar(keyword, topn=10)
    print(sim_word)

    words = [keyword]
    for word, _ in sim_word:
        words.append(word)
    print(words)

    sentence = []
    count = 10
    for word in words:
        sentence = sentence + [word] * count
        count -= 1
    sentence = ' '.join(sentence)
    print(sentence)
    sentence_vec = Tfidf.transform([sentence])
    cosin_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    recommendation = getReccomendation(cosin_sim)
    print(recommendation)
except:
    print('다른 키워드를 입력하세요')