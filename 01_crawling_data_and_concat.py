from selenium import webdriver  # 웹사이트(및 웹 애플리케이션)의 유효성 검사에 사용되는 자동화 테스트 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

df_movies = pd.DataFrame()
titles = []  # 중복 확인을 위한 영화 list

for year in range(18, 21):  # 연도 별 url 반복문
    for month in range(1, 13):  # 월 별 url 반복문
        url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}'.format(year)  # url 초기화
        month_url = url + '{}'.format(month).zfill(2)
        driver.get(month_url)  # 최종 url 불러오기
        time.sleep(1)
        for movie in range(1, 31):  # 영화 페이지 불러오기
            try:
                reviews = ''
                total_reviews = []
                movie_data = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(movie))
                title = movie_data.text
                # 중복 영화 제거
                title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title)
                if title not in titles:
                    # 제목 크롤링(특수 문자 제거) 및 영화 상세 페이지로 이동
                    titles.append(title)
                    movie_data.click()
                    time.sleep(1)
                    print('{}. {}'.format(movie, title))

                    # 리뷰 탭으로 이동
                    review_tap = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
                    review_tap.click()
                    time.sleep(1)

                    # 리뷰 수, 페이지 계산
                    review_num = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[2]/div[2]/div/strong/span').text
                    review_num = re.compile('[^0-9]').sub(' ', review_num)  # 숫자 데이터만 가져옴
                    review_page = ((int(review_num) - 10) // 30) + 1  # 리뷰 페이지 수 계산
                    if review_page > 5:
                        review_page = 5  # 최대 페이지 수 제한
                        review_num = 160
                    print('리뷰 수:{}, 페이지:{}'.format(review_num, review_page))

                    # 리뷰 더보기 클릭 (최대 5회)
                    for more in range(review_page):
                        try:
                            see_more = driver.find_element(By.XPATH,'//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'.format(more))
                            see_more.click()
                            time.sleep(0.8)
                        except:
                            print("review page error")
                            pass
                    # 리뷰 크롤링. 내용이 없는 리뷰는 pass
                    for review in range(1, int(review_num)):        # int(review_num)
                        try:
                            review_data = driver.find_element(
                                By.XPATH,
                                '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(
                                    review)).text
                            review_data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review_data)
                            # 지나치게 짧거나 중복 되는 리뷰 제거
                            if review_data not in reviews:
                                if len(review_data) > 6:
                                    reviews += review_data
                        except:
                            print('review error: {:0>2} {} {}'.format(month, title, review))
                    total_reviews.append(reviews)
                    df_movie_review = pd.DataFrame(total_reviews, columns=['review'])
                    df_movie_review['title'] = title
                    df_movies = pd.concat([df_movies, df_movie_review], ignore_index=True)
                    df_movies = df_movies.reindex(['title', 'review'], axis=1)
                else:                                       # 중복된 영화일 경우
                    print('{}: 이미 수집한 영화입니다.'.format(title))
                    time.sleep(1)
                    if movie == 30: pass                    # 마지막 영화일 경우 하단의 if문 실행
                    else: continue                          # 아닐 경우 하단의 if 문 생략

                # 창 종료
                driver.back()
                time.sleep(1)
                driver.back()
                time.sleep(1)

            except:                 # 영화가 없거나 오류가 있을 경우
                print('movie error: {:0>2}. {}'.format(month, movie))
                driver.back()
                time.sleep(1)

driver.quit()
df_movies.to_csv('./crawling_data/movie_reviews_test.csv', index=False)
print('test: save success')