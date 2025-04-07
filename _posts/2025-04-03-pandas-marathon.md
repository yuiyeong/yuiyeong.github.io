---
title: 🐼 Pandas 켠김에 왕까지
date: 2025-04-03 10:09:00 +0900
categories: [ PYTHON, PANDAS ]
tags: [ '급발진거북이', 'pandas', 'excel', 'csv', 'python', '파이썬', '데이터분석' ]
toc: true
comments: false
mermaid: true
math: true
---

> 💡 `import pandas as pd`

위 구문으로 [Pandas](https://pandas.pydata.org/docs/) 를 사용한다고 전제한다.

## ⭐ 설치 및 환경

- 가상환경은 [pyenv](https://github.com/pyenv/pyenv) 와 `pyenv` 의 [virtualenv](https://github.com/pyenv/pyenv-virtualenv)
  플러그인을 사용해서 만들었다.

    - `pyenv` 설치 및 사용법은 이 [문서](https://wikidocs.net/10936#pyenv)를 참고하는 것이 좋다.

- Python: 3.12.7

- Pandas: 2.2.3

아래의 명령어를 사용해서 panas 를 설치하고 실습을 진행했다.

```shell
pip install pandas==2.2.3
```

## 💾 Pandas 의 Data 형태

### Series

- 정의: 시리즈(Series)는 데이터가 순차적으로 나열된 1차원 배열 형태

- 구조: 인덱스(index)와 값(value)이 일대일로 대응되는 구조

- pandas 에서 사용하는 일종의 리스트

- dict 로 만들기

```python
import pandas as pd

data = {'a': 1, 'b': 2, 'c': 3}
series = pd.Series(data)
```

- list 로 만들기

```python
import pandas as pd

data = [1, 2, 3, 4, 5]
series = pd.Series(data)
```

- 인덱스를 지정하지 않으면 자동으로 0부터 시작하는 정수 인덱스가 부여됨(그것을 RangeIndex 라고 함)

- 인덱스 지정 예: `series = pd.Series(data, index=['a', 'b', 'c', 'd', 'e'])`

- 자주 사용하는 속성 값

```python
import numpy as np
import pandas as pd

se = pd.Series(np.arange(10) ** 2, name="Number")

# 형태 확인
se.shape  # (10,)

# 인데스 확인
se.index.  # RangeIndex(start=0, stop=10, step=1)d

# 이름 확인
se.name  # "Number"

# 데이터의 타입 확인
se.dtypes  # dtype('int64')

# 데이터 확인
se.values  # array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81])
```

### DataFrame

- 정의: 데이터프레임(DataFrame)은 행(row)과 열(column)로 구성된 2차원 배열 형태

- 구조: 여러 개의 Series가 모여 표 형태를 이룸 (각 열이 하나의 Series 객체)

- dict 로 만들기

```python
import pandas as pd

df = pd.DataFrame({
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [20, 25, 30],
    "성별": ["남", "남", "여"]
})
```

- list 로 만들기

    - ❗ 각 행의 데이터 길이가 동일해야 함 (길이가 다르면 에러 발생)

```python
import pandas as pd

df = pd.DataFrame([
    ["홍길동", 20, "남"],
    ["김철수", 25, "남"],
    ["이영희", 21, "여"],
], columns=["이름", "나이", "성별"])
```

- Series 로 만들기

```python
import pandas as pd

names = pd.Series(["홍길동", "김철수", "이영희"])
ages = pd.Series([20, 25, 21])
gender = pd.Series(["남", "남", "여"])
```

- 자주 사용하는 속성 값

```python
import pandas as pd

df = pd.DataFrame({
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [20, 25, 30],
    "성별": ["남", "남", "여"]
})

# 형태 확인
df.shape  # (3,3)

# 인데스 확인
df.index  # RangeIndex(start=0, stop=3, step=1)

# 컬럼 확인
df.columns  # Index(['이름', '나이', '성별'], dtype='object')

# 데이터의 타입 확인
df.dtypes
# 이름    object
# 나이     int64
# 성별    object
# dtype: object

# 데이터 확인
df.values
# array([['홍길동', 20, '남'],
#        ['김철수', 25, '남'],
#        ['이영희', 30, '여']], dtype=object)
```

## 🔨 다양한 DataFrame 만드는 방법

- Pandas 는 다양한 형태의 외부 파일을 읽어와서 DataFrame 을 생성하는 함수를 제공

| **File Format** | **Reader**                                                    | **Writer**                                                    | 
 |-----------------|---------------------------------------------------------------|---------------------------------------------------------------| 
| CSV             | `read_csv("data.csv", sep=",", header=0, encoding="utf-8")`   | `to_csv("output.csv", index=False, encoding="utf-8")`         | 
| Excel           | `read_excel("data.xlsx", sheet_name="Sheet1", usecols="A:C")` | `to_excel("output.xlsx", sheet_name="Results", index=False)`  | 
| JSON            | `read_json("data.json", orient="records", lines=True)`        | `to_json("output.json", orient="records", date_format="iso")` | 
| SQL             | `read_sql("SELECT * FROM table", conn, index_col="id")`       | `to_sql("table_name", conn, if_exists="replace")`             | 
| HTML            | `read_html("https://example.com/table.html", header=0)`       | `to_html("output.html", index=False, classes="table")`        | 

### CSV 예시

```python
# 읽기
df = pd.read_csv('sales.csv',  # 파일 경로
                 sep=',',  # 구분자(쉼표)
                 header=0,  # 첫 번째 행을 열 이름으로 사용
                 encoding='utf-8',  # 파일 인코딩 형식
                 skiprows=1,  # 첫 번째 행을 건너뜀(헤더 다음부터 데이터 시작)
                 na_values=['N/A', 'NULL'])  # 'N/A'와 'NULL' 문자열을 NaN으로 처리# 쓰기
df.to_csv('sales_report.csv',  # 저장할 파일 경로
          index=False,  # 인덱스 제외하고 저장
          header=True,  # 열 이름 포함
          encoding='utf-8')  # 파일 인코딩 형식
```

### Excel 예시

```python
# 읽기
df = pd.read_excel('report.xlsx',  # 파일 경로
                   sheet_name='2023',  # '2023'이라는 이름의 시트에서 데이터 읽기
                   header=0,  # 첫 번째 행을 열 이름으로 사용
                   usecols='A:E',  # A열부터 E열까지만 읽기
                   skiprows=2)  # 처음 2개 행을 건너뜀# 쓰기
df.to_excel('summary.xlsx',  # 저장할 파일 경로
            sheet_name='Q1_Results',  # 시트 이름 지정
            index=False,  # 인덱스 제외하고 저장
            startrow=1,  # 1행부터 데이터 쓰기 시작(0-based, 즉 두 번째 행)
            startcol=0)  # 0열부터 데이터 쓰기 시작(첫 번째 열)
```

### JSON 예시

```python
# 읽기
df = pd.read_json('users.json',  # 파일 경로
                  orient='records',  # 레코드 형식의 JSON 구조({'field': value})
                  lines=False,  # 한 줄에 하나의 JSON 객체가 아님
                  encoding='utf-8')  # 파일 인코딩 형식# 쓰기
df.to_json('users_export.json',  # 저장할 파일 경로
           orient='records',  # 각 행을 레코드 형식으로 저장
           date_format='iso')  # 날짜를 ISO 형식으로 저장(YYYY-MM-DD)
```

### SQL 예시

```python
# DB 연결 설정from sqlalchemyimport create_engine
engine = create_engine('sqlite:///mydatabase.db')  # SQLite DB 연결 문자열# 읽기
df = pd.read_sql('SELECT * FROM customers WHERE region="East"',  # SQL 쿼리문
                 con=engine,  # 데이터베이스 연결 객체
                 index_col='customer_id')  # 'customer_id' 열을 DataFrame의 인덱스로 사용# 쓰기
df.to_sql('customers_summary',  # 저장할 테이블 이름
          con=engine,  # 데이터베이스 연결 객체
          if_exists='replace',  # 테이블이 있으면 덮어쓰기
          index=False)  # 인덱스 제외하고 저장
```

### HTML 예시

- 한글이 깨져서 나올경우 encoding 을 `utf-8/cp949`로 설정하면 해결됨

```python
# 읽기
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries',  # 웹 페이지 URL
                      match='GDP',  # 'GDP'가 포함된 테이블만 가져오기
                      header=0)  # 첫 번째 행을 열 이름으로 사용
df = tables[0]  # 첫 번째 일치하는 테이블# 쓰기
df.to_html('countries.html',  # 저장할 파일 경로
           index=False,  # 인덱스 제외하고 저장
           classes='table table-striped',  # CSS 클래스 적용(부트스트랩 스타일)
           escape=False)  # HTML 태그를 이스케이프하지 않음(HTML 태그 허용)
```

## 🔎 DataFrame 의 데이터 내용 살펴보기

### head(행의 갯수)

- 데이터의 상단 (행의 갯수)개 행 출력

- 행의 갯수를 적지 않으면, default 로 5개 행을 보여줌

```python
# 예시 DataFrame 생성
import pandas as pd
import numpy as np

# 샘플 데이터 생성
data = {
    "이름": ["김철수", "이영희", "박민수", "정지영", "최현우", "한미나", "강준호"],
    "나이": [25, 30, 28, 32, 45, 23, 37],
    "성별": ["남", "여", "남", "여", "남", "여", "남"],
    "급여": [3500000, 4200000, 3800000, 5100000, 6500000, 3200000, 4800000]
}

df = pd.DataFrame(data)

# head() 함수 사용 - 기본값(5개 행)
print("# head() 기본 사용:")
print(df.head())

# head(3) 함수 사용 - 상위 3개 행만 보기
print("\n# head(3) 사용:")
print(df.head(3))

# 결과:
# head() 기본 사용:
#     이름  나이 성별      급여
# 0  김철수  25  남  3500000
# 1  이영희  30  여  4200000
# 2  박민수  28  남  3800000
# 3  정지영  32  여  5100000
# 4  최현우  45  남  6500000

# head(3) 사용:
#     이름  나이 성별      급여
# 0  김철수  25  남  3500000
# 1  이영희  30  여  4200000
# 2  박민수  28  남  3800000
```

### tail(행의 갯수)

- 데이터의 하단 (행의 갯수)개 행 출력

- 행의 갯수를 적지 않으면, default 로 5개 행을 보여줌

```python
# 위에서 만든 DataFrame 사용

# tail() 함수 사용 - 기본값(5개 행)
print("# tail() 기본 사용:")
print(df.tail())

# tail(2) 함수 사용 - 하위 2개 행만 보기
print("\n# tail(2) 사용:")
print(df.tail(2))

# 결과:
# tail() 기본 사용:
#     이름  나이 성별      급여
# 2  박민수  28  남  3800000
# 3  정지영  32  여  5100000
# 4  최현우  45  남  6500000
# 5  한미나  23  여  3200000
# 6  강준호  37  남  4800000

# tail(2) 사용:
#     이름  나이 성별      급여
# 5  한미나  23  여  3200000
# 6  강준호  37  남  4800000
```

### info()

- 전체 행의 갯수, 컬럼 정보, 결측치, 데이터 타입과 같이 데이터에 대한 전반적인 정보 제공

```python
# 결측치가 있는 DataFrame 생성
data_with_na = {
    "이름": ["김철수", "이영희", "박민수", "정지영", None],
    "나이": [25, 30, None, 32, 45],
    "성별": ["남", "여", "남", None, "남"],
    "급여": [3500000, None, 3800000, 5100000, 6500000]
}

df_with_na = pd.DataFrame(data_with_na)

# info() 함수 사용
print("# info() 사용:")
df_with_na.info()

# 결과:
# info() 사용:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 5 entries, 0 to 4
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   이름      4 non-null      object
#  1   나이      4 non-null      float64
#  2   성별      4 non-null      object
#  3   급여      4 non-null      float64
# dtypes: float64(2), object(2)
# memory usage: 288.0+ bytes
```

### describe()

- 컬럼별 값의 갯수, 평균, 표준편차, 최솟값, 최댓값, 사분위수를 보여줍니다.

```python
# 위에서 만든 DataFrame 사용

# describe() 함수 사용 - 수치형 데이터에 대한 통계 요약
print("# describe() 기본 사용 (수치형 데이터만):")
print(df.describe())

# describe(include='all') - 모든 컬럼에 대한 통계 요약
print("\n# describe(include='all') 사용:")
print(df.describe(include='all'))

# 결과:
# describe() 기본 사용 (수치형 데이터만):
#               나이          급여
# count   7.000000     7.000000
# mean   31.428571  4442857.142857
# std     7.479431  1184373.721177
# min    23.000000  3200000.000000
# 25%    26.500000  3650000.000000
# 50%    30.000000  4200000.000000
# 75%    34.500000  4950000.000000
# max    45.000000  6500000.000000

# describe(include='all') 사용:
#          이름         나이   성별          급여
# count     7  7.000000    7     7.000000
# unique    7       NaN    2          NaN
# top     김철수       NaN   남          NaN
# freq      1       NaN    4          NaN
# mean    NaN  31.428571  NaN  4442857.142857
# std     NaN   7.479431  NaN  1184373.721177
# min     NaN  23.000000  NaN  3200000.000000
# 25%     NaN  26.500000  NaN  3650000.000000
# 50%     NaN  30.000000  NaN  4200000.000000
# 75%     NaN  34.500000  NaN  4950000.000000
# max     NaN  45.000000  NaN  6500000.000000
```

## 🔢 DataFrame 의 행과 열

### column(열) 선택하기

- column 을 1개 선택 → Series 객체 반환

    - 대괄호(`[]`) 안에 column 이름을 따옴표(`""`)와 함께 입력(`데이터프레임[컬럼명]`)

    - 도트(`.`) 다음에 column 이름을 입력(`데이터프레임.컬럼명`)

```python
# DataFrame 생성
import pandas as pd

df = pd.DataFrame({
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [20, 25, 30],
    "성별": ["남", "남", "여"]
})

# 방법 1: 대괄호 사용
age_series = df["나이"]
print("대괄호 사용:")
print(age_series)
# 대괄호 사용:
# 0    20
# 1    25
# 2    30
# Name: 나이, dtype: int64

# 방법 2: 도트 표기법 사용
age_series2 = df.나이
print("\n도트 표기법 사용:")
print(age_series2)
# 도트 표기법 사용:
# 0    20
# 1    25
# 2    30
# Name: 나이, dtype: int64

```

- column 여러 개 선택 → DataFrame 객체 반환

    - 2중 대괄호(`[[]]`) 안에 column 이름을 입력(`데이터프레임[[컬럼명1, 컬럼명2, ...]]`)

    - 만약, column 1개를 DataFrame 객체로 추출하려면 2중 대괄호안에 그 column 이름을 str 로 입력

```python
# 여러 열 선택
name_gender_df = df[["이름", "성별"]]
print("여러 열 선택:")
print(name_gender_df)
# 여러 열 선택:
#     이름 성별
# 0  홍길동  남
# 1  김철수  남
# 2  이영희  여

# 열 1개를 데이터프레임으로 선택
age_df = df[["나이"]]
print("\n열 1개를 데이터프레임으로 선택:")
print(age_df)
# 열 1개를 데이터프레임으로 선택:
#    나이
# 0  20
# 1  25
# 2  30

```

### row(행) 선택하기

- 한 개: `데이터프레임명[인덱스:인덱스+1]`

- 여러 개: `데이터프레임명[시작인덱스:끝인덱스+1]`

```python
# 행 한 개 선택
row_one = df[1:2]
print("행 한 개 선택:")
print(row_one)
# 행 한 개 선택:
#     이름  나이 성별
# 1  김철수  25  남

# 행 여러 개 선택
multiple_rows = df[0:2]
print("\n행 여러 개 선택:")
print(multiple_rows)
# 행 여러 개 선택:
#     이름  나이 성별
# 0  홍길동  20  남
# 1  김철수  25  남

```

### loc와 iloc 활용하기

- loc: 레이블을 사용하여 조회(이름을 사용해서 조회)

    - `데이터프레임명.loc[행조건,열조건]`

    - 열만 조회할 때는 행조건에 `:`를 입력

- iloc: 위치 인덱스를 사용하여 조회

    - `데이터프레임명.iloc[행인덱스조건,열인덱스조건]`

```python
# loc 사용
print("loc를 사용한 특정 행과 열 선택:")
print(df.loc[1, "이름"])  # 특정 행과 열 선택
# loc를 사용한 특정 행과 열 선택:
# 김철수

# 모든 행의 특정 열 선택
print("\nloc를 사용한 모든 행의 특정 열 선택:")
print(df.loc[:, "나이"])
# loc를 사용한 모든 행의 특정 열 선택:
# 0    20
# 1    25
# 2    30
# Name: 나이, dtype: int64

# iloc 사용
print("\niloc를 사용한 특정 행과 열 선택:")
print(df.iloc[1, 0])  # 1행, 0열 선택
# iloc를 사용한 특정 행과 열 선택:
# 김철수

# 특정 범위의 행과 열 선택
print("\niloc를 사용한 특정 범위의 행과 열 선택:")
print(df.iloc[0:2, 1:3])
# iloc를 사용한 특정 범위의 행과 열 선택:
#    나이 성별
# 0  20  남
# 1  25  남
```

## 🧪 조건에 맞는 데이터 추출

### 데이터 정렬하기

- `데이터프레임명.sort_values(정렬기준컬럼)`

- 내림차순으로 정렬: `ascending=False` 조건 사용

```python
# 나이 기준 오름차순 정렬
sorted_df = df.sort_values("나이")
print("나이 기준 오름차순 정렬:")
print(sorted_df)
# 나이 기준 오름차순 정렬:
#     이름  나이 성별
# 0  홍길동  20  남
# 1  김철수  25  남
# 2  이영희  30  여

# 나이 기준 내림차순 정렬
sorted_df_desc = df.sort_values("나이", ascending=False)
print("\n나이 기준 내림차순 정렬:")
print(sorted_df_desc)
# 나이 기준 내림차순 정렬:
#     이름  나이 성별
# 2  이영희  30  여
# 1  김철수  25  남
# 0  홍길동  20  남

```

### 조건에 맞는 데이터 필터링하기

- `데이터프레임명[조건식]`

- `데이터프레임명.query('조건식')`

```python
# 나이가 25세 이상인 데이터 추출
filtered_df = df[df["나이"] >= 25]
print("나이가 25세 이상인 데이터:")
print(filtered_df)
# 나이가 25세 이상인 데이터:
#     이름  나이 성별
# 1  김철수  25  남
# 2  이영희  30  여

# query 함수 사용
query_df = df.query("나이 >= 25")
print("\nquery로 나이가 25세 이상인 데이터:")
print(query_df)
# query로 나이가 25세 이상인 데이터:
#     이름  나이 성별
# 1  김철수  25  남
# 2  이영희  30  여

```

### Boolean Indexing 과 isin 활용하기

- 불리언(Boolean) 인덱싱: bool 데이터 타입을 가진 Series 를 사용해서 인덱싱하는 기법

    - ❗ 이 Boolean Series 의 인덱스는 인덱싱하려는 DataFrame 의 인덱스와 반드시 일치해야 함

- `.isin()`: 각각의 요소가 DataFrame 또는 Series 에 존재하는지 파악하여 Boolean Series 반환

- `불리언 인덱싱 + .isin()`: 데이터의 특정 범위만 추출

```python
# 불리언 인덱싱 활용
male_df = df[df["성별"] == "남"]
print("성별이 남자인 데이터:")
print(male_df)
# 성별이 남자인 데이터:
#     이름  나이 성별
# 0  홍길동  20  남
# 1  김철수  25  남

# isin 활용
names_to_find = ["홍길동", "이영희"]
selected_names_df = df[df["이름"].isin(names_to_find)]
print("\n특정 이름 목록에 있는 데이터:")
print(selected_names_df)
# 특정 이름 목록에 있는 데이터:
#     이름  나이 성별
# 0  홍길동  20  남
# 2  이영희  30  여
```

## ⚠️결측값

### 결측값 확인하기

- `isna()`: 결측 값은 True 반환, 그 외에는 False 반환

- `notna()`: 결측 값은 False 반환, 그 외에는 True 반환

```python
# 결측치가 있는 DataFrame 생성
data_with_na = {
    "이름": ["김철수", "이영희", "박민수", "정지영", None],
    "나이": [25, 30, None, 32, 45],
    "성별": ["남", "여", "남", None, "남"],
    "급여": [3500000, None, 3800000, 5100000, 6500000]
}

df_with_na = pd.DataFrame(data_with_na)

# 결측값 확인
print("결측값 확인(isna):")
print(df_with_na.isna())
# 결측값 확인(isna):
#      이름     나이     성별     급여
# 0  False  False  False  False
# 1  False  False  False   True
# 2  False   True  False  False
# 3  False  False   True  False
# 4   True  False  False  False

# 결측값 합계 확인
print("\n결측값 합계:")
print(df_with_na.isna().sum())
# 결측값 합계:
# 이름    1
# 나이    1
# 성별    1
# 급여    1
# dtype: int64

```

### 결측값 제거하기

- `데이터명.dropna(axis=0, how='any', subset=None)`

    - axis: {0: index / 1: columns}

    - how: {'any': 존재하면 제거 / 'all': 모두 결측치면 제거}

    - subset: 행/열의 이름을 지정

```python
# 결측값이 있는 행 제거
df_drop_rows = df_with_na.dropna()
print("결측값이 있는 행 제거:")
print(df_drop_rows)
# 결측값이 있는 행 제거:
#     이름  나이 성별      급여
# 0  김철수  25  남  3500000

# 결측값이 있는 열 제거
df_drop_columns = df_with_na.dropna(axis=1)
print("\n결측값이 있는 열 제거:")
print(df_drop_columns)
# 결측값이 있는 열 제거:
# Empty DataFrame
# Columns: []
# Index: [0, 1, 2, 3, 4]

# 특정 열에서만 결측값 있는 행 제거
df_drop_subset = df_with_na.dropna(subset=["이름", "성별"])
print("\n이름과 성별에 결측값이 있는 행만 제거:")
print(df_drop_subset)
# 이름과 성별에 결측값이 있는 행만 제거:
#     이름    나이 성별      급여
# 0  김철수  25.0  남  3500000.0
# 1  이영희  30.0  여        NaN
# 2  박민수   NaN  남  3800000.0

```

### 결측값 대치하기

- 데이터 전체의 결측값을 특정 값으로 변경: `데이터명.fillna(대치할값)`

- 특정 컬럼의 결측값을 특정 값으로 변경: `데이터명[컬럼명].fillna(대치할값)`

- 결측값을 바로 위의 값과 동일하게 변경: `데이터명.fillna(method='ffill')`

- 결측값을 바로 아래의 값과 동일하게 변경: `데이터명.fillna(method='bfill')`

```python
# 모든 결측값 0으로 대치
df_fill_all = df_with_na.fillna(0)
print("모든 결측값 0으로 대치:")
print(df_fill_all)
# 모든 결측값 0으로 대치:
#     이름    나이  성별      급여
# 0  김철수  25.0  남  3500000.0
# 1  이영희  30.0  여        0.0
# 2  박민수   0.0  남  3800000.0
# 3  정지영  32.0  0  5100000.0
# 4      0  45.0  남  6500000.0

# 나이 컬럼의 결측값만 평균값으로 대치
age_mean = df_with_na["나이"].mean()
df_with_na_copy = df_with_na.copy()
df_with_na_copy["나이"] = df_with_na_copy["나이"].fillna(age_mean)
print("\n나이 컬럼의 결측값만 평균값으로 대치:")
print(df_with_na_copy)
# 나이 컬럼의 결측값만 평균값으로 대치:
#     이름        나이    성별      급여
# 0  김철수  25.000000    남  3500000.0
# 1  이영희  30.000000    여        NaN
# 2  박민수  33.000000    남  3800000.0
# 3  정지영  32.000000  None  5100000.0
# 4   None  45.000000    남  6500000.0

# 앞의 값으로 결측값 채우기
df_ffill = df_with_na.fillna(method="ffill")
print("\n앞의 값으로 결측값 채우기:")
print(df_ffill)
# 앞의 값으로 결측값 채우기:
#     이름    나이    성별      급여
# 0  김철수  25.0    남  3500000.0
# 1  이영희  30.0    여  3500000.0
# 2  박민수  30.0    남  3800000.0
# 3  정지영  32.0    남  5100000.0
# 4  정지영  45.0    남  6500000.0

```

## 🔀 타입 변환

### 타입 확인하기

- `.dtypes`: 열의 타입을 시리즈로 반환

- 특정 타입을 가진 컬럼만 추출: `데이터명.select_dtypes(타입)`

```python
# 타입 확인
print("각 열의 데이터 타입:")
print(df.dtypes)
# 각 열의 데이터 타입:
# 이름    object
# 나이     int64
# 성별    object
# dtype: object

# 특정 타입 컬럼만 추출
numeric_columns = df.select_dtypes(include="number")
print("\n숫자형 컬럼만 추출:")
print(numeric_columns)
# 숫자형 컬럼만 추출:
#    나이
# 0  20
# 1  25
# 2  30

```

### 타입 변환하기

- `데이터명[컬럼명].astype(타입)`

```python
# 나이를 문자열로 변환
df["나이_문자열"] = df["나이"].astype(str)
print("나이를 문자열로 변환:")
print(df[["나이", "나이_문자열"]])
# 나이를 문자열로 변환:
#    나이 나이_문자열
# 0  20      20
# 1  25      25
# 2  30      30

print("\n변환 후 타입 확인:")
print(df["나이_문자열"].dtype)
# 변환 후 타입 확인:
# dtype('O')

```

## ⚡ DataFrame 의 다양한 함수

### datetime 다루기

- 문자형을 날짜형으로 변경: `pd.to_datetime(컬럼, format='날짜 형식')`

```python
# 날짜 데이터 예시
date_df = pd.DataFrame({
    "날짜": ["2023-01-15", "2023-02-20", "2023-03-25"]
})

# 문자열을 날짜로 변환
date_df["날짜_datetime"] = pd.to_datetime(date_df["날짜"])
print("문자열을 날짜로 변환:")
print(date_df)
# 문자열을 날짜로 변환:
#          날짜   날짜_datetime
# 0  2023-01-15   2023-01-15
# 1  2023-02-20   2023-02-20
# 2  2023-03-25   2023-03-25

# 날짜 형식 지정하여 변환
custom_dates = pd.DataFrame({
    "날짜": ["15/01/2023", "20/02/2023", "25/03/2023"]
})
custom_dates["날짜_datetime"] = pd.to_datetime(custom_dates["날짜"], format="%d/%m/%Y")
print("\n특정 형식의 문자열을 날짜로 변환:")
print(custom_dates)
# 특정 형식의 문자열을 날짜로 변환:
#           날짜 날짜_datetime
# 0  15/01/2023   2023-01-15
# 1  20/02/2023   2023-02-20
# 2  25/03/2023   2023-03-25

```

- 날짜를 원하는 형식으로 변경: `데이터컬럼.dt.strftime(날짜형식)`

- dt 연산자 활용: year, month, day, dayofweek, day_name()

```python
# 날짜 형식 변경
date_df["년월일"] = date_df["날짜_datetime"].dt.strftime("%Y년 %m월 %d일")
print("날짜 형식 변경:")
print(date_df)
# 날짜 형식 변경:
#          날짜 날짜_datetime          년월일
# 0  2023-01-15   2023-01-15  2023년 01월 15일
# 1  2023-02-20   2023-02-20  2023년 02월 20일
# 2  2023-03-25   2023-03-25  2023년 03월 25일

# dt 연산자 활용
date_df["연도"] = date_df["날짜_datetime"].dt.year
date_df["월"] = date_df["날짜_datetime"].dt.month
date_df["요일"] = date_df["날짜_datetime"].dt.day_name()
print("\ndt 연산자 활용:")
print(date_df[["날짜_datetime", "연도", "월", "요일"]])
# dt 연산자 활용:
#   날짜_datetime  연도  월      요일
# 0   2023-01-15  2023  1  Sunday
# 1   2023-02-20  2023  2  Monday
# 2   2023-03-25  2023  3  Saturday

```

- 날짜 계산

    - day 연산: `pd.Timedelta(days=숫자)`

    - month 연산: `pd.DateOffset(months=숫자)`

    - year 연산: `pd.DateOffset(years=숫자)`

```python
# 날짜 계산
date_df["7일_후"] = date_df["날짜_datetime"] + pd.Timedelta(days=7)
date_df["1개월_후"] = date_df["날짜_datetime"] + pd.DateOffset(months=1)
date_df["1년_전"] = date_df["날짜_datetime"] - pd.DateOffset(years=1)
print("날짜 계산:")
print(date_df[["날짜_datetime", "7일_후", "1개월_후", "1년_전"]])
# 날짜 계산:
#   날짜_datetime      7일_후    1개월_후      1년_전
# 0   2023-01-15 2023-01-22 2023-02-15 2022-01-15
# 1   2023-02-20 2023-02-27 2023-03-20 2022-02-20
# 2   2023-03-25 2023-04-01 2023-04-25 2022-03-25

```

### 문자열 다루기

- `.str.contains(문자열)`: 문자열을 포함하고 있는지 유무

- `.str.replace(기존문자열, 대치문자열)`: 문자열 대치

- `.str.split(문자열, expand=True/False, n=개수)`: 특정 문자열을 기준으로 쪼개기

- `.str.lower()`: 소문자로 바꾸기

- `.str.upper()`: 대문자로 바꾸기

```python
# 문자열 예시 데이터
text_df = pd.DataFrame({
    "텍스트": ["Python 3.9", "Data Analysis", "pandas library", "PYTHON EXAMPLE"]
})

# 특정 문자열 포함 여부
contains_python = text_df["텍스트"].str.contains("Python")
print("'Python' 포함 여부:")
print(contains_python)
# 'Python' 포함 여부:
# 0     True
# 1    False
# 2    False
# 3    False
# Name: 텍스트, dtype: bool

# 문자열 대치
replaced_text = text_df["텍스트"].str.replace("Python", "Python 3.12")
print("\n문자열 대치:")
print(replaced_text)
# 문자열 대치:
# 0        Python 3.12 3.9
# 1         Data Analysis
# 2         pandas library
# 3         PYTHON EXAMPLE
# Name: 텍스트, dtype: object

# 문자열 분할
split_text = text_df["텍스트"].str.split(" ", expand=True)
print("\n문자열 분할:")
print(split_text)
# 문자열 분할:
#         0         1        2
# 0  Python       3.9     None
# 1    Data  Analysis     None
# 2  pandas   library     None
# 3  PYTHON   EXAMPLE     None

# 대소문자 변환
lower_text = text_df["텍스트"].str.lower()
upper_text = text_df["텍스트"].str.upper()
print("\n소문자 변환:")
print(lower_text)
# 소문자 변환:
# 0        python 3.9
# 1     data analysis
# 2     pandas library
# 3     python example
# Name: 텍스트, dtype: object

print("\n대문자 변환:")
print(upper_text)
# 대문자 변환:
# 0        PYTHON 3.9
# 1     DATA ANALYSIS
# 2     PANDAS LIBRARY
# 3     PYTHON EXAMPLE
# Name: 텍스트, dtype: object

```

### 데이터 결합하기

- `pd.merge(데이터1, 데이터2, on=기준컬럼, how=결합방법)`

- 두 데이터의 기준 컬럼명이 다를 경우: `pd.merge(데이터1, 데이터2, left_on=데이터1의 기준컬럼, right_on=데이터2의 기준컬럼, how=결합방법)`

```python
# 예시 데이터 생성
employees = pd.DataFrame({
    "사원번호": [101, 102, 103, 104],
    "이름": ["김영수", "이미나", "박지훈", "정수연"],
    "부서번호": [1, 2, 1, 3]
})

departments = pd.DataFrame({
    "부서번호": [1, 2, 3],
    "부서명": ["인사팀", "개발팀", "마케팅팀"]
})

# 내부 조인 (inner join)
inner_join = pd.merge(employees, departments, on="부서번호")
print("내부 조인 결과:")
print(inner_join)
# 내부 조인 결과:
#    사원번호   이름  부서번호   부서명
# 0    101  김영수     1   인사팀
# 1    103  박지훈     1   인사팀
# 2    102  이미나     2   개발팀
# 3    104  정수연     3  마케팅팀

# 왼쪽 조인 (left join)
left_join = pd.merge(employees, departments, on="부서번호", how="left")
print("\n왼쪽 조인 결과:")
print(left_join)
# 왼쪽 조인 결과:
#    사원번호   이름  부서번호   부서명
# 0    101  김영수     1   인사팀
# 1    103  박지훈     1   인사팀
# 2    102  이미나     2   개발팀
# 3    104  정수연     3  마케팅팀

# 컬럼명이 다른 경우
employees2 = pd.DataFrame({
    "사원번호": [101, 102, 103, 104],
    "이름": ["김영수", "이미나", "박지훈", "정수연"],
    "dept_id": [1, 2, 1, 3]
})

merge_diff_cols = pd.merge(
    employees2, departments,
    left_on="dept_id",
    right_on="부서번호"
)
print("\n컬럼명이 다른 경우 조인 결과:")
print(merge_diff_cols)
# 컬럼명이 다른 경우 조인 결과:
#    사원번호   이름  dept_id  부서번호   부서명
# 0    101  김영수        1      1   인사팀
# 1    103  박지훈        1      1   인사팀
# 2    102  이미나        2      2   개발팀
# 3    104  정수연        3      3  마케팅팀

```

### apply, map 함수 활용하기

- apply: 사용자 정의 함수를 데이터에 적용

    - `.apply(함수, axis=0/1)`

    - 간단한 함수는 lambda로 구현 가능

- map: 값을 특정 값으로 치환

    - `데이터명[컬럼명].map(매핑 딕셔너리)`

```python
# apply 예시
def calculate_bonus(row):
    if row["급여"] >= 5000000:
        return row["급여"] * 0.1
    else:
        return row["급여"] * 0.05


salary_df = pd.DataFrame({
    "이름": ["김철수", "이영희", "박민수", "정지영"],
    "급여": [3500000, 4200000, 5500000, 6000000]
})

# apply로 함수 적용
salary_df["보너스"] = salary_df.apply(calculate_bonus, axis=1)
print("apply 함수 활용:")
print(salary_df)
# apply 함수 활용:
#     이름      급여     보너스
# 0  김철수  3500000  175000.0
# 1  이영희  4200000  210000.0
# 2  박민수  5500000  550000.0
# 3  정지영  6000000  600000.0

# lambda로 간단한 함수 적용
salary_df["세후급여"] = salary_df.apply(lambda row: row["급여"] * 0.9, axis=1)
print("\nlambda 함수 활용:")
print(salary_df[["이름", "급여", "세후급여"]])
# lambda 함수 활용:
#     이름      급여    세후급여
# 0  김철수  3500000  3150000.0
# 1  이영희  4200000  3780000.0
# 2  박민수  5500000  4950000.0
# 3  정지영  6000000  5400000.0

# map 예시
gender_df = pd.DataFrame({
    "이름": ["김철수", "이영희", "박지훈", "정미나"],
    "성별코드": ["M", "F", "M", "F"]
})

# 매핑 딕셔너리 생성
gender_map = {"M": "남성", "F": "여성"}

# map으로 값 치환
gender_df["성별"] = gender_df["성별코드"].map(gender_map)
print("\nmap 함수 활용:")
print(gender_df)
# map 함수 활용:
#     이름 성별코드  성별
# 0  김철수     M  남성
# 1  이영희     F  여성
# 2  박지훈     M  남성
# 3  정미나     F  여성

```

## 📊 DataFrame 과 데이터 통계

### 기본 통계 함수

- `.mean()`: 평균값

- `.median()`: 중앙값

- `.describe()`: 다양한 통계량 요약

- `.agg()`: 여러 개의 열에 다양한 함수를 적용

- `.groupby()`: 그룹별 집계

- `.value_counts()`: 값의 개수

```python
# 통계 예시 데이터
stats_df = pd.DataFrame({
    "부서": ["영업", "개발", "영업", "마케팅", "개발", "영업"],
    "직급": ["대리", "과장", "과장", "대리", "사원", "사원"],
    "판매량": [120, 85, 130, 75, 90, 110],
    "매출액": [15000000, 8500000, 16000000, 7500000, 9000000, 12000000]
})

# 기본 통계
print("평균값:")
print(stats_df[["판매량", "매출액"]].mean())
# 평균값:
# 판매량        101.666667
# 매출액    11333333.333333
# dtype: float64

print("\n중앙값:")
print(stats_df[["판매량", "매출액"]].median())
# 중앙값:
# 판매량        100.0
# 매출액    10500000.0
# dtype: float64

# describe 통계 요약
print("\n통계 요약:")
print(stats_df[["판매량", "매출액"]].describe())
# 통계 요약:
#          판매량          매출액
# count   6.000000      6.000000
# mean  101.666667  11333333.333333
# std    22.290503   3559026.078362
# min    75.000000   7500000.000000
# 25%    86.250000   8625000.000000
# 50%   100.000000  10500000.000000
# 75%   117.500000  14250000.000000
# max   130.000000  16000000.000000

```

### 그룹별 통계

- groupby를 이용한 그룹별 통계 계산

```python
# 부서별 통계
dept_stats = stats_df.groupby("부서").agg({
    "판매량": ["count", "mean", "sum"],
    "매출액": ["mean", "sum"]
})
print("부서별 통계:")
print(dept_stats)
# 부서별 통계:
#         판매량                  매출액
#       count       mean    sum        mean        sum
# 부서
# 개발       2   87.500000   175   8750000.0  17500000
# 마케팅      1   75.000000    75   7500000.0   7500000
# 영업       3  120.000000   360  14333333.3  43000000

# 부서와 직급별 통계
multi_group = stats_df.groupby(["부서", "직급"]).agg({
    "판매량": "mean",
    "매출액": "sum"
})
print("\n부서와 직급별 통계:")
print(multi_group)
# 부서와 직급별 통계:
#              판매량      매출액
# 부서  직급
# 개발  과장     85.0   8500000
#     사원     90.0   9000000
# 마케팅 대리     75.0   7500000
# 영업  과장    130.0  16000000
#     대리    120.0  15000000
#     사원    110.0  12000000

```

### 값 개수 집계

- value_counts를 이용한 카테고리별 개수 집계

```python
# 값 개수 집계
print("부서별 직원 수:")
print(stats_df["부서"].value_counts())
# 부서별 직원 수:
# 영업      3
# 개발      2
# 마케팅     1
# Name: 부서, dtype: int64

print("\n직급별 직원 수:")
print(stats_df["직급"].value_counts())
# 직급별 직원 수:
# 사원    2
# 대리    2
# 과장    2
# Name: 직급, dtype: int64

# 부서와 직급별 조합 개수
print("\n부서와 직급 조합별 수:")
print(pd.crosstab(stats_df["부서"], stats_df["직급"]))
# 부서와 직급 조합별 수:
# 직급     과장  대리  사원
# 부서
# 개발     1   0   1
# 마케팅    0   1   0
# 영업     1   1   1

```

<br/>

