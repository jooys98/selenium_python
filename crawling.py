from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
import random

# Chrome 드라이버 설정
driver = webdriver.Chrome()
driver.get('https://www.cosmopolitan.co.kr/fashion')
time.sleep(random.uniform(2.0 , 5.0))

try:
    # 게시글 목록 찾기
    articles = driver.find_elements(By.CLASS_NAME, "atcbox")
    article_data = []

    # 각 게시글 순회
    for article in articles[:5]:  # 처음 5개 게시글만 테스트
        try:
            # 게시글 클릭
            article.click()
            time.sleep(2)  # 페이지 로드 대기

            # 상세 정보 수집
            title = driver.find_element(By.CLASS_NAME, "tit_article").text
            author = driver.find_element(By.CLASS_NAME, "txt_meta").text
           
            
            # 이미지 URL 수집
            try:
                image = driver.find_element(By.CLASS_NAME, "imgbox")
                image_url = image.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image_url = "이미지 없음"

            # 본문 내용 수집
            try:
                content_section = driver.find_element(By.XPATH, "//div[@id='content']/div[1]/div/div[2]/div[1]/div")
                content = content_section.get_attribute('textContent')
                photo_content = driver.find_element(By.CLASS_NAME, "ab_photo").text
                author = driver.find_element(By.XPATH, "//a[contains(@href, '/editorlist/detail')]").text
                content = content + "\n" + photo_content
            except Exception as e:
                content = "본문 없음"
                author = "작성자 없음"
            # 데이터 저장
            article_data.append({
                "title": title,
                "author": author,
                "image_url": image_url,
                "content": content
            })

            # 이전 페이지로 돌아가기
            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"게시글 처리 중 오류 발생: {e}")
            driver.back()
            continue

    # JSON 파일로 저장
    file_path = os.path.expanduser("~/lo5er/cosmopolitan_articles.json")
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(article_data, file, ensure_ascii=False, indent=4)
    
    # 텍스트 파일로도 저장
    text_file_path = os.path.expanduser("~/lo5er/cosmopolitan_articles.txt")
    
    with open(text_file_path, "w", encoding="utf-8") as file:
        for article in article_data:
            file.write(f"제목: {article['title']}\n")
            file.write(f"작성자: {article['author']}\n")
            file.write(f"이미지 URL: {article['image_url']}\n")
            file.write(f"본문:\n{article['content']}\n")
            file.write("=" * 50 + "\n\n")

    print(f"크롤링이 완료되었습니다. 총 {len(article_data)}개의 게시글을 수집했습니다.")

except Exception as e:
    print(f"크롤링 중 오류가 발생했습니다: {e}")

finally:
    driver.quit()