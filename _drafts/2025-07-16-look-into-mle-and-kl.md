---
title: "이미지 생성모델의 핵심: 최대 가능도 추정(MLE)과 KL Divergence"
date: 2025-07-16 18:19:00 +0900
categories: 
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- numpy==1.26.4
- matplotlib==3.10.1
- scipy==1.15.2
- torch==2.6.0
- torchvision==0.21.0
- seaborn==0.13.2

## 🚀 TL;DR

- **최대 가능도 추정(MLE)** 은 관측된 데이터가 나올 확률을 최대화하는 모델 파라미터를 찾는 기법으로, 생성모델 학습의 핵심 원리다
- **KL Divergence** 는 두 확률분포 간의 차이를 측정하는 지표로, 생성분포와 실제분포 간의 거리를 최소화할 때 사용된다
- **VAE** 는 KL Divergence를 정규화 항으로 사용하여 잠재공간을 제약하고, ELBO(Evidence Lower BOund)를 최대화한다
- **GAN** 은 판별자가 MLE 기반으로 학습하고, 생성자는 Jensen-Shannon Divergence(KL Divergence의 확장)를 최소화한다
- **Diffusion Model** 은 forward process와 reverse process 모두에서 KL Divergence를 활용하여 노이즈 제거 과정을 학습한다
- 두 개념 모두 **정보이론** 에서 출발하여 현대 생성모델의 수학적 기반을 제공하며, 실제 구현에서는 다양한 형태로 변형되어 사용된다

## 📓 실습 Jupyter Notebook

- [Maximum Likelihood Estimation & KL Divergence in Generative Models](https://github.com/yuiyeong/notebooks/blob/main/deep_learning/mle_kl_divergence_generative_models.ipynb)

## 🎯 최대 가능도 추정(Maximum Likelihood Estimation, MLE)이란?

**최대 가능도 추정(MLE)** 은 주어진 데이터가 특정 확률분포에서 나왔다고 가정할 때, 그 데이터가 나올 확률을 최대화하는 분포의 파라미터를 찾는 통계학적 방법이다.

쉽게 말해, "내가 관측한 데이터가 가장 그럴듯하게 나올 수 있는 모델의 설정값은 무엇일까?"라는 질문에 답하는 기법이다.

예를 들어, 동전을 10번 던져서 앞면이 7번 나왔다면, 이 동전의 앞면이 나올 확률 p는 얼마일까? MLE는 이 질문에 "관측된 결과가 가장 일어날 가능성이 높은 p값을 찾자"라고 접근한다.

### 언어적 표현

MLE의 핵심 아이디어는 다음과 같다:

- **가능도(Likelihood)**: 특정 파라미터 θ가 주어졌을 때, 관측된 데이터 X가 나올 확률
- **최대 가능도**: 가능한 모든 θ 중에서 가능도를 최대화하는 θ를 선택
- **객관적 추정**: 데이터에만 의존하여 파라미터를 추정하는 객관적 방법

[MLE 개념도: 동전 던지기 예시에서 앞면 확률 p에 따른 likelihood 곡선 그래프]

### 수학적 표현

주어진 데이터 $$X = {x_1, x_2, ..., x_n}$$과 파라미터 $$\theta$$를 가진 확률분포에 대해:

**가능도 함수(Likelihood Function)**:

$$ L(\theta) = P(X|\theta) = \prod_{i=1}^{n} P(x_i|\theta) $$

**로그 가능도 함수(Log-Likelihood Function)**:

$$ \ell(\theta) = \log L(\theta) = \sum_{i=1}^{n} \log P(x_i|\theta) $$

**MLE 추정량**:

$$ \hat{\theta}_{MLE} = \arg\max_{\theta} \ell(\theta) $$

> 로그 가능도를 사용하는 이유는 곱셈을 덧셈으로 변환하여 계산을 단순화하고, 수치적 안정성을 확보하기 때문이다. 로그는 단조증가 함수이므로 최대값의 위치는 변하지 않는다. {: .prompt-tip}

### 직관적 이해를 위한 예시

동전 던지기 예시를 통해 MLE를 이해해보자:

- 동전을 10번 던져서 앞면이 7번 나왔다
- 앞면이 나올 확률을 p라고 하자
- 이항분포를 따른다고 가정: $$P(k|n,p) = \binom{n}{k}p^k(1-p)^{n-k}$$

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# 동전 던지기 MLE 예시
n_trials = 10
n_heads = 7

# p 값의 범위
p_values = np.linspace(0.01, 0.99, 100)

# 각 p에 대한 likelihood 계산
likelihoods = [binom.pmf(n_heads, n_trials, p) for p in p_values]

# MLE 추정값 (이론적으로는 7/10 = 0.7)
mle_estimate = n_heads / n_trials

plt.figure(figsize=(10, 6))
plt.plot(p_values, likelihoods, 'b-', linewidth=2, label='Likelihood')
plt.axvline(mle_estimate, color='r', linestyle='--', linewidth=2, 
           label=f'MLE estimate: p = {mle_estimate:.1f}')
plt.xlabel('p (앞면이 나올 확률)')
plt.ylabel('Likelihood')
plt.title('동전 던지기 MLE: 10번 중 7번 앞면')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"MLE 추정값: p = {mle_estimate:.3f}")
print(f"최대 likelihood: {max(likelihoods):.6f}")
```

### 생성모델에서 MLE의 역할

생성모델에서 MLE는 다음과 같이 활용된다:

- **데이터 분포 학습**: 실제 데이터 분포 $$p_{data}(x)$$를 모방하는 모델 분포 $$p_{model}(x;\theta)$$의 파라미터 θ를 학습
- **손실 함수 설계**: Negative Log-Likelihood를 손실 함수로 사용
- **생성 품질 평가**: 학습된 모델이 실제 데이터를 얼마나 잘 설명하는지 평가

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 간단한 가우시안 분포 MLE 예시
class GaussianModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 평균과 로그 분산을 학습 가능한 파라미터로 설정
        self.mean = nn.Parameter(torch.tensor(0.0))
        self.log_var = nn.Parameter(torch.tensor(0.0))
    
    def forward(self, x):
        # 가우시안 분포의 로그 확률밀도 계산
        var = torch.exp(self.log_var)
        log_prob = -0.5 * torch.log(2 * torch.pi * var) - 0.5 * (x - self.mean)**2 / var
        return log_prob
    
    def sample(self, n_samples):
        # 학습된 분포에서 샘플링
        std = torch.sqrt(torch.exp(self.log_var))
        return torch.normal(self.mean, std, (n_samples,))

# 실제 데이터 생성 (평균=2, 표준편차=1.5인 가우시안)
true_mean, true_std = 2.0, 1.5
real_data = torch.normal(true_mean, true_std, (1000,))

# 모델 초기화 및 옵티마이저 설정
model = GaussianModel()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# MLE 학습
for epoch in range(1000):
    optimizer.zero_grad()
    
    # Negative Log-Likelihood 계산 (손실 함수)
    log_probs = model(real_data)
    nll_loss = -torch.mean(log_probs)  # Negative Log-Likelihood
    
    nll_loss.backward()
    optimizer.step()
    
    if epoch % 200 == 0:
        print(f"Epoch {epoch}, NLL Loss: {nll_loss.item():.4f}")

# 학습 결과
learned_mean = model.mean.item()
learned_std = torch.sqrt(torch.exp(model.log_var)).item()

print(f"\n실제 파라미터: 평균={true_mean:.2f}, 표준편차={true_std:.2f}")
print(f"학습된 파라미터: 평균={learned_mean:.2f}, 표준편차={learned_std:.2f}")
```

## 📐 KL Divergence(쿨백-라이블러 발산)란?

**KL Divergence** 는 두 확률분포 간의 차이를 측정하는 정보이론적 지표이다. "한 분포를 다른 분포로 근사할 때 발생하는 정보 손실량"으로 해석할 수 있다.

KL Divergence는 **비대칭적** 이며, 항상 0 이상의 값을 가진다. 두 분포가 동일할 때만 0이 되고, 다를수록 큰 값을 가진다.

[KL Divergence 개념도: 두 가우시안 분포 간의 KL Divergence 시각화]

### 언어적 표현

KL Divergence의 직관적 의미:

- **정보 이론적 해석**: 분포 P 대신 분포 Q를 사용할 때 추가로 필요한 정보량
- **압축 관점**: P로 인코딩된 메시지를 Q로 디코딩할 때의 비효율성
- **확률적 해석**: P에서 생성된 데이터를 Q로 설명할 때의 부정확성

### 수학적 표현

**이산 확률분포**에 대한 KL Divergence:

$$ D_{KL}(P||Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)} $$

**연속 확률분포**에 대한 KL Divergence:

$$ D_{KL}(P||Q) = \int P(x) \log \frac{P(x)}{Q(x)} dx $$

**기댓값으로 표현**:

$$ D_{KL}(P||Q) = \mathbb{E}_{x \sim P} \left[ \log \frac{P(x)}{Q(x)} \right] $$

**엔트로피 관점**:

$$ D_{KL}(P||Q) = \mathbb{E}_{x \sim P}[-\log Q(x)] - \mathbb{E}_{x \sim P}[-\log P(x)] = H(P,Q) - H(P) $$

여기서 $$H(P,Q)$$는 교차 엔트로피(Cross Entropy), $$H(P)$$는 P의 엔트로피이다.

> KL Divergence의 핵심 성질: 비대칭성 $$D_{KL}(P||Q) \neq D_{KL}(Q||P)$$, 비음성 $$D_{KL}(P||Q) \geq 0$$, P=Q일 때만 0 {: .prompt-tip}

### 직관적 이해를 위한 예시

두 가우시안 분포 간의 KL Divergence를 계산해보자:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad

def gaussian_pdf(x, mu, sigma):
    """가우시안 확률밀도함수"""
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def kl_divergence_gaussian(mu1, sigma1, mu2, sigma2):
    """두 가우시안 분포 간의 KL Divergence (해석적 해)"""
    return np.log(sigma2/sigma1) + (sigma1**2 + (mu1-mu2)**2)/(2*sigma2**2) - 0.5

# 두 가우시안 분포 설정
mu1, sigma1 = 0, 1    # P(x): 표준정규분포
mu2, sigma2 = 2, 1.5  # Q(x): 평균=2, 표준편차=1.5

# KL Divergence 계산
kl_pq = kl_divergence_gaussian(mu1, sigma1, mu2, sigma2)  # D_KL(P||Q)
kl_qp = kl_divergence_gaussian(mu2, sigma2, mu1, sigma1)  # D_KL(Q||P)

print(f"D_KL(P||Q) = {kl_pq:.4f}")
print(f"D_KL(Q||P) = {kl_qp:.4f}")
print(f"비대칭성 확인: {abs(kl_pq - kl_qp):.4f}")

# 시각화
x = np.linspace(-4, 6, 1000)
p_x = gaussian_pdf(x, mu1, sigma1)
q_x = gaussian_pdf(x, mu2, sigma2)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x, p_x, 'b-', linewidth=2, label='P(x): N(0,1)')
plt.plot(x, q_x, 'r-', linewidth=2, label='Q(x): N(2,1.5)')
plt.fill_between(x, p_x, alpha=0.3, color='blue')
plt.fill_between(x, q_x, alpha=0.3, color='red')
plt.xlabel('x')
plt.ylabel('확률밀도')
plt.title('두 가우시안 분포')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
# KL Divergence의 기여도 시각화 (P(x) * log(P(x)/Q(x)))
kl_contribution = p_x * np.log(p_x / (q_x + 1e-10))  # 수치적 안정성을 위한 epsilon
plt.plot(x, kl_contribution, 'g-', linewidth=2)
plt.fill_between(x, kl_contribution, alpha=0.3, color='green')
plt.xlabel('x')
plt.ylabel('P(x) × log(P(x)/Q(x))')
plt.title(f'KL Divergence 기여도\n∫ 면적 = D_KL(P||Q) = {kl_pq:.4f}')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### PyTorch를 사용한 KL Divergence 계산

```python
import torch
import torch.nn.functional as F
from torch.distributions import Normal, kl_divergence

# 가우시안 분포로 KL Divergence 계산
def compute_kl_divergence():
    # 두 가우시안 분포 정의
    p = Normal(torch.tensor(0.0), torch.tensor(1.0))    # N(0,1)
    q = Normal(torch.tensor(2.0), torch.tensor(1.5))    # N(2,1.5)
    
    # PyTorch의 내장 함수로 KL Divergence 계산
    kl_pq = kl_divergence(p, q)
    kl_qp = kl_divergence(q, p)
    
    print(f"PyTorch KL(P||Q): {kl_pq.item():.4f}")
    print(f"PyTorch KL(Q||P): {kl_qp.item():.4f}")
    
    # 수동 계산으로 검증
    mu1, sigma1 = 0.0, 1.0
    mu2, sigma2 = 2.0, 1.5
    
    manual_kl = torch.log(torch.tensor(sigma2/sigma1)) + \
                (sigma1**2 + (mu1-mu2)**2)/(2*sigma2**2) - 0.5
    
    print(f"수동 계산 KL(P||Q): {manual_kl.item():.4f}")

compute_kl_divergence()

# 이산 분포에서의 KL Divergence 계산
def discrete_kl_divergence():
    # 두 이산 확률분포 (소프트맥스 출력)
    logits_p = torch.tensor([1.0, 2.0, 0.5])
    logits_q = torch.tensor([0.5, 1.5, 1.0])
    
    p = F.softmax(logits_p, dim=0)
    q = F.softmax(logits_q, dim=0)
    
    # KL Divergence 계산
    kl_div = F.kl_div(torch.log(q), p, reduction='sum')
    
    # 수동 계산
    manual_kl = torch.sum(p * torch.log(p / q))
    
    print(f"\n이산 분포 KL Divergence:")
    print(f"P: {p}")
    print(f"Q: {q}")
    print(f"KL(P||Q): {manual_kl.item():.4f}")

discrete_kl_divergence()
```

## 🤖 VAE에서의 MLE와 KL Divergence 활용

**Variational Autoencoder(VAE)** 는 MLE와 KL Divergence를 가장 우아하게 결합한 생성모델이다. VAE의 핵심은 **Evidence Lower BOund(ELBO)** 를 최대화하는 것인데, 이는 결국 데이터의 로그 가능도를 최대화하는 것과 같다.

[VAE 구조도: 인코더-디코더 구조와 잠재변수 z의 흐름]

### VAE의 수학적 기반

VAE는 다음과 같은 확률적 그래프 모델을 가정한다:

- **잠재변수**: $$z \sim p(z)$$ (보통 표준정규분포)
- **생성과정**: $$x \sim p_\theta(x|z)$$ (디코더)
- **인식과정**: $$z \sim q_\phi(z|x)$$ (인코더)

**목표**: 데이터의 로그 가능도 $$\log p_\theta(x)$$를 최대화

하지만 $$p_\theta(x) = \int p_\theta(x|z)p(z)dz$$는 직접 계산하기 어렵다.

### ELBO 유도 과정

Jensen's 부등식을 사용하여 로그 가능도의 하한(Lower Bound)을 구한다:

$$ \log p_\theta(x) = \log \int p_\theta(x|z)p(z)dz $$

$$ = \log \mathbb{E}_{q_\phi(z|x)} \left[ \frac{p_\theta(x|z)p(z)}{q_\phi(z|x)} \right] $$

$$ \geq \mathbb{E}_{q_\phi(z|x)} \left[ \log \frac{p_\theta(x|z)p(z)}{q_\phi(z|x)} \right] $$

$$ = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x)||p(z)) $$

이것이 **ELBO(Evidence Lower BOund)** 이다:

$$ \mathcal{L}_{ELBO} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x)||p(z)) $$

### ELBO의 두 구성요소

1. **재구성 손실(Reconstruction Loss)**: $$\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]$$
    
    - 디코더가 원본 데이터를 잘 복원하는지 측정
    - MLE 관점에서 데이터 가능도를 최대화
2. **KL 정규화 항(KL Regularization)**: $$D_{KL}(q_\phi(z|x)||p(z))$$
    
    - 인코더의 출력분포가 사전분포에 가깝도록 제약
    - 잠재공간의 구조를 학습 가능하게 만듦

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal

class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=400, latent_dim=20):
        super(VAE, self).__init__()
        
        # 인코더 (recognition network)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # 잠재변수의 평균과 로그분산
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        
        # 디코더 (generative network)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()  # MNIST의 경우 [0,1] 범위
        )
    
    def encode(self, x):
        """인코더: x -> (mu, logvar)"""
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        """재매개화 트릭: (mu, logvar) -> z"""
        if self.training:
            std = torch.exp(0.5 * logvar)
            eps = torch.randn_like(std)
            return mu + eps * std
        else:
            return mu
    
    def decode(self, z):
        """디코더: z -> x"""
        return self.decoder(z)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon_x = self.decode(z)
        return recon_x, mu, logvar

def vae_loss_function(recon_x, x, mu, logvar, beta=1.0):
    """VAE 손실함수: ELBO = 재구성손실 + β×KL손실"""
    
    # 재구성 손실 (Negative Log-Likelihood)
    # 베르누이 분포 가정: BCE Loss
    recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
    
    # KL Divergence: q(z|x) || p(z)
    # 가우시안 분포 간의 KL divergence 해석적 해
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    
    # β-VAE: KL 항에 가중치 β 적용
    total_loss = recon_loss + beta * kl_loss
    
    return total_loss, recon_loss, kl_loss

# VAE 학습 예시
def train_vae_step(model, data, optimizer, beta=1.0):
    model.train()
    optimizer.zero_grad()
    
    # Forward pass
    recon_data, mu, logvar = model(data)
    
    # 손실 계산
    loss, recon_loss, kl_loss = vae_loss_function(
        recon_data, data, mu, logvar, beta
    )
    
    # Backward pass
    loss.backward()
    optimizer.step()
    
    return {
        'total_loss': loss.item(),
        'recon_loss': recon_loss.item(),
        'kl_loss': kl_loss.item()
    }

# 간단한 테스트
batch_size, input_dim = 32, 784
model = VAE(input_dim=input_dim)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 더미 데이터로 테스트
dummy_data = torch.randn(batch_size, input_dim).sigmoid()
losses = train_vae_step(model, dummy_data, optimizer)

print("VAE 손실 구성요소:")
print(f"재구성 손실: {losses['recon_loss']:.2f}")
print(f"KL 손실: {losses['kl_loss']:.2f}")
print(f"총 손실: {losses['total_loss']:.2f}")
```

### β-VAE: KL Divergence의 가중치 조절

β-VAE는 KL 항에 가중치 β를 도입하여 재구성 품질과 잠재표현의 분리성(disentanglement) 사이의 균형을 조절한다:

$$ \mathcal{L}_{\beta-VAE} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - \beta \cdot D_{KL}(q_\phi(z|x)||p(z)) $$

- **β > 1**: KL 제약을 강화하여 더 분리된 표현 학습 (표현력 감소)
- **β < 1**: 재구성에 집중하여 더 표현력 있는 잠재변수 (분리성 감소)

[β값에 따른 잠재공간 변화 시각화]

## 🎭 GAN에서의 MLE와 Divergence

**Generative Adversarial Network(GAN)** 는 두 신경망이 경쟁하는 미니맥스 게임으로 공식화되며, 판별자는 MLE 기반으로, 생성자는 분포 간 divergence를 최소화하도록 학습된다.

[GAN 구조도: 생성자와 판별자의 적대적 학습 과정]

### GAN의 수학적 기반

GAN의 목적함수는 다음과 같은 미니맥스 게임이다:

$$ \min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{data}(x)}[\log D(x)] + \mathbb{E}_{z \sim p_z(z)}[\log(1-D(G(z)))] $$

여기서:

- **판별자 D**: 실제 데이터와 가짜 데이터를 구분 (이진 분류기)
- **생성자 G**: 노이즈 z에서 가짜 데이터 생성

### 판별자에서의 MLE

판별자는 실제로 **이진 분류 문제를 MLE로 푸는 것**이다:

- 실제 데이터에 대해: $$\max_D \mathbb{E}_{x \sim p_{data}}[\log D(x)]$$
- 가짜 데이터에 대해: $$\max_D \mathbb{E}_{z \sim p_z}[\log(1-D(G(z)))]$$

이는 베르누이 분포의 MLE와 정확히 같은 형태이다.

### 생성자와 Jensen-Shannon Divergence

최적 판별자 $$D^*$$가 주어졌을 때, 생성자의 손실은 다음과 같이 변환된다:

$$ \min_G V(D^*,G) = -\log 4 + 2 \cdot JS(p_{data} || p_g) $$

여기서 $$JS(P||Q)$$는 Jensen-Shannon Divergence이다:

$$ JS(P||Q) = \frac{1}{2}D_{KL}(P||M) + \frac{1}{2}D_{KL}(Q||M) $$

$$M = \frac{1}{2}(P+Q)$$는 두 분포의 평균이다.

> Jensen-Shannon Divergence는 KL Divergence의 대칭화된 버전으로, 항상 0과 log 2 사이의 값을 가지며 거리 지표의 성질을 만족한다. {: .prompt-tip}

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class Generator(nn.Module):
    def __init__(self, noise_dim=100, hidden_dim=128, output_dim=784):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(noise_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Tanh()  # [-1, 1] 범위 출력
        )
    
    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=128):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()  # [0, 1] 확률 출력
        )
    
    def forward(self, x):
        return self.model(x)

def train_gan_step(generator, discriminator, real_data, noise_dim=100):
    batch_size = real_data.size(0)
    device = real_data.device
    
    # 레이블 정의
    real_labels = torch.ones(batch_size, 1, device=device)
    fake_labels = torch.zeros(batch_size, 1, device=device)
    
    # =================
    # 판별자 학습 (MLE)
    # =================
    discriminator.train()
    
    # 실제 데이터에 대한 손실 (MLE)
    real_output = discriminator(real_data)
    d_loss_real = F.binary_cross_entropy(real_output, real_labels)
    
    # 가짜 데이터에 대한 손실 (MLE)
    noise = torch.randn(batch_size, noise_dim, device=device)
    fake_data = generator(noise).detach()  # 생성자 그래디언트 차단
    fake_output = discriminator(fake_data)
    d_loss_fake = F.binary_cross_entropy(fake_output, fake_labels)
    
    # 판별자 총 손실 (Negative Log-Likelihood)
    d_loss = d_loss_real + d_loss_fake
    
    # =================
    # 생성자 학습 (JS Divergence 최소화)
    # =================
    generator.train()
    
    # 새로운 가짜 데이터 생성
    noise = torch.randn(batch_size, noise_dim, device=device)
    fake_data = generator(noise)
    fake_output = discriminator(fake_data)
    
    # 생성자 손실 (판별자를 속이려고 함)
    g_loss = F.binary_cross_entropy(fake_output, real_labels)
    
    return {
        'd_loss': d_loss.item(),
        'd_loss_real': d_loss_real.item(),
        'd_loss_fake': d_loss_fake.item(),
        'g_loss': g_loss.item(),
        'real_acc': (real_output > 0.5).float().mean().item(),
        'fake_acc': (fake_output <= 0.5).float().mean().item()
    }

# GAN 모델 초기화
noise_dim = 100
generator = Generator(noise_dim)
discriminator = Discriminator()

# 옵티마이저 설정
g_optimizer = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optimizer = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

# 더미 데이터로 테스트
batch_size = 32
dummy_real_data = torch.randn(batch_size, 784).tanh()

# 한 스텝 학습
losses = train_gan_step(generator, discriminator, dummy_real_data)

print("GAN 학습 결과:")
print(f"판별자 손실 (전체): {losses['d_loss']:.4f}")
print(f"판별자 손실 (실제): {losses['d_loss_real']:.4f}")
print(f"판별자 손실 (가짜): {losses['d_loss_fake']:.4f}")
print(f"생성자 손실: {losses['g_loss']:.4f}")
print(f"실제 데이터 정확도: {losses['real_acc']:.2f}")
print(f"가짜 데이터 정확도: {losses['fake_acc']:.2f}")
```

### WGAN과 Wasserstein Distance

기존 GAN의 학습 불안정성을 해결하기 위해 **Wasserstein GAN(WGAN)** 이 제안되었다. WGAN은 Jensen-Shannon Divergence 대신 **Wasserstein Distance(Earth Mover's Distance)** 를 사용한다.

Wasserstein Distance는 두 분포 간의 "최소 운송 비용"으로 해석되며, 분포가 겹치지 않아도 의미 있는 그래디언트를 제공한다:

$$ W(p_{data}, p_g) = \inf_{\gamma \in \Pi(p_{data}, p_g)} \mathbb{E}_{(x,y) \sim \gamma}[||x-y||] $$

[Wasserstein Distance vs JS Divergence 비교 시각화]

## 🌊 Diffusion Model에서의 활용

**Diffusion Model** 은 forward process와 reverse process 모두에서 KL Divergence를 핵심적으로 활용하는 생성모델이다. 노이즈를 점진적으로 추가하고 제거하는 과정을 확률적으로 모델링한다.

[Diffusion Process 시각화: Forward와 Reverse Process]

### Diffusion Model의 수학적 기반

**Forward Process(확산 과정)**: 데이터에 점진적으로 가우시안 노이즈 추가

$$ q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}x_{t-1}, \beta_t I) $$

$$ q(x_{1:T}|x_0) = \prod_{t=1}^{T} q(x_t|x_{t-1}) $$

**Reverse Process(역확산 과정)**: 노이즈에서 데이터로 복원

$$ p_\theta(x_{0:T}) = p(x_T) \prod_{t=1}^{T} p_\theta(x_{t-1}|x_t) $$

$$ p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t,t), \Sigma_\theta(x_t,t)) $$

### DDPM의 손실함수와 KL Divergence

**Denoising Diffusion Probabilistic Model(DDPM)** 의 학습 목표는 variational lower bound를 최대화하는 것이다:

$$ \mathbb{E}[-\log p_\theta(x_0)] \leq \mathbb{E}_q[-\log p_\theta(x_0|x_1)] + \sum_{t=2}^{T} \mathbb{E}_q[D_{KL}(q(x_{t-1}|x_t,x_0)||p_\theta(x_{t-1}|x_t))] + D_{KL}(q(x_T|x_0)||p(x_T)) $$

이 식의 각 항:

1. **재구성 항**: $$\mathbb{E}_q[-\log p_\theta(x_0|x_1)]$$
2. **중간 KL 항**: $$D_{KL}(q(x_{t-1}|x_t,x_0)||p_\theta(x_{t-1}|x_t))$$
3. **사전분포 매칭 항**: $$D_{KL}(q(x_T|x_0)||p(x_T))$$

### 단순화된 손실함수

복잡한 KL divergence를 단순화하면, 최종적으로 **노이즈 예측 문제**로 귀결된다:

$$ L_{simple} = \mathbb{E}_{t,x_0,\epsilon}[||\epsilon - \epsilon_\theta(x_t, t)||^2] $$

여기서 $$\epsilon$$은 실제 노이즈, $$\epsilon_\theta(x_t, t)$$는 모델이 예측한 노이즈이다.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class SimpleDiffusionModel(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=512, time_dim=128):
        super().__init__()
        
        # 시간 임베딩 (sinusoidal embedding)
        self.time_embedding = nn.Sequential(
            nn.Linear(time_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # 노이즈 예측 네트워크
        self.noise_predictor = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )
    
    def positional_encoding(self, timesteps, dim):
        """시간 스텝을 위한 positional encoding"""
        half_dim = dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim) * -emb)
        emb = timesteps.unsqueeze(1) * emb.unsqueeze(0)
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1)
        return emb
    
    def forward(self, x_t, t):
        # 시간 임베딩
        t_emb = self.positional_encoding(t.float(), 128)
        t_emb = self.time_embedding(t_emb)
        
        # 입력과 시간 임베딩 결합
        h = torch.cat([x_t, t_emb], dim=1)
        
        # 노이즈 예측
        predicted_noise = self.noise_predictor(h)
        return predicted_noise

class DDPMTrainer:
    def __init__(self, model, num_timesteps=1000):
        self.model = model
        self.num_timesteps = num_timesteps
        
        # 베타 스케줄 (linear schedule)
        self.betas = torch.linspace(1e-4, 0.02, num_timesteps)
        self.alphas = 1.0 - self.betas
        self.alpha_cumprod = torch.cumprod(self.alphas, dim=0)
        
        # 샘플링을 위한 사전 계산
        self.sqrt_alpha_cumprod = torch.sqrt(self.alpha_cumprod)
        self.sqrt_one_minus_alpha_cumprod = torch.sqrt(1.0 - self.alpha_cumprod)
    
    def q_sample(self, x_0, t, noise=None):
        """Forward process: x_0에서 x_t로 노이즈 추가"""
        if noise is None:
            noise = torch.randn_like(x_0)
        
        sqrt_alpha_cumprod_t = self.sqrt_alpha_cumprod[t].unsqueeze(1)
        sqrt_one_minus_alpha_cumprod_t = self.sqrt_one_minus_alpha_cumprod[t].unsqueeze(1)
        
        return sqrt_alpha_cumprod_t * x_0 + sqrt_one_minus_alpha_cumprod_t * noise
    
    def compute_loss(self, x_0):
        """DDPM 손실함수 계산"""
        batch_size = x_0.size(0)
        device = x_0.device
        
        # 랜덤 시간 스텝 샘플링
        t = torch.randint(0, self.num_timesteps, (batch_size,), device=device)
        
        # 노이즈 생성
        noise = torch.randn_like(x_0)
        
        # Forward process로 노이즈 추가
        x_t = self.q_sample(x_0, t, noise)
        
        # 모델로 노이즈 예측
        predicted_noise = self.model(x_t, t)
        
        # MSE 손실 (단순화된 KL divergence)
        loss = F.mse_loss(predicted_noise, noise)
        
        return loss
    
    def p_sample_step(self, x_t, t):
        """Reverse process: x_t에서 x_{t-1}로 한 스텝 역확산"""
        # 모델로 노이즈 예측
        predicted_noise = self.model(x_t, t)
        
        # 알파 값들 가져오기
        alpha_t = self.alphas[t].unsqueeze(1)
        alpha_cumprod_t = self.alpha_cumprod[t].unsqueeze(1)
        beta_t = self.betas[t].unsqueeze(1)
        
        if t[0] > 0:
            alpha_cumprod_prev = self.alpha_cumprod[t-1].unsqueeze(1)
        else:
            alpha_cumprod_prev = torch.ones_like(alpha_cumprod_t)
        
        # 평균 계산
        mean = (1.0 / torch.sqrt(alpha_t)) * (
            x_t - (beta_t / torch.sqrt(1.0 - alpha_cumprod_t)) * predicted_noise
        )
        
        # 분산 계산
        variance = beta_t * (1.0 - alpha_cumprod_prev) / (1.0 - alpha_cumprod_t)
        
        # 노이즈 샘플링 (t=0일 때는 노이즈 없음)
        if t[0] > 0:
            noise = torch.randn_like(x_t)
            return mean + torch.sqrt(variance) * noise
        else:
            return mean

# 사용 예시
def train_ddpm_step():
    # 모델 초기화
    model = SimpleDiffusionModel()
    trainer = DDPMTrainer(model, num_timesteps=1000)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    # 더미 데이터 (MNIST 형태)
    batch_size = 16
    x_0 = torch.randn(batch_size, 784) * 0.5  # 정규화된 이미지
    
    # 한 스텝 학습
    model.train()
    optimizer.zero_grad()
    
    loss = trainer.compute_loss(x_0)
    loss.backward()
    optimizer.step()
    
    print(f"DDPM 손실: {loss.item():.6f}")
    
    # 샘플링 테스트 (한 스텝만)
    model.eval()
    with torch.no_grad():
        # 순수 노이즈에서 시작
        x_t = torch.randn(1, 784)
        t = torch.tensor([999])  # 마지막 시간 스텝
        
        # 한 스텝 역확산
        x_prev = trainer.p_sample_step(x_t, t)
        
        print(f"샘플링 - 입력 노이즈 평균: {x_t.mean().item():.4f}")
        print(f"샘플링 - 출력 평균: {x_prev.mean().item():.4f}")

train_ddpm_step()
```

### Score-based Models과 KL Divergence

최근의 **Score-based Generative Models** 은 KL divergence를 직접 최소화하는 대신, **score function** (확률밀도의 로그 그래디언트)을 학습한다:

$$ s_\theta(x) \approx \nabla_x \log p_{data}(x) $$

이는 **Stein's Identity** 를 통해 KL divergence와 연결된다:

$$ \nabla_x D_{KL}(p_{data}||p_\theta) = \mathbb{E}_{p_{data}}[s_\theta(x) - \nabla_x \log p_\theta(x)] $$

[Score Function 시각화: 확률밀도의 그래디언트 필드]

## 🔗 생성모델들의 비교와 통합적 관점

각 생성모델이 MLE와 KL Divergence를 어떻게 활용하는지 비교해보면 흥미로운 패턴을 발견할 수 있다.

### 생성모델별 핵심 원리 비교

|모델|MLE 활용|KL Divergence 활용|핵심 아이디어|
|---|---|---|---|
|**VAE**|ELBO 최대화|잠재분포 정규화|변분추론으로 생성분포 근사|
|**GAN**|판별자 학습|JS Divergence 최소화|적대적 학습으로 분포 매칭|
|**Diffusion**|변분하한 최대화|각 스텝별 분포 매칭|점진적 노이즈 제거|
|**Flow-based**|직접 MLE|정규화 흐름|가역변환으로 정확한 likelihood|

### 통합적 관점: 정보이론적 해석

모든 생성모델의 공통 목표는 **정보이론적 관점에서 데이터 분포를 학습**하는 것이다:

1. **압축 관점**: 데이터의 본질적 구조를 저차원으로 압축
2. **복원 관점**: 압축된 표현에서 원본 데이터를 복원
3. **생성 관점**: 학습된 분포에서 새로운 샘플 생성

```python
import torch
import matplotlib.pyplot as plt
import numpy as np

def compare_generative_models():
    """생성모델들의 손실함수 비교"""
    
    # 더미 데이터 설정
    batch_size, data_dim, latent_dim = 32, 784, 64
    x = torch.randn(batch_size, data_dim) * 0.5
    
    print("=== 생성모델별 손실함수 비교 ===\n")
    
    # 1. VAE 손실
    mu = torch.randn(batch_size, latent_dim)
    logvar = torch.randn(batch_size, latent_dim)
    recon_x = torch.sigmoid(torch.randn(batch_size, data_dim))
    
    recon_loss = F.binary_cross_entropy(recon_x, torch.sigmoid(x))
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / batch_size
    vae_loss = recon_loss + kl_loss
    
    print(f"VAE 손실:")
    print(f"  재구성 손실 (NLL): {recon_loss.item():.4f}")
    print(f"  KL 정규화: {kl_loss.item():.4f}")
    print(f"  총 손실 (ELBO): {vae_loss.item():.4f}\n")
    
    # 2. GAN 손실
    real_output = torch.sigmoid(torch.randn(batch_size, 1))
    fake_output = torch.sigmoid(torch.randn(batch_size, 1))
    
    d_loss_real = F.binary_cross_entropy(real_output, torch.ones_like(real_output))
    d_loss_fake = F.binary_cross_entropy(fake_output, torch.zeros_like(fake_output))
    d_loss = d_loss_real + d_loss_fake
    g_loss = F.binary_cross_entropy(fake_output, torch.ones_like(fake_output))
    
    print(f"GAN 손실:")
    print(f"  판별자 손실 (MLE): {d_loss.item():.4f}")
    print(f"  생성자 손실 (JS): {g_loss.item():.4f}\n")
    
    # 3. Diffusion 손실
    noise = torch.randn_like(x)
    predicted_noise = torch.randn_like(x)
    diffusion_loss = F.mse_loss(predicted_noise, noise)
    
    print(f"Diffusion 손실:")
    print(f"  노이즈 예측 (단순화된 KL): {diffusion_loss.item():.4f}\n")
    
    # 정보이론적 해석
    print("=== 정보이론적 해석 ===")
    print("VAE: I(X;Z) 최대화, KL(q(z|x)||p(z)) 최소화")
    print("GAN: JS(p_data||p_g) 최소화")
    print("Diffusion: KL(q(x_{t-1}|x_t,x_0)||p_θ(x_{t-1}|x_t)) 최소화")

compare_generative_models()

def information_theory_perspective():
    """정보이론 관점에서의 생성모델 분석"""
    
    print("\n=== 정보이론적 통합 관점 ===\n")
    
    # 엔트로피 계산 예시
    def entropy(p):
        """이산 분포의 엔트로피 계산"""
        p = p + 1e-10  # 수치 안정성
        return -torch.sum(p * torch.log(p))
    
    def kl_divergence(p, q):
        """이산 분포의 KL divergence 계산"""
        p, q = p + 1e-10, q + 1e-10
        return torch.sum(p * torch.log(p / q))
    
    # 예시 분포들
    p_data = torch.tensor([0.5, 0.3, 0.2])  # 실제 데이터 분포
    p_model = torch.tensor([0.4, 0.4, 0.2])  # 모델 분포
    p_uniform = torch.tensor([1/3, 1/3, 1/3])  # 균등 분포
    
    h_data = entropy(p_data)
    h_model = entropy(p_model)
    h_uniform = entropy(p_uniform)
    
    kl_data_model = kl_divergence(p_data, p_model)
    kl_data_uniform = kl_divergence(p_data, p_uniform)
    
    print(f"데이터 분포 엔트로피: {h_data.item():.4f}")
    print(f"모델 분포 엔트로피: {h_model.item():.4f}")
    print(f"균등 분포 엔트로피: {h_uniform.item():.4f}\n")
    
    print(f"KL(p_data || p_model): {kl_data_model.item():.4f}")
    print(f"KL(p_data || p_uniform): {kl_data_uniform.item():.4f}\n")
    
    print("해석:")
    print("- 낮은 KL divergence는 더 좋은 모델을 의미")
    print("- 높은 엔트로피는 더 다양한 생성을 의미")
    print("- 생성모델은 KL divergence와 엔트로피의 균형을 맞춤")

information_theory_perspective()
```

### 실전 응용에서의 하이브리드 접근

실제 산업 응용에서는 여러 기법을 조합한 하이브리드 모델이 주로 사용된다:

- **VAE + GAN**: VAE의 안정성과 GAN의 생성 품질 결합
- **Diffusion + Classifier Guidance**: 조건부 생성을 위한 분류기 결합
- **Flow + VAE**: 정확한 likelihood와 효율적 샘플링 결합

[하이브리드 모델 구조 다이어그램]

## 🎓 마무리: 실무에서의 활용 가이드

### 모델 선택 가이드

생성모델을 선택할 때 고려해야 할 요소들:

1. **정확한 likelihood 필요**: Flow-based models
2. **안정적 학습 중요**: VAE, Diffusion
3. **고품질 이미지 생성**: GAN, Diffusion
4. **빠른 샘플링 필요**: VAE, GAN
5. **해석 가능성 중요**: VAE

### 하이퍼파라미터 튜닝 팁

```python
def hyperparameter_tuning_guide():
    """생성모델별 하이퍼파라미터 튜닝 가이드"""
    
    tuning_guide = {
        "VAE": {
            "beta": "0.1~10 (높을수록 분리된 표현, 낮을수록 재구성 품질)",
            "latent_dim": "16~512 (데이터 복잡도에 따라)",
            "learning_rate": "1e-4~1e-3",
            "architecture": "점진적 크기 감소/증가"
        },
        
        "GAN": {
            "learning_rate": "1e-4~2e-4 (G와 D 균형 중요)",
            "batch_size": "64~512 (클수록 안정적)",
            "noise_dim": "100~512",
            "discriminator_steps": "1~5 (판별자 강화 시)"
        },
        
        "Diffusion": {
            "num_timesteps": "1000~4000",
            "beta_schedule": "linear, cosine, quadratic",
            "learning_rate": "1e-5~1e-4",
            "ema_decay": "0.999~0.9999"
        }
    }
    
    for model, params in tuning_guide.items():
        print(f"=== {model} 하이퍼파라미터 가이드 ===")
        for param, description in params.items():
            print(f"{param}: {description}")
        print()

hyperparameter_tuning_guide()
```

### 성능 평가 메트릭

생성모델의 성능을 평가하는 주요 지표들:

- **FID (Fréchet Inception Distance)**: 생성 이미지의 품질과 다양성
- **IS (Inception Score)**: 생성 이미지의 품질과 다양성
- **LPIPS (Learned Perceptual Image Patch Similarity)**: 지각적 유사도
- **Precision/Recall**: 생성 품질과 다양성의 분리 측정

> 최대 가능도 추정과 KL Divergence는 현대 생성모델의 수학적 기반이다. 이 두 개념을 깊이 이해하면 새로운 생성모델 논문을 읽거나 직접 모델을 설계할 때 핵심 원리를 파악할 수 있다. {: .prompt-tip}

이제 여러분도 VAE 논문에서 ELBO를 보거나, GAN 논문에서 Jensen-Shannon Divergence를 보거나, Diffusion 논문에서 KL 항들을 볼 때 그 수학적 의미와 직관을 정확히 이해할 수 있을 것이다!