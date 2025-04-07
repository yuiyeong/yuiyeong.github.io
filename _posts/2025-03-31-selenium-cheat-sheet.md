---
title: 😜 Selenium with Python Cheat Sheet
date: 2025-03-31 19:59:00 +0900
categories: [ PYTHON, CRAWLING ]
tags: [ '급발진거북이', 'python', 'crawling', '크롤링', 'selenium', '셀레니움', '파이썬' ]
toc: true
comments: false
mermaid: true
math: true
---

## 🚀 기본 설정 및 브라우저 시작

```python
# 필요한 라이브러리 임포트
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 브라우저 시작하기
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 브라우저 창 크기 설정
driver.set_window_size(1920, 1080)

# 페이지 로드 타임아웃 설정 (초 단위)
driver.set_page_load_timeout(30)

# 웹사이트 방문
driver.get("https://example.com")

# 브라우저 종료
driver.quit()


```

## 🔍 요소 찾기 (Element Location)

```python
# ID로 요소 찾기
element = driver.find_element(By.ID, "login-button")

# 클래스 이름으로 요소들 찾기
elements = driver.find_elements(By.CLASS_NAME, "product-item")

# CSS 선택자로 요소 찾기
element = driver.find_element(By.CSS_SELECTOR, ".nav > li:first-child")

# XPath로 요소 찾기
element = driver.find_element(By.XPATH, "//div[@id='main']//button[contains(text(), '로그인')]")

# 링크 텍스트로 요소 찾기
element = driver.find_element(By.LINK_TEXT, "회원가입")

# 부분 링크 텍스트로 요소 찾기
element = driver.find_element(By.PARTIAL_LINK_TEXT, "회원")

# 자식 요소 찾기
parent = driver.find_element(By.ID, "parent")
child = parent.find_element(By.CSS_SELECTOR, ".child-class")


```

## 🖱️ 요소 상호작용

```python
# 요소 클릭하기
button = driver.find_element(By.ID, "submit-button")
button.click()

# 텍스트 입력하기
input_field = driver.find_element(By.NAME, "username")
input_field.clear()  # 기존 텍스트 지우기
input_field.send_keys("myusername")

# 요소의 텍스트 가져오기
text = driver.find_element(By.CLASS_NAME, "title").text

# 요소의 속성 가져오기
link = driver.find_element(By.CSS_SELECTOR, "a.product-link")
href = link.get_attribute("href")

# 요소가 표시되는지 확인
is_visible = driver.find_element(By.ID, "element").is_displayed()

# 요소가 활성화되어 있는지 확인
is_enabled = driver.find_element(By.ID, "button").is_enabled()

# 체크박스나 라디오 버튼이 선택되었는지 확인
is_selected = driver.find_element(By.ID, "checkbox").is_selected()


```

## ⏱️ 대기 전략 (Waiting)

```python
# 명시적 대기 - 특정 조건이 충족될 때까지 대기
wait = WebDriverWait(driver, 10)  # 최대 10초 대기
element = wait.until(EC.presence_of_element_located((By.ID, "element-id")))

# 요소가 클릭 가능할 때까지 대기
clickable = wait.until(EC.element_to_be_clickable((By.ID, "button")))

# 요소가 화면에 표시될 때까지 대기
visible = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "result")))

# 요소가 사라질 때까지 대기
wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

# 텍스트가 요소에 나타날 때까지 대기
wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "완료"))

# 여러 조건을 함께 사용
from selenium.webdriver.support.wait import WebDriverWait

wait.until(EC.all_of(
    EC.visibility_of_element_located((By.ID, "element")),
    EC.element_to_be_clickable((By.ID, "element"))
))

# 간단한 시간 지연 (권장하지 않음, 명시적 대기 대신 사용)
time.sleep(2)


```

## 📜 스크롤 및 JavaScript 실행

```python
# 페이지 맨 아래로 스크롤
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 특정 요소로 스크롤
element = driver.find_element(By.ID, "my-element")
driver.execute_script("arguments[0].scrollIntoView(true);", element)

# 특정 위치로 스크롤
driver.execute_script("window.scrollTo(0, 500);")

# 무한 스크롤 페이지 처리
SCROLL_PAUSE_TIME = 1.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩 대기
    time.sleep(SCROLL_PAUSE_TIME)

    # 새 스크롤 높이 계산
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # 더 이상 새 콘텐츠가 로드되지 않으면 종료
    last_height = new_height


```

## 🪟 프레임 및 창 처리

```python
# iframe으로 전환
iframe = driver.find_element(By.ID, "iframe-id")
driver.switch_to.frame(iframe)

# 기본 콘텐츠로 돌아가기
driver.switch_to.default_content()

# 새 창/탭 처리
original_window = driver.current_window_handle
# 새 창을 열 링크 클릭
driver.find_element(By.ID, "new-window-link").click()
# 모든 창 핸들 가져오기
all_windows = driver.window_handles
# 새 창으로 전환
for window in all_windows:
    if window != original_window:
        driver.switch_to.window(window)
        break
# 원래 창으로 돌아가기
driver.switch_to.window(original_window)


```

## ⚠️ 경고창(Alert) 처리

```python
# 경고창 대기 및 수락
WebDriverWait(driver, 10).until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()  # 확인 클릭

# 경고창 거부 (취소 클릭)
alert.dismiss()

# 경고창에 텍스트 입력
alert.send_keys("텍스트 입력")


```

## 🍪 쿠키 및 로컬스토리지 처리

```python
# 쿠키 추가
driver.add_cookie({"name": "session_id", "value": "12345"})

# 쿠키 가져오기
cookies = driver.get_cookies()

# 특정 쿠키 가져오기
cookie = driver.get_cookie("session_id")

# 로컬스토리지 항목 설정
driver.execute_script("window.localStorage.setItem('key', 'value');")

# 로컬스토리지 항목 가져오기
value = driver.execute_script("return window.localStorage.getItem('key');")


```

## 📁 파일 다운로드 및 업로드

```python
# 다운로드 경로 설정 (Chrome)
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": "/path/to/download/dir",
    "download.prompt_for_download": False,
})
driver = webdriver.Chrome(service=service, options=options)

# 파일 업로드 (input type="file" 요소)
file_input = driver.find_element(By.ID, "file-upload")
file_input.send_keys("/path/to/file.jpg")


```

## ⚙️ 헤드리스 모드 및 옵션 설정

```python
from selenium.webdriver.chrome.options import Options

options = Options()
# 헤드리스 모드 (UI 없이 실행)
options.add_argument("--headless")
# 사용자 에이전트 설정
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# 브라우저 창 크기 설정
options.add_argument("--window-size=1920,1080")
# 알림 비활성화
options.add_argument("--disable-notifications")
# GPU 가속 비활성화
options.add_argument("--disable-gpu")
# 이미지 로딩 비활성화 (더 빠른 크롤링)
options.add_argument("--blink-settings=imagesEnabled=false")

driver = webdriver.Chrome(service=service, options=options)


```

## 💾 데이터 추출 및 저장

```python
import pandas as pd
import csv
import json

# 웹 페이지에서 데이터 추출하여 DataFrame 생성
products = []
elements = driver.find_elements(By.CSS_SELECTOR, ".product-item")

for element in elements:
    title = element.find_element(By.CSS_SELECTOR, ".title").text
    price = element.find_element(By.CSS_SELECTOR, ".price").text
    rating = element.find_element(By.CSS_SELECTOR, ".rating").get_attribute("data-rating")
    products.append({
        "title": title,
        "price": price,
        "rating": rating
    })

# DataFrame으로 변환
df = pd.DataFrame(products)

# CSV로 저장
df.to_csv("products.csv", index=False, encoding="utf-8-sig")

# JSON으로 저장
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)


```

## 💡 유용한 팁

```python
# 페이지 HTML 소스 가져오기
html_source = driver.page_source

# 현재 URL 가져오기
current_url = driver.current_url

# 페이지 제목 가져오기
title = driver.title

# 스크린샷 저장
driver.save_screenshot("screenshot.png")

# 특정 요소의 스크린샷 저장
element = driver.find_element(By.ID, "element-id")
element.screenshot("element-screenshot.png")

# 페이지 리프레시
driver.refresh()

# 브라우저 히스토리 뒤로 가기
driver.back()

# 브라우저 히스토리 앞으로 가기
driver.forward()


```

