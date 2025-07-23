---
title: 🤔 왜 PyTorch 이고, PyTorch 는 어떻게 사용할까?
date: 2025-06-20 08:11:00 +0900
categories:
  - DEEP_LEARNING
  - PYTORCH
tags:
  - 급발진거북이
  - deeplearning
  - 딥러닝
  - machinelearning
  - 머신러닝
  - python
  - pytorch
  - tensor
  - torch
  - 파이썬
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- numpy==2.2.6  
- pandas==2.3.1  
- matplotlib==3.10.3  
- seaborn==0.13.2  
- tqdm==4.67.1  
- pillow==11.2.1  
- torch==2.5.1
- torchvision==0.21.0

## 🚀 TL;DR

- **딥러닝 프레임워크**는 복잡한 신경망 구현을 간소화하여 개발자가 모델 설계에 집중할 수 있게 해주는 필수 도구
- **PyTorch**는 Papers with Code 기준 2023년 가장 많이 사용되는 프레임워크로, 62%의 SOTA 모델이 PyTorch로 구현됨
- **PyTorch**는 동적 계산 그래프와 직관적인 API로 딥러닝 연구와 개발에 최적화된 프레임워크다
- **텐서(Tensor)** 는 PyTorch의 핵심 자료구조로, NumPy 배열과 유사하지만 GPU 가속과 자동 미분을 지원한다
- **Autograd**는 자동 미분 시스템으로 역전파 알고리즘을 자동으로 처리해 모델 학습을 간편하게 만든다
- **nn.Module**을 상속받아 신경망 모델을 정의하고, **DataLoader**로 효율적인 데이터 처리 파이프라인을 구축한다
- **CUDA 텐서**를 통해 GPU 연산을 투명하게 처리하며, 자동 메모리 관리와 비동기 실행으로 최적화된 성능 제공
- **torch.compile()**, **FSDP**, **DTensor** 등 최신 기능으로 대규모 모델 학습과 추론 속도를 획기적으로 개선

## 🔥 PyTorch란?

**PyTorch**는 페이스북(현 Meta)에서 개발한 오픈소스 딥러닝 프레임워크로, 연구와 프로덕션 환경 모두에서 널리 사용되고 있다.

PyTorch의 핵심 철학은 **"연구자 친화적"** 이다. 복잡한 모델도 직관적으로 구현할 수 있고, 디버깅이 쉬우며, 동적으로 네트워크를 변경할 수 있다는 장점이 있다.

```mermaid
mindmap
  root((PyTorch))
    (핵심 특징)
      [동적 계산 그래프]
        (실행 중 그래프 변경)
        (디버깅 용이)
      [파이썬다운 설계]
        (직관적 API)
        (NumPy 호환성)
      [강력한 GPU 지원]
        (CUDA 통합)
        (분산 학습)
    (주요 컴포넌트)
      [torch.Tensor]
        (기본 자료구조)
        (GPU 연산 지원)
      [torch.nn]
        (신경망 레이어)
        (손실함수)
      [torch.optim]
        (최적화 알고리즘)
        (학습률 스케줄러)
      [torch.utils.data]
        (데이터 로딩)
        (배치 처리)
    (이미지 처리)
      [torchvision]
        (전처리 도구)
        (사전학습 모델)
        (데이터셋)
```

> PyTorch는 **동적 계산 그래프(Dynamic Computation Graph)** 를 사용하여 모델을 실행하면서 그래프를 구성한다. 이는 TensorFlow 1.x의 정적 그래프와 달리 더 유연하고 직관적인 개발을 가능하게 한다.
{: .prompt-tip}


## 🎯 왜 딥러닝 프레임워크가 필요한가?

딥러닝 프레임워크의 필요성을 이해하기 위해, 요리에 비유해보자.

만약 라면을 끓이려는데 물을 끓이는 방법부터, 면을 만드는 방법, 스프를 조합하는 방법까지 모두 직접 해야 한다면? 엄청나게 복잡하고 시간이 오래 걸릴 것이다.

딥러닝도 마찬가지다. 간단한 신경망 하나를 만들려면,

1. 모든 neural network의 layer를 직접 구현
2. loss function 구현
3. 모든 layer의 weight, bias에 대해 gradient를 계산
4. 최적화 알고리즘 구현

이 모든 과정을 수작업으로 한다면 엄청난 시간과 노력이 필요하다. 더 중요한 것은, 복잡한 수학적 연산 과정에서 발생할 수 있는 오류들이다.

### 딥러닝 프레임워크가 제공하는 것

딥러닝 프레임워크는 마치 **요리 키트**와 같다. 필요한 재료와 도구를 모두 제공해주어, 우리는 레시피(모델 설계)에만 집중할 수 있다:

- **모델 구성 요소 제공**: 다양한 layer, activation function 등을 즉시 사용 가능
- **자동 미분(Automatic Differentiation)**: 복잡한 gradient 계산을 자동으로 처리
- **최적화 알고리즘**: Adam, SGD 등 다양한 optimizer 제공
- **GPU 가속**: CUDA 연산을 통한 학습 속도 향상

> 딥러닝 프레임워크는 개발자가 **모델 아키텍처 설계**와 **문제 해결**에 집중할 수 있도록 해주는 강력한 도구다.
{: .prompt-tip}

### 실무에서의 중요성

실제 취업 시장에서도 딥러닝 프레임워크 활용 능력은 필수 요구사항이 되었다. 대부분의 ML/DL 엔지니어 채용 공고에서 PyTorch나 TensorFlow 경험을 요구하고 있다.

## 🌟 딥러닝 프레임워크 트렌드

### 주요 딥러닝 프레임워크

현재 사용되는 주요 딥러닝 프레임워크들:

- **TensorFlow (Google)**: 2015년 공개, 초기 산업 표준
- **PyTorch (Meta)**: 2016년 공개, 연구자 친화적
- **JAX (Google)**: 함수형 프로그래밍 패러다임
- **MXNet (Apache)**: AWS에서 주로 사용

### PyTorch의 급성장

Papers with Code 통계에 따르면, PyTorch 사용률은 지속적으로 증가하고 있다:

```mermaid
graph LR
    A[2018년 3월] -->|PyTorch 25%| B[2023년 3월]
    B -->|PyTorch 62%| C[현재]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
```

### Why PyTorch?

PyTorch가 선호되는 이유는 다음과 같다:

**1. 강력한 커뮤니티와 생태계**

- **Hugging Face**: NLP 분야의 사실상 표준 플랫폼
- **timm**: Computer Vision을 위한 사전학습 모델 라이브러리
- **PyTorch Lightning**: 보일러플레이트 코드를 줄여주는 고수준 래퍼

**2. 직관적인 API**

- Python의 자연스러운 문법과 유사
- **동적 계산 그래프(Dynamic Computational Graph)**: 디버깅이 용이

**3. 연구와 프로덕션의 균형**

- 연구용 프로토타이핑이 쉬움
- TorchScript를 통한 프로덕션 배포 지원

> PyTorch는 **"연구자가 만든, 연구자를 위한"** 프레임워크로 시작했지만, 이제는 산업계에서도 널리 사용되는 표준이 되었다.
{: .prompt-tip}

## 🖥️ PyTorch 의 GPU 활용 메커니즘

PyTorch가 GPU를 활용하는 방식을 이해하기 위해, 택배 배송 시스템에 비유해보자.

**CPU**는 한 명의 숙련된 배송기사가 하나씩 정확하게 배송하는 것과 같다면, **GPU**는 수천 명의 배송기사가 동시에 배송하는 것과 같다. 복잡한 계산은 못하지만, 단순한 작업을 대량으로 처리하는 데 최적화되어 있다.

### CUDA 텐서와 디바이스 관리

PyTorch에서 텐서는 CPU 또는 GPU 메모리에 저장될 수 있다.

```python
import torch

# CPU 텐서 생성 (일반 창고에 보관)
cpu_tensor = torch.randn(1000, 1000)
print(f"CPU 텐서 디바이스: {cpu_tensor.device}")
# CPU 텐서 디바이스: cpu

# GPU 사용 가능 확인
if torch.cuda.is_available():
    # GPU 개수 확인 (배송 센터 개수 확인)
    gpu_count = torch.cuda.device_count()
    print(f"사용 가능한 GPU 개수: {gpu_count}")
    
    # 현재 GPU 정보
    for i in range(gpu_count):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  메모리: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
    
    # GPU로 텐서 이동 (특급 배송 센터로 이동)
    gpu_tensor = cpu_tensor.cuda()  # 또는 cpu_tensor.to('cuda')
    print(f"GPU 텐서 디바이스: {gpu_tensor.device}")
    # GPU 텐서 디바이스: cuda:0
```

### GPU 메모리 관리

GPU 메모리는 제한적이므로 효율적인 관리가 중요하다. 마치 배송 센터의 공간이 한정되어 있는 것과 같다.

```python
# GPU 메모리 모니터링
if torch.cuda.is_available():
    # 현재 메모리 사용량 (창고 사용 현황)
    allocated = torch.cuda.memory_allocated() / 1e9
    reserved = torch.cuda.memory_reserved() / 1e9
    print(f"할당된 메모리: {allocated:.2f} GB")
    print(f"예약된 메모리: {reserved:.2f} GB")
    
    # 대용량 텐서 생성 (큰 화물 입고)
    large_tensor = torch.randn(10000, 10000, device='cuda')
    
    # 메모리 사용량 재확인
    allocated_after = torch.cuda.memory_allocated() / 1e9
    print(f"텐서 생성 후 할당된 메모리: {allocated_after:.2f} GB")
    
    # 메모리 해제 (화물 출고)
    del large_tensor
    torch.cuda.empty_cache()  # 캐시된 메모리 해제
    
    # 메모리 사용량 최종 확인
    allocated_final = torch.cuda.memory_allocated() / 1e9
    print(f"메모리 해제 후: {allocated_final:.2f} GB")
```

## 📊 텐서(Tensor): PyTorch의 핵심

**텐서(Tensor)** 는 PyTorch의 가장 기본적인 자료구조로 **숫자들을 담는 다차원 상자**라고 생각하면 된다.

NumPy의 `ndarray`와 매우 유사하지만 GPU에서 연산할 수 있고 자동 미분을 지원한다는 차이점이 있다.

### 텐서의 기본 개념

텐서는 다차원 배열을 의미하며, 스칼라(0차원), 벡터(1차원), 행렬(2차원), 그리고 더 높은 차원의 데이터를 통합적으로 표현한다.

```python
import torch
import numpy as np

# 다양한 방법으로 텐서 생성
# 1. 직접 생성
tensor_direct = torch.tensor([1, 2, 3, 4])
print(f"직접 생성: {tensor_direct}")
# 출력: 직접 생성: tensor([1, 2, 3, 4])

# 2. NumPy 배열에서 변환
numpy_array = np.array([1, 2, 3, 4])
tensor_from_numpy = torch.from_numpy(numpy_array)
print(f"NumPy에서 변환: {tensor_from_numpy}")
# 출력: NumPy에서 변환: tensor([1, 2, 3, 4], dtype=torch.int64)

# 3. 특수 텐서 생성
zeros_tensor = torch.zeros(3, 4)  # 0으로 채워진 3x4 텐서
ones_tensor = torch.ones(2, 3)   # 1로 채워진 2x3 텐서
random_tensor = torch.randn(2, 3) # 정규분포 난수로 채워진 2x3 텐서

print(f"0 텐서 크기: {zeros_tensor.shape}")  
# 출력: 0 텐서 크기: torch.Size([3, 4])
print(f"난수 텐서:\n{random_tensor}")
# 출력: 난수 텐서:
# tensor([[-0.2947,  0.8459, -1.0341],
#         [ 0.5896, -0.4741,  1.0491]])
```

### 텐서의 주요 속성과 연산

```python
# 텐서의 기본 속성
tensor = torch.randn(3, 4, 5)
print(f"텐서 모양: {tensor.shape}")        # torch.Size([3, 4, 5])
print(f"텐서 차원: {tensor.dim()}")         # 3
print(f"데이터 타입: {tensor.dtype}")       # torch.float32
print(f"저장 장치: {tensor.device}")       # cpu

# 기본 연산
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

# 요소별 연산
print(f"덧셈: {a + b}")                    # tensor([5, 7, 9])
print(f"곱셈: {a * b}")                    # tensor([4, 10, 18])

# 행렬 연산
matrix_a = torch.randn(3, 4)
matrix_b = torch.randn(4, 2)
matrix_mult = torch.matmul(matrix_a, matrix_b)  # 또는 matrix_a @ matrix_b
print(f"행렬 곱셈 결과 크기: {matrix_mult.shape}")  
# 출력: 행렬 곱셈 결과 크기: torch.Size([3, 2])
```

### 텐서 기본 사용법

먼저 텐서가 무엇인지 간단한 예시로 알아보자.

```python
import torch
import numpy as np

# 1차원 텐서 (리스트와 비슷)
# 마치 일렬로 늘어선 사탕들
tensor_1d = torch.tensor([1, 2, 3, 4, 5])
print(f"1차원 텐서: {tensor_1d}")
print(f"모양(shape): {tensor_1d.shape}")  # torch.Size([5])

# 2차원 텐서 (표와 비슷)
# 마치 바둑판에 놓인 바둑돌들
tensor_2d = torch.tensor([[1, 2, 3],
                          [4, 5, 6]])
print(f"\n2차원 텐서:\n{tensor_2d}")
print(f"모양(shape): {tensor_2d.shape}")  # torch.Size([2, 3])

# 3차원 텐서 (큐브와 비슷)
# 마치 여러 층으로 쌓인 빌딩
tensor_3d = torch.tensor([[[1, 2], [3, 4]],
                          [[5, 6], [7, 8]]])
print(f"\n3차원 텐서의 모양: {tensor_3d.shape}")  # torch.Size([2, 2, 2])

# 텐서의 기본 속성들
print(f"\n텐서의 차원 수: {tensor_2d.ndim}")  # 2
print(f"텐서의 전체 원소 개수: {tensor_2d.numel()}")  # 6
print(f"텐서의 데이터 타입: {tensor_2d.dtype}")  # torch.int64
```

### 텐서의 다양한 생성 방법

텐서를 만드는 방법은 마치 요리 재료를 준비하는 것처럼 다양하다.

```python
# 1. 특정 값으로 가득 채우기
# 모든 값이 0인 텐서 (빈 그릇)
zeros = torch.zeros(3, 4)
print("영 텐서:")
print(zeros)

# 모든 값이 1인 텐서 (가득 찬 그릇)
ones = torch.ones(2, 3)
print("\n일 텐서:")
print(ones)

# 특정 값으로 채우기 (원하는 재료로 채우기)
sevens = torch.full((3, 3), 7)
print("\n7로 채운 텐서:")
print(sevens)

# 2. 랜덤 값으로 채우기 (주사위 굴리기)
# 0과 1 사이의 균등분포
random_uniform = torch.rand(2, 3)
print("\n균등분포 랜덤 텐서:")
print(random_uniform)

# 표준정규분포 (평균 0, 표준편차 1)
random_normal = torch.randn(2, 3)
print("\n정규분포 랜덤 텐서:")
print(random_normal)

# 3. 순서가 있는 숫자들
# 연속된 숫자 (계단 오르기)
sequence = torch.arange(0, 10, 2)  # 0부터 10까지 2씩 증가
print("\n순서 텐서:", sequence)
# 순서 텐서: tensor([0, 2, 4, 6, 8])

# 균등하게 나눈 숫자들 (케이크 자르기)
linspace = torch.linspace(0, 1, 5)  # 0과 1 사이를 5등분
print("균등 분할:", linspace)
# 균등 분할: tensor([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])

# 4. 다른 텐서를 참고해서 만들기 (복사하기)
original = torch.tensor([[1, 2], [3, 4]])
zeros_like_original = torch.zeros_like(original)
print("\n원본과 같은 모양의 영 텐서:")
print(zeros_like_original)
```

### 텐서 연산과 변형

텐서는 레고 블록처럼 다양하게 조작할 수 있다.

```python
# 기본 산술 연산
a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)

# 덧셈 (두 텐서의 같은 위치 원소끼리 더하기)
add_result = a + b  # 또는 torch.add(a, b)
print("덧셈 결과:")
print(add_result)

# 곱셈 (원소별 곱셈 - 같은 위치끼리 곱하기)
mul_result = a * b  # 또는 torch.mul(a, b)
print("\n원소별 곱셈:")
print(mul_result)

# 행렬 곱셈 (진짜 행렬 곱하기)
matmul_result = a @ b  # 또는 torch.matmul(a, b)
print("\n행렬 곱셈:")
print(matmul_result)

# 텐서 모양 바꾸기 (블록 재배치)
tensor = torch.arange(12)  # [0, 1, 2, ..., 11]
print("\n원본 텐서:", tensor)

# reshape: 원하는 모양으로 바꾸기
reshaped = tensor.reshape(3, 4)  # 3행 4열로
print("\nreshape(3, 4):")
print(reshaped)

# view: reshape와 비슷하지만 메모리를 공유
viewed = tensor.view(2, 6)  # 2행 6열로
print("\nview(2, 6):")
print(viewed)

# 차원 추가/제거
# unsqueeze: 차원 추가 (1층 건물을 아파트로)
expanded = reshaped.unsqueeze(0)  # 맨 앞에 차원 추가
print(f"\nunsqueeze 후 shape: {expanded.shape}")  # [1, 3, 4]

# squeeze: 크기가 1인 차원 제거 (불필요한 포장 제거)
squeezed = expanded.squeeze(0)  # 첫 번째 차원 제거
print(f"squeeze 후 shape: {squeezed.shape}")  # [3, 4]

# 전치 (행과 열 바꾸기)
transposed = reshaped.t()  # 또는 reshaped.transpose(0, 1)
print(f"\n전치 후 shape: {transposed.shape}")  # [4, 3]
```

### 텐서 인덱싱과 슬라이싱

텐서에서 원하는 부분만 꺼내는 방법은 마치 케이크를 자르는 것과 같다.

```python
# 2차원 텐서 생성
tensor = torch.tensor([[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12]])

print("원본 텐서:")
print(tensor)

# 기본 인덱싱 (특정 원소 선택)
print(f"\n첫 번째 행, 두 번째 열: {tensor[0, 1]}")  # 2

# 슬라이싱 (여러 원소 선택)
print("\n첫 두 행:")
print(tensor[:2])  # 0번째와 1번째 행

print("\n모든 행의 마지막 두 열:")
print(tensor[:, -2:])  # 모든 행의 뒤에서 2개 열

# 조건을 사용한 선택 (마스킹)
mask = tensor > 6  # 6보다 큰 원소 찾기
print("\n6보다 큰 원소들:", tensor[mask])
# 6보다 큰 원소들: tensor([ 7,  8,  9, 10, 11, 12])

# 특정 인덱스로 선택
indices = torch.tensor([0, 2])  # 0번째와 2번째 행 선택
selected_rows = tensor[indices]
print("\n선택된 행들:")
print(selected_rows)
```

### 텐서 심화 활용

이제 좀 더 고급 기능들을 살펴보자.

```python
# 브로드캐스팅 (자동 크기 맞추기)
# 마치 작은 스탬프를 큰 종이 전체에 찍는 것
matrix = torch.ones(3, 4)
vector = torch.tensor([1, 2, 3, 4])

# vector는 자동으로 모든 행에 적용됨
result = matrix + vector
print("브로드캐스팅 결과:")
print(result)

# einsum (아인슈타인 표기법)
# 복잡한 텐서 연산을 간단하게 표현
a = torch.randn(2, 3)
b = torch.randn(3, 4)

# 행렬 곱셈을 einsum으로
result = torch.einsum('ij,jk->ik', a, b)
print(f"\neinsum 행렬곱 결과 shape: {result.shape}")  # [2, 4]

# 배치 연산 (여러 데이터 동시 처리)
# 마치 여러 장의 사진을 한 번에 처리
batch_images = torch.randn(32, 3, 224, 224)  # 32장의 224x224 RGB 이미지
print(f"\n배치 이미지 shape: {batch_images.shape}")

# In-place 연산 (메모리 절약)
# 원본을 직접 수정 (주의해서 사용!)
x = torch.tensor([1, 2, 3], dtype=torch.float32)
print(f"원본: {x}")
x.add_(10)  # _ 가 붙으면 in-place 연산
print(f"In-place 덧셈 후: {x}")

# 그래디언트 추적
# 딥러닝에서 중요한 기능!
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2  # x의 제곱
y.sum().backward()  # 역전파
print(f"\nx의 그래디언트: {x.grad}")  # 2x = [2, 4, 6]
```

> 텐서는 PyTorch의 **기본 빌딩 블록**이다. 레고 블록처럼 이것들을 조합해서 복잡한 신경망을 만들 수 있다!
{: .prompt-tip}

### GPU 활용

```python
# GPU 사용 가능 여부 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 장치: {device}")

# CPU 텐서를 GPU로 이동
if torch.cuda.is_available():
    tensor_cpu = torch.randn(1000, 1000)
    tensor_gpu = tensor_cpu.to(device)  # 또는 tensor_cpu.cuda()
    print(f"GPU 텐서 장치: {tensor_gpu.device}")
    # 출력: GPU 텐서 장치: cuda:0
    
    # GPU에서 연산 수행
    result = torch.matmul(tensor_gpu, tensor_gpu.T)
    print(f"GPU 연산 결과 크기: {result.shape}")
```

> 텐서를 GPU로 이동시킬 때는 `.to(device)` 메서드를 사용하는 것이 권장된다. 이는 장치에 관계없이 일관된 코드를 작성할 수 있게 해준다.
{: .prompt-tip}

## ⚡ Autograd: 자동 미분의 마법

**Autograd**는 PyTorch의 자동 미분 시스템으로, 텐서의 모든 연산을 추적하여 자동으로 그래디언트를 계산한다. 이는 딥러닝의 핵심인 역전파(Backpropagation) 알고리즘을 자동으로 처리해준다.

### 계산 그래프와 그래디언트

```python
import torch

# requires_grad=True로 그래디언트 추적 활성화
x = torch.tensor([2.0], requires_grad=True)
y = torch.tensor([3.0], requires_grad=True)

# 순전파 계산
z = x * y + x**2
loss = z.sum()

print(f"x: {x}")           # tensor([2.], requires_grad=True)
print(f"y: {y}")           # tensor([3.], requires_grad=True)
print(f"z: {z}")           # tensor([10.], grad_fn=<AddBackward0>)
print(f"loss: {loss}")     # tensor(10., grad_fn=<SumBackward0>)

# 역전파 수행
loss.backward()

# 그래디언트 확인
print(f"x의 그래디언트: {x.grad}")  # tensor([7.]) = dy/dx = y + 2*x = 3 + 2*2
print(f"y의 그래디언트: {y.grad}")  # tensor([2.]) = dy/dy = x = 2
```

### 실제 신경망에서의 활용

```python
import torch
import torch.nn as nn

# 간단한 선형 회귀 예제
# 데이터 준비
x_data = torch.randn(100, 1)
y_data = 3 * x_data + 2 + torch.randn(100, 1) * 0.1  # y = 3x + 2 + noise

# 모델 정의
model = nn.Linear(1, 1)  # 입력 1개, 출력 1개
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 학습 과정
for epoch in range(100):
    # 순전파
    y_pred = model(x_data)
    loss = criterion(y_pred, y_data)
    
    # 역전파
    optimizer.zero_grad()  # 그래디언트 초기화
    loss.backward()        # 그래디언트 계산
    optimizer.step()       # 파라미터 업데이트
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# 학습된 파라미터 확인
print(f"학습된 가중치: {model.weight.item():.4f}")  # 약 3에 가까운 값
print(f"학습된 편향: {model.bias.item():.4f}")     # 약 2에 가까운 값
```

> `optimizer.zero_grad()`는 매우 중요하다. PyTorch는 기본적으로 그래디언트를 누적하므로, 각 배치마다 그래디언트를 초기화해야 올바른 학습이 가능하다.
{: .prompt-warning}

## 🧠 torch.nn: 신경망 구축의 핵심

**torch.nn** 모듈은 신경망 레이어, 활성화 함수, 손실 함수 등 딥러닝 모델 구축에 필요한 모든 구성 요소를 제공한다.

### nn.Module: 모든 모델의 기반

모든 PyTorch 모델은 `nn.Module`을 상속받아 구현한다. 이는 파라미터 관리, GPU 이동, 저장/로딩 등의 기능을 자동으로 제공한다.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# 모델 인스턴스 생성
model = SimpleNet(input_size=784, hidden_size=128, output_size=10)

# 모델 정보 확인
print(f"모델 구조:\n{model}")
print(f"전체 파라미터 수: {sum(p.numel() for p in model.parameters())}")
# 출력: 전체 파라미터 수: 101770

# 순전파 테스트
sample_input = torch.randn(32, 784)  # 배치 크기 32, 입력 차원 784
output = model(sample_input)
print(f"출력 크기: {output.shape}")  # torch.Size([32, 10])
```

### 주요 레이어와 활성화 함수

```python
# 다양한 레이어 예시
conv_layer = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=1)
pool_layer = nn.MaxPool2d(kernel_size=2, stride=2)
batch_norm = nn.BatchNorm2d(64)
linear_layer = nn.Linear(512, 256)

# 활성화 함수
relu = nn.ReLU()
sigmoid = nn.Sigmoid()
tanh = nn.Tanh()
leaky_relu = nn.LeakyReLU(0.2)

# 정규화 레이어
dropout = nn.Dropout(0.5)
layer_norm = nn.LayerNorm(256)

# 손실 함수
mse_loss = nn.MSELoss()                    # 회귀용
cross_entropy = nn.CrossEntropyLoss()      # 분류용
bce_loss = nn.BCEWithLogitsLoss()          # 이진 분류용

print("주요 컴포넌트들이 성공적으로 생성되었습니다.")
```

### Sequential 을 활용한 간단한 모델 정의

```python
# Sequential을 사용한 간단한 모델 정의
simple_model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 10)
)

print(f"Sequential 모델:\n{simple_model}")

# 파라미터 확인
for name, param in simple_model.named_parameters():
    print(f"{name}: {param.shape}")
# 출력 예시:
# 0.weight: torch.Size([256, 784])
# 0.bias: torch.Size([256])
# 3.weight: torch.Size([128, 256])
# ...
```

## 🎯 torch.optim: 최적화의 핵심

**torch.optim** 모듈은 다양한 최적화 알고리즘을 제공하여 모델의 파라미터를 효율적으로 업데이트한다.

### 주요 최적화 알고리즘

```python
import torch.optim as optim

# 모델 정의 (앞서 정의한 SimpleNet 사용)
model = SimpleNet(784, 128, 10)

# 다양한 최적화 알고리즘
sgd_optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
adam_optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
rmsprop_optimizer = optim.RMSprop(model.parameters(), lr=0.01)
adamw_optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

print("다양한 최적화 알고리즘이 준비되었습니다.")

# 학습률 스케줄러
scheduler = optim.lr_scheduler.StepLR(adam_optimizer, step_size=10, gamma=0.1)
cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(adam_optimizer, T_max=50)

# 학습률 변화 확인
for epoch in range(5):
    print(f"Epoch {epoch}: 학습률 = {adam_optimizer.param_groups[0]['lr']:.6f}")
    scheduler.step()
# 출력:
# Epoch 0: 학습률 = 0.001000
# Epoch 1: 학습률 = 0.001000
# ...
```

## 📁 torch.utils.data: 효율적인 데이터 처리

**torch.utils.data** 모듈은 대용량 데이터를 효율적으로 처리하기 위한 도구들을 제공한다.

### Dataset 과 DataLoader

```python
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

# 커스텀 데이터셋 정의
class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        
        if self.transform:
            sample = self.transform(sample)
            
        return sample, label

# 예시 데이터 생성
data = np.random.randn(1000, 784)
labels = np.random.randint(0, 10, 1000)

# 데이터셋과 데이터로더 생성
dataset = CustomDataset(data, labels)
dataloader = DataLoader(
    dataset, 
    batch_size=32, 
    shuffle=True, 
    num_workers=2,  # 멀티프로세싱
    pin_memory=True  # GPU 사용 시 성능 향상
)

print(f"데이터셋 크기: {len(dataset)}")
print(f"배치 수: {len(dataloader)}")

# 데이터로더 사용 예시
for batch_idx, (data, target) in enumerate(dataloader):
    print(f"배치 {batch_idx}: 데이터 크기 {data.shape}, 레이블 크기 {target.shape}")
    if batch_idx >= 2:  # 처음 3개 배치만 확인
        break
# 출력:
# 배치 0: 데이터 크기 torch.Size([32, 784]), 레이블 크기 torch.Size([32])
# 배치 1: 데이터 크기 torch.Size([32, 784]), 레이블 크기 torch.Size([32])
# 배치 2: 데이터 크기 torch.Size([32, 784]), 레이블 크기 torch.Size([32])
```

## 📦 PyTorch Dataset 구현 가이드

PyTorch의 `torch.utils.data.Dataset`을 상속받아 커스텀 데이터셋을 만들 때 **반드시 구현해야 하는 함수**는 다음 2개다.

#### `__len__` 메서드

```python
from typing import Any, Optional, Callable, Tuple, Union, List
import torch
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __len__(self) -> int:
        """
        데이터셋의 전체 크기를 반환
        
        Returns:
            int: 데이터셋에 포함된 샘플의 총 개수
        """
        pass  # 구현 필요
```

#### `__getitem__` 메서드

```python
def __getitem__(self, index: int) -> Any:
    """
    주어진 인덱스에 해당하는 데이터 샘플을 반환
    
    Args:
        index (int): 가져올 데이터의 인덱스 (0 <= index < len(dataset))
        
    Returns:
        Any: 보통 (data, label) 튜플 형태이지만, 용도에 따라 다양한 형태 가능
        
    Raises:
        IndexError: 인덱스가 범위를 벗어날 때
    """
    pass  # 구현 필요
```

### 자주 구현되는 부가적인 함수들

#### `__init__` 생성자

```python
def __init__(
    self, 
    data_path: str,
    transform: Optional[Callable] = None,
    target_transform: Optional[Callable] = None,
    **kwargs
) -> None:
    """
    데이터셋 초기화
    
    Args:
        data_path (str): 데이터가 저장된 경로
        transform (Optional[Callable]): 입력 데이터에 적용할 변환
        target_transform (Optional[Callable]): 레이블에 적용할 변환
        **kwargs: 기타 설정 파라미터
    """
    super().__init__()
    self.data_path = data_path
    self.transform = transform
    self.target_transform = target_transform
    # 데이터 로딩 및 초기화 로직
```

#### `__repr__` 메서드

```python
def __repr__(self) -> str:
    """
    데이터셋의 문자열 표현을 반환 (디버깅용)
    
    Returns:
        str: 데이터셋 정보를 포함한 문자열
    """
    head = "Dataset " + self.__class__.__name__
    body = [f"Number of datapoints: {self.__len__()}"]
    if hasattr(self, 'data_path'):
        body.append(f"Root location: {self.data_path}")
    body += [f"Transforms: {self.transform}"]
    body += [f"Target transforms: {self.target_transform}"]
    
    lines = [head] + [" " * 4 + line for line in body]
    return '\n'.join(lines)
```

#### 클래스 정보 관련 메서드들

```python
def get_classes(self) -> List[str]:
    """
    데이터셋의 클래스 이름 목록을 반환
    
    Returns:
        List[str]: 클래스 이름들의 리스트
    """
    pass

def get_class_to_idx(self) -> dict:
    """
    클래스 이름을 인덱스로 매핑하는 딕셔너리 반환
    
    Returns:
        dict: {클래스_이름: 인덱스} 형태의 딕셔너리
    """
    pass

@property
def num_classes(self) -> int:
    """
    클래스의 총 개수를 반환
    
    Returns:
        int: 클래스 개수
    """
    return len(self.get_classes())
```

#### 데이터 분할 관련 메서드들

```python
def split_dataset(
    self, 
    train_ratio: float = 0.8, 
    random_seed: Optional[int] = None
) -> Tuple['CustomDataset', 'CustomDataset']:
    """
    데이터셋을 훈련용과 검증용으로 분할
    
    Args:
        train_ratio (float): 훈련 데이터 비율 (0.0 ~ 1.0)
        random_seed (Optional[int]): 랜덤 시드
        
    Returns:
        Tuple[CustomDataset, CustomDataset]: (훈련용, 검증용) 데이터셋
    """
    pass

def get_subset(self, indices: List[int]) -> 'CustomDataset':
    """
    주어진 인덱스들에 해당하는 서브셋 반환
    
    Args:
        indices (List[int]): 추출할 인덱스들의 리스트
        
    Returns:
        CustomDataset: 서브셋 데이터셋
    """
    pass
```

#### 통계 정보 메서드들

```python
def get_sample_weights(self) -> torch.Tensor:
    """
    클래스 불균형 해결을 위한 샘플 가중치 반환
    
    Returns:
        torch.Tensor: 각 샘플의 가중치
    """
    pass

def compute_mean_std(self) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    데이터셋의 평균과 표준편차 계산 (정규화용)
    
    Returns:
        Tuple[torch.Tensor, torch.Tensor]: (평균, 표준편차)
    """
    pass

def get_label_distribution(self) -> dict:
    """
    각 클래스별 샘플 개수 반환
    
    Returns:
        dict: {클래스_인덱스: 샘플_개수} 딕셔너리
    """
    pass
```

## 🖼️ 이미지 데이터 처리: torchvision의 활용

**torchvision** 은 컴퓨터 비전 작업을 위한 도구들을 제공하는 PyTorch의 확장 패키지다. 이미지 전처리, 데이터 증강, 사전 훈련된 모델 등을 포함한다.

### 이미지 전처리와 데이터 증강

```python
import torchvision.transforms as transforms
from torchvision import datasets
from PIL import Image
import matplotlib.pyplot as plt

# 기본 전처리 파이프라인
basic_transform = transforms.Compose([
    transforms.Resize((224, 224)),          # 크기 조정
    transforms.ToTensor(),                  # PIL Image를 텐서로 변환
    transforms.Normalize(                   # 정규화
        mean=[0.485, 0.456, 0.406],        # ImageNet 평균
        std=[0.229, 0.224, 0.225]          # ImageNet 표준편차
    )
])

# 데이터 증강을 포함한 전처리 (훈련용)
train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),             # 랜덤 크롭
    transforms.RandomHorizontalFlip(p=0.5), # 50% 확률로 좌우 반전
    transforms.RandomRotation(10),          # ±10도 랜덤 회전
    transforms.ColorJitter(                 # 색상 변화
        brightness=0.2, 
        contrast=0.2, 
        saturation=0.2, 
        hue=0.1
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 테스트용 전처리 (증강 없음)
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

print("이미지 전처리 파이프라인이 준비되었습니다.")
```

### 내장 데이터셋 활용

```python
from torchvision import datasets
import os

# 데이터 저장 경로
data_dir = './data'

# CIFAR-10 데이터셋 로딩
train_dataset = datasets.CIFAR10(
    root=data_dir,
    train=True,
    download=True,
    transform=train_transform
)

test_dataset = datasets.CIFAR10(
    root=data_dir,
    train=False,
    download=False,
    transform=test_transform
)

# 데이터로더 생성
train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=64,
    shuffle=False,
    num_workers=4,
    pin_memory=True
)

print(f"훈련 데이터: {len(train_dataset)}개")
print(f"테스트 데이터: {len(test_dataset)}개")
print(f"클래스 수: {len(train_dataset.classes)}")
print(f"클래스 이름: {train_dataset.classes}")

# 샘플 데이터 확인
sample_data, sample_label = train_dataset[0]
print(f"샘플 이미지 크기: {sample_data.shape}")
print(f"샘플 레이블: {sample_label} ({train_dataset.classes[sample_label]})")
```

## 🏗️ PyTorch로 실제 모델 구현하기

이제 실제로 간단한 신경망을 만들어보자. 먼저 **다층 퍼셉트론(MLP)** 을 의사코드부터 시작해서 단계별로 구현해보겠다.

### MLP 의사코드로 이해하기

MLP는 마치 **결정을 내리는 과정**과 같다. 여러 정보(입력)를 받아서, 중간에 여러 단계의 판단을 거쳐, 최종 결정(출력)을 내린다.

```
# MLP 의사코드
함수 MLP(입력_데이터):
    # 첫 번째 판단 단계
    중간결과1 = 선형변환1(입력_데이터)
    활성화1 = 활성화함수(중간결과1)
    
    # 두 번째 판단 단계
    중간결과2 = 선형변환2(활성화1)
    활성화2 = 활성화함수(중간결과2)
    
    # 최종 결정
    최종결과 = 선형변환3(활성화2)
    
    반환 최종결과

# 학습 과정
반복 (에폭 수만큼):
    데이터_배치마다:
        1. 예측 = MLP(입력)
        2. 오차 = 손실함수(예측, 정답)
        3. 그래디언트 = 오차의_미분값_계산()
        4. 가중치_업데이트(그래디언트)
```

### PyTorch로 MLP 구현하기

이제 위의 의사코드를 실제 PyTorch 코드로 구현해보자.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# 간단한 MLP 모델 정의
class SimpleMLP(nn.Module):
    """
    다층 퍼셉트론 (Multi-Layer Perceptron)
    마치 여러 단계의 필터를 거쳐 결정을 내리는 것과 같다
    """
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleMLP, self).__init__()
        
        # 레이어 정의 (레고 블록 준비)
        self.layer1 = nn.Linear(input_size, hidden_size)    # 첫 번째 판단 단계
        self.layer2 = nn.Linear(hidden_size, hidden_size)   # 두 번째 판단 단계
        self.layer3 = nn.Linear(hidden_size, output_size)   # 최종 결정 단계
        
        # Dropout (과적합 방지 - 일부러 일부 연결을 끊기)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        """
        순전파 과정 (입력에서 출력까지의 흐름)
        """
        # 첫 번째 단계: 입력 → 첫 번째 은닉층
        x = self.layer1(x)
        x = F.relu(x)  # ReLU 활성화 함수 (음수는 0으로)
        x = self.dropout(x)
        
        # 두 번째 단계: 첫 번째 은닉층 → 두 번째 은닉층
        x = self.layer2(x)
        x = F.relu(x)
        x = self.dropout(x)
        
        # 최종 단계: 두 번째 은닉층 → 출력
        x = self.layer3(x)
        
        return x

# 모델 생성 예시
input_size = 784   # 28x28 이미지를 펼친 크기 (MNIST)
hidden_size = 128  # 은닉층 크기
output_size = 10   # 0~9 숫자 분류

model = SimpleMLP(input_size, hidden_size, output_size)
print("모델 구조:")
print(model)

# 모델의 파라미터 개수 확인
total_params = sum(p.numel() for p in model.parameters())
print(f"\n총 파라미터 개수: {total_params:,}")
```

### 모델 학습 과정 구현

이제 모델을 학습시켜보자. 학습은 마치 **선생님이 학생에게 문제를 내고 답을 확인하며 가르치는 과정**과 같다.

```python
# 간단한 학습 함수
def train_model(model, train_loader, num_epochs=10, learning_rate=0.001):
    """
    모델 학습 함수
    
    Args:
        model: 학습할 모델
        train_loader: 학습 데이터
        num_epochs: 전체 데이터를 몇 번 반복할지
        learning_rate: 한 번에 얼마나 크게 수정할지
    """
    # 최적화기 (가중치를 어떻게 업데이트할지 결정)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # 손실 함수 (예측이 얼마나 틀렸는지 측정)
    criterion = nn.CrossEntropyLoss()
    
    # 학습 시작
    model.train()  # 학습 모드로 전환
    
    for epoch in range(num_epochs):
        total_loss = 0.0
        correct = 0
        total = 0
        
        # 배치 단위로 학습
        for batch_idx, (data, target) in enumerate(train_loader):
            # 1. 이전 그래디언트 초기화 (칠판 지우기)
            optimizer.zero_grad()
            
            # 2. 순전파: 예측하기
            output = model(data)
            
            # 3. 손실 계산: 얼마나 틀렸는지 확인
            loss = criterion(output, target)
            
            # 4. 역전파: 어떻게 고쳐야 할지 계산
            loss.backward()
            
            # 5. 가중치 업데이트: 실제로 수정하기
            optimizer.step()
            
            # 통계 기록
            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # 진행 상황 출력 (100 배치마다)
            if batch_idx % 100 == 0:
                print(f'에폭 [{epoch+1}/{num_epochs}] '
                      f'배치 [{batch_idx}/{len(train_loader)}] '
                      f'손실: {loss.item():.4f}')
        
        # 에폭별 결과 출력
        avg_loss = total_loss / len(train_loader)
        accuracy = 100. * correct / total
        print(f'에폭 {epoch+1} 완료 - 평균 손실: {avg_loss:.4f}, 정확도: {accuracy:.2f}%\n')

# 예시: 가상의 데이터로 학습
# 실제로는 DataLoader를 사용해서 데이터를 준비
from torch.utils.data import TensorDataset, DataLoader

# 가상의 데이터 생성
X_train = torch.randn(1000, 784)  # 1000개의 784차원 데이터
y_train = torch.randint(0, 10, (1000,))  # 1000개의 레이블 (0~9)

# 데이터셋과 데이터로더 생성
dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# 학습 실행
# train_model(model, train_loader, num_epochs=5)
```

### 모델 평가하기

학습한 모델이 잘 작동하는지 확인해보자.

```python
def evaluate_model(model, test_loader):
    """
    모델 평가 함수
    """
    model.eval()  # 평가 모드로 전환 (dropout 등 비활성화)
    correct = 0
    total = 0
    
    # 그래디언트 계산 비활성화 (평가할 때는 불필요)
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
    
    accuracy = 100. * correct / total
    print(f'테스트 정확도: {accuracy:.2f}%')
    return accuracy

# 예시: 테스트 데이터로 평가
X_test = torch.randn(200, 784)
y_test = torch.randint(0, 10, (200,))
test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=32)

# evaluate_model(model, test_loader)
```

### 커스텀 레이어 만들기

때로는 특별한 기능이 필요할 때가 있다. 직접 레이어를 만들어보자.

```python
class CustomAttentionLayer(nn.Module):
    """
    간단한 어텐션 레이어
    중요한 부분에 더 집중하는 기능
    """
    def __init__(self, input_dim):
        super().__init__()
        self.attention_weights = nn.Linear(input_dim, 1)
        
    def forward(self, x):
        # 각 위치의 중요도 계산
        scores = self.attention_weights(x)
        
        # 소프트맥스로 확률로 변환
        attention = F.softmax(scores, dim=1)
        
        # 중요도를 반영하여 가중 평균
        weighted = x * attention
        
        return weighted, attention

# 커스텀 레이어를 포함한 모델
class ModelWithAttention(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.attention = CustomAttentionLayer(input_size)
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # 어텐션 적용
        x, attention_weights = self.attention(x)
        
        # 일반적인 순전파
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x, attention_weights

# 사용 예시
model_with_attention = ModelWithAttention(784, 128, 10)
sample_input = torch.randn(32, 784)
output, attention = model_with_attention(sample_input)
print(f"출력 shape: {output.shape}")
print(f"어텐션 가중치 shape: {attention.shape}")
```

> PyTorch로 모델을 만드는 것은 **레고 블록을 조립하는 것**과 같다. 기본 블록(레이어)들을 조합해서 원하는 구조를 만들 수 있다!
{: .prompt-tip}

## 🏗️ CNN 모델 구현: 이미지 분류의 핵심

**합성곱 신경망(Convolutional Neural Network, CNN)** 은 이미지 데이터 처리에 특화된 딥러닝 아키텍처다.

### 기본 CNN 모델 구현

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BasicCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(BasicCNN, self).__init__()
        
        # 합성곱 레이어들
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)   # 32x32x3 -> 32x32x32
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # 32x32x32 -> 32x32x64
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1) # 16x16x64 -> 16x16x128
        
        # 배치 정규화
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        
        # 풀링 레이어
        self.pool = nn.MaxPool2d(2, 2)  # 크기를 절반으로 축소
        
        # 완전연결 레이어들
        self.fc1 = nn.Linear(128 * 8 * 8, 512)  # 8x8x128 = 8192
        self.fc2 = nn.Linear(512, num_classes)
        
        # 드롭아웃
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        # 첫 번째 합성곱 블록
        x = self.pool(F.relu(self.bn1(self.conv1(x))))  # 32x32x32 -> 16x16x32
        
        # 두 번째 합성곱 블록  
        x = self.pool(F.relu(self.bn2(self.conv2(x))))  # 16x16x64 -> 8x8x64
        
        # 세 번째 합성곱 블록
        x = F.relu(self.bn3(self.conv3(x)))             # 8x8x128
        
        # 평탄화 (Flatten)
        x = x.view(x.size(0), -1)  # (batch_size, 8*8*128)
        
        # 완전연결 레이어들
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

# 모델 생성 및 정보 확인
model = BasicCNN(num_classes=10)
print(f"모델 구조:\n{model}")

# 파라미터 수 계산
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"전체 파라미터 수: {total_params:,}")
print(f"훈련 가능한 파라미터 수: {trainable_params:,}")

# 순전파 테스트
sample_input = torch.randn(4, 3, 32, 32)  # CIFAR-10 크기
output = model(sample_input)
print(f"입력 크기: {sample_input.shape}")
print(f"출력 크기: {output.shape}")
```

### 고급 CNN 아키텍처: ResNet 스타일 블록

```python
class ResidualBlock(nn.Module):
    """ResNet의 기본 블록"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels, out_channels, 
                              kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, 
                              kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # 스킵 연결을 위한 다운샘플링
        self.downsample = None
        if stride != 1 or in_channels != out_channels:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 
                         kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = x
        
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out += identity  # 스킵 연결
        out = F.relu(out)
        
        return out

class ResNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet, self).__init__()
        
        self.in_channels = 64
        
        # 초기 합성곱 레이어
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        # ResNet 블록들
        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        
        # 전역 평균 풀링과 분류기
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)
        
    def _make_layer(self, out_channels, num_blocks, stride):
        layers = []
        layers.append(ResidualBlock(self.in_channels, out_channels, stride))
        self.in_channels = out_channels
        
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
            
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        
        x = self.layer1(x)
        x = self.layer2(x)  
        x = self.layer3(x)
        
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        return x

# ResNet 모델 생성
resnet_model = ResNet(num_classes=10)
print(f"ResNet 파라미터 수: {sum(p.numel() for p in resnet_model.parameters()):,}")
```

## 🚀 최신 PyTorch 트렌드

### torch.compile() - PyTorch 2.0의 게임체인저

PyTorch 2.0에서 도입된 `torch.compile()`은 모델을 자동으로 최적화한다. 마치 **터보 엔진**을 달아주는 것과 같다:

```python
import torch
import time

# 모델 정의
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        return self.layers(x)

# 일반 모델과 컴파일된 모델 비교
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SimpleModel().to(device)
compiled_model = torch.compile(model)  # 모델 컴파일 (터보 모드!)

# 성능 비교
x = torch.randn(1000, 784).to(device)

# Warmup (엔진 예열)
for _ in range(10):
    _ = model(x)
    _ = compiled_model(x)

# 일반 모델 속도 측정
torch.cuda.synchronize()
start = time.time()
for _ in range(100):
    _ = model(x)
torch.cuda.synchronize()
normal_time = time.time() - start

# 컴파일된 모델 속도 측정
torch.cuda.synchronize()
start = time.time()
for _ in range(100):
    _ = compiled_model(x)
torch.cuda.synchronize()
compiled_time = time.time() - start

print(f"일반 모델: {normal_time:.4f}초")
print(f"컴파일된 모델: {compiled_time:.4f}초")
print(f"속도 향상: {normal_time/compiled_time:.2f}x")
```

### TorchScript - 프로덕션 배포

TorchScript는 PyTorch 모델을 Python 없이도 실행할 수 있게 만든다. 마치 **포장해서 배송 준비**를 하는 것과 같다.

```python
# 모델을 TorchScript로 변환
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(64 * 31 * 31, 10)
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 모델 인스턴스 생성
model = MyModel()
model.eval()

# 예시 입력
example_input = torch.randn(1, 3, 64, 64)

# Tracing (모델의 실행 경로를 기록)
traced_model = torch.jit.trace(model, example_input)

# 저장 (배송 준비 완료!)
traced_model.save("traced_model.pt")

# 나중에 로드해서 사용
loaded_model = torch.jit.load("traced_model.pt")
output = loaded_model(example_input)
```

## 🎨 PyTorch 생태계와 확장

### PyTorch Lightning - 연구 코드 구조화

PyTorch Lightning은 코드를 깔끔하게 정리해주는 **정리 도우미**와 같다.

```python
import pytorch_lightning as pl

class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = SimpleMLP(784, 128, 10)
        
    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('train_loss', loss)  # 자동으로 기록
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

# 학습은 이렇게 간단하게!
trainer = pl.Trainer(max_epochs=10)
trainer.fit(model, train_dataloader)
```
