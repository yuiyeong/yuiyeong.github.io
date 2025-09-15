---
title: "⚙️ Streamlit 의 설정들: config.toml로 애플리케이션 커스터마이징하기"
date: 2025-09-13 22:12:00 +0900
categories:
  - PYTHON
  - STREAMLIT
tags:
  - 급발진거북이
  - GeekAndChill
  - 기깬칠
  - streamlit
  - python-web
  - 스트림릿
  - 파이썬
  - python
  - configutation
  - streamlit_config
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- streamlit==1.49.1
- python==3.12

## 🚀 TL;DR

- **Streamlit config.toml**은 애플리케이션의 모든 동작을 세밀하게 제어할 수 있는 설정 파일이다
- **전역 설정**에서는 위젯 중복 경고, 스크립트 실행 경고 등 기본 동작을 제어한다
- **서버 설정**으로 포트, 주소, CORS, 파일 업로드 제한 등 웹 서버 동작을 커스터마이징할 수 있다
- **테마 설정**을 통해 색상, 폰트, 레이아웃 등 UI 전반을 브랜딩에 맞게 변경할 수 있다
- **개발 환경**에서는 자동 새로고침, 에러 표시 수준, 매직 명령어 등으로 개발 효율성을 높일 수 있다
- **보안 설정**으로 CORS, XSRF 보호, SSL 인증서 등을 구성하여 프로덕션 환경에 안전하게 배포할 수 있다
- **로깅 설정**으로 디버깅과 모니터링에 필요한 상세한 로그 정보를 수집할 수 있다
- 설정 파일은 `~/.streamlit/config.toml` 또는 프로젝트 루트의 `.streamlit/config.toml`에 위치한다

## 📓 실습 환경

- w.i.p.

## 🌍 전역 설정 (Global Configuration)

전역 설정은 Streamlit 애플리케이션의 기본 동작을 제어하는 최상위 설정이다.

### 위젯 상태 중복 경고 비활성화

```toml
[global]
disableWidgetStateDuplicationWarning = false
```

위젯 함수에서 기본값을 설정하고 동시에 `st.session_state`에서도 같은 키로 값을 설정했을 때 나타나는 경고를 제어한다.

```python
import streamlit as st

# 이런 상황에서 경고가 발생
st.session_state.my_slider = 50
value = st.slider("값 선택", 0, 100, 25, key="my_slider")  # 경고 발생
```

> **개발 팁**: 프로덕션 환경에서는 `true`로 설정하여 사용자에게 불필요한 경고를 숨기는 것이 좋다. 
{: .prompt-tip}

### 직접 실행 경고

```toml
[global]
showWarningOnDirectExecution = true
```

`python my_app.py`로 직접 실행할 때 `streamlit run` 사용을 권장하는 경고를 표시한다.

## 📊 로깅 설정 (Logger Configuration)

개발과 운영 환경에서 효과적인 디버깅과 모니터링을 위한 로깅 설정이다.

### 로그 레벨 설정

```toml
[logger]
level = "info"  # "error", "warning", "info", "debug"
messageFormat = "%(asctime)s %(message)s"
```

**로그 레벨별 활용 사례**

- `"error"`: 프로덕션 환경에서 심각한 오류만 기록
- `"warning"`: 운영 환경에서 잠재적 문제 모니터링
- `"info"`: 일반적인 개발/운영 환경
- `"debug"`: 개발 중 상세한 디버깅 정보 필요시

```python
# 로그 활용 예시
import logging
import streamlit as st

logger = logging.getLogger(__name__)

@st.cache_data
def load_data():
    logger.info("데이터 로딩 시작")
    try:
        # 데이터 로딩 로직
        data = fetch_data()
        logger.info(f"데이터 로딩 완료: {len(data)}개 행")
        return data
    except Exception as e:
        logger.error(f"데이터 로딩 실패: {e}")
        raise
```

## 🌐 브라우저 설정 (Browser Configuration)

클라이언트 브라우저와의 연결 및 상호작용을 제어하는 설정이다.

### 서버 주소 및 포트 설정

```toml
[browser]
serverAddress = "localhost"
serverPort = 8501
gatherUsageStats = true
```

**실무 활용 사례**

```toml
# 개발 환경
[browser]
serverAddress = "localhost"
serverPort = 8501

# 내부 네트워크 공유
[browser]
serverAddress = "0.0.0.0"  # 모든 인터페이스에서 접근 가능
serverPort = 8080

# 프로덕션 환경 (리버스 프록시 뒤)
[browser]
serverAddress = "127.0.0.1"
serverPort = 8501
gatherUsageStats = false  # 개인정보 보호
```

## 🖥️ 서버 설정 (Server Configuration)

Streamlit 웹 서버의 핵심 동작을 제어하는 가장 중요한 설정 섹션이다.

### 파일 감시 및 자동 새로고침

```toml
[server]
runOnSave = false
fileWatcherType = "auto"  # "auto", "watchdog", "poll", "none"
folderWatchList = []
folderWatchBlacklist = []
```

**개발 환경 최적화**

```toml
[server]
runOnSave = true  # 파일 저장시 자동 새로고침
fileWatcherType = "watchdog"  # 빠른 파일 변경 감지
folderWatchBlacklist = [
    "node_modules",
    ".git",
    "__pycache__",
    "logs"
]
```

### 네트워크 및 보안 설정

```toml
[server]
port = 8501
address = ""  # 비어있으면 모든 인터페이스
baseUrlPath = ""
enableCORS = true
corsAllowedOrigins = []
enableXsrfProtection = true
```

**프로덕션 환경 보안 설정:**

```toml
[server]
port = 8501
address = "127.0.0.1"  # 로컬호스트만 허용
baseUrlPath = "/myapp"  # 서브패스에서 서비스
enableCORS = true
corsAllowedOrigins = [
    "https://mydomain.com",
    "https://api.mydomain.com"
]
enableXsrfProtection = true
cookieSecret = "your-production-secret-key-here"
```

### 파일 업로드 제한

```toml
[server]
maxUploadSize = 200  # MB
maxMessageSize = 200  # MB
```

**용도별 업로드 제한 설정**

```python
# 이미지 처리 앱
maxUploadSize = 50  # 이미지는 50MB로 제한

# 데이터 분석 앱  
maxUploadSize = 500  # CSV 파일 등 대용량 데이터 허용

# 간단한 텍스트 처리 앱
maxUploadSize = 10   # 작은 파일만 허용
```

### SSL/HTTPS 설정

```toml
[server]
sslCertFile = "/path/to/cert.pem"
sslKeyFile = "/path/to/key.pem"
```

> **프로덕션 주의사항**: Streamlit의 내장 SSL은 개발용이므로, 프로덕션에서는 nginx나 Apache 같은 리버스 프록시를 사용하는 것이 권장된다.
{: .prompt-warning}

## 🎨 테마 설정 (Theme Configuration)

Streamlit 애플리케이션의 시각적 스타일링을 완전히 커스터마이징할 수 있는 강력한 기능이다.

### 기본 테마 색상 설정

```toml
[theme]
base = "light"  # "light" or "dark"
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
linkColor = "#FF6B6B"
linkUnderline = true
```

**브랜딩 예시 - 기업용 테마**

```toml
[theme]
base = "light"
primaryColor = "#1f77b4"      # 기업 메인 컬러
backgroundColor = "#ffffff"    # 깔끔한 흰색 배경
secondaryBackgroundColor = "#f8f9fa"  # 연한 회색
textColor = "#212529"         # 진한 회색 텍스트
linkColor = "#1f77b4"         # 메인 컬러와 통일
codeBackgroundColor = "#f8f9fa"
```

**다크 테마 예시**

```toml
[theme]
base = "dark"
primaryColor = "#00D4AA"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
linkColor = "#00D4AA"
codeBackgroundColor = "#1E1E1E"
```

### 폰트 설정

```toml
[theme]
font = "sans-serif"  # "sans-serif", "serif", "monospace"
baseFontSize = 16
baseFontWeight = 400
headingFont = "serif"
headingFontSizes = ["2.75rem", "2.25rem", "1.75rem", "1.5rem", "1.25rem", "1rem"]
headingFontWeights = [700, 600, 600, 600, 600, 600]
```

**커스텀 폰트 설정**

```toml
[theme]
font = "Noto Sans KR, sans-serif"  # 한글 지원 폰트
headingFont = "Roboto Slab, serif"
baseFontSize = 14
codeFontSize = "0.875rem"
codeFontWeight = 400

# 커스텀 폰트 파일 사용시
[[theme.fontFaces]]
family = "MyCustomFont"
url = "static/fonts/custom-font.woff2"
weight = "400"
style = "normal"
```

### 차트 색상 설정

```toml
[theme]
chartCategoricalColors = [
    "#FF6B6B",  # 빨간색
    "#4ECDC4",  # 청록색
    "#45B7D1",  # 파란색
    "#96CEB4",  # 초록색
    "#FFEAA7",  # 노란색
    "#DDA0DD",  # 보라색
    "#98D8C8",  # 민트색
    "#F7DC6F",  # 금색
    "#BB8FCE",  # 라벤더색
    "#85C1E9"   # 하늘색
]

chartSequentialColors = [
    "#E8F4FD",
    "#D1E7FC", 
    "#B9D9FB",
    "#A2CCFA",
    "#8ABEF9",
    "#73B1F8",
    "#5BA4F7",
    "#4496F6",
    "#2C89F5",
    "#157BF4"
]
```

### 레이아웃 및 스타일링

```toml
[theme]
baseRadius = "0.5rem"        # 모든 요소의 기본 모서리 둥글기
buttonRadius = "0.25rem"     # 버튼 모서리 둥글기
borderColor = "#E0E0E0"      # 테두리 색상
showWidgetBorder = true      # 위젯 테두리 표시
```

## 🎛️ 사이드바 테마 설정 (Sidebar Theme)

사이드바만을 위한 별도 테마 설정으로, 메인 영역과 다른 스타일을 적용할 수 있다.

```toml
[theme.sidebar]
backgroundColor = "#F0F2F6"
primaryColor = "#1F77B4"
textColor = "#262730"
headingFontSizes = ["1.5rem", "1.25rem", "1.125rem", "1rem", "0.875rem", "0.75rem"]
showSidebarBorder = true
```

> **디자인 팁**: 사이드바는 보통 메인 영역보다 어둡거나 밝은 색상으로 구분감을 주는 것이 좋다.
{: .prompt-tip}

## 👤 클라이언트 설정 (Client Configuration)

사용자 인터페이스와 개발자 도구의 표시 방식을 제어한다.

### 에러 표시 설정

```toml
[client]
showErrorDetails = "full"  # "full", "stacktrace", "type", "none"
toolbarMode = "auto"       # "auto", "developer", "viewer", "minimal"
showSidebarNavigation = true
```

**환경별 에러 표시 설정**

```toml
# 개발 환경
[client]
showErrorDetails = "full"     # 모든 에러 정보 표시
toolbarMode = "developer"     # 개발자 도구 모두 표시

# 스테이징 환경
[client]
showErrorDetails = "stacktrace"  # 스택트레이스만 표시
toolbarMode = "auto"

# 프로덕션 환경
[client]
showErrorDetails = "none"     # 일반 에러 메시지만
toolbarMode = "viewer"        # 사용자용 도구만 표시
```

## 🏃‍♂️ 실행 환경 설정 (Runner Configuration)

Streamlit 애플리케이션의 실행 방식과 성능을 제어하는 핵심 설정이다.

### 매직 명령어 및 실행 방식

```toml
[runner]
magicEnabled = true           # 변수명만으로 출력 가능
fastReruns = true            # 빠른 재실행
enforceSerializableSessionState = false
enumCoercion = "nameOnly"    # "off", "nameOnly", "nameAndValue"
```

**매직 명령어 예시**

```python
import streamlit as st
import pandas as pd

# magicEnabled = true일 때 가능
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df  # 이것만으로도 데이터프레임이 출력됨

# 동일한 결과
st.dataframe(df)
```

**성능 최적화 설정**

```toml
# 고성능 환경
[runner]
magicEnabled = false         # 명시적 출력으로 성능 향상
fastReruns = true           # 빠른 사용자 반응
enforceSerializableSessionState = true  # 세션 상태 직렬화 강제

# 개발 편의성 우선
[runner]
magicEnabled = true         # 편리한 개발
fastReruns = true
enforceSerializableSessionState = false
```

## 🗝️ 시크릿 관리 (Secrets Management)

민감한 정보를 안전하게 관리하기 위한 설정이다.

```toml
[secrets]
files = [
    "~/.streamlit/secrets.toml",
    ".streamlit/secrets.toml"
]
```

**시크릿 파일 구조 예시**

```toml
# secrets.toml
[database]
host = "localhost"
port = 5432
username = "myuser"
password = "mypassword"

[api_keys]
openai = "sk-xxxxxxxxxxxxxxxx"
google_maps = "AIzaxxxxxxxxxxxxxxxx"

[aws]
access_key_id = "AKIAXXXXXXXXXXXXXXXX"
secret_access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
region = "us-west-2"
```

**시크릿 사용 예시**

```python
import streamlit as st

# 시크릿 정보 접근
db_config = st.secrets["database"]
api_key = st.secrets["api_keys"]["openai"]

# 데이터베이스 연결
import psycopg2
conn = psycopg2.connect(
    host=db_config["host"],
    port=db_config["port"],
    user=db_config["username"],
    password=db_config["password"]
)
```

> **보안 주의사항**: secrets.toml 파일은 절대 버전 관리 시스템에 커밋하지 말고, .gitignore에 추가해야 한다.
{: .prompt-warning}

## 🗺️ 맵박스 설정 (Mapbox Configuration)

> 현재는 deprecated!
{: .prompt-warning} 

지도 표시를 위한 맵박스 API 설정이다.

```toml
[mapbox]
token = ""  # DEPRECATED: 환경변수 MAPBOX_API_KEY 사용 권장
```

**권장 사용법**

```python
# 환경변수 사용
import os
import streamlit as st
import pydeck as pdk

# .env 파일이나 시스템 환경변수에 설정
mapbox_token = os.getenv("MAPBOX_API_KEY")

# 또는 secrets.toml에 설정
mapbox_token = st.secrets.get("MAPBOX_API_KEY", "")

# PyDeck에서 사용
st.pydeck_chart(pdk.Deck(
    api_keys={"mapbox": mapbox_token},
    # ... 차트 설정
))
```

## 🛠️ 실무 적용 시나리오

### 개발 환경 설정

```toml
# .streamlit/config.toml (개발용)
[global]
disableWidgetStateDuplicationWarning = false
showWarningOnDirectExecution = true

[logger]
level = "debug"

[server]
runOnSave = true
fileWatcherType = "watchdog"
port = 8501
address = "localhost"
maxUploadSize = 50

[client]
showErrorDetails = "full"
toolbarMode = "developer"

[runner]
magicEnabled = true
fastReruns = true
enforceSerializableSessionState = false

[theme]
base = "light"
primaryColor = "#FF4B4B"
```

### 프로덕션 환경 설정

```toml
# .streamlit/config.toml (프로덕션용)
[global]
disableWidgetStateDuplicationWarning = true
showWarningOnDirectExecution = false

[logger]
level = "warning"
messageFormat = "%(asctime)s [%(levelname)s] %(message)s"

[server]
runOnSave = false
fileWatcherType = "none"
port = 8501
address = "127.0.0.1"
headless = true
enableCORS = true
corsAllowedOrigins = ["https://mycompany.com"]
enableXsrfProtection = true
maxUploadSize = 100
cookieSecret = "production-secret-key"

[client]
showErrorDetails = "none"
toolbarMode = "viewer"

[runner]
magicEnabled = false
fastReruns = true
enforceSerializableSessionState = true

[theme]
base = "light"
primaryColor = "#1F77B4"
backgroundColor = "#FFFFFF"
font = "Roboto, sans-serif"
```

### 팀 협업 환경 설정

```toml
# .streamlit/config.toml (팀용)
[server]
port = 8501
address = "0.0.0.0"  # 네트워크 공유
runOnSave = true

[logger]
level = "info"

[client]
showErrorDetails = "stacktrace"
toolbarMode = "auto"

[theme]
base = "light"
primaryColor = "#2E86AB"
font = "Source Sans Pro, sans-serif"
```

## 📋 설정 파일 위치 및 우선순위

Streamlit은 다음 순서로 설정 파일을 찾는다.

1. **명령줄 인수**: `streamlit run app.py --server.port 8502`
2. **환경변수**: `STREAMLIT_SERVER_PORT=8502`
3. **프로젝트 설정**: `./streamlit/config.toml`
4. **전역 설정**: `~/.streamlit/config.toml`
5. **기본값**: Streamlit 내장 기본값

```python
# 설정 확인 코드
import streamlit as st

# 현재 설정값 확인
st.write("현재 테마 설정:")
st.write(f"Primary Color: {st.get_option('theme.primaryColor')}")
st.write(f"Background Color: {st.get_option('theme.backgroundColor')}")
st.write(f"Server Port: {st.get_option('server.port')}")
```

## 🎯 설정 최적화 가이드

### 성능 최적화

```toml
[server]
maxMessageSize = 50      # 메시지 크기 제한
enableWebsocketCompression = true  # 압축 활성화

[runner]
fastReruns = true       # 빠른 재실행
magicEnabled = false    # 성능을 위해 비활성화
```

### 메모리 최적화

```toml
[server]
maxUploadSize = 100     # 업로드 크기 제한
disconnectedSessionTTL = 60  # 세션 정리 주기 단축
```

### 보안 강화

```toml
[server]
enableCORS = true
enableXsrfProtection = true
corsAllowedOrigins = ["https://yourdomain.com"]
cookieSecret = "strong-random-secret"

[client]
showErrorDetails = "none"  # 에러 정보 숨김
```

> **운영 팁**: 개발, 스테이징, 프로덕션 환경별로 별도의 config.toml 파일을 관리하고, 배포 시 환경에 맞는 파일을 사용하는 것이 좋다.
{: .prompt-tip}

## 🚀 결론

Streamlit의 config.toml 파일은 단순한 웹 애플리케이션을 넘어 기업급 솔루션으로 발전시킬 수 있는 강력한 도구다. 적절한 설정을 통해 성능, 보안, 사용성을 모두 만족하는 애플리케이션을 구축할 수 있다.

**핵심 포인트**

- 개발 단계별로 적절한 설정 적용
- 보안과 성능의 균형 잡힌 구성
- 사용자 경험을 고려한 테마 커스터마이징
- 운영 환경에서의 모니터링과 로깅 체계 구축

이러한 설정들을 통해 Streamlit은 프로토타입부터 프로덕션까지 모든 단계에서 활용할 수 있는 진정한 엔터프라이즈급 플랫폼이 된다.