from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'
options.add_argument('user-agent='+user_agent)
options.add_argument('lang=ko_KR')
# options.add_argument('window-size=1920x1080')
# options.add_argument('disable-gpu')
# options.add_argument('--no-sandbox')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

years = [2021, 2022, 2023]
url = 'https://movie.daum.net/ranking/boxoffice/monthly?date='
titles = []

for year in years:
    for month in range(1,13):
        df_movies = pd.DataFrame()

        date = str(year)+str('%02d'%month)
        url = url+date
        driver.get(url)
        time.sleep(2)

        reviews = []
        title = ''
        for movie in range(1, 31):
            movie_title = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(movie))
            title = movie_title.text
            if title not in titles:
                titles.append(title)
                movie_title.click()
                time.sleep(2)
                movie_review = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span').click()
                time.sleep(2)

                button_cnt = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[2]/div/strong/span').text
                button_cnt = re.sub(r'[^0-9]','',button_cnt)
                button_cnt = 1+int(button_cnt)//30 if 1+int(button_cnt)//30 < 5 else 5 # 총 리뷰 개수를 찾아서 리뷰 더보기 누를 횟수 계산

                for i in range(button_cnt):
                    review_button = driver.find_element('xpath','//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
                    time.sleep(1)
                for r in range(1,161):
                    try:
                        review = driver.find_element('xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(r)).text
                        review = re.compile('[^가-힣]').sub(' ',review)
                        reviews.append(review)
                    except:
                        print('Error {}{} movie {} {}th review'.format(year,month, movie, r))
            if movie % 5 == 0:
                df_movie_review = pd.DataFrame(reviews, columns=['review'])
                df_movie_review['title'] = title
                df_movies = pd.concat([df_movies, df_movie_review], ignore_index=True)
                df_movies = df_movies.reindex(['title','review'],axis=1)
                df_movies.to_csv('./crawling_data/movie_reviews_{}{}_{}.csv'.format(year,month,movie),index=False)
                reviews = []

            driver.back()
            time.sleep(2)
            driver.back()
            time.sleep(2)

        df_movie_review = pd.DataFrame(reviews,columns=['review'])
        df_movie_review['title'] = title
        df_movies = pd.concat([df_movies, df_movie_review], ignore_index=True)
        df_movies = df_movies.reindex(['title', 'review'], axis=1)
        df_movies.to_csv('./crawling_data/movie_reviews_{}{}_last.csv'.format(year, month), index=False)
