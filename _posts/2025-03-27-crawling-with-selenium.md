---
title: 🐍 Crawling 맛 보기(w. selenium)
date: 2025-03-27 15:56:00 +0900
categories: [ PYTHON, CRAWLING ]
tags: [ '급발진거북이', 'python', 'crawling', '크롤링', 'selenium', '셀레니움', 'GeekAndChill', '기깬칠' ]
toc: true
comments: false
mermaid: true
math: true
---

## ☕ 크롤링을 하기위한 package 설치하기

필요한 package 는 `selenium` 과 `webdriver-manager` 이다.

아래 명령어를 사용해서 설치한다.

```shell
pip install selenium webdriver-manager
```

그럼 webdriver-manager 와 selenium 은 각각 역할이 뭘까?

![selenium_system.png](/assets/img/selenium_system.png)

### Selenium

Selenium 은 웹 브라우저를 자동화하는 도구이고, 아래와 같은 기능을 할 수 있다.

- 웹 페이지 자동 탐색

- 클릭, 입력, 스크롤 등 사용자 동작 시뮬레이션

- JavaScript가 실행된 후의 DOM 요소에 접근 가능

- 동적으로 생성되는 콘텐츠 수집 가능

특히, 마지막이 제일 중요한데, 요즘은 대부분의 사이트가 Next.js 와 같은 프레임워크로 웹 사이트를 만들기 때문에 웹 사이트들이 거의 동적 생성 콘텐츠로 되어있다. 즉, Selenium 을 사용하면 그 콘텐츠로
수집할 수 있게 되는 것이다.

### webdriver-manager

webdriver-manager 는 브라우저별 WebDriver를 관리하는 도구이고, 아래와 같은 기능을 제공한다.

- 필요한 브라우저 드라이버(Chrome, Firefox 등) 자동 설치

- 드라이버 버전 관리 및 업데이트

- 서로 다른 OS 환경에서도 일관된 설정 제공

### Selenium 만으로 크롤링을 할 수 있을 것 같은데, 왜 webdriver-manager 가 필요할까?

selenium 으로 브라우저를 제어하기 위해서는 별도의 WebDriver 가 필요하다. 즉, 내 컴퓨터에 설치되어있는 브라우저(나의 경우는 Chrome 을 사용한다.) 에 맞는 WebDriver 를 설치해야하는
것이다.

그런데 이 driver 관리가 번거롭다. (driver 관리는 항상 번거롭다…)

그 번거로운 driver 설치 및 관리를 webdriver-manger 를 사용해서 하는 것이다!!

그 이유말고도, 환경 설정이라던지 협업이나 유지보수를 위해서 webdriver-manager 를 사용하는 것이 훨씬 효율적이다.

## 🫰 Selenium 사용법

### 원리

기본 적인 원리는 웹 browser 를 켜고, 그 browser 에서 크롤링하고자하는 사이트로 이동을 한 뒤, 그 사이트의 html 을 가지고 parsing 을 해서 원하는 데이터만 뽑는 것이다.

즉, 모든 크롤링은 해당 웹 사이트의 HTML 이 어떻게 생긴지를 본 뒤 우리가 원하는 정보가 어떤 위치있는지를 확인하고 코드를 작성한다!

우리는 `Selenium` 을 가지고 웹 browser 켜기, url 이동하기, html 파싱하기 를 python code 로 진행하는 것이다.

### 웹 브라우저 켜기(driver 가져오기)

로컬에서 Chrome 브라우저를 사용하고 있기때문에, Chrome 의 driver 를 켠다.

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
chrome_driver = webdriver.Chrome(service=service)  # => 크롬 browser 가 켜진다.
```

![selenium_chrome_driver01.png](/assets/img/selenium_chrome_driver01.png)

위 코드가 실행되면 아래와 같이, chrom browser 가 켜진다.

💡 크롤링을 진행하는 동안에 이 browser 를 종료하면 안 된다!

	browser 를 종료하면, 세션이 종료되면서 데이터를 가져올 수가 없게 된다.

browser 를 종료하려면 즉, driver 의 세션을 정상적으로 종료하려면 아래의 코드를 실행하면된다.

```python
chrome_driver.quit()  # driver 의 session 을 종료한다.
service.stop()  # chrome driver 를 만들 때 넣어준 service 도 멈춰주는 것이 좋다.
```

### 특정 웹 사이트로 이동하기

이동하고자 하는 사이트의 url 을 가지고 `get()` 을 호출하면 된다.

```python
url = "https://yuiyeong.github.io"
chrome_driver.get(url)
```

url 을 이 블로그의 홈으로 정했고, 위 코드를 실행하면 아래와 같이 웹 페이지가 보인다.

![selenium_chrome_driver02.png](/assets/img/selenium_chrome_driver02.png)

### HTML 파싱하기

그럼 블로그 홈에서 보이는 글 목록을 가져오는 코드를 작성해보자.

우선, 글 목록의 HTML tag 를 확인해보자.

![selenium_chrome_driver03.png](/assets/img/selenium_chrome_driver03.png)

article tag 에 card-wrapper 를 class 로 가지는 HTMLDomElement 가 글 내용을 감싸고 있다.

이걸 바탕으로 selenium 에서 글 data 를 가져오게 하는 코드가 아래의 코드이다.

```python
from selenium.webdriver.common.by import By

first_article = chrome_driver.find_element(By.TAG_NAME, "article")

link = first_article.find_element(By.TAG_NAME, "a").get_attribute("href")
title = first_article.find_element(By.CLASS_NAME, "card-title").text
text = first_article.find_element(By.CLASS_NAME, "card-text").text
post_meta = first_article.find_element(By.CLASS_NAME, "post-meta").text
```

`Selenium` 에서 `WebElement` 를 찾는 함수로, `find_element` 와 `find_elements` 를 사용한다. 전자는 찾은 것 중 첫번째 `WebElement` 를 반환하고, 후자는 찾은
모든 `WebElement` 를 list 로 반환한다.

위 코드에서는 `find_element` 를 사용해서, 첫번째 글을 감싸고 있는 WebElement 를 가져왔다.

그 WebElement 의 자식 element 중에서 tag 이름, class 이름 등을 가지고 필요한 정보를 가져왔다.

모든 글을 가져오고 싶다면, find_element 대신에 find_elements 를 사용하고, 각 article WebElement 를 for loop 을 돌면서 정보를 가져오는 코드로 변경하면 된다.

```python
articles = chrome_driver.find_element(By.TAG_NAME, "article")
for article in articles:
    link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
    title = article.find_element(By.CLASS_NAME, "card-title").text
    text = article.find_element(By.CLASS_NAME, "card-text").text
    post_meta = article.find_element(By.CLASS_NAME, "post-meta").text
```

그럼 대표적으로 사용하는 By 종류는 어떻게 될까?

### By 종류

- By.ID

  HTML 요소의 id 속성으로 요소를 찾는다. 가장 빠르고 안정적인 방법이다.

```python
from selenium.webdriver.common.by import By

# ID로 요소 찾기
element = driver.find_element(By.ID, "login-button")

```

- By.NAME

  name 속성으로 요소를 찾는다. 주로 폼 요소에서 사용된다.

```python
# NAME으로 요소 찾기
search_field = driver.find_element(By.NAME, "q")  # Google 검색창

```

- By.CLASS_NAME

  class 속성으로 요소를 찾는다.

```python
# CLASS_NAME으로 요소 찾기
menu_items = driver.find_elements(By.CLASS_NAME, "menu-item")

```

- By.TAG_NAME

  HTML 태그 이름으로 요소를 찾는다.

```python
# TAG_NAME으로 요소 찾기
all_links = driver.find_elements(By.TAG_NAME, "a")
all_inputs = driver.find_elements(By.TAG_NAME, "input")

```

- By.LINK_TEXT

  링크 텍스트가 정확히 일치하는 요소를 찾는다.

```python
# LINK_TEXT로 요소 찾기
contact_link = driver.find_element(By.LINK_TEXT, "Contact Us")

```

- By.PARTIAL_LINK_TEXT

  링크 텍스트의 일부만 일치해도 찾는다.

```python
# PARTIAL_LINK_TEXT로 요소 찾기
help_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Help")  # "Help Center"나 "Get Help" 등 찾을 수 있음

```

- By.CSS_SELECTOR

  [CSS 선택자](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_selectors)로 요소를 찾는다. 매우 유연하고 강력하다.

```python
# CSS_SELECTOR로 요소 찾기
active_items = driver.find_elements(By.CSS_SELECTOR, ".item.active")
header_logo = driver.find_element(By.CSS_SELECTOR, "header .logo")
first_item = driver.find_element(By.CSS_SELECTOR, "ul.menu li:first-child")
input_with_placeholder = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")

```

- By.XPATH

  [XPath 표현식](https://developer.mozilla.org/ko/docs/Web/XML/XPath)으로 요소를 찾는다. 매우 강력하지만 CSS 선택자보다 느릴 수 있다.

```python
# XPATH로 요소 찾기
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
menu_text = driver.find_element(By.XPATH, "//div[@id='menu']//span[contains(text(), '메뉴')]")
second_row = driver.find_element(By.XPATH, "//table/tr[2]")
parent_div = driver.find_element(By.XPATH, "//input[@id='child']/..")
dynamic_element = driver.find_element(By.XPATH, "//*[contains(@class, 'dynamic-') and contains(@class, '-content')]")

```

- 일반적으로 요소를 찾을 때는 다음과 같은 우선순위로 By 를 사용하는 것이 좋다.

    1. ID (가장 빠르고 안정적)

    1. NAME

    1. CSS_SELECTOR (유연하고 강력함)

    1. XPATH (가장 유연하지만 상대적으로 느림)

## 🚴‍♀️ Headless 모드로 실행하

헤드리스 모드는 브라우저를 실제로 화면에 표시하지 않고 백그라운드에서 실행하는 방식이다.

### 장점

- 리소스 절약: GUI를 표시하지 않아 메모리 및 CPU 사용량이 감소

- 속도 향상: 화면 렌더링이 필요 없어 일반적으로 더 빠르게 실행

- 서버 환경 지원: GUI가 없는 서버 환경(ex: 리눅스 서버)에서도 실행 가능

- 자동화에 적합: CI/CD 파이프라인이나 배치 작업에 이상적

- 멀티태스킹: 컴퓨터를 다른 작업에 사용하면서 백그라운드에서 크롤링을 실행 가능

### 설정 방법

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 옵션 객체 생성
options = Options()

# 헤드리스 모드 설정
options.add_argument("--headless")

# 필요한 경우 윈도우 크기 설정 (헤드리스 모드에서도 중요할 수 있음)
options.add_argument("--window-size=1920,1080")

# 브라우저 시작 시 옵션 적용
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 이후 일반 Selenium 코드와 동일하게 사용
driver.get("https://example.com")
# ...

```

### 주의사항

- 디버깅 어려움: 화면이 보이지 않아 문제가 발생했을 때 디버깅이 어려울 수 있다.

- 사용자 에이전트 설정: 일부 웹사이트는 헤드리스 브라우저를 봇으로 인식하고 차단할 수 있습니다. 이 경우 사용자 에이전트를 설정해주는 것이 좋다.

```python
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

```

- 스크린샷 활용: 헤드리스 모드에서도 `driver.save_screenshot()`을 사용해 디버깅을 위한 스크린샷을 저장할 수 있다.

- 일부 기능 제한: 극히 드물게 일부 웹사이트에서는 헤드리스 모드에서 제대로 작동하지 않는 요소가 있을 수 있다.

- 추가 옵션 설정

```python
options.add_argument("--disable-gpu")  # GPU 가속 비활성화
options.add_argument("--no-sandbox")  # 리눅스 환경에서 필요할 수 있음
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 문제 해결
options.add_argument("--disable-notifications")  # 알림 비활성화
options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 로딩 비활성화 (더 빠른 크롤링)
```

## 🏁 동적 컨텐츠 가져오기

최근에는 대부분의 웹 사이트가 동적 컨텐츠로 이루어져있다. 스크롤이 끝까지 가면 데이터를 더 호출한다든지, React나 Vue 등으로 만들어진 SPA 앱이라든지, iframe 내부의 동적 콘텐츠라든지 말이다.

이러한 내용도 크롤링할 수 있도록 Selenium은 다양한 방법을 제공한다.

### execute_script()

JavaScript 코드를 직접 실행할 수 있도록 해주는 함수이다. 이 함수를 통해 브라우저에서 직접 JavaScript를 실행하여 동적 콘텐츠를 조작하거나 가져올 수 있다.

```python
# 스크롤을 페이지 맨 아래로 내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 특정 요소까지 스크롤
element = driver.find_element(By.ID, "my-element")
driver.execute_script("arguments[0].scrollIntoView(true);", element)

# 페이지의 높이 가져오기
page_height = driver.execute_script("return document.body.scrollHeight")

# 특정 요소의 내부 HTML 콘텐츠 가져오기
html_content = driver.execute_script("return arguments[0].innerHTML;", element)

# 웹 페이지에 있는 숨겨진 요소 표시하기
driver.execute_script("arguments[0].style.display = 'block';", hidden_element)

# 페이지의 JavaScript 변수 접근하기
js_variable = driver.execute_script("return window.someGlobalVariable;")

```

### 로딩 대기 메커니즘

동적 컨텐츠는 비동기적으로 로드되기 때문에, 요소가 실제로 나타날 때까지 기다려야 한다. Selenium은 이를 위한 여러 대기 방법을 제공한다.

### WebDriverWait

명시적 대기를 구현하는 클래스로, 특정 조건이 만족될 때까지 지정된 시간 동안 대기한다.

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 최대 10초 동안 ID가 'myDynamicElement'인 요소가 나타날 때까지 대기
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "myDynamicElement"))
)

# 또는 더 복잡한 조건 조합
element = WebDriverWait(driver, 10).until(
    EC.all_of(
        EC.presence_of_element_located((By.ID, "myElement")),
        EC.visibility_of_element_located((By.ID, "myElement"))
    )
)

```

### expected_conditions (EC)

`WebDriverWait`와 함께 사용되는 사전 정의된 조건들로, 다양한 대기 조건을 제공한다.

주요 expected_conditions:

```python
# 요소가 존재할 때까지 대기
EC.presence_of_element_located((By.ID, "element"))

# 요소가 보일 때까지 대기
EC.visibility_of_element_located((By.ID, "element"))

# 요소가 클릭 가능할 때까지 대기
EC.element_to_be_clickable((By.ID, "element"))

# 요소가 선택 가능할 때까지 대기
EC.element_to_be_selected((By.ID, "checkbox"))

# 요소의 텍스트에 특정 문자열이 포함될 때까지 대기
EC.text_to_be_present_in_element((By.ID, "element"), "예상 텍스트")

# 요소가 화면에서 사라질 때까지 대기
EC.invisibility_of_element_located((By.ID, "loading-spinner"))

# 페이지 제목이 특정 문자열을 포함할 때까지 대기
EC.title_contains("완료")

# URL이 특정 문자열을 포함할 때까지 대기
EC.url_contains("success")

# alert가 표시될 때까지 대기
EC.alert_is_present()

# 새 창/탭이 열릴 때까지 대기
EC.new_window_is_opened(current_windows)

```

### 동적 콘텐츠 로딩 예시

- 무한 스크롤 처리

```python
# 무한 스크롤 페이지에서 모든 콘텐츠 로드
SCROLL_PAUSE_TIME = 1.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩 대기
    time.sleep(SCROLL_PAUSE_TIME)

    # 새 스크롤 높이 계산 후 마지막 스크롤 높이와 비교
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # 더 이상 로드할 콘텐츠가 없으면 종료
    last_height = new_height

# 이제 모든 아이템이 로드되었으므로 데이터 추출
items = driver.find_elements(By.CSS_SELECTOR, ".item")

```

- 비동기 버튼 클릭 및 콘텐츠 로드 대기

```python
# "더 보기" 버튼을 클릭하여 추가 콘텐츠 로드
load_more_button = driver.find_element(By.ID, "load-more")

# 초기 아이템 개수 확인
items = driver.find_elements(By.CSS_SELECTOR, ".item")
initial_count = len(items)

# 버튼 클릭
load_more_button.click()

# 새로운 아이템이 로드될 때까지 대기
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(By.CSS_SELECTOR, ".item")) > initial_count
)

# 이제 새 아이템이 로드되었으므로 추가 데이터 추출
new_items = driver.find_elements(By.CSS_SELECTOR, ".item")

```

- iframe 내부의 동적 콘텐츠 처리

```python
# iframe으로 전환
iframe = driver.find_element(By.ID, "content-frame")
driver.switch_to.frame(iframe)

# iframe 내부의 동적 콘텐츠 대기
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "dynamic-content"))
)

# 데이터 추출
content = element.text

# 메인 콘텐츠로 돌아가기
driver.switch_to.default_content()

```

- SPA 네비게이션

```python
# React/Vue/Angular 앱의 메뉴 클릭
menu_item = driver.find_element(By.CSS_SELECTOR, ".nav-item[data-route='products']")
menu_item.click()

# 라우팅 후 콘텐츠 로드 대기
WebDriverWait(driver, 10).until(
    EC.url_contains("/products")
)

# URL 변경 후에도 콘텐츠 로드를 위한 시간이 필요할 수 있음
content_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "products-container"))
)

# 이제 로드된 콘텐츠에서 데이터 추출
products = content_element.find_elements(By.CSS_SELECTOR, ".product-item")

```

위와 같은 기술들을 활용하면 대부분의 동적 웹 콘텐츠에 접근하고 데이터를 추출할 수 있다. 중요한 것은 적절한 대기 전략을 사용하여 동적 콘텐츠가 완전히 로드된 후 접근함으로써 안정적인 크롤링을 구현하는 것이다.

## 🔎 execute_script() 좀 더 살펴보기

### execute_script 기본 사용법

```python
driver.execute_script(script, *args)
```

- `script`: 실행할 JavaScript 코드 문자열

- `args`: JavaScript 코드에 전달할 인자들 (선택 사항)

`execute_script`에 전달하는 문자열은 유효한 JavaScript 코드여야 한다. 그 외에는 특별한 형식 제한은 없으며, 짧은 한 줄의 코드부터 복잡한 여러 줄의 함수까지 실행할 수 있다.

### return 사용 여부

JavaScript의 `return` 문을 사용하면 `execute_script` 함수도 그 값을 Python으로 반환한다. 반환하지 않으면 `None`이 반환된다.

1. 값을 반환하는 경우:

```python
height = driver.execute_script("return document.body.scrollHeight;")
# height에는 페이지 높이 값이 저장됨

```

1. 값을 반환하지 않는 경우:

```python
driver.execute_script("window.scrollTo(0, 100);")
# 액션만 수행하고 아무것도 반환하지 않음 (None 반환)

```

### 다양한 사용 예시

- WebElement 인자 전달하기

```python
element = driver.find_element(By.ID, "my-element")
driver.execute_script("arguments[0].scrollIntoView(true);", element)

```

- 여러 인자 전달하기

```python
x, y = 100, 200
driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", x, y)

```

- 복잡한 JavaScript 로직 실행하기

```python
script = """
let elements = document.querySelectorAll('.product');
let results = [];
for (let el of elements) {
    results.push({
        name: el.querySelector('.name').textContent,
        price: el.querySelector('.price').textContent,
        available: !el.classList.contains('out-of-stock')
    });
}
return results;
"""
products = driver.execute_script(script)

```

- 비동기 JavaScript 처리

```python
# 간단한 타이머 설정
driver.execute_script("""
setTimeout(function() {
    document.getElementById('delayed-element').style.display = 'block';
}, 2000);
""")

```

- JavaScript 변수 접근하기

```python
# 페이지에 정의된 전역 변수 접근
app_data = driver.execute_script("return window.appData;")

```

<br/>

