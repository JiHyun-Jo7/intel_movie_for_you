import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import word2vec
from scipy.io import  mmread
import pickle
from PyQt5.QtCore import QStringListModel
from gensim.models import Word2Vec

form_window = uic.loadUiType('./movie_recommendation.ui')[0]
class Exam(QWidget, form_window):           # 클래스 생성
    def __init__(self):
        super().__init__()                  # 부모 클래스
        self.setupUi(self)

        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
        self.df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
        self.titles = list(self.df_reviews['title'])
        self.titles.sort()                  # 오름차순 정렬
        for title in self.titles:
            self.comboBox.addItem(self.title)   # comboBox에 title 추가
        self.comboBox.currentIndexChanged.connect(self.comboBox_slot)

    def combobox_slot(self):
        title = self.combobox.currentText()
        recommendation = self.recommendation_by_movie_title(title)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_movie(self, title):
        movie_idx = self.df_reviews[self.df_reviews['title']==title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        return recommendation

    def getReccomendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        recMovieList = '\n'.join(recMovieList[1:])
        return recMovieList

if __name__ == '__main__':                  # 메인
    app = QApplication(sys.argv)            # 객체 생성
    MainWindow = Exam()
    MainWindow.show()                       # 창를 화면에 출력
    sys.exit(app.exec_())                   # 창 화면 출력을 유지하는 함수