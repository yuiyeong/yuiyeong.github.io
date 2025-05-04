---
title: 시계열 데이터
date: 2025-05-04 19:52:00 +0900
categories: [ ]
tags: [ "급발진거북이" ]
toc: true
comments: false
mermaid: true
math: true
---
## 🚀 TL;DR



## 📦 사용하는 python package

- 
- 

## 📓 실습 Jupyter Notebook

- 

## 시계열 데이터와 순차적 데이터


## 시계열 데이터의 구성 성분

### 규칙 성분(또는 체계적 성분 , Systematic or Regular Component)


### 불규칙 성분


## 시계열 데이터의 특성

### 기술적 분석(Descriptive Analysis)


### 예측적 분석(Predictive Analysis)


### 독립 항등 분포(IID, Independent and Identically Distributed)


### 자기 상관(Autocorrelation)


### 마르코프 속성(Markov Property)


### 정상성(Stationarity)


## 시계열 데이터의 분석과정


## 시계열의 진동수를 활용한 분석


## 시간에 따른 변화를 분석


## 시계열 데이터의 성분 분해


## 이동 평균 모델(Moving Average Model)


## 자기 회귀 모델(Auto-Regressive Model)



---

## 📊 시계열 데이터의 특성

### 📈 시계열 데이터와 순차적 데이터

**시계열 데이터(Time-series data)**는 **시간 순서로 관측된 일련의 데이터**이다. 일반적으로 동일한 시간 간격마다 측정된 값들의 시퀀스를 말한다.

```python
import pandas as pd
import numpy as np

# 시계열 데이터 생성 예제
dates = pd.date_range(start='2020-01-01', periods=365, freq='D')
values = np.random.randn(365).cumsum()
time_series = pd.Series(values, index=dates)

print(f"시계열 데이터 첫 5개 값:\n{time_series.head()}")
# 출력:
# 2020-01-01   -0.152389
# 2020-01-02   -0.896142
# 2020-01-03   -0.527841
# 2020-01-04   -0.128342
# 2020-01-05    0.275849
```

대표적인 시계열 데이터:

- 시간별 기온
- 음성 데이터
- 연도별 전세계 총 인구수
- 일별 교통사고 건수
- 주식의 가격 데이터

**순차적 데이터(Sequential data)**는 어떠한 순서를 가지는 데이터로, 순서가 바뀌면 의미를 잃는다. 시계열 데이터는 순차적 데이터의 부분집합이다.

```python
# 순차적 데이터 예제 - DNA 시퀀스
dna_sequence = "ATCGATCG"
shuffled_dna = "AGTGTCAC"  # 순서가 바뀌면 다른 의미가 됨

# 시간적 순서를 가진 데이터
text = "시계열 데이터는 시간의 흐름에 따라 발생한다"
```

![시계열과 순차적 데이터의 관계](https://claude.ai/assets/img/2025-01-05/sequential_data_venn.png){: .w-75 .center}

### 🧩 시계열 데이터의 구성성분

시계열 데이터는 규칙(체계적) 성분과 불규칙 성분의 두 부분으로 나눌 수 있다.

#### 1. 규칙 성분(Systematic Component)

시간에 따른 데이터의 변동 중에서, 시간에 따라 보이는 데이터의 패턴이나 경향성에 의해 설명될 수 있는 예측 가능한 변동 성분이다.

**추세(Trend)**

- 데이터가 장기적으로 증가하거나 감소하는 방향성
- 예: 인구 증가, 기술 발전에 따른 생산성 향상

```python
# 추세 분석 예제
from scipy import signal

# 추세가 있는 데이터 생성
t = np.linspace(0, 10, 1000)
trend = 2 * t + 5
seasonal = 10 * np.sin(2 * np.pi * t)
noise = np.random.randn(1000)
data = trend + seasonal + noise

# 이동평균으로 추세 추출
window_size = 30
moving_average = pd.Series(data).rolling(window=window_size).mean()
```

**계절성(Seasonality)**

- 일정한 주기로 규칙적으로 반복되는 패턴
- 예: 계절별 기온 변화, 주중/주말 매출 차이

```python
# 계절성 분석 예제
import matplotlib.pyplot as plt

# 계절성 시각화
months = pd.date_range('2010-01-01', '2020-12-31', freq='M')
seasonal_component = np.sin(2 * np.pi * np.arange(len(months)) / 12)
```

**순환성(Cycle)**

- 불규칙한 주기로 발생하는 변동
- 예: 경제 주기, 태양 흑점 활동

#### 2. 불규칙 성분(Irregular Component)

시간에 따른 규칙적인 움직임과 무관한, 랜덤한 원인에 의한 변동으로 예측이 불가능한 노이즈 성분이다.

```python
# 불규칙 성분 분리 예제
from statsmodels.tsa.seasonal import seasonal_decompose

# 데이터 분해
result = seasonal_decompose(time_series, model='additive', period=30)
trend = result.trend
seasonal = result.seasonal
residual = result.resid

plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(time_series)
plt.title('Original Data')
plt.subplot(412)
plt.plot(trend)
plt.title('Trend')
plt.subplot(413)
plt.plot(seasonal)
plt.title('Seasonal')
plt.subplot(414)
plt.plot(residual)
plt.title('Residual (Irregular)')
plt.tight_layout()
```

### 🔄 시계열 데이터의 특성

#### 1. 독립항등분포(IID) 가정의 한계

머신러닝에서 다루는 대부분의 모델은 IID(Independent and Identically Distributed) 가정을 전제로 한다. 하지만 시계열 데이터는 이 가정을 만족하지 못한다.

```python
# 주사위 예제 - IID 성질을 가짐
dice_rolls = np.random.randint(1, 7, size=1000)
print(f"주사위 첫 10회 결과: {dice_rolls[:10]}")

# 시계열 데이터 - IID 가정 불성립
stock_prices = pd.Series(np.random.randn(1000).cumsum())
print(f"주식 가격 변화 첫 10개: {stock_prices[:10]}")
```

과거 값이 미래 값에 영향을 주는 자기상관(Autocorrelation) 때문에 시계열 데이터는 독립성을 만족하지 않는다.

#### 2. 자기상관(Autocorrelation)

한 시계열 내에서 자기자신과 다른 시점과의 상관관계를 나타낸다.

$$\text{Corr}(x_t, x_{t+k})$$

```python
# 자기상관 분석
from statsmodels.graphics.tsaplots import plot_acf

# 자기상관 시각화
fig, ax = plt.subplots(figsize=(12, 6))
plot_acf(time_series, lags=40, ax=ax)
ax.set_title('Autocorrelation Function')
```

- 시차 1의 자기상관이 높으면: 오늘의 데이터는 어제의 데이터가 가장 잘 설명
- 시차 12의 자기상관이 높으면: 한 달 전 데이터와 강한 상관관계

#### 3. 마르코프 속성(Markov Property)

현재 상태가 오직 직전 상태에만 의존하는 성질이다.

$$p(x_N|x_{N-1}, \ldots, x_1) = p(x_N|x_{N-1})$$

```python
# 마르코프 체인 예제
import networkx as nx

# 날씨 상태 전이 모델
weather_transitions = {
    'sunny': {'sunny': 0.7, 'rainy': 0.3},
    'rainy': {'sunny': 0.5, 'rainy': 0.5}
}

# 마르코프 체인 시뮬레이션
def simulate_weather(days, initial_state='sunny'):
    states = [initial_state]
    current = initial_state
    
    for _ in range(days-1):
        next_state = np.random.choice(
            list(weather_transitions[current].keys()),
            p=list(weather_transitions[current].values())
        )
        states.append(next_state)
        current = next_state
    
    return states

weather_sequence = simulate_weather(30)
print(f"30일간 날씨 시퀀스: {weather_sequence}")
```

#### 4. 정상성(Stationarity)

정상성은 시계열 분석에서 가장 중요한 개념 중 하나이다.

- **강정상성**: 모든 시점에서의 결합 확률분포가 동일
- **약정상성**: 평균과 분산이 시간에 따라 일정, 공분산이 시차에만 의존

```python
# 정상성 테스트
from statsmodels.tsa.stattools import adfuller

def check_stationarity(timeseries):
    # ADF 테스트 수행
    result = adfuller(timeseries)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value}')
    
    # 결과 해석
    if result[1] <= 0.05:
        print("데이터는 정상적(stationary)")
    else:
        print("데이터는 비정상적(non-stationary)")

# 비정상성 데이터
non_stationary = pd.Series(np.random.randn(1000).cumsum())
check_stationarity(non_stationary)

# 차분으로 정상성 확보
differenced = non_stationary.diff().dropna()
check_stationarity(differenced)
```

비정상성 데이터는 다음과 같은 방법으로 정상화할 수 있다:

- 차분(Differencing): $y_t = x_t - x_{t-1}$
- 로그 변환: $y_t = \log(x_t)$
- 계절차분: $y_t = x_t - x_{t-s}$

## 🛠️ 시계열 데이터 모델링 방법론

### 📑 시계열 데이터의 분석방법

시계열 데이터 분석은 크게 두 가지 접근법으로 나눌 수 있다:

1. **시계열의 진동수를 활용한 분석**
    
    - 푸리에(Fourier) 분석
    - 스펙트럼 밀도(Spectrum Density) 분석
    - 웨이브렛(Wavelet) 분석
2. **시간에 따른 변화를 분석**
    
    - 자기회귀모델(Autoregressive model)
    - 이동평균(Moving Average)
    - 추세(trend)분석
    - 성분분해(decomposition)

```python
# 푸리에 변환 예제
from scipy.fft import fft, fftfreq

# 주파수 성분 분석
n = len(time_series)
yf = fft(time_series)
xf = fftfreq(n, 1 / n)  # 샘플링 주파수 가정

plt.figure(figsize=(12, 6))
plt.plot(xf[:n//2], 2.0/n * np.abs(yf[:n//2]))
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title('Frequency Spectrum')
```

### 🔬 시계열 데이터의 분해

시계열 데이터를 각 성분으로 분해하여 예측이나 계절성에 따른 변화를 조정하는데 활용한다.

```python
# 계절성 분해 예제
from statsmodels.tsa.seasonal import seasonal_decompose

# 가법 모델 분해
additive_decomposition = seasonal_decompose(time_series, 
                                           model='additive', 
                                           period=30)

# 곱셈 모델 분해  
multiplicative_decomposition = seasonal_decompose(time_series,
                                                  model='multiplicative',
                                                  period=30)

# 시각화
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
ax1.plot(time_series)
ax1.set_title('Original')
ax2.plot(additive_decomposition.trend)
ax2.set_title('Trend')
ax3.plot(additive_decomposition.seasonal)
ax3.set_title('Seasonal')
ax4.plot(additive_decomposition.resid)
ax4.set_title('Residual')
```

### 📊 이동평균과 자기회귀 모델

#### 이동평균 모델 (Moving Average Model)

이동평균은 시계열 데이터에서 단기적인 변동을 smoothing하여 제거하고, 장기적인 추세를 더 잘 확인할 수 있게 한다.

```python
# 이동평균 계산
def calculate_moving_average(data, window):
    return data.rolling(window=window).mean()

# 여러 윈도우 크기로 이동평균 계산
data = pd.Series(np.random.randn(100).cumsum())
ma_5 = calculate_moving_average(data, 5)
ma_20 = calculate_moving_average(data, 20)

# 시각화
plt.figure(figsize=(12, 6))
plt.plot(data.index, data, label='Original', alpha=0.5)
plt.plot(data.index, ma_5, label='MA(5)', linewidth=2)
plt.plot(data.index, ma_20, label='MA(20)', linewidth=2)
plt.legend()
plt.title('Moving Average Comparison')
```

#### 자기회귀 모델 (Autoregressive Model)

AR 모델은 과거의 값들을 이용해 현재의 값을 예측하는 모델이다.

$$x_t = \phi_1 x_{t-1} + \phi_2 x_{t-2} + ... + \phi_p x_{t-p} + \epsilon_t$$

```python
# AR 모델 구현
from statsmodels.tsa.ar_model import AutoReg

# AR 모델 학습
model = AutoReg(time_series, lags=5)
model_fitted = model.fit()

# 예측
predictions = model_fitted.predict(start=len(time_series), 
                                  end=len(time_series)+10)

# 모델 평가
print(model_fitted.summary())
```

#### ARIMA 모델

ARIMA는 AR, I(통합), MA를 결합한 모델로 비정상성 시계열 데이터에 적용할 수 있다.

```python
# ARIMA 모델 구현
from statsmodels.tsa.arima.model import ARIMA

# 모델 선택을 위한 AIC 비교
best_aic = float('inf')
best_order = None
best_model = None

for p in range(0, 3):
    for d in range(0, 3):
        for q in range(0, 3):
            try:
                model = ARIMA(time_series, order=(p,d,q))
                model_fit = model.fit()
                if model_fit.aic < best_aic:
                    best_aic = model_fit.aic
                    best_order = (p,d,q)
                    best_model = model_fit
            except:
                continue

print(f"Best ARIMA{best_order} with AIC: {best_aic}")

# 예측
forecast = best_model.forecast(steps=30)
```

## 💡 실무 활용 사례

### 1. 주식 가격 예측

```python
# 주식 데이터로드 및 전처리
import yfinance as yf

# 데이터 다운로드
stock = yf.download('AAPL', start='2020-01-01', end='2023-12-31')

# 기술적 지표 계산
stock['MA50'] = stock['Close'].rolling(window=50).mean()
stock['MA200'] = stock['Close'].rolling(window=200).mean()
stock['RSI'] = calculate_rsi(stock['Close'], 14)

# 예측 모델 구축
X = stock[['MA50', 'MA200', 'RSI']].dropna()
y = stock['Close'].shift(-1).dropna()
```

### 2. 웹 트래픽 예측

```python
# 웹 트래픽 데이터 분석
web_traffic = pd.read_csv('web_traffic.csv', parse_dates=['date'])
web_traffic.set_index('date', inplace=True)

# 계절성 패턴 분석
hourly_pattern = web_traffic.groupby(web_traffic.index.hour).mean()
weekly_pattern = web_traffic.groupby(web_traffic.index.dayofweek).mean()

# Prophet 모델 적용
from prophet import Prophet

prophet_data = web_traffic.reset_index()
prophet_data.columns = ['ds', 'y']

model = Prophet(yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True)
model.fit(prophet_data)

# 예측
future = model.make_future_dataframe(periods=30*24, freq='H')
forecast = model.predict(future)
```

### 3. 이상 탐지 (Anomaly Detection)

```python
# 시계열 이상 탐지
from sklearn.ensemble import IsolationForest

# 특성 추출
features = pd.DataFrame({
    'value': time_series,
    'rolling_mean': time_series.rolling(window=24).mean(),
    'rolling_std': time_series.rolling(window=24).std(),
    'hour': time_series.index.hour,
    'dayofweek': time_series.index.dayofweek
}).dropna()

# 이상 탐지 모델
iso_forest = IsolationForest(contamination=0.05, random_state=42)
anomalies = iso_forest.fit_predict(features)

# 이상치 시각화
plt.figure(figsize=(12, 6))
plt.plot(time_series.index, time_series, label='Time Series')
plt.scatter(time_series.index[anomalies == -1], 
           time_series[anomalies == -1],
           color='red', label='Anomalies')
plt.legend()
plt.title('Anomaly Detection in Time Series')
```
