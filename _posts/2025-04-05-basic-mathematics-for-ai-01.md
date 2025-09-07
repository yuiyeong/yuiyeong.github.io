---
title: 🎲 기초 수학 for 인공지능 01; 확률
date: 2025-04-05 06:02:00 +0900
categories: [ MATHEMATICS, PROBABILITY ]
tags: [ '급발진거북이', 'numpy', 'mathematics', '기초수학', '확률', 'GeekAndChill', '기깬칠' ]
toc: true
comments: false
mermaid: true
math: true
---

> 💡 머신러닝과 딥러닝을 공부하다보면 다양한 용어를 마추치게된다…
>
> 그 용어들이 어떤 수학적 개념인지 대략적으로 알고 있어야, 의사소통도 편하지만, 여러 모델을 다룰 때(특히 논문을 읽을 때) 도움이 된다.

# ⚡ TL;DR

> 💡 이 개념들은 나이브 베이즈, 마르코프 모델, 결정 트리, 베이지안 네트워크, 앙상블 모델 등 다양한 머신러닝 알고리즘의 기반이 되며, 데이터의 불확실성을 모델링하고 의미 있는 패턴을 발견하는 데 필수적!!
(머신러닝의 용어는 나중에 따로 정리할 예정)

- 🧮 합의 법칙: 서로 다른 방법의 경우의 수를 더해 총 경우의 수 계산 ($P(A \cup B) = P(A) + P(B)$, 배타적일 때)

- 🔢 곱의 법칙: 순차적 선택에서 각 단계의 선택 수를 곱해 총 경우의 수 계산 ($P(A \cap B) = P(A) \times P(B|A)$)

- 🎲 독립 사건: 한 사건이 다른 사건의 확률에 영향을 주지 않음 ($P(A \cap B) = P(A) \times P(B)$)

- 📚 순열: 순서가 중요한 선택 방법 ($_nP_r = \frac{n!}{(n-r)!}$)

- 🔄 조합: 순서가 중요하지 않은 선택 방법 ($_nC_r = \frac{n!}{r!(n-r)!}$)

- 🧪 시행: 결과를 관찰하기 위한 반복 가능한 과정 (실험 설계, 시뮬레이션에 활용)

- 🌐 표본공간: 가능한 모든 결과의 집합 (데이터 공간 정의, 확률 분포 모델링에 활용)

- 🎯 사건: 표본공간의 부분집합 (의미 있는 데이터 패턴이나 조건 정의)

- 🔀 합사건: 두 사건 중 하나라도 발생하는 사건 (다중 조건, OR 연산)

- 🔗 곱사건: 두 사건이 동시에 발생하는 사건 (특성 교차, AND 연산)

- 🚫 배반사건: 동시에 발생할 수 없는 사건들 (상호 배타적 분류, 의사결정 트리)

- 🔄 여사건: 사건이 발생하지 않는 경우 (이진 분류, 부정 샘플링)

- 🧮 수학적 확률: 이론적인 확률 계산 (균등 분포, 사전 확률 설정)

- 📈 통계적 확률: 실제 데이터에서 관측된 빈도로 확률 계산 (경험적 확률 분포)

- ➕ 덧셈법칙: 합사건의 확률 계산 ($P(A \cup B) = P(A) + P(B) - P(A \cap B)$)

- 🔮 조건부 확률: 특정 조건이 주어졌을 때 사건의 확률 ($P(A|B) = \frac{P(A \cap B)}{P(B)}$)

---

## 🧮 합의 법칙 (Rule of Sum)

두 가지 이상의 서로 다른 방법으로 작업을 수행할 수 있을 때, 각 방법의 경우의 수를 더하면 총 경우의 수를 구할 수 있다.

수학적으로는 사건 $A$와 $B$가 *서로 배타적(동시에 일어날 수 없음)*일 때, $A$ 또는 $B$가 일어날 확률은,

$$ P(A \cup B) = P(A) + P(B) $$

### 실생활 예시

학교 동아리에서 프로그래밍반(10명)과 데이터분석반(15명) 중 한 명을 뽑는 경우의 수는,

$$ 10 + 15 = 25 $$

- (10명 중 1명을 뽑을 수 있는 10가지) + (15명 중 1명을 뽑을 수 있는 15가지) → 총 25가지

### Python 예시

```python
# 두 집합의 합집합 원소 개수 구하기
programming_club = {"김철수", "이영희", "박민수", "정지우", "최동현", "한미래", "오예슬", "윤성준", "임하늘", "조태양"}
data_analysis_club = {"강하늘", "구름비", "남하얀", "도하람", "라온희", "마루미", "바람솔", "사랑이", "아리안", "자유롭", "차미소", "카라스", "타우너", "파랑새",
                      "하늘빛"}

# 합의 법칙: 두 집합의 크기를 더함 (단, 중복 없을 때)
total_possibilities = len(programming_club) + len(data_analysis_club)
print(f"한 명을 뽑는 경우의 수: {total_possibilities}")

# 만약 두 집합에 중복 원소가 있을 경우 (합집합을 구해야 함)
both_clubs = {"김철수", "이영희", "강하늘"}  # 가정: 두 동아리 모두 속한 학생
programming_club_2 = programming_club.union(both_clubs)
data_analysis_club_2 = data_analysis_club.union(both_clubs)

# 중복을 제외한 합집합
total_with_overlap = len(programming_club_2.union(data_analysis_club_2))
print(f"중복을 제외한 경우의 수: {total_with_overlap}")
```

### 머신러닝/딥러닝에서의 활용

- 앙상블 학습(Ensemble Learning): 여러 모델의 예측 결과를 합산할 때 활용

- 분류 문제에서 다중 클래스 확률 계산: 여러 클래스 중 하나에 속할 확률을 계산할 때

- 데이터 분할(Split) 전략에서 다양한 파티션의 데이터셋을 관리할 때

> 💡 합의 법칙은 확률 모델의 기반이 되며, 머신러닝에서 다양한 경우의 수를 계산하고 모델의 다양한 경로를 분석하는 데 필수적

## 🔢 곱의 법칙 (Rule of Product)

순차적으로 여러 선택을 해야 할 때, 각 단계에서의 선택 수를 곱하면 총 경우의 수를 구할 수 있습니다.

수학적으로는 사건 $A$와 $B$가 *연속적으로 일어날 때*, $A$와 $B$가 *모두 일어날 확률*은,

$$ P(A \cap B) = P(A) \times P(B|A) $$

### 실생활 예시

4개의 셔츠와 3개의 바지를 가지고 있을 때, 가능한 복장 조합은,

$$ 4 \times 3 = 12 $$

- (4개의 셔츠 중 1개를 고르는 경우의 수는 4가지) x (3개의 바지 중 1개를 고르는 경우의 수 3가지) → 12

### Python 예시

```python
# 곱의 법칙 사용
shirts = ["흰색 셔츠", "파란색 셔츠", "검은색 셔츠", "빨간색 셔츠"]
pants = ["청바지", "검은색 바지", "베이지색 바지"]

# 가능한 모든 조합 출력
outfits = []
for shirt in shirts:
    for pant in pants:
        outfits.append((shirt, pant))

print(f"가능한 복장 조합 수: {len(outfits)}")
print("가능한 복장 예시:")
for outfit in outfits[:3]:  # 처음 3개만 출력
    print(f"- {outfit[0]} + {outfit[1]}")
```

### 머신러닝/딥러닝에서의 활용

- 신경망 구성: 각 층의 노드 수와 층 간 가능한 연결 수를 계산

- 하이퍼파라미터 튜닝: 여러 하이퍼파라미터 조합의 경우의 수 계산

- 특성(feature) 조합: 여러 특성을 조합하여 새로운 특성을 만들 때

> 💡 곱의 법칙은 딥러닝 모델의 복잡도를 이해하고, 가능한 모델 구성과 파라미터 공간을 탐색하는 데 중요

## 🎲 독립 사건 (Independent Event)

두 사건이 서로 영향을 주지 않을 때, 즉 *하나의 사건이 일어나도 다른 사건의 확률에 영향을 주지 않는 경우*를 말합니다.

사건 $ A $ 와 $ B $ 가 *독립*일 때, $ A $ 와 $ B $ 가 동시에 일어날 확률은,

$$ P(A \cap B) = P(A) \times P(B) $$

### 실생활 예시

동전을 두 번 던질 때, 첫 번째 던진 결과는 두 번째 던지는 결과에 영향을 주지 않는다.

### Python 예시

```python
import numpy as np

# 독립 사건 시뮬레이션: 동전 두 번 던지기
trials = 10000
first_coin = np.random.choice(['앞면', '뒷면'], size=trials)
second_coin = np.random.choice(['앞면', '뒷면'], size=trials)

# 개별 확률 계산
p_heads_first = np.mean(first_coin == '앞면')
p_heads_second = np.mean(second_coin == '앞면')

# 두 동전 모두 앞면일 확률
both_heads = np.mean((first_coin == '앞면') & (second_coin == '앞면'))

print(f"첫 번째 동전이 앞면일 확률: {p_heads_first:.4f}")
print(f"두 번째 동전이 앞면일 확률: {p_heads_second:.4f}")
print(f"두 동전 모두 앞면일 확률 (실제): {both_heads:.4f}")
print(f"두 동전 모두 앞면일 확률 (독립 가정): {p_heads_first * p_heads_second:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 나이브 베이즈(Naive Bayes): 특성들이 서로 독립적이라는 가정 하에 작동하는 분류 알고리즘

- 특성 선택(Feature Selection): 독립적인 특성을 선택하여 모델 성능 개선

- 교차 검증(Cross-Validation): 훈련 데이터와 테스트 데이터의 독립성 확보

> 💡 많은 머신러닝 알고리즘이 데이터의 독립성을 가정!

## 📚 순열 (Permutation)

n개의 원소 중에서 r개를 선택하여 순서대로 나열하는 방법의 수, 순서가 중요!

$$ _nP_r = \frac{n!}{(n-r)!} $$

### 실생활 예시

5명의 후보 중 회장, 부회장, 총무를 선출하는 경우의 수는,

$$ _5P_3 = \frac{5!}{(5-3)!} = \frac{5!}{2!} = 60 $$

- 첫 번째 직책(회장)에는 5명 중 한 명을 선택할 수 있습니다. (5가지 경우)

- 두 번째 직책(부회장)에는 남은 4명 중 한 명을 선택할 수 있습니다. (4가지 경우)

- 세 번째 직책(총무)에는 남은 3명 중 한 명을 선택할 수 있습니다. (3가지 경우)

- 따라서 총 경우의 수는 5 × 4 × 3 = 60가지이다.

### Python 예시

```python
import itertools

# 순열 계산
candidates = ["김후보", "이후보", "박후보", "정후보", "최후보"]
positions = 3  # 회장, 부회장, 총무

# itertools의 permutations 함수 사용
permutations = list(itertools.permutations(candidates, positions))

print(f"가능한 임원 구성 수: {len(permutations)}")
print("가능한 임원 구성 예시 (처음 3개):")
for i, perm in enumerate(permutations[:3]):
    print(f"{i + 1}. 회장: {perm[0]}, 부회장: {perm[1]}, 총무: {perm[2]}")


# 순열 직접 계산
def permutation(n, r):
    return factorial(n) // factorial(n - r)


def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


print(f"₅P₃ = {permutation(5, 3)}")

```

### 머신러닝/딥러닝에서의 활용

- 시퀀스 모델링: 자연어 처리(NLP)에서 단어 순서의 중요성

- 순위 학습(Learning to Rank): 검색 결과나 추천 시스템에서 항목의 순서 결정

- 데이터 증강(Data Augmentation): 이미지나 시퀀스 데이터에서 순서를 바꿔 새로운 학습 데이터 생성

> 💡 순열은 *시퀀스 데이터*를 다루는 모델에서 가능한 순서의 경우의 수를 이해하고, *최적의 순서*를 찾는 데 중요!

## 🔄 조합 (Combination)

n개의 원소 중에서 r개를 선택하는 방법의 수, 순서는 중요하지 않음

$$ _nC_r = \frac{n!}{r! \times (n-r)!} $$

### 실생활 예시

10명의 학생 중 3명을 뽑아 팀을 구성하는 경우의 수는,

$$ _{10}C_3 = \frac{10!}{3! \times 7!} = 120 $$

- 순열에서는 ABC와 ACB, BAC 등을 모두 다른 경우로 센다(순서 중요).

- 조합에서는 ABC, ACB, BAC 등을 모두 같은 경우로 센다(순서 무관).

- 만약 10명 중 3명을 순서 있게 나열하는 경우(순열)라면,

$$ _{10}P_3 = \frac{10!}{7!} = 10 \times 9 \times 8 = 720 $$

- 그러나 조합에서는 순서를 고려하지 않으므로, 각 3명의 가능한 배열 수인 3!(=6)으로 나눠야 한다.

$$ _{10}C_3 = \frac{_{10}P_3}{3!} = \frac{720}{6} = 120 $$

### Python 예시

```python
import itertools
import math

# 조합 계산
students = ["학생1", "학생2", "학생3", "학생4", "학생5",
            "학생6", "학생7", "학생8", "학생9", "학생10"]
team_size = 3

# itertools의 combinations 함수 사용
combinations = list(itertools.combinations(students, team_size))

print(f"가능한 팀 구성 수: {len(combinations)}")
print("가능한 팀 구성 예시 (처음 3개):")
for i, comb in enumerate(combinations[:3]):
    print(f"{i + 1}. 팀원: {', '.join(comb)}")


# 조합 직접 계산
def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


print(f"₁₀C₃ = {combination(10, 3)}")
```

### 머신러닝/딥러닝에서의 활용

- 앙상블 모델: 여러 모델 중에서 일부를 선택하여 앙상블 구성

- 특성 선택(Feature Selection): 많은 특성 중에서 최적의 부분집합 선택

- 배깅(Bagging): 랜덤 포레스트와 같은 알고리즘에서 데이터 샘플링

> 💡 조합은 모델의 하이퍼파라미터 튜닝, 특성 선택, 모델 앙상블 구성 등 최적의 부분집합을 선택하는 많은 문제에서 핵심적인 개념

## 🧪 확률론의 기본 개념 - 시행 (Experiment)

결과를 관찰하기 위해 *수행하는 행위나 과정*을 의미. 동일한 조건에서 반복 가능해야 한다.

### 실생활 예시

동전 던지기, 주사위 굴리기, 카드 한 장 뽑기 등

### Python 예시

```python
import numpy as np


# 동전 던지기 시행 시뮬레이션
def coin_flip_experiment(num_trials=1000):
    # 0은 앞면, 1은 뒷면을 의미
    results = np.random.randint(0, 2, num_trials)
    return results


# 시행 실행
trials = coin_flip_experiment(10)
print("10번의 동전 던지기 결과:", ["앞면" if r == 0 else "뒷면" for r in trials])


# 주사위 굴리기 시행
def dice_roll_experiment(num_trials=1000):
    # 1부터 6까지의 숫자
    results = np.random.randint(1, 7, num_trials)
    return results


# 시행 실행
dice_trials = dice_roll_experiment(10)
print("10번의 주사위 굴리기 결과:", dice_trials)

```

### 머신러닝/딥러닝에서의 활용

- 실험 설계: 모델 평가를 위한 실험 설계 및 수행

- 시뮬레이션: 다양한 시나리오에서 모델 성능 테스트

- 샘플링: 몬테카를로 방법과 같은 샘플링 기법의 기초

> 💡 시행의 개념은 머신러닝에서 실험 설계와 데이터 수집의 기본! 모델의 성능 평가 및 신뢰성 있는 결과 도출을 위해 중요하다.

## 🌐 확률론의 기본 개념 - 표본공간 (Sample Space)

특정 시행에서 *발생 가능한 모든 결과*의 집합이다. 보통 Ω(오메가)로 표기.

$$ \Omega = {가능한 모든 결과} $$

### 실생활 예시

- 동전 던지기의 표본공간

$$ \Omega = {앞면, 뒷면} $$

- 주사위 굴리기의 표본공간

$$ \Omega = {1, 2, 3, 4, 5, 6} $$

### Python 예시

```python
# 표본공간 정의
coin_sample_space = ["앞면", "뒷면"]
dice_sample_space = [1, 2, 3, 4, 5, 6]
cards_sample_space = [(suit, rank) for suit in ["스페이드", "하트", "다이아몬드", "클로버"]
                      for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

print(f"동전 던지기 표본공간의 크기: {len(coin_sample_space)}")
print(f"주사위 굴리기 표본공간의 크기: {len(dice_sample_space)}")
print(f"카드 뽑기 표본공간의 크기: {len(cards_sample_space)}")
print(f"카드 표본공간의 일부: {cards_sample_space[:5]}")

```

### 머신러닝/딥러닝에서의 활용

- 데이터 공간 정의: 입력 및 출력 변수의 가능한 값 범위 설정

- 확률 분포 모델링: 가능한 모든 데이터 포인트에 대한 확률 할당

- 가설 공간(Hypothesis Space): 모델이 학습할 수 있는 가능한 모든 함수의 집합

> 💡 표본공간을 이해하면 모델이 다루는 데이터의 범위와 특성을 명확히 정의할 수 있으며, 적절한 확률 분포를 선택하는 데 도움이 된다.

## 🎯 확률론의 기본 개념 - 근원사건 (Elementary Event)

표본공간의 *단일 원소, 즉 더 이상 분해할 수 없는 가장 기본적인 결과*를 의미한다.

[TODO 여기에 근원사건의 정의를 더 쉽게 설명 적기]

### 실생활 예시

주사위 굴리기에서 "3이 나오는 것"은 근원사건

### Python 예시

```python
import random


# 주사위 굴리기 시행에서 근원사건 발생 확인
def check_elementary_event(event_value, num_trials=10000):
    # 주사위 굴리기 시행
    dice_rolls = [random.randint(1, 6) for _ in range(num_trials)]

    # 특정 근원사건(예: 3이 나오는 것) 발생 횟수
    event_count = dice_rolls.count(event_value)

    # 근원사건의 실험적 확률
    probability = event_count / num_trials

    return probability


# 주사위에서 3이 나오는 근원사건의 확률
prob_3 = check_elementary_event(3)
print(f"주사위에서 3이 나올 확률(시뮬레이션): {prob_3:.4f}")
print(f"주사위에서 3이 나올 이론적 확률: {1 / 6:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 분류 문제: 개별 클래스가 근원사건이 될 수 있음

- 데이터 포인트 분석: 개별 데이터 포인트를 근원사건으로 간주

- 결정 트리: 노드에서의 개별 결정 경로

> 💡 근원사건은 확률 계산의 기본 단위로, 복잡한 사건을 근원사건들의 집합으로 분해하여 분석할 수 있도록 해준다.

## 🎭 확률론의 기본 개념 - 사건 (Event)

*표본공간의 부분집합*으로, *특정 조건을 만족하는 결과들의 모임*입니다.

수식으로 표현하면, (A는 표본공간 Ω의 부분집합)

$$ A \subseteq \Omega $$

### 실생활 예시

주사위를 굴렸을 때 짝수가 나오는 사건

$$ A = {2, 4, 6} $$

### Python 예시

```python
import numpy as np


# 주사위 굴리기 시행에서 사건 정의 및 확인
def check_event_probability(event_function, num_trials=10000):
    # 주사위 굴리기 시행
    dice_rolls = np.random.randint(1, 7, num_trials)

    # 사건 조건을 만족하는 결과 확인
    event_occurrences = sum(event_function(roll) for roll in dice_rolls)

    # 사건의 실험적 확률
    probability = event_occurrences / num_trials

    return probability


# 짝수가 나오는 사건
def is_even(roll):
    return roll % 2 == 0


# 5보다 큰 수가 나오는 사건
def is_greater_than_five(roll):
    return roll > 5


prob_even = check_event_probability(is_even)
prob_greater_than_five = check_event_probability(is_greater_than_five)

print(f"주사위에서 짝수가 나올 확률(시뮬레이션): {prob_even:.4f}")
print(f"주사위에서 5보다 큰 수가 나올 확률(시뮬레이션): {prob_greater_than_five:.4f}")
```

### 머신러닝/딥러닝에서의 활용

- 이상 탐지(Anomaly Detection): 특정 조건을 만족하는 데이터 포인트 식별

- 조건부 확률 계산: 특정 조건 하에서의 확률 계산

- 특성 조합: 여러 특성이 특정 조건을 만족하는 경우 분석

> 💡 사건은 데이터에서 의미 있는 패턴이나 조건을 정의하고 분석하는 데 필수적인 개념!

## 🔄 확률론의 핵심 연산 - 합사건 (Union of Events)

두 사건 중 *적어도 하나가 발생하는 사건*입니다. A와 B의 합사건은 $ A\cup B $로 표기합니다.

$$ A\cup B = {x | x\in A \text{ 또는 } x\in B} $$

### 실생활 예시

주사위를 굴렸을 때,

$$ A = \text{"3 이하가 나오는 사건"} = {1, 2, 3} $$

$$ B = \text{"짝수가 나오는 사건"} = {2, 4, 6} $$

$$ A\cup B = \text{"3 이하이거나 짝수가 나오는 사건"} = {1, 2, 3, 4, 6} $$

### Python 예시

```python
# 합사건 계산
def union_event(event_A, event_B):
    return set(event_A).union(set(event_B))


# 주사위 사건 정의
event_less_than_or_equal_3 = [1, 2, 3]
event_even = [2, 4, 6]

# 합사건 계산
union_result = union_event(event_less_than_or_equal_3, event_even)
print(f"A∪B = {union_result}")

# 확률 계산
prob_union = len(union_result) / 6
print(f"P(A∪B) = {prob_union:.4f}")


# 시뮬레이션으로 확인
def is_in_union_event(roll):
    return roll <= 3 or roll % 2 == 0


import numpy as np

rolls = np.random.randint(1, 7, 10000)
union_count = sum(is_in_union_event(roll) for roll in rolls)
prob_union_sim = union_count / 10000
print(f"P(A∪B) 시뮬레이션 결과: {prob_union_sim:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 특성 결합: 여러 특성 중 하나라도 조건을 만족하는 데이터 포인트 식별

- 다중 조건 모델링: "또는(OR)" 조건을 사용한 규칙 기반 모델

- 오류 분석: 다양한 유형의 오류 중 하나라도 발생하는 경우 식별

> 💡 합사건은 여러 조건 중 하나라도 만족하는 경우를 모델링하는 데 중요하며, <u>복잡한 조건부 확률 계산에 필수적</u>입니다.

## 🔗 확률론의 핵심 연산 - 곱사건 (Intersection of Events)

두 사건이 *동시에 발생하는 사건*입니다. A와 B의 곱사건은 $ A\cap B $로 표기합니다.

$$ A\cap B = {x | x\in A \text{ 그리고 } x\in B} $$

### 실생활 예시

주사위를 굴렸을 때,

$$ A = \text{"3 이하가 나오는 사건"} = {1, 2, 3} $$

$$ B = \text{"짝수가 나오는 사건"} = {2, 4, 6} $$

$$ A\cap B = \text{"3 이하이면서 짝수가 나오는 사건"} = {2} $$

### Python 예시

```python
# 곱사건 계산
def intersection_event(event_A, event_B):
    return set(event_A).intersection(set(event_B))


# 주사위 사건 정의
event_less_than_or_equal_3 = [1, 2, 3]
event_even = [2, 4, 6]

# 곱사건 계산
intersection_result = intersection_event(event_less_than_or_equal_3, event_even)
print(f"A∩B = {intersection_result}")

# 확률 계산
prob_intersection = len(intersection_result) / 6
print(f"P(A∩B) = {prob_intersection:.4f}")


# 시뮬레이션으로 확인
def is_in_intersection_event(roll):
    return roll <= 3 and roll % 2 == 0


import numpy as np

rolls = np.random.randint(1, 7, 10000)
intersection_count = sum(is_in_intersection_event(roll) for roll in rolls)
prob_intersection_sim = intersection_count / 10000
print(f"P(A∩B) 시뮬레이션 결과: {prob_intersection_sim:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 조건부 확률: 특정 조건이 주어졌을 때의 확률 계산

- 특성 교차(Feature Interaction): 여러 특성이 동시에 영향을 미치는 패턴 식별

- 규칙 기반 분류: "그리고(AND)" 조건을 사용한 규칙 생성

> 💡 곱사건은 여러 조건이 동시에 만족되는 경우를 모델링하는 데 중요하며, 특히<u> 베이즈 정리와 조건부 확률 계산에서 핵심적인 역할</u>을 합니다.

## 🚫 확률론의 핵심 연산 - 배반사건 (Mutually Exclusive Events)

두 사건이 *동시에 일어날 수 없는 경우*, 즉 $ A\cap B = \emptyset $인 경우를 배반사건이라고 합니다.

### 실생활 예시

주사위를 한 번 굴렸을 때,

$$ A = \text{"홀수가 나오는 사건"} = {1, 3, 5} $$

$$ B = \text{"짝수가 나오는 사건"} = {2, 4, 6} $$

→ $ A $ 와 $ B $ 는 배반사건입니다.

### Python 예시

```python
import numpy as np


# 배반사건 확인 함수
def are_mutually_exclusive(event_A, event_B):
    intersection = set(event_A).intersection(set(event_B))
    return len(intersection) == 0


# 주사위 사건 정의
event_odd = [1, 3, 5]
event_even = [2, 4, 6]
event_prime = [2, 3, 5]
event_less_than_3 = [1, 2]

# 배반사건 여부 확인
print(f"홀수와 짝수는 배반사건인가? {are_mutually_exclusive(event_odd, event_even)}")
print(f"소수와 짝수는 배반사건인가? {are_mutually_exclusive(event_prime, event_even)}")
print(f"소수와 3 미만은 배반사건인가? {are_mutually_exclusive(event_prime, event_less_than_3)}")


# 시뮬레이션으로 확인
def simultaneous_events_count(event_func_A, event_func_B, num_trials=10000):
    count = 0
    for _ in range(num_trials):
        roll = np.random.randint(1, 7)
        if event_func_A(roll) and event_func_B(roll):
            count += 1
    return count


def is_odd(roll):
    return roll % 2 == 1


def is_even(roll):
    return roll % 2 == 0


simultaneous_count = simultaneous_events_count(is_odd, is_even)
print(f"홀수와 짝수가 동시에 발생한 횟수(10000번 시행): {simultaneous_count}")

```

### 머신러닝/딥러닝에서의 활용

- 상호 배타적 분류(Mutually Exclusive Classification): 데이터 포인트가 하나의 클래스에만 속하는 분류 문제

- 의사결정 트리: 각 노드에서의 분기가 배반사건을 형성

- 원-핫 인코딩(One-Hot Encoding): 범주형 데이터를 상호 배타적인 이진 특성으로 변환

> 💡 배반사건은 확률 계산을 단순화할 수 있으며($ P(A\cup B) = P(A) + P(B) $), 분류 문제에서 클래스 간 관계를 정의하는 데 중요

## 🔄 확률론의 핵심 연산 - 여사건 (Complement of an Event)

*어떤 사건 A가 일어나지 않는 사건을 A의 여사건*이라고 하며, $ A^c $ 또는 $ A' $로 표기합니다.

$$ A^c = {x \in \Omega | x \notin A} $$

### 실생활 예시

주사위를 굴렸을 때,

$$ A = \text{"짝수가 나오는 사건"} = {2, 4, 6} $$

$$ A^c = \text{"홀수가 나오는 사건"} = {1, 3, 5} $$

### Python 예시

```python
# 여사건 계산 함수
def complement_event(event, sample_space):
    return [x for x in sample_space if x not in event]


# 주사위 표본공간과 사건 정의
dice_sample_space = [1, 2, 3, 4, 5, 6]
event_even = [2, 4, 6]
event_greater_than_3 = [4, 5, 6]

# 여사건 계산
complement_even = complement_event(event_even, dice_sample_space)
complement_greater_than_3 = complement_event(event_greater_than_3, dice_sample_space)

print(f"짝수의 여사건: {complement_even}")
print(f"3보다 큰 수의 여사건: {complement_greater_than_3}")

# 여사건의 확률 계산
prob_complement_even = len(complement_even) / len(dice_sample_space)
print(f"P(A^c) = {prob_complement_even}, P(A) = {1 - prob_complement_even}")


# 시뮬레이션으로 확인
def is_even(roll):
    return roll % 2 == 0


def is_not_even(roll):
    return not is_even(roll)


import numpy as np

rolls = np.random.randint(1, 7, 10000)
not_even_count = sum(is_not_even(roll) for roll in rolls)
prob_not_even_sim = not_even_count / 10000
print(f"P(A^c) 시뮬레이션 결과: {prob_not_even_sim:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 이진 분류: 양성/음성 클래스 간의 관계

- 부정 샘플링(Negative Sampling): 모델 학습을 위한 부정 예제 생성

- 확률 계산 단순화: $ P(A^c) = 1 - P(A) $를 이용한 복잡한 확률 계산 단순화

> 💡 여사건은 확률 계산을 단순화하고, 특히 복잡한 사건의 확률을 계산할 때 유용하다. 또한, 이진 분류 문제에서 클래스 간 관계를 이해하는 데 중요하다.

## 🧮 확률의 계산 방법 - 수학적 확률 (Mathematical Probability)

모든 가능한 결과가 일어날 가능성이 동일하다고 가정할 때, 특정 사건이 일어날 확률을 계산하는 방법이다. *표본공간의 원소 개수에 대한 특정 사건에 속하는 원소 개수의 비율*로 정의됩니다.

$$ P(A) = \frac{n(A)}{n(\Omega)} $$

여기서 $ n(A) $는 사건 A에 포함된 원소의 개수, $ n(\Omega) $는 표본공간의 원소 개수입니다.

### 실생활 예시

균일한 주사위를 던졌을 때 짝수가 나올 확률은,

$$ P(짝수) = \frac{n({2, 4, 6})}{n({1, 2, 3, 4, 5, 6})} = \frac{3}{6} = \frac{1}{2} $$

### Python 예시

```python
# 수학적 확률 계산 함수
def mathematical_probability(event, sample_space):
    return len(event) / len(sample_space)


# 주사위 표본공간과 사건 정의
dice_sample_space = [1, 2, 3, 4, 5, 6]
event_even = [2, 4, 6]
event_prime = [2, 3, 5]
event_greater_than_4 = [5, 6]

# 수학적 확률 계산
prob_even = mathematical_probability(event_even, dice_sample_space)
prob_prime = mathematical_probability(event_prime, dice_sample_space)
prob_greater_than_4 = mathematical_probability(event_greater_than_4, dice_sample_space)

print(f"P(짝수) = {prob_even}")
print(f"P(소수) = {prob_prime}")
print(f"P(4보다 큰 수) = {prob_greater_than_4}")

```

### 머신러닝/딥러닝에서의 활용

- 균등 분포(Uniform Distribution) 가정: 초기 가중치 설정이나 랜덤 샘플링에서 활용

- 사전 확률(Prior Probability) 설정: 베이지안 방법론에서 사전 정보가 없을 때 균등 확률 사용

- 랜덤 초기화: 신경망의 가중치 초기화 등에 사용

> 💡 수학적 확률은 확률론의 기초가 되며, 모든 가능성이 동등하게 중요한 상황에서의 확률 모델링에 필수적이다.

## 📈 확률의 계산 방법 - 통계적 확률 (Statistical Probability)

*실제 관측 데이터를 기반으로 사건의 발생 빈도*로 확률을 계산하는 방법입니다. 충분히 많은 시행 횟수에서 특정 사건이 발생한 비율로 정의됩니다.

$$ P(A) \approx \frac{n(A)}{n} $$

여기서 $ n(A) $는 사건 A가 발생한 횟수, $ n $은 총 시행 횟수입니다.

### 실생활 예시

동전을 1000번 던져서 앞면이 540번 나왔다면, 앞면이 나올 통계적 확률은,

$$ \frac{540}{1000} = 0.54 $$

### Python 예시

```python
import numpy as np


# 통계적 확률 계산을 위한 시뮬레이션
def statistical_probability_simulation(event_function, num_trials=10000):
    # 시행 실행
    event_count = 0
    for _ in range(num_trials):
        # 시행 결과 생성 (예: 주사위 굴리기)
        outcome = np.random.randint(1, 7)
        # 사건 발생 여부 확인
        if event_function(outcome):
            event_count += 1

    # 통계적 확률 계산
    return event_count / num_trials


# 짝수가 나오는 사건 정의
def is_even(outcome):
    return outcome % 2 == 0


# 통계적 확률 계산
prob_even_statistical = statistical_probability_simulation(is_even, 100000)
print(f"P(짝수) 통계적 확률 (100,000번 시행): {prob_even_statistical:.4f}")


# 동전 던지기 시뮬레이션
def coin_flip_simulation(num_flips=10000):
    # 0은 앞면, 1은 뒷면
    flips = np.random.randint(0, 2, num_flips)
    heads_count = np.sum(flips == 0)
    return heads_count / num_flips


prob_heads = coin_flip_simulation(100000)
print(f"P(앞면) 통계적 확률 (100,000번 시행): {prob_heads:.4f}")

```

### 머신러닝/딥러닝에서의 활용

- 빈도주의적 확률(Frequentist Probability): 관측 데이터를 기반으로 한 확률 계산

- 경험적 확률 분포 추정: 히스토그램이나 커널 밀도 추정 등을 통한 확률 분포 구성

- 교차 검증(Cross-Validation): 모델 성능의 통계적 추정

> 💡 통계적 확률은 *실제 데이터에서 패턴과 확률을 추정하는 머신러닝의 핵심 개념*으로, 모델이 데이터에서 학습하는 방식의 기반이 된다!

## ➕ 확률의 덧셈법칙 (Addition Rule of Probability)

*두 사건 A와 B의 합사건(A 또는 B가 발생하는 사건)의 확률*을 계산하는 규칙이다.

$$ P(A \cup B) = P(A) + P(B) - P(A \cap B) $$

❗ 특별한 경우: *A와 B가 배반사건(서로 겹치지 않는 사건)*이면,

$$ P(A \cup B) = P(A) + P(B) $$

두 사건이 배반 사건이므로, $ P(A \cap B) = 0  $ 이기 때문에 위와 같은 공식이 되는 것.

### 실생활 예시

주사위를 던졌을 때 홀수(A = {1, 3, 5})나 4 이상(B = {4, 5, 6})이 나올 확률

$$ P(A \cup B) = P(A) + P(B) - P(A \cap B) = \frac{3}{6} + \frac{3}{6} - \frac{1}{6} = \frac{5}{6} $$

### Python 예시

```python
# 확률의 덧셈법칙 계산 함수
def addition_rule(prob_A, prob_B, prob_intersection):
    return prob_A + prob_B - prob_intersection


# 주사위 사건의 확률
prob_odd = 3 / 6  # P(홀수) = P({1, 3, 5})
prob_greater_equal_4 = 3 / 6  # P(4 이상) = P({4, 5, 6})
prob_intersection = 1 / 6  # P(홀수 ∩ 4 이상) = P({5})

# 덧셈법칙으로 합사건의 확률 계산
prob_union = addition_rule(prob_odd, prob_greater_equal_4, prob_intersection)
print(f"P(홀수 ∪ 4 이상) = {prob_union}")

# 시뮬레이션으로 확인
import numpy as np


def is_odd_or_greater_equal_4(outcome):
    return outcome % 2 == 1 or outcome >= 4


dice_rolls = np.random.randint(1, 7, 100000)
event_count = sum(is_odd_or_greater_equal_4(roll) for roll in dice_rolls)
prob_union_sim = event_count / 100000
print(f"P(홀수 ∪ 4 이상) 시뮬레이션 결과: {prob_union_sim:.4f}")
```

### 머신러닝/딥러닝에서의 활용

- 다중 클래스 분류: 여러 클래스에 속할 확률의 결합

- 앙상블 모델: 여러 모델의 예측 결합(OR 조건)

- 오류 분석: 여러 유형의 오류 중 하나라도 발생할 확률 계산

> 💡 덧셈법칙은 복잡한 사건의 확률을 더 간단한 확률들로 분해하여 계산할 수 있게 해주며, 특히 여러 조건 중 하나라도 만족하는 경우를 모델링할 때 필수적이다.

## 🔮 조건부 확률 (Conditional Probability)

*사건 B가 발생했다는 조건 하에 사건 A가 발생할 확률*입니다. $ P(A|B) $ 로 표기한다.

$$ P(A|B) = \frac{P(A \cap B)}{P(B)}, P(B) > 0 $$

### 실생활 예시

두 개의 주사위를 던졌을 때, 합이 8이라는 조건 하에 첫 번째 주사위가 3이 나올 확률

$$ P(\text{첫번째 주사위=3 | 합=8}) = \frac{P(\text{첫번째 주사위=3} \cap \text{합=8})}{P(\text{합=8})} = \frac{P({(3,5)})}{P({(2,6), (3,5), (4,4), (5,3), (6,2)})} = \frac{1}{5} $$

### Python 예시

```python
# 조건부 확률 계산 함수
def conditional_probability(event_A_and_B, event_B):
    return len(event_A_and_B) / len(event_B)


# 두 주사위를 던지는 표본공간
sample_space = [(i, j) for i in range(1, 7) for j in range(1, 7)]

# 사건 정의
event_sum_8 = [(i, j) for i, j in sample_space if i + j == 8]
event_first_die_3 = [(i, j) for i, j in sample_space if i == 3]
event_first_die_3_and_sum_8 = [(i, j) for i, j in sample_space if i == 3 and i + j == 8]

# 조건부 확률 계산
prob_first_3_given_sum_8 = conditional_probability(event_first_die_3_and_sum_8, event_sum_8)
print(f"P(첫번째 주사위=3 | 합=8) = {prob_first_3_given_sum_8}")

# 시뮬레이션으로 확인
import numpy as np


def simulate_conditional_probability(num_trials=100000):
    # 두 주사위 굴리기
    die1 = np.random.randint(1, 7, num_trials)
    die2 = np.random.randint(1, 7, num_trials)
    dice_sum = die1 + die2

    # 합이 8인 경우 필터링
    sum_8_indices = np.where(dice_sum == 8)[0]
    first_die_values = die1[sum_8_indices]

    # 첫번째 주사위가 3인 비율 계산
    prob = np.mean(first_die_values == 3)
    return prob


prob_sim = simulate_conditional_probability()
print(f"P(첫번째 주사위=3 | 합=8) 시뮬레이션 결과: {prob_sim:.4f}")

```

### 머신러닝/딥러닝에서의 의미

머신러닝 모델은 본질적으로 조건부 확률을 모델링한다. 예를 들어, 분류 문제에서 모델은 입력 $ X $ 가 주어졌을 때 클래스 $ Y $ 의 조건부 확률 $ P(Y|X) $를 학습하는 것이다.

이는 "이 입력 특성들이 주어졌을 때, 각 클래스에 속할 확률은 얼마인가?"를 계산하는 것인다.

- 즉, 머신러닝/딥러닝에서 중요한 이유는,

    - 분류 모델의 기초: 나이브 베이즈, 로지스틱 회귀 등의 분류 알고리즘은 조건부 확률에 기반한다.

    - 확률적 의사결정: 머신러닝 모델은 종종 "이 입력이 주어졌을 때, 출력이 Y일 확률"을 계산한다.

    - 베이지안 추론: 불확실성을 다루는 베이지안 방법론의 핵심 개념이다.

    - 생성 모델: GAN, VAE 같은 생성 모델들은 조건부 확률 분포를 학습한다.

<br/>

## 👨‍🏫 기본적으로 알아야할 정리인, 베이즈 정리

$$ P(A|B) = \frac{P(B|A) \times P(A)}{P(B)} $$

### 유도 과정

1. 조건부 확률의 정의에서 $ P(A|B) = \frac{P(A \cap B)}{P(B)} $

1. 마찬가지로, $ P(B|A) = \frac{P(A \cap B)}{P(A)} $

1. 따라서, 이항 등을 진행하다보면 $ P(A \cap B) = P(B|A) \times P(A) $

1. 이를 1번 식에 대입하면 $ P(A|B) = \frac{P(B|A) \times P(A)}{P(B)} $

### Python 예시: 의료 검사 문제

```python
# 베이즈 정리를 이용한 의료 검사 문제
# 질병 유병률: 1%
# 검사 민감도(sensitivity): 질병이 있을 때 양성 결과가 나올 확률 = 95%
# 검사 특이도(specificity): 질병이 없을 때 음성 결과가 나올 확률 = 90%

# P(D): 질병을 가지고 있을 사전 확률
p_disease = 0.01

# P(+|D): 질병이 있을 때 검사 양성일 확률
p_positive_given_disease = 0.95

# P(+|~D): 질병이 없을 때 검사 양성일 확률
p_positive_given_no_disease = 0.10

# P(+): 검사 양성일 총 확률 (전체 확률 법칙 사용)
p_positive = p_positive_given_disease * p_disease + p_positive_given_no_disease * (1 - p_disease)

# P(D|+): 검사 양성일 때 실제 질병이 있을 확률 (베이즈 정리)
p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print(f"검사 양성일 때 실제 질병이 있을 확률: {p_disease_given_positive:.4f}")
print(f"즉, 양성 판정을 받은 사람 중 약 {p_disease_given_positive * 100:.1f}%만이 실제 질병이 있습니다.")
```

### Python 예시: 스팸 필터링

- 특정 단어들이 등장했을 때 그 메일이 스팸일 확률

```python
# 베이즈 정리를 이용한 이메일 스팸 필터 예시

# 기본 통계 (가정)
# 1. 전체 이메일 중 30%가 스팸이라고 가정 (사전 확률)
p_spam = 0.3  # P(스팸)
p_ham = 0.7  # P(정상)

# 2. 특정 단어들의 조건부 확률
# "무료"라는 단어가 포함될 확률
p_free_given_spam = 0.6  # P("무료"|스팸) - 스팸에서 "무료" 단어 포함 확률
p_free_given_ham = 0.05  # P("무료"|정상) - 정상에서 "무료" 단어 포함 확률

# "당첨"이라는 단어가 포함될 확률
p_win_given_spam = 0.4  # P("당첨"|스팸)
p_win_given_ham = 0.02  # P("당첨"|정상)

# "회의"라는 단어가 포함될 확률
p_meeting_given_spam = 0.05  # P("회의"|스팸)
p_meeting_given_ham = 0.3  # P("회의"|정상)


# 3. 베이즈 정리를 적용한 스팸 필터 함수
def calculate_spam_probability(has_free, has_win, has_meeting):
    """
    베이즈 정리를 사용하여 이메일이 스팸일 확률 계산

    Args:
        has_free (bool): "무료" 단어가 포함되었는지 여부
        has_win (bool): "당첨" 단어가 포함되었는지 여부
        has_meeting (bool): "회의" 단어가 포함되었는지 여부

    Returns:
        float: 스팸일 확률 (0~1 사이 값)
    """
    # 각 단어에 대한 가능도(likelihood) 계산
    p_words_given_spam = 1.0
    p_words_given_ham = 1.0

    # "무료" 단어 처리
    if has_free:
        p_words_given_spam *= p_free_given_spam
        p_words_given_ham *= p_free_given_ham
    else:
        p_words_given_spam *= (1 - p_free_given_spam)
        p_words_given_ham *= (1 - p_free_given_ham)

    # "당첨" 단어 처리
    if has_win:
        p_words_given_spam *= p_win_given_spam
        p_words_given_ham *= p_win_given_ham
    else:
        p_words_given_spam *= (1 - p_win_given_spam)
        p_words_given_ham *= (1 - p_win_given_ham)

    # "회의" 단어 처리
    if has_meeting:
        p_words_given_spam *= p_meeting_given_spam
        p_words_given_ham *= p_meeting_given_ham
    else:
        p_words_given_spam *= (1 - p_meeting_given_spam)
        p_words_given_ham *= (1 - p_meeting_given_ham)

    # 증거(evidence) 계산: P(words) = P(words|spam)P(spam) + P(words|ham)P(ham)
    p_words = p_words_given_spam * p_spam + p_words_given_ham * p_ham

    # 베이즈 정리 적용: P(spam|words) = P(words|spam)P(spam) / P(words)
    p_spam_given_words = (p_words_given_spam * p_spam) / p_words

    return p_spam_given_words


# 여러 이메일 예시에 대한 스팸 확률 계산
print("이메일 예시와 스팸 확률:")

# 이메일 1: "무료", "당첨" 포함, "회의" 미포함
email1_prob = calculate_spam_probability(True, True, False)
print(f"이메일 1 (무료+당첨): 스팸 확률 = {email1_prob:.4f} ({email1_prob * 100:.1f}%)")

# 이메일 2: "무료" 포함, "당첨", "회의" 미포함
email2_prob = calculate_spam_probability(True, False, False)
print(f"이메일 2 (무료만): 스팸 확률 = {email2_prob:.4f} ({email2_prob * 100:.1f}%)")

# 이메일 3: "회의" 포함, "무료", "당첨" 미포함
email3_prob = calculate_spam_probability(False, False, True)
print(f"이메일 3 (회의만): 스팸 확률 = {email3_prob:.4f} ({email3_prob * 100:.1f}%)")

# 이메일 4: "무료", "회의" 포함, "당첨" 미포함
email4_prob = calculate_spam_probability(True, False, True)
print(f"이메일 4 (무료+회의): 스팸 확률 = {email4_prob:.4f} ({email4_prob * 100:.1f}%)")

```

- 사전 확률(Prior)

    - 전체 이메일 중 30%가 스팸이라고 가정: P(스팸) = 0.3

- 가능도(Likelihood)

    - 각 단어가 스팸 또는 정상 이메일에 나타날 조건부 확률

    - 예: P("무료"|스팸) = 0.6은 스팸 이메일의 60%에 "무료"라는 단어가 포함됨을 의미

- 증거(Evidence)

    - 특정 단어 조합이 나타날 확률: P(단어들) = P(단어들|스팸)×P(스팸) + P(단어들|정상)×P(정상)

- 사후 확률(Posterior)

    - 베이즈 정리 적용: P(스팸|단어들) = P(단어들|스팸)×P(스팸) / P(단어들)

### 실제 응용에서의 스팸 필터링 예시 의미

위 예시는 단순화되었지만, 실제 스팸 필터의 기본 원리를 잘 보여준다.

- 단어의 증거 가치: "무료"와 "당첨" 같은 단어는 스팸 가능성을 높이는 증거로 작용한다. 반면, "회의" 같은 단어는 정상 이메일 가능성을 높인다.

- 결합된 증거: 여러 단어가 함께 나타날 때의 확률이 어떻게 계산되는지 보여준다. 예를 들어, "무료"와 "당첨"이 함께 나타나면 스팸 가능성이 크게 높아진다.

- 직관과 일치: "무료"만 있는 이메일보다 "무료"와 "당첨"이 함께 있는 이메일이 스팸일 확률이 더 높은 것은 직관적으로도 이해된다.

실제 스팸 필터에서는 훨씬 많은 단어를 고려하고, 단어의 위치, 빈도, 다른 특성(이메일 발신자, HTML 사용 여부 등)도 함께 고려하지만, 기본 원리는 이 예시와 동일하게 베이즈 정리에 기반한다.

> 💡 이후 수학을 더 공부하게 된다면, 아래의 내용을 알아 두는 것도 좋다!
> - 확률 분포: 이산/연속 확률 분포에서의 조건부 확률
> - 체인 룰: $ P(A,B,C) = P(A|B,C) * P(B|C) * P(C) $와 같은 결합확률의 분해
> - 최대 우도 추정(MLE): 조건부 확률을 최대화하는 모델 파라미터 찾기
