---
title: 🎲 기초 수학 for 인공지능 03; 벡터
date: 2025-04-07 13:32:00 +0900
categories: [ MATHEMATICS, VECTOR ]
tags: [ '급발진거북이', 'numpy', 'mathematics', '기초수학', 'torch', 'tensor', '행렬', 'matrix', 'machen learning', 'deeplearning', 'python', '파이썬' ]
toc: true
comments: false
mermaid: true
math: true
---

## 📦 사용하는 python package

- torch==2.6.0

- matplotlib==3.10.1

## 🚀 TL;DR

-

## 🔢 스칼라 (Scalar)

### 언어적 표현 (Linguistic Expression)

- 단일 값 또는 크기만 가지는 양을 의미

- 방향이 없는 단순한 숫자

- 예시) 온도, 질량, 거리

- 머신러닝에서 scalar 는 다음과 같이 사용된다.

    - 학습률(learning rate)

    - 손실 함수(loss function)의 출력값

    - 데이터 포인트의 단일 특성(feature)

    - 임계값(threshold) 설정

### 대수적 표현 (Algebraic Expression)

수식에서 scalar 는 보통 소문자 이탤릭체로 표현한다.

$$ a, b, c, \lambda \in \mathbb{R} $$

여기서 $$ \mathbb{R} $$ 은 실수 집합을 의미한다.

예시) $$ x = 5, y = -3.14, \lambda = 0.01 $$

### 공간에서의 표현 (Spatial Representation)

- 스칼라는 1차원, 2차원, 3차원에서 점으로 표현할 수 있다.

  ![img_scalar.png](/assets/img/img_scalar.png)

### Python Code 로 표현 (Python Code Representation)

```python
import torch

# 스칼라 정의
learning_rate = torch.tensor(0.01)  # tensor(0.0100)
temperature = torch.tensor(27)  # tensor(27)
threshold = torch.tensor(0.5)  # tensor(0.5000)

# 스칼라 연산
z = temperature + 1
# item 함수는 tensor 의 값을 python 의 기본 숫자로 반환하는 함수
print(f"temperature + 1 = {z.item()}")  # 28
```

## 🔍 벡터 (Vector)

### 언어적 표현 (Linguistic Expression)

- 크기와 방향을 모두 가진 양

- 여러 개의 스칼라 값이 순서대로 나열된 것으로도 생각할 수 있음

- 머신러닝에서 vector 는 다음과 같이 사용한다.

    - 데이터 포인트의 특성(feature) 집합

    - 신경망의 가중치(weights)와 편향(biases)

    - 워드 임베딩(word embedding)

    - 이미지의 픽셀 값 배열

### 대수적 표현 (Algebraic Expression)

vector 는 보통 굵은 소문자나 화살표 표시($$ \mathbf{v},\ \vec{v} $$)로 표현한다.

$$ \mathbf{v} = [v_1, v_2, ..., v_n] \in \mathbb{R}^n\ 또는\ \mathbf{v} = \begin{pmatrix} v_1 \ v_2 \ \vdots \ v_n \end{pmatrix} \in \mathbb{R}^n $$

여기서 $$ \mathbb{R}^n $$은 n차원 실수 공간을 의미한다.

### 공간에서의 표현 (Spatial Representation)

- 벡터는 공간상의 점 또는 원점에서 특정 점까지의 화살표로 표현할 수 있다.

- 2차원 벡터는 x-y 평면에, 3차원 벡터는 x-y-z 공간에서 표현된다.

![img_vector_in_2d.png](/assets/img/img_vector_in_2d.png)

![img_vector_in_3d.png](/assets/img/img_vector_in_3d.png)

### Python Code 로 표현 (Python Code Representation)

```python
import torch
import matplotlib.pyplot as plt

# vector 정의
feature_vector = torch.tensor([1.2, 3.5, 2.1, 0.8])  # 4차원 vector
word_embedding = torch.tensor([0.2, -0.4, 0.1, 0.5, 0.3])  # 5차원 vector


# 2D vector 시각화
def plot_vector(vector, color='blue', label='Vector'):
    plt.quiver(0, 0, vector[0].item(), vector[1].item(),
               angles='xy', scale_units='xy', scale=1, color=color, label=label)
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.title("Visualize Vector")
    plt.xlabel("x")
    plt.ylabel("y")


v1 = torch.tensor([3.0, 2.0])
v2 = torch.tensor([-1.0, 4.0])

plot_vector(v1, 'blue', 'Vector 1')
plot_vector(v2, 'red', 'Vector 2')
plt.show()
```

> 💡 tensor 를 간단히 n 차원 vector 라고 말하기도 한다!

## 📊 행렬 (Matrix)

### 언어적 표현 (Linguistic Expression)

- 행렬은 2차원으로 배열된 숫자들의 집합

- 행(row)과 열(column)로 구성되며, m×n 행렬은 m개의 행과 n개의 열을 가진다.

- 머신러닝에서 행렬은 다음과 같이 사용된다.

    - 데이터셋 (각 행은 데이터 포인트, 각 열은 특성)

    - 가중치 행렬 (신경망 레이어 사이의 연결 강도)

    - 이미지 데이터 (픽셀 값의 2D 배열)

    - 변환 및 회전을 표현하는 연산자

    - 공분산 행렬 (특성 간의 관계 표현)

### 대수적 표현 (Algebraic Expression)

행렬은 보통 대문자로 표현한다.

$$ A,\ B,\ W \in \mathbb{R}^{m \times n} $$

$$ A = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \
a_{21} & a_{22} & \cdots & a_{2n} \
\vdots & \vdots & \ddots & \vdots \
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix} \in \mathbb{R}^{m \times n} $$

여기서 
$$ \mathbb{R}^{m \times n} $$
은 m행 n열의 실수 행렬 집합을 의미한다.

### 공간에서의 표현 (Spatial Representation)

![matrix_spatial_representation.png](/assets/img/matrix_spatial_representation.png)

- matrix 는 2차원 숫자 배열이므로, 흑백 이미지로 해석할 수 있다.

- 또한 matrix 는 선형 변환으로 해석할 수 있다.

- 행렬을 벡터에 곱하면 해당 벡터가 회전, 확장, 축소, 반사 등의 변환을 겪게 된다!

### Python Code 로 표현 (Python Code Representation)

```python
import torch

# 행렬 정의
A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print("행렬 A:")
print(A)
# 행렬 A:
# tensor([[1., 2.],
#         [3., 4.]])

B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
print("행렬 B:")
print(B)
# 행렬 B:
# tensor([[5., 6.],
#         [7., 8.]])

# 행렬 연산
print("행렬 덧셈 A + B:")  # 각 위치의 요소끼리 더함
print(A + B)
# 행렬 덧셈 A + B:
# tensor([[ 6.,  8.],
#         [10., 12.]])
```

## 📏 노름(Norm of Vector)이란

- vector 가 원점에서 얼마나 떨어져 있는지를 의미한다.

- vector 의 크기 또는 길이를 측정하는 방법으로 사용한다.

- 다양한 norm 방식이 있으며, 각각 다른 기하학적 의미를 가진다.

- 일반적인 p-norm( $$ L_p $$  norm) 수식

$$ ||x||_p = \left( \sum_{i=1}^{n} |x_i|^p \right)^{1/p}, \quad \text{여기서 } p \geq 1, x \in \mathbb{R}^n $$

- 머신러닝에서 norm 은 다음과 같이 사용된다.

    - 정규화(regularization)

    - 거리 계산 (두 데이터 포인트 간의 유사도)

    - 오차/손실 측정

    - 기울기 크기 측정

## 📐 L1 노름 (L1 Norm)

### 수식 표현 (Mathematical Expression)

- L1 norm 은 vector 요소의 절대값 합으로 정의

$$ ||x||_1 = \sum_{i=1}^{n} |x_i|,\ 여기서 x \in \mathbb{R}^n $$

- 머신러닝에서는 다음과 같이 사용된다.

    - 희소성(sparsity)을 촉진하는 정규화(Lasso 회귀)

    - 이상치(outlier)에 덜 민감한 거리 측정

    - 특성 선택(feature selection)

### 기하학적 표현 (Geometric Representation)

- L1 노름은 각 차원의 절대값 합이다.

- $$ \vec x = [x_1, x_2] $$ 일 때,

![l1_geometric_representation.png](/assets/img/l1_geometric_representation.png)

### 맨하튼 노름 (Manhattan Norm)

![l1_manhattan_street.png](/assets/img/l1_manhattan_street.png)

- 맨하탄 노름이라고도 불리는 L1 노름은 도시 블록 거리를 의미한다.

### Python Code 로 표현 (Python Code Representation)

```python
import torch


# 커스텀 L1 norm 계산 함수
def l1_norm(v):
    return torch.sum(torch.abs(v))


vector = torch.tensor([4.0, 3.0])
norm_l1 = l1_norm(vector)
print(f"{vector} 의 L1 노름: {norm_l1.item()}")
# tensor([4., 3.]) 의 L1 노름: 7.0

# PyTorch 내장 함수 사용
norm_l1_torch = torch.norm(vector, p=1)
print(f"PyTorch 로 계산한 {vector} 의 L1 노름: {norm_l1_torch.item()}")
# PyTorch 로 계산한 L1 노름: 7.0
```

## 📊 L2 노름 (L2 Norm)

### 수식 표현 (Mathematical Expression)

- L2 norm 은 vector 요소 제곱합의 제곱근으로 정의한다.

- 일반적으로 숫자가 생략되어있다면, L2 norm 이라고 여긴다. $$ |x| $$ → L2 norm

$$ ||x||_2 = \sqrt{\sum_{i=1}^{n} x_i^2},\ 여기서 x \in \mathbb{R}^n $$

### 유클리드 노름 (Euclidean Norm)

- L2 norm 은 유클리드 거리라고도 하며, 우리가 일상적으로 생각하는 "직선" 거리를 의미한다.

- 피타고라스 정리를 일반화한 것이다.

- 머신러닝에서는 다음과 같이 사용된다.

    - 가중치 정규화(Ridge 회귀)

    - 그래디언트 크기 측정

    - 표준 거리 측정

    - 이미지 비교

### Python Code 로 표현 (Python Code Representation)

```python
import torch


# 커스텀 L2 norm 계산 함수
def l2_norm(v):
    return torch.sqrt(torch.sum(v ** 2))


vector = torch.tensor([3.0, -4.0])
norm_l2 = l2_norm(vector)
print(f"{vector} 의 L2 노름: {norm_l2.item()}")
# tensor([ 3., -4.]) 의 L2 노름: 5.0

# PyTorch 내장 함수 사용
norm_l2_torch = torch.norm(vector, p=2)
print(f"PyTorch 로 계산한 {vector} 의 L2 노름: {norm_l2_torch.item()}")
# PyTorch 로 계산한 tensor([ 3., -4.]) 의 L2 노름: 5.0
```

## 🏆 L∞ 노름 (L-infinity Norm)

### 수식 표현 (Mathematical Expression)

- L∞ 노름(무한 노름)은 vector 요소들의 절대값 중 최대값으로 정의된다.

$$ ||x||_\infty = \max(|x_1|, |x_2|,..., |x_n|), 여기서 x \in \mathbb{R}^n $$

- 머신러닝에서는 다음과 같이 사용된다.

    - 최악의 경우 오류 평가

    - 이미지 처리에서 최대 픽셀 변화 측정

    - 적대적 예제(adversarial examples) 생성

        - 적대적 예제란, 인공지능 모델, 특히 딥러닝 모델을 의도적으로 속이거나 오분류하도록 만들기 위해 설계된 입력 데이터

    - 신경망의 강건성(robustness) 평가

        - 적대적 예제를 얼마나 잘 판단하는지를 가지고 평가하기도 함

### Python Code 로 표현 (Python Code Representation)

```python
import torch


# L∞ 노름 계산
def l_inf_norm(v):
    return torch.max(torch.abs(v))


vector = torch.tensor([3.0, -4.0, 2.0, -1.0])
norm_inf = l_inf_norm(vector)
print(f"{vector}의 L∞ 노름: {norm_inf.item()}")
# tensor([ 3., -4.,  2., -1.])의 L∞ 노름: 4.0

# PyTorch 내장 함수 사용
norm_inf_torch = torch.norm(vector, p=float('inf'))
print(f"PyTorch 로 계산한 {vector} 의 L∞ 노름: {norm_inf_torch.item()}")
# PyTorch 로 계산한 tensor([ 3., -4.,  2., -1.]) 의 L∞ 노름: 4.0
```

## 🔄 유사도 (Similarity)

- 유사도는 두 vector 가 얼마나 비슷한지를 측정하는 방법이다.

- 머신러닝에서는 데이터 포인트 간의 유사성을 측정하는 데 중요하게 사용된다.

> 💡 모든 데이터는 vector 로 표현될 수 있고, 이 vector 간의 연산을 통해 데이터 간의 관계를 파악할 수 있다!

### 맨하튼 유사도 (Manhattan Similarity)

- 맨하튼 노름(L1 norm 에 기반)를 사용한 유사도

- 두 vector 간 맨하튼 거리를 역수로 변환하여 계산한 값으로, 그 값이 작을수록 유사도가 높다.

- $$ x = [x_1,\ x_2,\ ...,\ x_n], y = [y_1,\ y_2,\ ...,\ y_n] $$ 일 때,

$$ \text{similarity}_{manhattan}(x, y) = \frac{1}{1 + \sum_{i=1}^n |x_i - y_i|_1}, 여기서 x, y \in \mathbb{R}^n $$

- 머신러닝에서는 아래의 내용과 같이 활용된다.

    - 희소 데이터에 대한 유사도 측정

    - 이상치에 덜 민감한 유사도 측정

    - 텍스트 분석에서 문서 유사도 측정

```python
import torch

x = torch.tensor([1, 0, 2], dtype=torch.float32)
y = torch.tensor([0, 1, 2], dtype=torch.float32)

# 맨해튼 거리 계산
manhattan_distance = torch.norm(x - y, p=1)

# 유사도 계산
manhattan_similarity = 1 / (1 + manhattan_distance)

print(f"Manhattan Distance: {manhattan_distance}")
# Manhattan Distance: 2.0
print(f"Manhattan Similarity: {manhattan_similarity}")
# Manhattan Similarity: 0.3333333432674408
```

### 유클리드 유사도 (Euclidean Similarity)

- 유클리드 거리(L2 norm 에 기반)를 사용한 유사도

- $$ x = [x_1,\ x_2,\ ...,\ x_n], y = [y_1,\ y_2,\ ...,\ y_n] $$ 일 때,

$$ \text{similarity}_{euclidean}(x, y) = \frac{1}{1 + \sqrt{\sum_{i=1}^n|x_i - y_i|^2}},\ 여기서\ x, y \in \mathbb{R}^n $$

- 머신러닝에서는 아래의 분야에서 사용된다.

    - K-최근접 이웃(KNN) 알고리즘

    - 클러스터링(K-means 등)

    - 추천 시스템

```python
import torch

x = torch.tensor([1, 0, 2], dtype=torch.float32)
y = torch.tensor([0, 1, 2], dtype=torch.float32)

# 유클리드 거리 계산
euclidean_distance = torch.norm(x - y, p=2)

# 유사도 계산
euclidean_similarity = 1 / (1 + euclidean_distance)

print(f"Euclidean Distance: {euclidean_distance.item()}")
# Euclidean Distance: 1.4142135381698608
print(f"Euclidean Similarity: {euclidean_similarity.item()}")
# Euclidean Similarity: 0.41421353816986084
```

### 코사인 유사도 (Cosine Similarity)

- 두 vector 간의 각도의 cos 값을 사용한 유사도

- vector 의 방향만 고려하며 크기는 무시 즉, 두 vector 사이의 각도를 측정하여 계산한 값

- 코사인 유사도의 값이 1 에 가까울 수록 두 vector 가 유사하다고 판단

<br/>

*그럼 어떻게 두 vector 사이의 각도를 측정할 수 있을까?*

⇒ 이 때 vector 의 내적(dot product 또는 inner product) 를 활용

### 벡터의 내적 (Dot Product)

- 두 vector 의 내적은, 각 성분의 곱의 합으로 정의

- $$ x = [x_1,\ x_2,\ ...,\ x_n], y = [y_1,\ y_2,\ ...,\ y_n] $$ 일 때,
- 내적에 대한 대수적 표현은 다음과 같다.

$$ x \cdot y = <x,y> = \sum_{i=1}^{n} x_i y_i,\ 여기서\ x, y \in \mathbb{R}^n $$

- 두 vector 의 내적을 구하는 두 번째 방법은,

    - 각도의 성질이 포함된 $$ \vec x $$ 에 대한 정사영을 $ \vec y $ 의 길이와 곱한 값이다.

![projection_between_two_vectors.png](/assets/img/projection_between_two_vectors.png)

<br/>

$$ Proj(x) = ||{x}||_2\cos\theta $$

$$ <x,y>=Proj(x)\times ||y||_2 = ||x||_2\cos\theta \times ||y||_2 = ||x||_2||y||_2\cos\theta $$

### 내적을 활용한 코사인 유사도의 수식 표현

- 위의 식을 활용하여 다음 수식을 도출한다.

- $$ x = [x_1,\ x_2,\ ...,\ x_n], y = [y_1,\ y_2,\ ...,\ y_n] $$ 일 때,

$$ \cos(x,y) = \frac{<x,y>}{||x||_2||y||_2} $$

- 머신러닝에서는 이 코사인 유사도를 많은 곳에서 활용한다.

- 대표적인 예로는 아래와 같은 내용이 있다.

    - 자연어 처리: 문서 간 유사도 측정

    - 추천 시스템: 사용자 선호도 분석

    - 정보 검색: 쿼리와 문서 간 관련성 평가

    - 이미지 인식: 특징 벡터 간 유사성 비교

> 💡 코사인 유사도는 벡터의 방향만 고려하고 크기는 무시하기 때문에, 텍스트 분석이나 고차원 데이터 비교에 특히 유용하다.

```python
import torch
import torch.nn.functional as F

x = torch.tensor([1, 0, 2], dtype=torch.float32)
y = torch.tensor([0, 1, 2], dtype=torch.float32)

# 코사인 유사도 계산
dot_product = torch.dot(x, y)
norm_b = torch.norm(x, p=2)
norm_c = torch.norm(y, p=2)
cosine_similarity = dot_product / (norm_b * norm_c)
print(f"Cosine Similarity: {cosine_similarity.item()}")
# Cosine Similarity: 0.800000011920929


# 함수형 API 사용
cosine_sim = F.cosine_similarity(x, y, dim=0)
print(f"Cosine Similarity (함수형): {cosine_sim.item()}")
# Cosine Similarity (함수형): 0.7999999523162842

# nn 모듈 사용
cos = torch.nn.CosineSimilarity(dim=0)
output = cos(x, y)
print(f"Cosine Similarity (nn 모듈): {output.item()}")
# Cosine Similarity (nn 모듈): 0.7999999523162842
```
