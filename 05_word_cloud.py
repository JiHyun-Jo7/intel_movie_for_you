import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

df = pd.read_csv('./crawling_data/cleaned_one_review.csv')
words = df.iloc[0, 1].split()                 # 형태소 단위로 잘려있는 리스트로 출력
print(words)

worddict = collections.Counter(words)         # 단어가 반복된 횟수 출력 (type : dict)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
    ).generate_from_frequencies(worddict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()