---
title: 🎲 기초 수학 for 인공지능 02; 통계
date: 2025-04-07 13:27:00 +0900
categories: [ MATHEMATICS, STATISTICS ]
tags: [ '급발진거북이', 'numpy', 'mathematics', 'statistics', '통계', '기초수학', 'statistic', '기술통계', 'GeekAndChill', '기깬칠' ]
toc: true
comments: false
mermaid: true
math: true
---

## 📦 사용하는 python package

- numpy==1.26.4
- pandas==2.2.3
- matplotlib==3.10.1
- seaborn==0.13.2
- scipy==1.15.2

## 🚀 TL;DR

- 인공지능에 필수적인 통계 개념들을 개발자 관점에서 설명

- 변수 유형, 데이터 척도, 모집단과 표본의 차이를 코드 예제와 함께 소개

- 평균, 중앙값, 분산 등의 계산 방법과 파이썬 구현

- 히스토그램, 상자수염그림 등 데이터 시각화와 분포 특성 분석 방법 제공

- 각 통계 개념이 머신러닝/딥러닝에서 어떻게 활용되는지 실용적 관점에서 설명

## 📓 실습 Jupyter Notebook

- [https://github.com/yuiyeong/notebooks/blob/main/math/statistics.ipynb](https://github.com/yuiyeong/notebooks/blob/main/math/statistics.ipynb)

## 📦 변수(Variable)

- 변화하는 모든 수를 의미

### 독립변수(Independent Variable)

- 다른 변수에 영향을 주는 변수

- 머신러닝에서는 입력(input) 또는 특성(feature)이라고도 함

- 실제 사용 예: 집값 예측 모델에서 집의 크기, 방 개수, 위치 등

- 중요성: 독립변수가 모델의 입력이 되어 결과를 예측하는 데 사용

### 종속변수(Dependent Variable)

- 독립변수의 영향을 받는 변수

- 예측하려는 타겟(target) 또는 레이블(label)이라고도 함

- 실제 사용 예: 집값 예측에서 집의 '가격'이 종속변수

> 💡 머신러닝 모델의 최종 목표는 종속변수를 정확히 예측하는 것!

### 질적변수(Qualitative Variable)

- 범주나 속성을 나타내는 변수로, 수치로 표현되지 않는 변수 즉, 분류를 위하여 용어로 정의되는 변수

- 비서열 질적변수와 서열 질적변수로 나눌 수 있음

### 비서열 질적변수(Nominal Variable)

- 순서가 없는 범주를 나타내는 변수

- 예시) 고객 세그먼트 분류에서 '성별', '직업', '혈액형' 등

> 💡 머신러닝/딥러닝에서, 원-핫 인코딩(One-Hot Encoding)을 통해 수치화하여 모델에 사용한다.

### 서열 질적변수(Ordinal Variable)

- 순서가 있는 범주를 나타내는 변수

- 예시) 고객 만족도 조사에서 '매우 불만족', '불만족', '보통', '만족', '매우 만족' 등

> 💡 머신러닝/딥러닝에서, 순서 정보를 보존하는 레이블 인코딩(Label Encoding)으로 처리

### 양적변수 (Quantitative Variable)

- 양의 크기를 나타내기 위하여 수량으로 표시되는 변수

- 머신러닝에서 수치형 특성(numerical features)으로 다루어짐

- 연속변수와 이산변수(비연속변수)로 나눌 수 있음

> 💡 대부분의 기계학습 알고리즘은 수치 데이터를 기반으로 작동하므로, 텍스트나 범주형 데이터도 결국 양적변수 형태로 변환하여 사용함

### 연속변수 (Continuous Variable)

- 주어진 범위 내에서 어떤 값도 가질 수 있는 변수

- 이론적으로 무한히 많은 값을 가질 수 있음

- 측정 도구의 정밀도에 따라 더 세밀한 값 측정 가능

- 예시) 체중, 키, 시간, 온도, 거리, 전압, 확률 등

### 이산변수 (Discrete Variable)

- 비연속변수라고도 함

- 특정 수치만을 가질 수 있는 변수

- 값 사이에 간격이 있고, 셀 수 있는(countable) 값을 가짐

- 예시) IQ 점수, 만 나이, 자녀 수, 방문 횟수, 고객 수, 제품 개수 등

## 💽 데이터(Data)

- 데이터는 연구나 조사의 목적에 맞는 변수를 토대로, 표본으로부터 수집한 자료

- 예시) 이미지 분류를 위한 이미지 데이터셋, 자연어 처리를 위한 텍스트 데이터셋 등

> 💡 데이터의 질과 양이 모델의 성능을 좌우!!

## 📏 척도(Scale)

- 척도는 변수를 측정하는 방법이나 단위를 의미

- 데이터 성격에 따라 크게 범주형 척도와 연속형 척도로 구분

> 💡 데이터 전처리 방법이 다르므로 범주형 변수와 연속형 변수를 구분해야 한다.

### 범주형 척도 (Categorical Scale)

- 범주나 그룹을 나타내는 척도

- 예시) 고객 세그먼테이션에서의 인구통계학적 특성(성별, 직업 등)

### 연속형 척도 (Continuous Scale)

- 연속적인 값을 가질 수 있는 척도

- 예시) 집 가격 예측에서의 집 크기, 주가 예측 모델에서의 과거 주가 등

### 범주형 척도 - 명목 척도 (Nominal Scale)

- 순서가 없는 범주를 나타내는 척도로, 비서열 질적변수와 동일

- 예시) 이미지 분류에서 '고양이', '개', '말' 등의 클래스 레이블

> 💡 머신러닝/딥러닝에서는, 다중 클래스 분류 문제에서 자주 사용

### 범주형 척도 - 서열 척도 (Ordinal Scale)

- 순서가 있는 범주를 나타내는 척도로, 서열 질적변수와 동일합니다.

- 예시) 추천 시스템에서의 사용자 별점(1점, 2점, 3점, 4점, 5점)

> 💡 머신러닝/딥러닝에서는, 순서 정보가 중요한 추천 시스템이나 감성 분석에서 사용

### 연속형 척도 - 등간 척도 (Interval Scale)

- 등간격으로 측정되지만 절대적인 0점이 없는 척도입니다.

- 예시) 온도(섭씨, 화씨), 시험 점수 등

> 💡 머신러닝/딥러닝에서는, 절대적인 비율 비교는 불가능하지만 차이는 의미가 있다.

### 연속형 척도 - 비율 척도 (Ratio Scale)

- 등간격으로 측정되며 절대적인 0점이 있는 척도입니다.

- 예시) 키, 몸무게, 시간, 거리 등

> 💡 머신러닝/딥러닝에서는, 비율 비교가 가능하여 가장 많은 정보를 제공한다.

## ❕ 머신러닝/딥러닝에서의 중요성

- 변수, 데이터, 척도의 이해는 머신러닝과 딥러닝에서 데이터 전처리와 모델 설계의 기초가 된다.

- 각 변수의 특성에 맞는 전처리와 인코딩을 통해 모델의 성능을 크게 향상시킬 수 있기 때문이다.

## 👪 모집단 (Population)

![population_sample.png](/assets/img/population_sample.png)

- 연구하고자 하는 대상의 전체 집합

- 예를 들어, "한국 성인의 키"를 연구한다면, 한국의 모든 성인이 모집단

> 💡 머신러닝/딥러닝에서는 우리가 예측하려는 모든 가능한 데이터가 모집단이다. 예를 들어, 이미지 분류 모델을 만든다면 "세상의 모든 고양이 사진"이 모집단이 될 수 있다.

### 모수(Parameter)

![parameter_statistic.png](/assets/img/parameter_statistic.png)

- 모집단의 특성을 나타내는 값

- 모집단의 평균(μ), 분산(σ²), 표준편차(σ) 등

```python
import numpy as np

# 전 국민의 키 data 라고 가정
population_heights = np.linspace(150, 180, 1000)

# 모집단의 모수 계산
population_mean = np.mean(population_heights)  # 모평균
population_variance = np.var(population_heights)  # 모분산
population_std = np.std(population_heights)  # 모표준편차

print(f"모평균: {population_mean:.2f}")
print(f"모분산: {population_variance:.2f}")
print(f"모표준편차: {population_std:.2f}")
```

> 💡 머신러닝/딥러닝에서는 우리가 찾으려는 *이상적인 모델 가중치*는 모수에 해당한다. 우리는 이 "진짜" 값을 모르기 때문에 표본을 통해 추정한다.

## 🔬 표본(Sample)

- 모집단에서 선택된 일부 구성원의 집합

- 통계적 추론은, 표본을 통해 모집단의 특성을 추정하는 과정

```python
import numpy as np

# 모집단에서 표본 추출
sample_size = 100
sample = np.random.choice(population_heights, sample_size, replace=False)
```

> 💡 머신러닝/딥러닝에서는, 훈련 데이터셋이 표본이고, 전체 데이터(모집단)의 일부만 사용하여 모델을 훈련한다.

### 통계량(Statistic)

- 통계량은 *표본에서 계산된 값*으로, 모수를 추정하는 데 사용된다.

```python
import numpy as np

# 표본 통계량 계산
sample_mean = np.mean(sample)  # 표본평균
sample_variance = np.var(sample, ddof=1)  # 표본분산 (비편향 추정을 위해 ddof=1)
sample_std = np.std(sample, ddof=1)  # 표본표준편차

print(f"표본평균: {sample_mean:.2f}")
print(f"표본분산: {sample_variance:.2f}")
print(f"표본표준편차: {sample_std:.2f}")
```

> 💡 머신러닝/딥러닝에서는, 모델 평가 지표(정확도, 손실 함수 값 등)는 표본 통계량이다. 이 값들을 통해 모델의 실제 성능(모수)을 추정한다.

![relation_population_sample.png](/assets/img/relation_population_sample.png)

## 🧩 표본 추출 방법

### 확률적 표본 추출 방법 - 단순 무작위 표본추출(Simple Random Sampling)

- 모집단에서 각 구성원이 동일한 확률로 선택되는 방법

```python
import numpy as np

# 단순 무작위 표본추출
simple_random_sample = np.random.choice(population_heights, sample_size, replace=False)

```

### 확률적 표본 추출 방법 - 체계적 표본추출(Systematic Sampling)

- 모집단을 일정한 간격으로 표본을 선택하는 방법

```python
import numpy as np

# 체계적 표본추출
N = len(population_heights)
k = N // sample_size  # 추출 간격
start = np.random.randint(0, k)  # 시작점
systematic_sample = population_heights[start::k][:sample_size]
```

### 확률적 표본 추출 방법 - 비례 층화 표본추출(Proportional Stratified Sampling)

- 모집단을 특성에 따라 층으로 나누고, 각 층의 크기에 비례하여 표본을 추출하는 방법

```python
import numpy as np

# 비례 층화 표본추출 예시
# 모집단을 성별로 나누어 표본 추출한다고 가정
male_heights = np.random.normal(175, 7, 500000)  # 남성 키
female_heights = np.random.normal(162, 6, 500000)  # 여성 키

# 층별 비율에 맞게 표본 크기 결정
male_sample_size = int(sample_size * 0.5)  # 남성 비율 50%
female_sample_size = sample_size - male_sample_size  # 여성 비율 50%

# 각 층에서 표본 추출
male_sample = np.random.choice(male_heights, male_sample_size, replace=False)
female_sample = np.random.choice(female_heights, female_sample_size, replace=False)

# 추출된 표본 합치기
stratified_sample = np.concatenate([male_sample, female_sample])

```

> 💡 머신러닝/딥러닝에서는, 불균형 데이터셋에서 train_test_split 의 stratify 매개변수를 사용할 때 층화 표본추출이 적용된다. 이는 클래스 비율을 유지하여 데이터를 나누는 방법이다.

### 확률적 표본 추출 방법 - 다단계 층화 표본추출(Multi-stage Stratified Sampling)

- 여러 단계를 거쳐 표본을 추출하는 방법

- 예를 들어, 국가 → 지역 → 도시 → 가구 순으로 표본을 추출

```python
import numpy as np

# 다단계 층화 표본추출 간단 예시
# 1단계: 지역별 선택
regions = ['서울', '부산', '대구', '인천', '광주']
selected_regions = np.random.choice(regions, 2, replace=False)

# 2단계: 선택된 지역에서 구/군 선택
districts = {
    '서울': ['강남구', '서초구', '종로구', '마포구', '강서구'],
    '부산': ['해운대구', '부산진구', '남구', '북구', '사상구'],
    # 다른 지역도 유사하게 정의
}

selected_districts = []
for region in selected_regions:
    region_districts = districts.get(region, [])
    if region_districts:
        selected_districts.extend(np.random.choice(region_districts, 2, replace=False))

print(f"선택된 지역: {selected_regions}")
print(f"선택된 구/군: {selected_districts}")

```

### 확률적 표본 추출 방법 - 군집 표본추출(Cluster Sampling)

- 모집단을 자연적인 군집으로 나누고, 무작위로 군집을 선택한 후 선택된 군집 내 모든 구성원 또는 일부를 표본으로 사용하는 방법

```python
import numpy as np

# 군집 표본추출 예시
# 학교(군집)를 선택하고, 선택된 학교의 모든 학생을 표본으로 사용
schools = ['A고', 'B고', 'C고', 'D고', 'E고', 'F고', 'G고', 'H고', 'I고', 'J고']
students_per_school = 100

# 각 학교 학생들의 키 생성
school_heights = {}
for school in schools:
    school_heights[school] = np.random.normal(170, 7, students_per_school)

# 군집(학교) 선택
selected_schools = np.random.choice(schools, 3, replace=False)

# 선택된 학교의 모든 학생을 표본으로 사용
cluster_sample = np.concatenate([school_heights[school] for school in selected_schools])

```

> 💡 컴퓨터 비전에서 이미지 일부 영역(패치)을 선택하여 처리할 때 군집 표본추출 개념이 적용된다.

### 비확률적 표본 추출 방법 - 편의 표본추출(Convenience Sampling)

- 쉽게 접근할 수 있는 대상을 표본으로 선택하는 방법

- 예시) 대학생을 대상으로 한 심리학 실험 데이터로 모델을 훈련하는 경우

### 비확률적 표본 추출 방법 - 판단 표본추출(Judgmental Sampling)

- 연구자의 판단에 따라 표본을 선택하는 방법

- 특정 조건에 맞는 데이터만 선별적으로 사용하여 모델을 훈련시킬 때 적용

### 비확률적 표본 추출 방법 - 할당 표본추출(Quota Sampling)

- 모집단의 특성 비율을 고려하여 표본을 선택하되, 선택 과정에서 연구자의 판단이 개입되는 방법

> 💡 이미지 분류 모델을 훈련할 때, 각 클래스별로 일정 수의 이미지를 선별적으로 선택하는 경우 할당 표본추출과 유사

## 📊 기술통계량(Descriptive statistic)

- 데이터의 주요 특성을 요약하는 통계량으로, 데이터의 중심 경향성과 분포 특성을 파악하는 데 사용된다.

- 중심 경향(평균, 중앙값, 최빈값), 분산(표준편차, 분산, 범위), 분포 형태 등을 포함

```python
import pandas as pd

# pandas를 사용한 기술통계량 계산
df = pd.DataFrame({
    "부서": ["영업", "개발", "영업", "마케팅", "개발", "영업", "마케팅"],
    "성별": ["남", "여", "여", "남", "남", "남", "여"],
    "급여": [350, 480, 320, 400, 520, 380, 450],
    "보너스": [50, 70, 40, 60, 80, 60, 70],
})
print(df.describe())
```

- 모델 학습 전에 데이터의 특성을 이해하는 것은 필수적이다.

- 기술통계는 데이터 분포 파악, 이상치 탐지, 적절한 전처리 방법 선택에 도움을 준다.

- 실제 사용 사례

    - 이미지 데이터 전처리에서 픽셀값 정규화(normalization)를 위해 평균과 표준편차 사용

    - 데이터 이상치(outlier) 탐지 시 평균과 표준편차 기반 방법 사용

    - 데이터 품질 검사 및 초기 탐색에서 기본 통계량으로 사용

### 중심 경향도 - 평균

- 산술평균(Arithmetic Mean): 모든 값의 합을 데이터 개수로 나눈 값으로, 가장 일반적으로 사용되는 평균

    - 이상치에 민감하며, 값이 한쪽으로 치우친 분포에서는 중심을 잘 대표하지 못할 수 있음

$$ \bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i $$

```python
import numpy as np

data = [1, 2, 3, 4, 5]
arithmetic_mean = np.mean(data)
print("산술평균:", arithmetic_mean)  # 결과: 3.0
```

- 기하평균(Geometric Mean): 모든 값을 곱한 후 데이터 개수만큼 제곱근을 취한 값

    - 비율이나 성장률과 관련된 데이터에 적합하며, 금융이나 투자 수익률 분석에 유용함

$$ GM = \sqrt[n]{x_1 \times x_2 \times ... \times x_n} $$

```python
import numpy as np

data = [1, 2, 3, 4, 5]
geometric_mean = np.exp(np.mean(np.log(data)))  # 로그 변환 후 평균 계산, 다시 지수 취함
print("기하평균:", geometric_mean)  # 결과: 약 2.61
```

- 조화평균(Harmonic Mean): 각 값의 역수의 산술평균의 역수

    - 비율의 평균을 계산할 때 유용하며, 속도나 비율 관련 문제에 적합함

$$ HM = \frac{n}{\sum_{i=1}^{n}\frac{1}{x_i}} $$

```python
import numpy as np

data = [1, 2, 3, 4, 5]
harmonic_mean = len(data) / sum(1 / x for x in data)
print("조화평균:", harmonic_mean)  # 결과: 약 2.19
```

### 중심 경향도 - 중앙값(Median)

- 데이터를 크기순으로 정렬했을 때 정중앙에 위치한 값

- 이상치에 강건하며, 데이터가 치우친 분포를 가질 때 중심을 더 잘 나타냄

- n이 홀수일 때, 수식

$$ Median = x_{(\frac{n+1}{2})} $$

- n이 짝수일 때, 수식

$$ Median = \frac{x_{(\frac{n}{2})} + x_{(\frac{n}{2}+1)}}{2} $$

```python
import numpy as np

data1 = [1, 3, 5, 7, 9]  # 홀수 개수
data2 = [1, 3, 5, 7, 9, 11]  # 짝수 개수

median1 = np.median(data1)
median2 = np.median(data2)

print("홀수 데이터 중앙값:", median1)  # 결과: 5.0
print("짝수 데이터 중앙값:", median2)  # 결과: 6.0
```

### 중심 경향도 - 최빈값(Mode)

- 데이터에서 가장 빈번하게 나타나는 값

- 범주형 데이터에 특히 유용하며, 여러 개의 최빈값이 존재할 수 있음

```python
from scipy import stats
import numpy as np

data = [1, 2, 2, 3, 3, 3, 4, 5, 5]
mode = stats.mode(data)
print("최빈값:", mode.mode[0])  # 결과: 3
```

### 산포도 - 분산(Variance)

- 데이터가 평균으로부터 퍼져있는 정도를 나타내는 지표

- 평균과의 차이를 제곱하기 때문에 이상치에 매우 민감함

$$ \sigma^2 = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2 $$

```python
import numpy as np

data = [1, 2, 3, 4, 5]
variance = np.var(data)
print("분산:", variance)  # 결과: 2.0
```

### 산포도 - 표준편차(Standard Deviation)

- 분산의 제곱근으로, 원본 데이터와 같은 단위를 가짐

- 데이터의 흩어진 정도를 원래 단위로 해석할 수 있어 직관적임

$$ \sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2} $$

```python
import numpy as np

data = [1, 2, 3, 4, 5]
std_dev = np.std(data)
print("표준편차:", std_dev)  # 결과: 약 1.41
```

## 🔬 모분산(Population Variance)

- 모집단 전체 데이터의 분산을 의미

$$ \sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2 $$

- 여기서 `N` 은 모집단 크기, `μ` 는 모집단 평균

- 실제로는 모집단 전체를 측정하기 어려워 *표본에서 추정*하게 됨

```python
# 가상의 모집단(전체 데이터)에 대한 모분산 계산
import numpy as np

population = np.random.normal(0, 1, 10000)  # 큰 모집단 가정
pop_variance = np.var(population)
print("모분산:", pop_variance)
```

## 📏 표본분산(Sample Variance)

- 모집단의 일부인 표본 데이터로부터 계산한 분산

$$ s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 $$

- n-1 로 나누는 이유는 불편추정량(unbiased estimator)을 얻기 위함

- 불편 추정량(unbiased estimator)

    - 간단히 말해서, 편향되지 않고 추정에 사용되는 값

    - 통계학에서 추정량의 편향(bias)이란 추정량의 기댓값과 실제 모수(parameter) 값의 차이를 말한다.

    - 불편 추정량은 이 편향이 0인 추정량, 즉 추정량의 기댓값이 추정하고자 하는 모수의 실제 값과 일치하는 추정량을 의미한다.

- 표본에서 계산한 분산이 모분산에 가까워지도록 자유도(degrees of freedom) 조정

```python
import numpy as np

sample = np.random.normal(0, 1, 30)  # 30개 표본
# ddof=1은 n-1로 나누는 표본분산 계산 의미
sample_variance = np.var(sample, ddof=1)
print("표본분산:", sample_variance)
```

### 자유도(Degrees of Freedom)

- 간단히 말해서 "독립적으로 변할 수 있는 값의 개수"를 의미

- 통계적 추정에서 자유도는 계산에 사용된 데이터 포인트의 수에서 추정해야 하는 모수(parameter)의 수를 뺀 값입니다.

- 표본 분산의 경우,

    - n개의 데이터 포인트가 있을 때, 각 데이터 포인트는 자유롭게 어떤 값이든 가질 수 있다.

    - 그러나 우리가 표본 평균을 계산하면, 이 평균값이 고정된다!

    - 평균이 고정되면, n개 중 n-1개만 자유롭게 값을 가질 수 있고, 결국 마지막 하나는 평균을 맞추기 위해 특정 값으로 결정된다.

    - ⇒ `표본 분산의 자유도는 n-1 이다.`

## 📊 표본표준편차(Sample Standard Deviation)

- 표본분산의 제곱근으로, 원본 데이터와 같은 단위를 가짐

$$ s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2} $$

- 표본으로부터 모집단의 표준편차를 추정하는 통계량

```python
import numpy as np

sample = [1, 2, 3, 4, 5]
# ddof=1은 n-1로 나누는 표본표준편차 계산 의미
sample_std = np.std(sample, ddof=1)
print("표본표준편차:", sample_std)  # 결과: 약 1.58
```

## 🧮 도수분포표(Frequency Distribution Table)

- 데이터값들이 얼마나 자주 발생하는지 보여주는 표

- 값의 범위를 구간으로 나누고 각 구간에 속하는 데이터의 개수(도수)를 계산

```python
import pandas as pd

# 샘플 데이터
ages = [23, 25, 28, 32, 34, 35, 37, 38, 41, 42, 45, 47, 48, 52, 55, 57, 58, 60, 62, 65]

# 구간 생성
# labels 은 bins 의 개수보다 1개 적어야함(n개의 경계에 대해서 n-1개의 구간이 만들어지니까)
bins = [20, 30, 40, 50, 60]
labels = ["20-30", "30-40", "40-50", "50-60"]

# 도수분포표 생성
freq_dist = pd.cut(ages, bins, labels=labels)
freq_dist.value_counts()
```

![freq_dist_table.png](/assets/img/freq_dist_table.png)

## 📊 히스토그램 그래프(Histogram)

- 히스토그램은 도수분포표를 시각화한 그래프

- x축은 데이터 값의 구간(bin), y축은 각 구간에 속하는 데이터의 빈도(frequency)를 나타냄

```python
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# 정규 분포(가우시안 분포)를 따르는 난수 생성
# size: 생성할 데이터 개수, loc:평균, scale: 표준편차
data = np.random.normal(loc=0.0, scale=1.0, size=100)  # 평균은 0, 표준편차는 1인 정규분포에서 100개의 데이터를 뽑음

# sns.histplot 만 호출하면, 그래프를 그리기만 할 뿐 보여주지 않음.
sns.histplot(data)

# plt.show() 를 해야 그래프가 보임.
plt.show()
```

- 히스토그램은 데이터의 분포 형태(정규분포, 왜도, 첨도 등)를 직관적으로 파악할 수 있게 해주며, 이상치나 패턴을 *시각적으로* 확인하는 데 유용

![histogram.png](/assets/img/histogram.png)

- 실제 사용 사례

    - 고객 데이터 분석에서 연령대별 구매 패턴 파악

    - 센서 데이터에서 특정 범위의 측정값 빈도 분석

    - 텍스트 데이터에서 단어 빈도수 분석 (TF-IDF의 기초)

## 🪓 사분위수

- 데이터를 4등분하는 값들이며, Q1(25%), Q2(50%, 중앙값), Q3(75%)로 표현

- Q1(25%): 25% 위치 번째에 자리한 값

- Q2(50%, 중앙값): 50% 위치 번째에 자리한 값. 즉, 중앙값

- Q3(75%): 75% 위치 번째에 자리한 값

- 찾은 위치가 실수라면(9번재의 25% 위치는 2.25),

### 사분위간 범위(Interquartile Range, IQR)

- Q3 에서 Q1 을 뺀 값( Q3 - Q1)

### Maximum, Minimum, Outliers

- `maximum = Q3 + IQR * 1.5`

- `minimun = Q1 - IQR * 1.5`

- `maximum` 보다 큰 값이거나, `minumum` 보다 작은 값이면 이상치(outlier) 라고 한다.

### 코드로 계산해보기

- 거의 계산할 일은 없으나, 개념들을 이해하기 위해 진행

- 대부분 box plot 을 그려서 파악함

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

town_a = [14, 28, 35, 42, 47, 51, 80, 130, 140]  # 마을 A 주민들의 나이
town_b = [43, 44, 45, 46, 47, 48, 49, 50, 51]  # 마을 B 주민들의 나이

# 사분위수 구하기
a_q1, a_q2, a_q3 = np.percentile(town_a, [25, 50, 75])
print("마을 A 데이터의", "Q1:", a_q1, "| Q2:", a_q2, "| Q3:", a_q3)
# 결과:
#      마을 A 데이터의 Q1: 35.0 | Q2: 47.0 | Q3: 80.0
b_q1, b_q2, b_q3 = np.percentile(town_b, [25, 50, 75])
print("마을 B 데이터의", "Q1:", b_q1, "| Q2:", b_q2, "| Q3:", b_q3)
# 결과:
#      마을 B 데이터의 Q1: 45.0 | Q2: 47.0 | Q3: 49.0


# IQR 구하기
a_iqr = a_q3 - a_q1
b_iqr = b_q3 - b_q1
print("마을 A 데이터의 IQR:", a_iqr, "| 마을 B 데이터의 IQR:", b_iqr)
# 결과:
#      마을 A 데이터의 IQR: 45.0 | 마을 B 데이터의 IQR: 4.0


a_lower_bound = a_q1 - a_iqr * 1.5
a_upper_bound = a_q3 + a_iqr * 1.5
print(a_lower_bound, "~", a_upper_bound)
# 결과:
#      -32.5 ~ 147.5


b_lower_bound = b_q1 - b_iqr * 1.5
b_upper_bound = b_q3 + b_iqr * 1.5
print(b_lower_bound, "~", b_upper_bound)
# 결과:
#      39.0 ~ 55.0


# 위 내용의 시각화(Box Plot 그리기)
df = pd.DataFrame({
    "Ages of Town A": town_a,
    "Ages of Town B": town_b
})
sns.boxplot(data=df)
plt.show()
```

![practice_box_plot.png](/assets/img/practice_box_plot.png)

### 실제 사용 사례

- 특성(feature) 간의 분포 비교 및 이상치 탐지

- 모델 성능 비교 (예: 여러 알고리즘의 정확도 분포)

- 시계열 데이터에서 계절별/월별 분포 비교

##  📦 상자수염그림 (Box Plot)

![understanding_boxplots.jpg](/assets/img/understanding_boxplots.jpg)

- 데이터의 분포와 이상치를 시각화하는 그래프

- 중앙값, 사분위수(Q1, Q3), 이상치 등을 한눈에 볼 수 있다.

- 데이터의 중심 경향, 퍼짐 정도, 이상치를 동시에 보여주어 데이터 전처리와 특성 선택에 중요한 정보를 제공

- 특히 이상치 처리와 다양한 특성의 분포 비교에 매우 유용

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# 여러 분포의 데이터 생성
data1 = np.random.normal(0, 1, 100)  # 평균 0, 표준편차 1인 정규분포
data2 = np.random.normal(2, 0.5, 100)  # 평균 2, 표준편차 0.5인 정규분포
data3 = np.random.exponential(2, 100)  # 지수분포

# 데이터프레임 생성
df = pd.DataFrame({
    'normal dist 0 1': data1,
    'normal dist 2 0.5': data2,
    'exponential dist': data3
})

# 상자수염그림 그리기
sns.boxplot(data=df)
plt.show()
```

![box_plot.png](/assets/img/box_plot.png)

## 📈 변동 계수(Coefficient of Variation)

- 평균에 대한 표준편차의 비율로, 서로 다른 단위나 규모를 가진 데이터의 변동성을 비교할 때 유용함

$$ CV = \frac{\sigma}{\mu} \times 100\% $$

- 여기서 σ는 표준편차, μ는 평균

- 변동 계수가 클수록 데이터의 상대적 변동성이 큼을 의미함

```python
import numpy as np

# 두 가지 다른 데이터셋
data1 = [1000, 1100, 950, 1050, 1025]  # 평균이 큰 데이터
data2 = [10, 11, 9.5, 10.5, 10.25]  # 평균이 작은 데이터


# 변동 계수 계산
def coefficient_of_variation(data):
    return np.std(data) / np.mean(data) * 100


cv1 = coefficient_of_variation(data1)
cv2 = coefficient_of_variation(data2)

print(f"데이터1의 변동 계수: {cv1:.2f}%")
print(f"데이터2의 변동 계수: {cv2:.2f}%")
```

## 📈 왜도(Skewness)

![relationship_between_mean_and_median_under_different_skewness.png](/assets/img/relationship_between_mean_and_median_under_different_skewness.png)

[https://study.com/learn/lesson/mean-median-mode-range-measures-central-tendency.html](https://study.com/learn/lesson/mean-median-mode-range-measures-central-tendency.html)

- 분포의 비대칭성을 측정하는 지표로, 데이터가 어느 쪽으로 치우쳐 있는지를 나타냄

$$ Skewness = \frac{1}{n}\sum_{i=1}^{n}(\frac{x_i - \bar{x}}{\sigma})^3 $$

- 양의 왜도: 오른쪽으로 긴 꼬리를 가진 분포, (오른쪽으로 치우침, `mode > median > mean`)

- 음의 왜도: 왼쪽으로 긴 꼬리를 가진 분포 (왼쪽으로 치우침, `mode < median < mean`)

- 왜도가 0: 대칭 분포 (예: 정규 분포)

```python
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 다양한 분포 생성
right_skewed = np.random.exponential(size=1000)  # 양의 왜도(오른쪽으로 치우침)
left_skewed = -np.random.exponential(size=1000)  # 음의 왜도(왼쪽으로 치우침)
symmetric = np.random.normal(size=1000)  # 대칭 분포

# 왜도 계산
right_skew = stats.skew(right_skewed)
left_skew = stats.skew(left_skewed)
sym_skew = stats.skew(symmetric)

print(f"양의 왜도(오른쪽 치우침): {right_skew:.4f}")  # 양의 왜도(오른쪽 치우침): 1.7757
print(f"음의 왜도(왼쪽 치우침): {left_skew:.4f}")  # 음의 왜도(왼쪽 치우침): -2.1880
print(f"대칭 분포 왜도: {sym_skew:.4f}")  # 대칭 분포 왜도: 0.0603

# 분포 시각화
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(right_skewed, kde=True)
plt.title(f"right_skew: {right_skew:.4f}")

plt.subplot(1, 3, 2)
sns.histplot(symmetric, kde=True)
plt.title(f"sym_skew: {sym_skew:.4f}")

plt.subplot(1, 3, 3)
sns.histplot(left_skewed, kde=True)
plt.title(f"left_skew: {left_skew:.4f}")

plt.tight_layout()
plt.show()
```

## 📉 첨도(Kurtosis)

![img_kurtosis.jpg](/assets/img/img_kurtosis.jpg)

[https://www.sciencedirect.com/topics/social-sciences/kurtosis](https://www.sciencedirect.com/topics/social-sciences/kurtosis)

- 분포의 뾰족한 정도(꼬리의 두께)를 측정하는 지표

$$ Kurtosis = \frac{1}{n}\sum_{i=1}^{n}(\frac{x_i - \bar{x}}{\sigma})^4 - 3 $$

- 정규분포는 첨도가 0(위 수식에서 -3 항으로 인해)

- 양의 첨도(leptokurtic): 정규분포보다 뾰족하고 두꺼운 꼬리를 가짐

- 음의 첨도(platykurtic): 정규분포보다 납작하고 얇은 꼬리를 가짐

```python
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 다양한 첨도를 가진 분포 생성
high_kurtosis = np.random.laplace(size=1000)  # 두꺼운 꼬리(양의 첨도)
normal_dist = np.random.normal(size=1000)  # 정규분포(기준 첨도)
low_kurtosis = np.random.uniform(size=1000)  # 얇은 꼬리(음의 첨도)

# 첨도 계산
high_kurt = stats.kurtosis(high_kurtosis)
normal_kurt = stats.kurtosis(normal_dist)
low_kurt = stats.kurtosis(low_kurtosis)

print(f"양의 첨도(뾰족함): {high_kurt:.4f}")  # 양의 첨도(뾰족함): 2.6262
print(f"정규분포 첨도: {normal_kurt:.4f}")  # 정규분포 첨도: 0.1184
print(f"음의 첨도(납작함): {low_kurt:.4f}")  # 음의 첨도(납작함): -1.2049

# 분포 시각화
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(high_kurtosis, kde=True)
plt.title(f"high_kurt: {high_kurt:.4f}")

plt.subplot(1, 3, 2)
sns.histplot(normal_dist, kde=True)
plt.title(f"normal_kurt: {normal_kurt:.4f}")

plt.subplot(1, 3, 3)
sns.histplot(low_kurtosis, kde=True)
plt.title(f"low_kurt: {low_kurt:.4f}")

plt.tight_layout()
plt.show()
```
