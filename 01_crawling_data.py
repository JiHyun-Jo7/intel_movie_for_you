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

url = 'https://movie.daum.net/'

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

for year in range(18, 21):
    year_url = url + 'ranking/boxoffice/monthly?date=2023{}'.format(year)
    df_title = pd.DataFrame()
    title = []
    review = []
    for month in range(1, 13):
        month_url = year_url + '{}'.format(month)

        for movie in range (1, 31):
            movie_data = '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(movie)
            movie_data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', movie_data)
            title.append(movie_data)

            driver.find_element('xpath', movie_data).click()
            time.sleep(3)
            print('count = %d' % movie)

            review_tap = '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span'
            driver.find_element('xpath', review_tap).click()
            for more in range (5):
                see_more = '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'.format(more)
                driver.find_element('xpath', see_more).click()
            try :
                for review in range (1, 161) :
                    review_data = driver.find_element(
                        'xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(review)).text
                    review_data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review_data)
                    title.append(review_data)
            except : pass

            df_section_title = pd.DataFrame(title, columns=['title'])
            df_section_title['review'] = review
            df_titles = pd.concat([df_title, df_section_title], ignore_index=True)
