from selenium import webdriver              # 웹사이트(및 웹 애플리케이션)의 유효성 검사에 사용되는 자동화 테스트 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

for year in range(18, 21):
    url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}'.format(year)
    df_movies = pd.DataFrame()

    for month in range(1, 13):
        month_url = url + '{}'.format(month).zfill(2)
        url = month_url
        driver.get(url)
        time.sleep(3)
        for movie in range (1, 31):
            movie_data = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(movie))
            title = movie_data.text
            titles = []
            reviews = []
            if title not in titles :
                title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title)
                titles.append(movie_data)
                movie_data.click()
                time.sleep(3)
                print(title)

                review_tap = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
                review_tap.click()
                time.sleep(2)
                for more in range (5):
                    see_more = driver.find_element(By.XPATH,'//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'.format(more))
                    see_more.click()
                    time.sleep(2)
                    try :
                        for review in range (1, 161) :
                            review_data = driver.find_element(
                                'xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(review)).text
                            review_data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review_data)
                            reviews.append(review_data)
                    except : pass

                df_movie_review = pd.DataFrame(reviews, columns=['review'])
                df_movie_review['title'] = title
                df_movies = pd.concat([df_movies, df_movie_review], ignore_index=True)
                df_movies = df_movies.reindex(['title', 'review'], axis=1)

                driver.back()
                time.sleep(2)
                driver.back()
                time.sleep(2)

            df_movies.to_csv('./crawling_data/movie_reviews_{}{}_{}.csv'.format(year,month,movie),index=False)

