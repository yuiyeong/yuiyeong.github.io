---
title: "Streamlit으로 5분 만에 데이터 앱 만들기: 파이썬 개발자를 위한 완벽 가이드"
date: 2025-08-25 16:01:00 +0900
categories: []
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- streamlit==1.40.0
- pandas==2.2.3
- numpy==1.26.4
- matplotlib==3.10.1
- plotly==5.24.1
- altair==5.4.1

## 🚀 TL;DR

- **Streamlit**은 파이썬 스크립트를 몇 줄의 코드만으로 **웹 애플리케이션**으로 변환해주는 오픈소스 프레임워크
- HTML/CSS/JavaScript 지식 없이도 **데이터 시각화**, **머신러닝 모델 데모**, **대시보드**를 빠르게 구축 가능
- **위젯**(버튼, 슬라이더, 텍스트 입력 등)과 **데이터 시각화** 도구가 내장되어 있어 즉시 활용 가능
- **파일 업로드**, **세션 상태 관리**, **캐싱** 기능으로 복잡한 애플리케이션도 구현 가능
- **핫 리로드** 기능으로 코드 수정 시 자동으로 앱이 업데이트되어 개발 속도가 매우 빠름
- 데이터 과학자, ML 엔지니어가 **프로토타입**을 빠르게 만들고 **공유**하는 데 최적화
- **Streamlit Community Cloud**를 통해 무료로 앱을 배포하고 공유 가능

## 📓 실습 Jupyter Notebook

- w.i.p.

## 🎯 Streamlit이란 무엇인가?

Streamlit은 데이터 과학자와 머신러닝 엔지니어를 위해 설계된 **오픈소스 파이썬 프레임워크**다. 복잡한 웹 개발 지식 없이도 데이터 중심의 웹 애플리케이션을 만들 수 있도록 해준다.

### 왜 Streamlit을 사용하는가?

기존 웹 개발과 Streamlit의 차이를 비교해보면 그 장점이 명확해진다.

- **기존 웹 개발**: Flask/Django + HTML + CSS + JavaScript + 배포 설정
- **Streamlit**: 파이썬 코드만으로 모든 것을 해결

```python
# 전통적인 Flask 앱 (복잡함)
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    # 처리 로직
    return json.dumps(result)

# HTML, CSS, JavaScript 파일 별도 필요...
```

```python
# Streamlit 앱 (간단함!)
import streamlit as st

st.title("내 첫 Streamlit 앱")
user_input = st.text_input("이름을 입력하세요")
if st.button("제출"):
    st.write(f"안녕하세요, {user_input}님!")
# 끝! 이게 전부다.
```

### Streamlit의 핵심 철학

- **파이썬이 전부다**: 프론트엔드 지식이 필요 없다
- **선언적 프로그래밍**: 무엇을 보여줄지만 작성하면 된다
- **자동 리렌더링**: 사용자 입력에 따라 자동으로 화면이 업데이트된다
- **상태 관리 자동화**: 복잡한 상태 관리를 프레임워크가 처리한다

## 🛠️ Streamlit 설치 및 첫 앱 실행

### 설치하기

Streamlit 설치는 pip 한 줄이면 충분하다.

```python
# 터미널에서 실행
pip install streamlit

# 설치 확인
streamlit hello
# 브라우저가 자동으로 열리며 데모 앱이 실행됨
```

### 첫 번째 앱 만들기

`app.py` 파일을 만들고 다음 코드를 작성한다.

```python
import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="나의 첫 Streamlit 앱",
    page_icon="🎈",
    layout="wide"
)

# 제목과 설명
st.title("🎈 Streamlit 입문하기")
st.markdown("""
이것은 **Streamlit**으로 만든 첫 번째 웹 애플리케이션이다.
- 설치가 간단하다
- 코드가 직관적이다
- 결과가 즉시 보인다
""")

# 데이터 생성
data = pd.DataFrame({
    'x': np.arange(1, 11),
    'y': np.random.randn(10).cumsum()
})

# 데이터 표시
st.subheader("📊 샘플 데이터")
st.dataframe(data)

# 차트 그리기
st.subheader("📈 라인 차트")
st.line_chart(data.set_index('x'))
```

### 앱 실행하기

```bash
# 터미널에서 실행
streamlit run app.py

# 출력:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.1.100:8501
```

> Streamlit은 **핫 리로드**를 지원한다. 코드를 수정하고 저장하면 브라우저에서 자동으로 새로고침되어 변경사항이 즉시 반영된다! {: .prompt-tip}

## 📝 텍스트 표시 컴포넌트

Streamlit은 다양한 텍스트 표시 방법을 제공한다. 각각의 용도와 스타일이 다르므로 상황에 맞게 선택해서 사용한다.

### 기본 텍스트 표시

```python
import streamlit as st

# 제목 계층 구조
st.title("가장 큰 제목 - Title")
st.header("중간 제목 - Header")
st.subheader("작은 제목 - Subheader")

# 일반 텍스트
st.text("일반 텍스트는 고정폭 글꼴로 표시된다.")
st.write("write는 거의 모든 것을 표시할 수 있는 만능 함수다.")

# 마크다운
st.markdown("""
### 마크다운 지원
- **굵은 글씨**
- *기울임체*
- `코드 하이라이트`
- [링크](https://streamlit.io)

수식도 지원한다:
$$ E = mc^2 $$
""")

# 코드 블록
code = '''
def hello():
    print("Hello, Streamlit!")
'''
st.code(code, language='python')

# LaTeX 수식
st.latex(r'''
    \begin{pmatrix}
    a & b \\
    c & d
    \end{pmatrix}
''')
```

### 특수 텍스트 표시

```python
# 성공/정보/경고/에러 메시지
st.success("✅ 작업이 성공적으로 완료되었다!")
st.info("ℹ️ 참고할 정보가 있다.")
st.warning("⚠️ 주의가 필요한 사항이다.")
st.error("❌ 오류가 발생했다!")

# 예외 표시
try:
    1 / 0
except Exception as e:
    st.exception(e)

# 풍선과 눈 애니메이션 (재미있는 효과)
if st.button("축하합니다! 🎉"):
    st.balloons()  # 풍선 애니메이션
    
if st.button("겨울이 왔어요! ❄️"):
    st.snow()  # 눈 내리는 애니메이션
```

> `st.write()`는 Streamlit의 **스위스 아미 나이프**다. 텍스트, 데이터프레임, 차트, 딕셔너리 등 거의 모든 파이썬 객체를 자동으로 적절한 형태로 표시해준다! {: .prompt-tip}

## 🎮 입력 위젯 컴포넌트

사용자로부터 입력을 받는 다양한 위젯을 제공한다. 각 위젯은 사용자 입력값을 반환한다.

### 텍스트 입력

```python
import streamlit as st

# 한 줄 텍스트 입력
name = st.text_input("이름을 입력하세요", placeholder="홍길동")
if name:
    st.write(f"안녕하세요, {name}님!")

# 비밀번호 입력
password = st.text_input("비밀번호", type="password")

# 여러 줄 텍스트 입력
bio = st.text_area("자기소개", height=150, max_chars=500)
st.write(f"입력한 글자 수: {len(bio)}")

# 숫자 입력
age = st.number_input("나이", min_value=0, max_value=150, value=25, step=1)
st.write(f"당신은 {age}살이군요!")

# 실수 입력
price = st.number_input("가격", min_value=0.0, max_value=1000000.0, 
                        value=100.0, step=0.01, format="%.2f")
```

### 선택 위젯

```python
# 선택 박스 (드롭다운)
genre = st.selectbox(
    "좋아하는 영화 장르를 선택하세요",
    ["액션", "코미디", "드라마", "공포", "SF"]
)
st.write(f"선택한 장르: {genre}")

# 다중 선택
languages = st.multiselect(
    "할 수 있는 프로그래밍 언어를 모두 선택하세요",
    ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
    default=["Python"]
)
st.write(f"선택한 언어: {', '.join(languages)}")

# 라디오 버튼
gender = st.radio(
    "성별을 선택하세요",
    ["남성", "여성", "기타"],
    horizontal=True  # 가로 배치
)

# 체크박스
agree = st.checkbox("이용약관에 동의합니다")
if agree:
    st.write("동의해주셔서 감사합니다!")
```

### 슬라이더와 범위 선택

```python
# 단일 값 슬라이더
volume = st.slider("볼륨", min_value=0, max_value=100, value=50)
st.write(f"현재 볼륨: {volume}")

# 범위 슬라이더
price_range = st.slider(
    "가격 범위를 선택하세요",
    min_value=0, max_value=1000,
    value=(100, 500),  # 튜플로 초기값 설정
    step=10
)
st.write(f"선택한 범위: ${price_range[0]} - ${price_range[1]}")

# 날짜/시간 선택
import datetime

date = st.date_input(
    "날짜를 선택하세요",
    value=datetime.date.today(),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)

time = st.time_input("시간을 선택하세요", datetime.time(8, 45))
```

### 버튼과 액션

```python
# 일반 버튼
if st.button("클릭하세요!", type="primary"):
    st.write("버튼이 클릭되었다!")
    # 버튼 클릭 시에만 실행되는 코드
    result = expensive_computation()
    st.write(result)

# 다운로드 버튼
data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
csv = data.to_csv(index=False)
st.download_button(
    label="CSV 다운로드",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
)

# 링크 버튼
st.link_button("Streamlit 공식 사이트", "https://streamlit.io")

# 색상 선택기
color = st.color_picker("좋아하는 색상을 선택하세요", "#00f900")
st.write(f"선택한 색상: {color}")
```

## 📊 데이터 표시 컴포넌트

데이터를 효과적으로 표시하는 것은 데이터 앱의 핵심이다. Streamlit은 다양한 데이터 표시 방법을 제공한다.

### 데이터프레임 표시

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '정수진', '최동욱'],
    '나이': [25, 30, 35, 28, 42],
    '부서': ['개발', '마케팅', '개발', '인사', '영업'],
    '연봉': [4500, 5200, 6800, 4800, 5500],
    '평가': [4.2, 4.8, 4.5, 4.6, 4.3]
})

# 기본 데이터프레임 표시
st.subheader("📋 기본 데이터프레임")
st.dataframe(df)

# 스타일링된 데이터프레임
st.subheader("🎨 스타일링된 데이터프레임")
st.dataframe(
    df.style.highlight_max(axis=0, subset=['연봉', '평가']),
    use_container_width=True,
    hide_index=True
)

# 편집 가능한 데이터프레임
st.subheader("✏️ 편집 가능한 데이터프레임")
edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # 행 추가/삭제 가능
    disabled=['이름'],  # 특정 컬럼 편집 불가
    column_config={
        "평가": st.column_config.NumberColumn(
            "평가 점수",
            help="5점 만점",
            min_value=0,
            max_value=5,
            step=0.1,
            format="%.1f ⭐"
        ),
        "연봉": st.column_config.NumberColumn(
            "연봉 (만원)",
            help="연간 급여",
            format="₩%d"
        )
    }
)

# 정적 테이블 (스크롤 없음)
st.subheader("📊 정적 테이블")
st.table(df.head(3))

# 메트릭 표시
st.subheader("📈 주요 지표")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="평균 연봉",
        value=f"₩{df['연봉'].mean():.0f}만원",
        delta=f"+{df['연봉'].std():.0f}"
    )
    
with col2:
    st.metric(
        label="평균 나이",
        value=f"{df['나이'].mean():.1f}세",
        delta="-2.3세",
        delta_color="inverse"
    )
    
with col3:
    st.metric(
        label="직원 수",
        value=len(df),
        delta="+2명"
    )
```

### JSON과 딕셔너리 표시

```python
# JSON 데이터 표시
json_data = {
    "name": "Streamlit",
    "version": "1.40.0",
    "features": {
        "widgets": ["button", "slider", "text_input"],
        "charts": ["line", "bar", "scatter"],
        "layout": ["columns", "sidebar", "expander"]
    },
    "is_awesome": True
}

st.json(json_data, expanded=True)

# 딕셔너리를 테이블로 표시
info = {
    "프레임워크": "Streamlit",
    "언어": "Python",
    "난이도": "쉬움",
    "추천도": "⭐⭐⭐⭐⭐"
}

st.table(pd.DataFrame([info]))
```

## 📈 차트와 시각화

Streamlit은 여러 차트 라이브러리를 지원한다. 내장 차트부터 Plotly, Altair, Matplotlib까지 다양하게 활용할 수 있다.

### 내장 차트

```python
import numpy as np
import pandas as pd

# 샘플 데이터 생성
dates = pd.date_range('2024-01-01', periods=30)
data = pd.DataFrame({
    '매출': np.random.randn(30).cumsum() + 100,
    '비용': np.random.randn(30).cumsum() + 80,
    '이익': np.random.randn(30).cumsum() + 20
}, index=dates)

# 라인 차트
st.subheader("📈 라인 차트")
st.line_chart(data)

# 영역 차트
st.subheader("📊 영역 차트")
st.area_chart(data[['매출', '비용']])

# 바 차트
st.subheader("📊 바 차트")
monthly_data = data.resample('W').sum()
st.bar_chart(monthly_data)

# 산점도
st.subheader("🔵 산점도")
scatter_data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'size': np.random.randint(10, 100, 100)
})
st.scatter_chart(scatter_data, x='x', y='y', size='size')
```

### Plotly 차트

```python
import plotly.express as px
import plotly.graph_objects as go

# Plotly Express 차트
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", 
                 color="species", size="petal_length",
                 hover_data=['petal_width'])
fig.update_layout(title="Iris Dataset Scatter Plot")
st.plotly_chart(fig, use_container_width=True)

# Plotly Graph Objects
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='lines+markers',
    name='추세선'
))
fig.add_trace(go.Bar(
    x=[1, 2, 3, 4],
    y=[8, 9, 10, 11],
    name='막대'
))
fig.update_layout(title="복합 차트", hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)
```

### Matplotlib/Seaborn 차트

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib 차트
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

ax.plot(x, y1, label='sin(x)', color='blue')
ax.plot(x, y2, label='cos(x)', color='red')
ax.set_xlabel('X축')
ax.set_ylabel('Y축')
ax.set_title('삼각함수 그래프')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Seaborn 히트맵
corr = df.select_dtypes(include=[np.number]).corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
```

### 지도 시각화

```python
# 샘플 위치 데이터
map_data = pd.DataFrame({
    'lat': [37.5665, 37.5510, 37.5795, 37.5407],
    'lon': [126.9780, 126.9882, 126.9773, 126.9906],
    'name': ['서울시청', '남산타워', '경복궁', '이태원']
})

# 기본 지도
st.map(map_data)

# Pydeck을 사용한 고급 지도
import pydeck as pdk

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.5665,
        longitude=126.9780,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=map_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))
```

## 🎨 레이아웃과 컨테이너

효과적인 UI를 만들기 위해서는 레이아웃 구성이 중요하다. Streamlit은 다양한 레이아웃 옵션을 제공한다.

### 컬럼 레이아웃

```python
# 균등한 컬럼
col1, col2, col3 = st.columns(3)

with col1:
    st.header("첫 번째 컬럼")
    st.write("이곳은 첫 번째 컬럼이다.")
    st.button("버튼 1")

with col2:
    st.header("두 번째 컬럼")
    st.write("이곳은 두 번째 컬럼이다.")
    st.button("버튼 2")

with col3:
    st.header("세 번째 컬럼")
    st.write("이곳은 세 번째 컬럼이다.")
    st.button("버튼 3")

# 비율을 지정한 컬럼
col1, col2 = st.columns([2, 1])  # 2:1 비율

with col1:
    st.write("넓은 컬럼 (66.6%)")
    st.area_chart(np.random.randn(20, 3))

with col2:
    st.write("좁은 컬럼 (33.3%)")
    st.metric("KPI", "123", "+10%")
```

### 탭 레이아웃

```python
tab1, tab2, tab3 = st.tabs(["📊 데이터", "📈 차트", "🔍 분석"])

with tab1:
    st.header("데이터 탭")
    df = pd.DataFrame(np.random.randn(10, 5))
    st.dataframe(df)

with tab2:
    st.header("차트 탭")
    st.line_chart(df)

with tab3:
    st.header("분석 탭")
    st.write("통계 요약:")
    st.write(df.describe())
```

### 확장 가능한 컨테이너

```python
# Expander
with st.expander("자세한 정보 보기"):
    st.write("이 섹션은 기본적으로 접혀있다.")
    st.write("사용자가 클릭하면 펼쳐진다.")
    st.code("""
    def hello():
        return "Hello, World!"
    """)

# Container
with st.container():
    st.write("컨테이너 안의 내용")
    
    # 컨테이너 안에 컬럼
    col1, col2 = st.columns(2)
    with col1:
        st.write("컨테이너 내 첫 번째 컬럼")
    with col2:
        st.write("컨테이너 내 두 번째 컬럼")

# Empty placeholder (나중에 업데이트 가능)
placeholder = st.empty()
placeholder.text("로딩 중...")

# 나중에 업데이트
import time
time.sleep(2)
placeholder.success("로딩 완료!")
```

### 사이드바

```python
# 사이드바에 위젯 추가
with st.sidebar:
    st.title("⚙️ 설정")
    
    # 사이드바 위젯
    model = st.selectbox(
        "모델 선택",
        ["Linear Regression", "Random Forest", "XGBoost"]
    )
    
    st.slider("하이퍼파라미터", 0, 100, 50)
    
    st.write("---")  # 구분선
    
    # 파일 업로더
    uploaded_file = st.file_uploader("데이터 업로드")
    
    # 정보 표시
    st.info("사이드바는 설정이나 필터를 배치하기 좋다.")

# 메인 영역
st.title("메인 대시보드")
st.write(f"선택한 모델: {model}")
```

## 📁 파일 업로드와 처리

파일 업로드는 데이터 앱에서 매우 중요한 기능이다. Streamlit은 다양한 파일 형식을 쉽게 처리할 수 있도록 지원한다.

### 기본 파일 업로드

```python
import streamlit as st
import pandas as pd
from PIL import Image
import io

# 단일 파일 업로드
uploaded_file = st.file_uploader(
    "파일을 선택하세요",
    type=['csv', 'txt', 'xlsx', 'json']
)

if uploaded_file is not None:
    # 파일 정보 표시
    file_details = {
        "파일명": uploaded_file.name,
        "파일 타입": uploaded_file.type,
        "파일 크기": f"{uploaded_file.size} bytes"
    }
    st.write(file_details)
    
    # 파일 타입에 따른 처리
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    
    elif uploaded_file.type == "application/json":
        import json
        data = json.load(uploaded_file)
        st.json(data)

# 다중 파일 업로드
uploaded_files = st.file_uploader(
    "여러 파일 선택 가능",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"업로드된 파일: {uploaded_file.name}")
```

### CSV 파일 처리 예제

```python
st.header("📊 CSV 파일 분석기")

# CSV 파일 업로더
csv_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if csv_file is not None:
    # 데이터 읽기
    df = pd.read_csv(csv_file)
    
    # 탭으로 구성
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 데이터", "📊 통계", "📈 시각화", "🔍 필터링"]
    )
    
    with tab1:
        st.subheader("원본 데이터")
        st.dataframe(df, use_container_width=True)
        
        # 데이터 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("행 수", len(df))
        with col2:
            st.metric("열 수", len(df.columns))
        with col3:
            st.metric("결측값", df.isnull().sum().sum())
    
    with tab2:
        st.subheader("기술 통계")
        st.dataframe(df.describe())
        
        # 데이터 타입
        st.subheader("데이터 타입")
        dtype_df = pd.DataFrame({
            '컬럼': df.columns,
            '타입': df.dtypes.values
        })
        st.table(dtype_df)
    
    with tab3:
        st.subheader("데이터 시각화")
        
        # 숫자형 컬럼만 선택
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) > 0:
            # 차트 타입 선택
            chart_type = st.selectbox(
                "차트 타입",
                ["Line Chart", "Bar Chart", "Scatter Plot"]
            )
            
            if chart_type == "Line Chart":
                st.line_chart(df[numeric_cols])
            elif chart_type == "Bar Chart":
                st.bar_chart(df[numeric_cols].head(20))
            else:  # Scatter Plot
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X축", numeric_cols)
                    y_col = st.selectbox("Y축", numeric_cols)
                    st.scatter_chart(df[[x_col, y_col]].dropna())
    
    with tab4:
        st.subheader("데이터 필터링")
        
        # 컬럼 선택
        selected_cols = st.multiselect(
            "표시할 컬럼 선택",
            df.columns.tolist(),
            default=df.columns.tolist()
        )
        
        # 필터 조건
        filtered_df = df[selected_cols].copy()
        
        for col in selected_cols:
            if df[col].dtype in ['int64', 'float64']:
                min_val, max_val = st.slider(
                    f"{col} 범위",
                    float(df[col].min()),
                    float(df[col].max()),
                    (float(df[col].min()), float(df[col].max()))
                )
                filtered_df = filtered_df[
                    (filtered_df[col] >= min_val) & 
                    (filtered_df[col] <= max_val)
                ]
        
        st.dataframe(filtered_df)
        
        # 필터링된 데이터 다운로드
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 필터링된 데이터 다운로드",
            csv,
            "filtered_data.csv",
            "text/csv"
        )
```

### 이미지 파일 처리

```python
st.header("🖼️ 이미지 처리기")

uploaded_image = st.file_uploader(
    "이미지를 업로드하세요",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp']
)

if uploaded_image is not None:
    # PIL로 이미지 열기
    image = Image.open(uploaded_image)
    
    # 이미지 정보
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("원본 이미지")
        st.image(image, caption=uploaded_image.name, use_column_width=True)
        
        # 이미지 정보
        st.write(f"크기: {image.size}")
        st.write(f"모드: {image.mode}")
        st.write(f"포맷: {image.format}")
    
    with col2:
        st.subheader("이미지 편집")
        
        # 크기 조절
        scale = st.slider("크기 조절 (%)", 10, 200, 100)
        new_size = (
            int(image.size[0] * scale / 100),
            int(image.size[1] * scale / 100)
        )
        resized_image = image.resize(new_size)
        
        # 회전
        rotation = st.slider("회전 (도)", -180, 180, 0)
        rotated_image = resized_image.rotate(rotation)
        
        # 편집된 이미지 표시
        st.image(rotated_image, caption="편집된 이미지", use_column_width=True)
        
        # 편집된 이미지 다운로드
        buf = io.BytesIO()
        rotated_image.save(buf, format='PNG')
        byte_im = buf.getvalue()
        
        st.download_button(
            label="편집된 이미지 다운로드",
            data=byte_im,
            file_name='edited_image.png',
            mime='image/png'
        )
```

## 💾 세션 상태 관리

Streamlit은 기본적으로 스크립트를 위에서 아래로 재실행하는 방식으로 동작한다. 따라서 상태를 유지하려면 **세션 상태(Session State)**를 사용해야 한다.

### 기본 세션 상태

```python
import streamlit as st

# 세션 상태 초기화
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# 카운터 앱
st.title("🔢 카운터 앱")
st.write(f"현재 카운트: {st.session_state.counter}")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ 증가"):
        st.session_state.counter += 1
        st.rerun()  # 화면 새로고침

with col2:
    if st.button("➖ 감소"):
        st.session_state.counter -= 1
        st.rerun()

with col3:
    if st.button("🔄 리셋"):
        st.session_state.counter = 0
        st.rerun()
```

### 폼과 세션 상태

```python
# 사용자 정보 폼
st.header("📝 회원가입 폼")

# 세션 상태로 사용자 정보 관리
if 'users' not in st.session_state:
    st.session_state.users = []

with st.form("registration_form"):
    st.subheader("사용자 정보 입력")
    
    name = st.text_input("이름")
    email = st.text_input("이메일")
    age = st.number_input("나이", min_value=1, max_value=100)
    country = st.selectbox("국가", ["한국", "미국", "일본", "중국", "기타"])
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("등록", type="primary")
    with col2:
        clear = st.form_submit_button("초기화")
    
    if submitted and name and email:
        # 사용자 정보 저장
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "country": country
        }
        st.session_state.users.append(user_info)
        st.success(f"✅ {name}님이 등록되었습니다!")
    
    if clear:
        st.session_state.users = []
        st.info("모든 사용자 정보가 삭제되었습니다.")

# 등록된 사용자 목록
if st.session_state.users:
    st.subheader("📋 등록된 사용자")
    df = pd.DataFrame(st.session_state.users)
    st.dataframe(df, use_container_width=True)
    
    # 통계
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 사용자", len(df))
    with col2:
        st.metric("평균 나이", f"{df['age'].mean():.1f}")
    with col3:
        most_common = df['country'].mode()[0]
        st.metric("가장 많은 국가", most_common)
```

### 콜백 함수와 세션 상태

```python
# 콜백 함수를 사용한 상태 관리
st.header("🎮 실시간 계산기")

def update_result():
    """두 숫자의 합을 계산하는 콜백 함수"""
    st.session_state.result = st.session_state.num1 + st.session_state.num2

# 숫자 입력 (콜백 함수 연결)
col1, col2 = st.columns(2)

with col1:
    st.number_input(
        "첫 번째 숫자",
        key="num1",
        on_change=update_result
    )

with col2:
    st.number_input(
        "두 번째 숫자",
        key="num2",
        on_change=update_result
    )

# 결과 표시
if 'result' in st.session_state:
    st.success(f"결과: {st.session_state.result}")
```

## ⚡ 캐싱과 성능 최적화

대용량 데이터나 복잡한 계산을 다룰 때는 캐싱이 필수다. Streamlit은 강력한 캐싱 메커니즘을 제공한다.

### @st.cache_data 데코레이터

```python
import time

@st.cache_data  # 데이터 캐싱
def load_large_dataset(file_path):
    """대용량 데이터셋 로딩 (캐싱됨)"""
    time.sleep(3)  # 시뮬레이션: 로딩에 3초 소요
    return pd.read_csv(file_path)

@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def fetch_api_data(api_url):
    """API 데이터 가져오기 (1시간 캐싱)"""
    response = requests.get(api_url)
    return response.json()

@st.cache_data
def expensive_computation(n):
    """복잡한 계산 (결과 캐싱)"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result

# 캐싱된 함수 사용
st.header("⚡ 캐싱 데모")

if st.button("대용량 데이터 로드"):
    with st.spinner("데이터 로딩 중... (첫 번째만 느림)"):
        # 첫 실행은 3초, 이후는 즉시 로드
        df = load_large_dataset("large_data.csv")
        st.success("데이터 로드 완료!")
        st.dataframe(df.head())

n = st.slider("계산 복잡도", 1000, 1000000, 10000)
result = expensive_computation(n)
st.write(f"계산 결과: {result:,}")
```

### @st.cache_resource 데코레이터

```python
@st.cache_resource  # 리소스 캐싱 (ML 모델, DB 연결 등)
def load_model():
    """머신러닝 모델 로드 (한 번만 로드)"""
    import joblib
    model = joblib.load("model.pkl")
    return model

@st.cache_resource
def init_database_connection():
    """데이터베이스 연결 초기화"""
    import sqlite3
    conn = sqlite3.connect("database.db")
    return conn

# 캐싱된 모델 사용
model = load_model()
prediction = model.predict(input_data)
```

### 캐시 관리

```python
# 캐시 클리어 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("데이터 캐시 클리어"):
        st.cache_data.clear()
        st.success("데이터 캐시가 클리어되었습니다!")

with col2:
    if st.button("리소스 캐시 클리어"):
        st.cache_resource.clear()
        st.success("리소스 캐시가 클리어되었습니다!")

with col3:
    if st.button("전체 캐시 클리어"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("모든 캐시가 클리어되었습니다!")
```

## 🚀 실제 활용 예제: 머신러닝 모델 데모 앱

모든 기능을 종합한 실제 머신러닝 데모 앱을 만들어보자.

```python
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="ML Model Demo",
    page_icon="🤖",
    layout="wide"
)

# 제목과 설명
st.title("🤖 머신러닝 모델 데모")
st.markdown("""
이 앱은 Streamlit의 주요 기능을 활용한 머신러닝 모델 데모입니다.
- 데이터 업로드 및 전처리
- 모델 학습 및 평가
- 예측 및 시각화
""")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 모델 설정")
    
    # 모델 파라미터
    n_estimators = st.slider("트리 개수", 10, 200, 100)
    max_depth = st.slider("최대 깊이", 1, 20, 10)
    test_size = st.slider("테스트 데이터 비율", 0.1, 0.5, 0.2)
    
    random_state = st.number_input("Random State", 0, 100, 42)

# 메인 컨텐츠
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 데이터", "🎯 모델 학습", "🔮 예측", "📈 시각화"]
)

with tab1:
    st.header("데이터 업로드")
    
    # 샘플 데이터 생성 옵션
    use_sample = st.checkbox("샘플 데이터 사용")
    
    if use_sample:
        # 샘플 데이터 생성
        from sklearn.datasets import make_classification
        X, y = make_classification(
            n_samples=1000,
            n_features=20,
            n_informative=15,
            n_redundant=5,
            random_state=random_state
        )
        
        # DataFrame으로 변환
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        
        st.success("✅ 샘플 데이터가 생성되었습니다!")
    else:
        # 파일 업로드
        uploaded_file = st.file_uploader(
            "CSV 파일을 업로드하세요",
            type=['csv']
        )
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ {uploaded_file.name} 파일이 로드되었습니다!")
    
    # 데이터 표시
    if 'df' in locals():
        st.subheader("데이터 미리보기")
        st.dataframe(df.head(), use_container_width=True)
        
        # 데이터 정보
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("샘플 수", len(df))
        with col2:
            st.metric("특성 수", len(df.columns)-1)
        with col3:
            st.metric("타겟 클래스", df['target'].nunique())
        with col4:
            st.metric("결측값", df.isnull().sum().sum())
        
        # 세션 상태에 저장
        st.session_state.df = df

with tab2:
    st.header("모델 학습")
    
    if 'df' in st.session_state:
        df = st.session_state.df
        
        # 특성과 타겟 분리
        X = df.drop('target', axis=1)
        y = df['target']
        
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # 모델 학습 버튼
        if st.button("🚀 모델 학습 시작", type="primary"):
            with st.spinner("모델 학습 중..."):
                # 모델 생성 및 학습
                model = RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    random_state=random_state
                )
                model.fit(X_train, y_train)
                
                # 예측 및 평가
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                # 세션 상태에 저장
                st.session_state.model = model
                st.session_state.accuracy = accuracy
                st.session_state.X_test = X_test
                st.session_state.y_test = y_test
                st.session_state.y_pred = y_pred
                st.session_state.feature_names = X.columns.tolist()
            
            st.success(f"✅ 모델 학습 완료! 정확도: {accuracy:.4f}")
            
            # 특성 중요도
            st.subheader("특성 중요도")
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            fig = px.bar(
                feature_importance.head(10),
                x='importance',
                y='feature',
                orientation='h',
                title="Top 10 중요 특성"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("먼저 데이터를 업로드해주세요!")

with tab3:
    st.header("새로운 데이터 예측")
    
    if 'model' in st.session_state:
        model = st.session_state.model
        feature_names = st.session_state.feature_names
        
        st.subheader("특성 값 입력")
        
        # 입력 폼 생성
        input_data = {}
        cols = st.columns(4)
        
        for i, feature in enumerate(feature_names):
            with cols[i % 4]:
                input_data[feature] = st.number_input(
                    feature,
                    value=0.0,
                    format="%.4f",
                    key=f"input_{feature}"
                )
        
        # 예측 버튼
        if st.button("🔮 예측하기"):
            # 입력 데이터를 DataFrame으로 변환
            input_df = pd.DataFrame([input_data])
            
            # 예측
            prediction = model.predict(input_df)[0]
            prediction_proba = model.predict_proba(input_df)[0]
            
            # 결과 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("예측 클래스", int(prediction))
            
            with col2:
                st.metric(
                    "예측 확률",
                    f"{prediction_proba[prediction]:.2%}"
                )
            
            # 확률 분포 차트
            proba_df = pd.DataFrame({
                'Class': range(len(prediction_proba)),
                'Probability': prediction_proba
            })
            
            fig = px.bar(
                proba_df,
                x='Class',
                y='Probability',
                title="클래스별 예측 확률"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("먼저 모델을 학습시켜주세요!")

with tab4:
    st.header("모델 성능 시각화")
    
    if 'y_test' in st.session_state:
        y_test = st.session_state.y_test
        y_pred = st.session_state.y_pred
        
        # Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)
        
        fig = px.imshow(
            cm,
            labels=dict(x="예측", y="실제", color="개수"),
            title="Confusion Matrix",
            color_continuous_scale="Blues"
        )
        fig.update_xaxis(side="bottom")
        st.plotly_chart(fig, use_container_width=True)
        
        # 분류 리포트
        st.subheader("분류 성과 리포트")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(
            report_df.style.highlight_max(axis=0),
            use_container_width=True
        )
    else:
        st.warning("먼저 모델을 학습시켜주세요!")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
```

> Streamlit은 데이터 과학자와 ML 엔지니어가 **복잡한 웹 개발 지식 없이도** 강력한 데이터 앱을 만들 수 있게 해주는 혁신적인 도구다. 몇 줄의 파이썬 코드만으로 프로토타입부터 프로덕션 수준의 앱까지 만들 수 있다! {: .prompt-tip}

## 🎯 Streamlit 활용 팁과 모범 사례

### 성능 최적화

- **캐싱 적극 활용**: 데이터 로딩, API 호출, 복잡한 계산은 반드시 캐싱
- **세션 상태 활용**: 불필요한 재계산 방지를 위해 결과를 세션 상태에 저장
- **청크 단위 처리**: 대용량 데이터는 청크로 나누어 처리
- **비동기 처리**: 오래 걸리는 작업은 스피너와 함께 표시

### 사용자 경험

- **명확한 레이아웃**: 컬럼, 탭, 사이드바를 활용한 구조화
- **진행 상태 표시**: 긴 작업에는 프로그레스 바나 스피너 사용
- **에러 처리**: try-except로 에러를 잡아 사용자 친화적 메시지 표시
- **도움말 제공**: 위젯의 help 파라미터나 expander로 설명 추가

### 배포 준비

- **requirements.txt 작성**: 필요한 패키지 버전 명시
- **config.toml 설정**: 테마, 포트 등 설정 커스터마이징
- **환경 변수 활용**: 민감한 정보는 st.secrets나 환경 변수로 관리
- **Streamlit Cloud 활용**: GitHub 연동으로 무료 배포

> Streamlit은 계속 발전하고 있는 프레임워크다. 공식 문서와 커뮤니티를 통해 최신 기능과 모범 사례를 지속적으로 학습하는 것이 중요하다! {: .prompt-tip}