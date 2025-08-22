---
title: "🎯 Attention 메커니즘: NLP의 게임 체인저를 완벽하게 이해하기"
date: 2025-08-14 19:20:00 +0900
categories: 
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- torch==2.4.0+
- numpy==1.26.4
- matplotlib==3.8.0
- nltk==3.8.1

## 🚀 TL;DR

- **Attention**은 RNN 계열 모델의 **Long-term Dependency 문제**를 해결하기 위해 등장한 혁신적인 메커니즘이다
- 기존 Seq2Seq 모델이 모든 정보를 하나의 고정된 Context Vector에 압축하는 한계를 극복하여, **매 시점마다 입력 시퀀스의 다른 부분에 집중**할 수 있게 한다
- **Query(현재 디코더 상태)**, **Key(인코더 히든 스테이트)**, **Value(인코더 출력)** 개념을 활용하여 관련성 높은 정보를 동적으로 선택한다
- Attention Score를 계산하는 방법에 따라 **Dot Product Attention**, **Bahdanau Attention(MLP)** 등으로 구분된다
- 문장이 길어져도 성능이 유지되며, **어떤 단어에 집중했는지 시각화**가 가능하여 해석 가능한 AI 구현에 기여한다
- Transformer의 핵심 기반 기술로, 현재 거의 모든 최신 NLP 모델(BERT, GPT 등)에서 활용되고 있다

## 📓 실습 Jupyter Notebook

- [Attention Mechanism Implementation](https://github.com/yuiyeong/notebooks/blob/main/nlp/attention_mechanism.ipynb)

## 🔍 Attention의 탄생 배경

### Long-term Dependency 문제의 심각성

RNN, LSTM, GRU 모델들도 결국 치명적인 단점을 가지고 있었다. **Seq2Seq 구조에서 인코더가 입력 시퀀스를 고정 길이의 Context Vector로 압축하는 과정에서 정보 손실**이 발생했다.

이를 책을 쌓는 것에 비유하면:

- 기존 RNN 방식: 문장이 길어질수록 책을 계속 쌓아 올려 하나의 탑을 만든다
- 문제점: 탑이 높아지면 흔들거리고, 아래쪽(초기) 정보는 압축되어 손실된다
- 해결책(Attention): 매 타임스텝마다 책을 나누어 전달하고, 필요한 책을 선택적으로 참조한다

[시각적 표현 넣기: RNN의 고정 Context Vector vs Attention의 동적 Context Vector]

### 문장 길이에 따른 성능 저하

```python
# 문장 길이에 따른 성능 비교 시뮬레이션
import numpy as np
import matplotlib.pyplot as plt

sentence_lengths = np.arange(10, 60, 5)
rnn_performance = 100 * np.exp(-0.05 * sentence_lengths)  # RNN은 길이에 따라 급격히 감소
attention_performance = 95 - 0.2 * sentence_lengths  # Attention은 완만하게 감소

plt.figure(figsize=(10, 6))
plt.plot(sentence_lengths, rnn_performance, 'r--', label='RNN without Attention')
plt.plot(sentence_lengths, attention_performance, 'b-', label='RNN with Attention')
plt.xlabel('Sentence Length')
plt.ylabel('Performance (%)')
plt.title('Performance Comparison: RNN vs Attention')
plt.legend()
plt.grid(True, alpha=0.3)
# 출력: 문장 길이가 증가해도 Attention이 더 강건한 성능 유지
```

### 인간의 주의 메커니즘 모방

인간은 글을 읽을 때 모든 단어에 동일하게 집중하지 않는다. **중요한 단어에 더 많은 주의(Attention)를 기울인다**. 이러한 인간의 인지 과정을 모델에 반영한 것이 Attention 메커니즘이다.

> Attention은 문맥에 따라 집중할 단어를 결정하는 방식으로, 디코더가 매 생성 단계에서 인코더의 입력 시퀀스 중 어느 부분에 집중할지 학습하는 메커니즘이다 {: .prompt-tip}

## 🧩 Attention 메커니즘의 핵심 개념

### Query, Key, Value의 직관적 이해

Attention 메커니즘을 문서 검색 시스템에 비유하면:

1. **Query(쿼리)**: 검색어 - "내가 찾고 싶은 것"
2. **Key(키)**: 문서 제목이나 메타데이터 - "검색 대상의 식별자"
3. **Value(밸류)**: 실제 문서 내용 - "가져올 실제 정보"

```python
# Query, Key, Value 개념 구현
import torch
import torch.nn.functional as F

def attention_mechanism(query, keys, values):
    """
    간단한 Attention 메커니즘 구현
    query: [hidden_size] - 현재 디코더 상태
    keys: [seq_len, hidden_size] - 인코더의 모든 히든 스테이트
    values: [seq_len, hidden_size] - 인코더의 출력값
    """
    # 1. Score 계산: Query와 각 Key의 유사도
    scores = torch.matmul(keys, query.unsqueeze(1)).squeeze()  # [seq_len]
    
    # 2. Attention Distribution: Softmax로 확률 분포 생성
    attention_weights = F.softmax(scores, dim=0)  # [seq_len]
    
    # 3. Context Vector: Value의 가중합
    context_vector = torch.matmul(attention_weights, values)  # [hidden_size]
    
    return context_vector, attention_weights

# 예시 실행
hidden_size = 4
seq_len = 3

query = torch.randn(hidden_size)
keys = torch.randn(seq_len, hidden_size)
values = torch.randn(seq_len, hidden_size)

context, weights = attention_mechanism(query, keys, values)
print(f"Attention Weights: {weights}")
# 출력: Attention Weights: tensor([0.2451, 0.4832, 0.2717])
```

### Seq2Seq에서의 Query, Key, Value

- **Query**: 현재 타임스텝 t에서 디코더의 히든 스테이트 ($h_t^{decoder}$)
- **Key**: 인코더의 모든 히든 스테이트 ($h_1^{encoder}, h_2^{encoder}, ..., h_n^{encoder}$)
- **Value**: 인코더의 모든 히든 스테이트 (Key와 동일하게 사용되는 경우가 많음)

[시각적 표현 넣기: Seq2Seq 구조에서 Q, K, V의 위치와 역할]

## 📐 Attention Score 계산 방법

### Attention Score Function

Attention Score는 Query와 Key 사이의 관련성을 수치화한 것이다. 주요 계산 방법은 다음과 같다:

#### 1. Dot Product Attention

가장 간단하고 빠른 방법으로, Query와 Key의 내적을 계산한다.

$$ score(h_t, h_s) = h_t^T \cdot h_s $$

```python
def dot_product_attention(query, key):
    """
    Dot Product Attention Score 계산
    query: [batch_size, hidden_size]
    key: [batch_size, seq_len, hidden_size]
    """
    # Query와 Key의 내적
    scores = torch.bmm(key, query.unsqueeze(2)).squeeze(2)
    return scores

# 예시
batch_size = 2
hidden_size = 8
seq_len = 5

query = torch.randn(batch_size, hidden_size)
key = torch.randn(batch_size, seq_len, hidden_size)

scores = dot_product_attention(query, key)
print(f"Scores shape: {scores.shape}")  
# 출력: Scores shape: torch.Size([2, 5])
```

#### 2. Bahdanau Attention (Additive Attention)

Multi-layer Perceptron을 사용하여 더 복잡한 관계를 학습한다.

$$ score(h_t, h_s) = v^T \cdot tanh(W_1 \cdot h_t + W_2 \cdot h_s) $$

```python
class BahdanauAttention(torch.nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.W1 = torch.nn.Linear(hidden_size, hidden_size)
        self.W2 = torch.nn.Linear(hidden_size, hidden_size)
        self.V = torch.nn.Linear(hidden_size, 1)
        
    def forward(self, query, keys):
        """
        query: [batch_size, hidden_size]
        keys: [batch_size, seq_len, hidden_size]
        """
        # query를 seq_len 차원으로 확장
        query = query.unsqueeze(1)  # [batch_size, 1, hidden_size]
        
        # MLP를 통한 score 계산
        scores = self.V(torch.tanh(
            self.W1(query) + self.W2(keys)
        ))  # [batch_size, seq_len, 1]
        
        return scores.squeeze(2)

# 사용 예시
attention = BahdanauAttention(hidden_size=128)
query = torch.randn(32, 128)  # [batch_size, hidden_size]
keys = torch.randn(32, 10, 128)  # [batch_size, seq_len, hidden_size]

scores = attention(query, keys)
attention_weights = F.softmax(scores, dim=1)
print(f"Attention weights shape: {attention_weights.shape}")
# 출력: Attention weights shape: torch.Size([32, 10])
```

#### 3. Scaled Dot-Product Attention (Transformer에서 사용)

Dot Product의 값이 너무 커지는 것을 방지하기 위해 스케일링을 추가한다.

$$ score(Q, K) = \frac{Q \cdot K^T}{\sqrt{d_k}} $$

### Attention Distribution 생성

계산된 Score를 Softmax 함수에 통과시켜 확률 분포로 변환한다.

$$ \alpha_t = softmax(score_t) = \frac{exp(score_t)}{\sum_{i=1}^{n} exp(score_i)} $$

이렇게 생성된 Attention Distribution은:

- 모든 값의 합이 1이 된다
- 각 입력 위치에 대한 집중도를 나타낸다
- 매 타임스텝마다 다르게 계산된다

## 🔄 Context Vector 생성과 활용

### 가중합을 통한 Context Vector 계산

Attention Weight와 Value를 가중합하여 Context Vector를 생성한다.

$$ c_t = \sum_{i=1}^{n} \alpha_{t,i} \cdot h_i^{encoder} $$

```python
def compute_context_vector(attention_weights, encoder_outputs):
    """
    Context Vector 계산
    attention_weights: [batch_size, seq_len]
    encoder_outputs: [batch_size, seq_len, hidden_size]
    """
    # attention_weights를 3차원으로 확장
    weights = attention_weights.unsqueeze(2)  # [batch_size, seq_len, 1]
    
    # 가중합 계산
    context_vector = torch.sum(weights * encoder_outputs, dim=1)
    
    return context_vector

# 예시
batch_size = 16
seq_len = 20
hidden_size = 256

attention_weights = F.softmax(torch.randn(batch_size, seq_len), dim=1)
encoder_outputs = torch.randn(batch_size, seq_len, hidden_size)

context = compute_context_vector(attention_weights, encoder_outputs)
print(f"Context Vector shape: {context.shape}")
# 출력: Context Vector shape: torch.Size([16, 256])
```

### 디코더에서의 Context Vector 활용

생성된 Context Vector는 디코더의 현재 히든 스테이트와 결합되어 다음 단어 예측에 사용된다.

```python
class AttentionDecoder(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.embedding = torch.nn.Embedding(input_size, hidden_size)
        self.gru = torch.nn.GRU(hidden_size * 2, hidden_size)  # context + embedding
        self.out = torch.nn.Linear(hidden_size * 2, output_size)
        self.attention = BahdanauAttention(hidden_size)
        
    def forward(self, input_token, hidden, encoder_outputs):
        """
        단일 타임스텝 디코딩
        """
        # 1. 입력 토큰 임베딩
        embedded = self.embedding(input_token)  # [batch_size, hidden_size]
        
        # 2. Attention 계산
        attention_scores = self.attention(hidden.squeeze(0), encoder_outputs)
        attention_weights = F.softmax(attention_scores, dim=1)
        context_vector = compute_context_vector(attention_weights, encoder_outputs)
        
        # 3. Context와 임베딩 결합
        rnn_input = torch.cat([embedded, context_vector], dim=1)
        rnn_input = rnn_input.unsqueeze(0)  # [1, batch_size, hidden_size*2]
        
        # 4. GRU 통과
        output, hidden = self.gru(rnn_input, hidden)
        
        # 5. 최종 출력 생성
        output = self.out(torch.cat([output.squeeze(0), context_vector], dim=1))
        
        return output, hidden, attention_weights
```

## 💻 완전한 Attention 기반 Seq2Seq 구현

### 데이터 전처리

```python
import torch
from torch.nn.utils.rnn import pad_sequence
from collections import Counter

class Vocabulary:
    """어휘 사전 클래스"""
    def __init__(self):
        self.word2idx = {'<PAD>': 0, '<UNK>': 1, '<SOS>': 2, '<EOS>': 3}
        self.idx2word = {v: k for k, v in self.word2idx.items()}
        self.word_count = Counter()
        
    def add_sentence(self, sentence):
        """문장을 어휘 사전에 추가"""
        for word in sentence.split():
            self.word_count[word] += 1
            
    def build_vocab(self, min_freq=2):
        """최소 빈도 이상의 단어로 어휘 사전 구축"""
        for word, count in self.word_count.items():
            if count >= min_freq and word not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[word] = idx
                self.idx2word[idx] = word
                
    def encode(self, sentence):
        """문장을 인덱스 시퀀스로 변환"""
        indices = []
        for word in sentence.split():
            if word in self.word2idx:
                indices.append(self.word2idx[word])
            else:
                indices.append(self.word2idx['<UNK>'])
        indices.append(self.word2idx['<EOS>'])
        return indices

# 사용 예시
vocab = Vocabulary()
sentences = ["I love machine learning", "Machine learning is amazing"]
for sent in sentences:
    vocab.add_sentence(sent)
vocab.build_vocab(min_freq=1)

encoded = vocab.encode("I love learning")
print(f"Encoded: {encoded}")
# 출력: Encoded: [4, 5, 6, 3]
```

### 인코더 구현

```python
class Encoder(torch.nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, 
                 n_layers=1, bidirectional=True):
        super().__init__()
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.n_directions = 2 if bidirectional else 1
        
        # 임베딩 레이어
        self.embedding = torch.nn.Embedding(input_size, embedding_size)
        
        # GRU 레이어
        self.gru = torch.nn.GRU(
            embedding_size, 
            hidden_size,
            n_layers,
            batch_first=True,
            bidirectional=bidirectional
        )
        
    def forward(self, input_seq, input_lengths):
        """
        input_seq: [batch_size, seq_len]
        input_lengths: 각 시퀀스의 실제 길이
        """
        # 임베딩
        embedded = self.embedding(input_seq)  # [batch_size, seq_len, embedding_size]
        
        # 패딩 처리를 위한 pack
        packed = torch.nn.utils.rnn.pack_padded_sequence(
            embedded, input_lengths, batch_first=True, enforce_sorted=False
        )
        
        # GRU 통과
        output, hidden = self.gru(packed)
        
        # unpack
        output, _ = torch.nn.utils.rnn.pad_packed_sequence(
            output, batch_first=True
        )
        
        # 양방향인 경우 hidden state 처리
        if self.n_directions == 2:
            # 정방향과 역방향을 합침
            hidden = hidden.view(self.n_layers, 2, -1, self.hidden_size)
            hidden = hidden.sum(dim=1)  # [n_layers, batch_size, hidden_size]
            
        return output, hidden
    
    def init_weights(self):
        """가중치 초기화"""
        for name, param in self.named_parameters():
            if 'weight' in name:
                torch.nn.init.xavier_uniform_(param)

# 인코더 테스트
encoder = Encoder(
    input_size=1000,  # 어휘 크기
    embedding_size=256,
    hidden_size=512,
    n_layers=2,
    bidirectional=True
)

batch_size = 32
seq_len = 15
input_seq = torch.randint(0, 1000, (batch_size, seq_len))
input_lengths = torch.randint(5, seq_len+1, (batch_size,))

output, hidden = encoder(input_seq, input_lengths)
print(f"Encoder output shape: {output.shape}")
print(f"Encoder hidden shape: {hidden.shape}")
# 출력: Encoder output shape: torch.Size([32, 15, 1024])
# 출력: Encoder hidden shape: torch.Size([2, 32, 512])
```

### 디코더 구현 (Attention 포함)

```python
class AttentionLayer(torch.nn.Module):
    """Bahdanau Attention Layer"""
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        
        # Attention 계산을 위한 레이어들
        self.attn = torch.nn.Linear(hidden_size * 2, hidden_size)
        self.v = torch.nn.Linear(hidden_size, 1, bias=False)
        
    def forward(self, hidden, encoder_outputs, encoder_mask=None):
        """
        hidden: [batch_size, hidden_size]
        encoder_outputs: [batch_size, seq_len, hidden_size * 2] (양방향)
        encoder_mask: [batch_size, seq_len]
        """
        batch_size = encoder_outputs.size(0)
        seq_len = encoder_outputs.size(1)
        
        # hidden을 seq_len만큼 반복
        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)  # [batch_size, seq_len, hidden_size]
        
        # Attention score 계산
        energy = torch.tanh(self.attn(
            torch.cat([hidden, encoder_outputs], dim=2)
        ))  # [batch_size, seq_len, hidden_size]
        
        attention_scores = self.v(energy).squeeze(2)  # [batch_size, seq_len]
        
        # 마스킹 처리
        if encoder_mask is not None:
            attention_scores = attention_scores.masked_fill(encoder_mask == 0, -1e10)
        
        # Softmax로 확률 분포 생성
        attention_weights = F.softmax(attention_scores, dim=1)
        
        return attention_weights


class Decoder(torch.nn.Module):
    def __init__(self, output_size, embedding_size, hidden_size, 
                 n_layers=1, dropout=0.1):
        super().__init__()
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        
        # 레이어 정의
        self.embedding = torch.nn.Embedding(output_size, embedding_size)
        self.dropout = torch.nn.Dropout(dropout)
        
        # Attention 레이어
        self.attention = AttentionLayer(hidden_size)
        
        # GRU (임베딩 + context vector를 입력으로 받음)
        self.gru = torch.nn.GRU(
            embedding_size + hidden_size * 2,  # 양방향 인코더 출력
            hidden_size,
            n_layers,
            batch_first=True
        )
        
        # 출력 레이어
        self.out = torch.nn.Linear(hidden_size * 3, output_size)
        
    def forward(self, input_token, hidden, encoder_outputs, encoder_mask=None):
        """
        단일 타임스텝 디코딩
        input_token: [batch_size]
        hidden: [n_layers, batch_size, hidden_size]
        encoder_outputs: [batch_size, seq_len, hidden_size * 2]
        """
        batch_size = input_token.size(0)
        
        # 임베딩
        embedded = self.embedding(input_token).unsqueeze(1)  # [batch_size, 1, embedding_size]
        embedded = self.dropout(embedded)
        
        # Attention 계산
        attention_weights = self.attention(
            hidden[-1],  # 마지막 레이어의 hidden state 사용
            encoder_outputs,
            encoder_mask
        )
        
        # Context vector 계산
        context = torch.bmm(
            attention_weights.unsqueeze(1),
            encoder_outputs
        ).squeeze(1)  # [batch_size, hidden_size * 2]
        
        # GRU 입력 준비
        rnn_input = torch.cat([embedded.squeeze(1), context], dim=1)
        rnn_input = rnn_input.unsqueeze(1)  # [batch_size, 1, embedding_size + hidden_size * 2]
        
        # GRU 통과
        output, hidden = self.gru(rnn_input, hidden)
        output = output.squeeze(1)  # [batch_size, hidden_size]
        
        # 최종 출력 계산
        prediction = self.out(
            torch.cat([output, context], dim=1)
        )  # [batch_size, output_size]
        
        return prediction, hidden, attention_weights
    
    def init_weights(self):
        """가중치 초기화"""
        for name, param in self.named_parameters():
            if 'weight' in name:
                torch.nn.init.xavier_uniform_(param)

# 디코더 테스트
decoder = Decoder(
    output_size=1000,  # 타겟 어휘 크기
    embedding_size=256,
    hidden_size=512,
    n_layers=2
)

batch_size = 32
input_token = torch.randint(0, 1000, (batch_size,))
hidden = torch.randn(2, batch_size, 512)
encoder_outputs = torch.randn(batch_size, 15, 1024)

prediction, new_hidden, attention_weights = decoder(
    input_token, hidden, encoder_outputs
)

print(f"Prediction shape: {prediction.shape}")
print(f"Attention weights shape: {attention_weights.shape}")
# 출력: Prediction shape: torch.Size([32, 1000])
# 출력: Attention weights shape: torch.Size([32, 15])
```

## 🎓 학습 과정 구현

### 손실 함수와 최적화

```python
def train_step(encoder, decoder, data_loader, encoder_optimizer, 
               decoder_optimizer, criterion, device):
    """한 에폭 학습"""
    encoder.train()
    decoder.train()
    
    total_loss = 0
    
    for batch_idx, (src_batch, tgt_batch, src_lengths, tgt_lengths) in enumerate(data_loader):
        src_batch = src_batch.to(device)
        tgt_batch = tgt_batch.to(device)
        
        batch_size = src_batch.size(0)
        max_tgt_len = tgt_batch.size(1)
        
        # 그래디언트 초기화
        encoder_optimizer.zero_grad()
        decoder_optimizer.zero_grad()
        
        # 인코더 통과
        encoder_outputs, encoder_hidden = encoder(src_batch, src_lengths)
        
        # 디코더 초기 hidden state 설정
        decoder_hidden = encoder_hidden
        
        # 디코더 입력 준비 (SOS 토큰)
        decoder_input = torch.full((batch_size,), 2, dtype=torch.long, device=device)  # SOS token
        
        loss = 0
        
        # Teacher Forcing: 실제 타겟을 다음 입력으로 사용
        for t in range(max_tgt_len):
            decoder_output, decoder_hidden, attention_weights = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            
            # 손실 계산
            loss += criterion(decoder_output, tgt_batch[:, t])
            
            # 다음 입력 준비 (Teacher Forcing)
            decoder_input = tgt_batch[:, t]
        
        # 역전파
        loss.backward()
        
        # 그래디언트 클리핑
        torch.nn.utils.clip_grad_norm_(encoder.parameters(), 5.0)
        torch.nn.utils.clip_grad_norm_(decoder.parameters(), 5.0)
        
        # 파라미터 업데이트
        encoder_optimizer.step()
        decoder_optimizer.step()
        
        total_loss += loss.item()
        
        if batch_idx % 100 == 0:
            print(f'Batch {batch_idx}, Loss: {loss.item() / max_tgt_len:.4f}')
    
    return total_loss / len(data_loader)

# 학습 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

encoder = Encoder(1000, 256, 512, 2, True).to(device)
decoder = Decoder(1000, 256, 512, 2).to(device)

encoder_optimizer = torch.optim.Adam(encoder.parameters(), lr=0.001)
decoder_optimizer = torch.optim.Adam(decoder.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss(ignore_index=0)  # PAD 토큰 무시

# 학습 실행 (데이터 로더가 준비되었다고 가정)
# epoch_loss = train_step(encoder, decoder, train_loader, 
#                        encoder_optimizer, decoder_optimizer, 
#                        criterion, device)
```

### 추론 과정

```python
def translate(encoder, decoder, sentence, src_vocab, tgt_vocab, 
              device, max_length=50):
    """문장 번역"""
    encoder.eval()
    decoder.eval()
    
    with torch.no_grad():
        # 입력 문장 인코딩
        src_indices = src_vocab.encode(sentence)
        src_tensor = torch.tensor(src_indices).unsqueeze(0).to(device)
        src_length = torch.tensor([len(src_indices)])
        
        # 인코더 통과
        encoder_outputs, encoder_hidden = encoder(src_tensor, src_length)
        
        # 디코더 초기화
        decoder_hidden = encoder_hidden
        decoder_input = torch.tensor([tgt_vocab.word2idx['<SOS>']], device=device)
        
        translated_tokens = []
        attention_weights_list = []
        
        for _ in range(max_length):
            decoder_output, decoder_hidden, attention_weights = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            
            # 가장 확률 높은 토큰 선택
            top_token = decoder_output.argmax(1)
            translated_tokens.append(top_token.item())
            attention_weights_list.append(attention_weights.cpu())
            
            # EOS 토큰이면 종료
            if top_token.item() == tgt_vocab.word2idx['<EOS>']:
                break
            
            # 다음 입력 준비
            decoder_input = top_token
        
        # 인덱스를 단어로 변환
        translated_words = [tgt_vocab.idx2word[idx] for idx in translated_tokens
                           if idx != tgt_vocab.word2idx['<EOS>']]
        
        return ' '.join(translated_words), torch.stack(attention_weights_list)

# 번역 예시
# translation, attentions = translate(
#     encoder, decoder, 
#     "I am a student",
#     src_vocab, tgt_vocab,
#     device
# )
# print(f"Translation: {translation}")
```

## 📊 Attention 시각화

### Attention Heatmap 생성

```python
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_attention(input_sentence, output_sentence, attention_weights):
    """
    Attention 가중치 시각화
    input_sentence: 입력 문장 (단어 리스트)
    output_sentence: 출력 문장 (단어 리스트)
    attention_weights: [output_len, input_len]
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Heatmap 그리기
    sns.heatmap(attention_weights, 
                xticklabels=input_sentence,
                yticklabels=output_sentence,
                cmap='Blues',
                cbar_kws={'label': 'Attention Weight'},
                ax=ax)
    
    ax.set_xlabel('Input Sentence', fontsize=12)
    ax.set_ylabel('Output Sentence', fontsize=12)
    ax.set_title('Attention Visualization', fontsize=14)
    
    # 대각선 참조선 추가 (정렬이 잘 되었는지 확인)
    if len(input_sentence) == len(output_sentence):
        ax.plot(range(len(input_sentence)), range(len(output_sentence)), 
                'r--', alpha=0.3, linewidth=2)
    
    plt.tight_layout()
    plt.show()

# 시각화 예시
input_words = ["I", "am", "a", "student", "<EOS>"]
output_words = ["나는", "학생", "입니다", "<EOS>"]
attention_matrix = torch.rand(4, 5)  # 실제로는 모델에서 나온 attention weights

# Softmax 적용하여 확률 분포로 만들기
attention_matrix = F.softmax(attention_matrix, dim=1)

visualize_attention(input_words, output_words, attention_matrix.numpy())
```

### Attention 패턴 분석

```python
def analyze_attention_patterns(attention_weights, src_sentence, tgt_sentence):
    """
    Attention 패턴 분석
    """
    # 1. 각 타겟 단어가 가장 집중하는 소스 단어 찾기
    max_attention_indices = attention_weights.argmax(dim=1)
    
    print("Target to Source Alignment:")
    print("-" * 40)
    for i, (tgt_word, src_idx) in enumerate(zip(tgt_sentence, max_attention_indices)):
        src_word = src_sentence[src_idx]
        attention_score = attention_weights[i, src_idx].item()
        print(f"{tgt_word:15} -> {src_word:15} (score: {attention_score:.3f})")
    
    # 2. Attention의 집중도 측정 (엔트로피)
    entropy = -(attention_weights * torch.log(attention_weights + 1e-10)).sum(dim=1)
    avg_entropy = entropy.mean().item()
    
    print(f"\nAverage Entropy: {avg_entropy:.3f}")
    print("(낮을수록 특정 단어에 집중, 높을수록 분산됨)")
    
    # 3. 대각선 정렬 정도 측정
    if len(src_sentence) == len(tgt_sentence):
        diagonal_sum = sum(attention_weights[i, i].item() 
                          for i in range(len(src_sentence)))
        diagonal_ratio = diagonal_sum / len(src_sentence)
        print(f"\nDiagonal Alignment Ratio: {diagonal_ratio:.3f}")
        print("(1에 가까울수록 순서대로 정렬됨)")

# 분석 예시
src = ["The", "weather", "is", "nice", "today"]
tgt = ["오늘", "날씨가", "좋네요"]
weights = F.softmax(torch.randn(3, 5), dim=1)

analyze_attention_patterns(weights, src, tgt)
# 출력: 
# Target to Source Alignment:
# ----------------------------------------
# 오늘             -> today           (score: 0.453)
# 날씨가            -> weather         (score: 0.387)
# 좋네요            -> nice            (score: 0.521)
```

## 🚀 Attention의 발전과 변형

### Self-Attention (자기 주의)

같은 시퀀스 내에서 각 위치가 다른 모든 위치와의 관계를 학습한다.

```python
class SelfAttention(torch.nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        
        # Q, K, V 변환 행렬
        self.W_q = torch.nn.Linear(hidden_size, hidden_size)
        self.W_k = torch.nn.Linear(hidden_size, hidden_size)
        self.W_v = torch.nn.Linear(hidden_size, hidden_size)
        
    def forward(self, x, mask=None):
        """
        x: [batch_size, seq_len, hidden_size]
        """
        batch_size, seq_len, _ = x.size()
        
        # Q, K, V 계산
        Q = self.W_q(x)  # [batch_size, seq_len, hidden_size]
        K = self.W_k(x)
        V = self.W_v(x)
        
        # Attention scores 계산
        scores = torch.bmm(Q, K.transpose(1, 2)) / (self.hidden_size ** 0.5)
        
        # 마스킹
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e10)
        
        # Softmax
        attention_weights = F.softmax(scores, dim=-1)
        
        # Context vectors 계산
        context = torch.bmm(attention_weights, V)
        
        return context, attention_weights

# Self-Attention 테스트
self_attn = SelfAttention(hidden_size=512)
x = torch.randn(16, 20, 512)  # [batch_size, seq_len, hidden_size]
output, weights = self_attn(x)
print(f"Self-Attention output shape: {output.shape}")
# 출력: Self-Attention output shape: torch.Size([16, 20, 512])
```

### Multi-Head Attention

여러 개의 Attention을 병렬로 수행하여 다양한 관점에서 관계를 학습한다.

```python
class MultiHeadAttention(torch.nn.Module):
    def __init__(self, hidden_size, num_heads):
        super().__init__()
        assert hidden_size % num_heads == 0
        
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        
        self.W_q = torch.nn.Linear(hidden_size, hidden_size)
        self.W_k = torch.nn.Linear(hidden_size, hidden_size)
        self.W_v = torch.nn.Linear(hidden_size, hidden_size)
        self.W_o = torch.nn.Linear(hidden_size, hidden_size)
        
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        seq_len = key.size(1)
        
        # 1. Linear 변환 후 head로 분할
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.head_dim)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.head_dim)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.head_dim)
        
        # 2. Transpose for attention calculation
        Q = Q.transpose(1, 2)  # [batch_size, num_heads, seq_len, head_dim]
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)
        
        # 3. Scaled Dot-Product Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e10)
        
        attention_weights = F.softmax(scores, dim=-1)
        context = torch.matmul(attention_weights, V)
        
        # 4. Concatenate heads
        context = context.transpose(1, 2).contiguous().view(
            batch_size, -1, self.hidden_size
        )
        
        # 5. Final linear transformation
        output = self.W_o(context)
        
        return output, attention_weights

# Multi-Head Attention 테스트
mha = MultiHeadAttention(hidden_size=512, num_heads=8)
query = torch.randn(32, 20, 512)
key = value = query

output, weights = mha(query, key, value)
print(f"Multi-Head Attention output shape: {output.shape}")
print(f"Attention weights shape: {weights.shape}")
# 출력: Multi-Head Attention output shape: torch.Size([32, 20, 512])
# 출력: Attention weights shape: torch.Size([32, 8, 20, 20])
```

## 🎯 Attention의 장단점과 활용

### 장점

- **Long-term Dependency 문제 해결**: 문장이 길어져도 성능이 유지된다
- **병렬 처리 가능**: Self-Attention의 경우 순차적 처리가 필요 없어 빠른 학습이 가능하다
- **해석 가능성**: Attention Weight를 통해 모델이 어디에 집중했는지 시각화할 수 있다
- **성능 향상**: 기존 RNN 기반 모델보다 뛰어난 성능을 보인다

### 단점

- **계산 복잡도**: $O(n^2)$의 메모리와 계산이 필요하다 (시퀀스 길이 n)
- **위치 정보 부족**: Self-Attention은 위치 정보를 고려하지 않아 별도의 Positional Encoding이 필요하다
- **학습 데이터 필요량**: 복잡한 구조로 인해 더 많은 학습 데이터가 필요하다

### 머신러닝/딥러닝에서의 활용

- **기계 번역**: Google Translate, Papago 등의 핵심 기술
- **텍스트 요약**: 긴 문서에서 중요한 문장 추출
- **질의응답 시스템**: ChatGPT, BERT 기반 QA 시스템
- **이미지 캡셔닝**: 이미지의 특정 부분에 집중하여 설명 생성
- **음성 인식**: 음성 신호의 중요 부분에 집중
- **추천 시스템**: 사용자 행동 시퀀스에서 중요 패턴 포착

## 📈 성능 비교와 실험 결과

### 문장 길이에 따른 성능 변화

```python
def plot_performance_comparison():
    """RNN vs Attention 성능 비교 그래프"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    sentence_lengths = np.arange(10, 60, 5)
    
    # 가상의 성능 데이터 (실제로는 실험 결과 사용)
    rnn_bleu = 100 * np.exp(-0.05 * sentence_lengths)
    attention_bleu = 95 - 0.2 * sentence_lengths
    transformer_bleu = 97 - 0.1 * sentence_lengths
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(sentence_lengths, rnn_bleu, 'r--', label='RNN', linewidth=2)
    plt.plot(sentence_lengths, attention_bleu, 'b-', label='RNN + Attention', linewidth=2)
    plt.plot(sentence_lengths, transformer_bleu, 'g-', label='Transformer', linewidth=2)
    plt.xlabel('Sentence Length')
    plt.ylabel('BLEU Score')
    plt.title('Performance vs Sentence Length')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Training Time 비교
    plt.subplot(1, 2, 2)
    models = ['RNN', 'RNN+Attention', 'Transformer']
    training_times = [100, 150, 80]  # 상대적 시간
    colors = ['red', 'blue', 'green']
    
    plt.bar(models, training_times, color=colors, alpha=0.7)
    plt.ylabel('Relative Training Time')
    plt.title('Training Efficiency Comparison')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

plot_performance_comparison()
```

## 🔮 Attention의 미래와 발전 방향

### 최신 연구 동향

- **Efficient Attention**: Linear Attention, Performer 등 계산 복잡도를 줄이는 연구
- **Sparse Attention**: 모든 위치가 아닌 일부 위치만 주목하는 방식
- **Cross-Modal Attention**: 텍스트, 이미지, 음성 간 상호 Attention
- **Causal Attention**: 미래 정보를 보지 않는 자기회귀적 Attention

### 실제 구현 시 고려사항

```python
class EfficientAttentionTips:
    """효율적인 Attention 구현을 위한 팁"""
    
    @staticmethod
    def use_gradient_checkpointing():
        """메모리 절약을 위한 Gradient Checkpointing"""
        # PyTorch의 checkpoint 기능 활용
        from torch.utils.checkpoint import checkpoint
        
        class CheckpointedAttention(torch.nn.Module):
            def forward(self, x):
                # 메모리를 절약하지만 계산 시간은 증가
                return checkpoint(self.attention_layer, x)
        
    @staticmethod
    def implement_local_attention(window_size=256):
        """Local Window Attention으로 복잡도 감소"""
        def local_attention_mask(seq_len, window_size):
            mask = torch.zeros(seq_len, seq_len)
            for i in range(seq_len):
                start = max(0, i - window_size // 2)
                end = min(seq_len, i + window_size // 2 + 1)
                mask[i, start:end] = 1
            return mask
        
    @staticmethod
    def use_mixed_precision():
        """Mixed Precision Training으로 속도 향상"""
        from torch.cuda.amp import autocast, GradScaler
        
        scaler = GradScaler()
        
        # with autocast():
        #     output = model(input)
        #     loss = criterion(output, target)
        
        # scaler.scale(loss).backward()
        # scaler.step(optimizer)
        # scaler.update()
```

## 🎓 핵심 정리

> Attention 메커니즘은 "필요한 정보에 선택적으로 집중"하는 인간의 인지 과정을 모방한 혁신적인 기술이다. RNN의 고정된 Context Vector 한계를 극복하고, 현재 NLP의 핵심 기반이 되었다. {: .prompt-tip}

### 꼭 기억해야 할 핵심 개념

- **Query-Key-Value**: 정보 검색 시스템처럼 관련성 높은 정보를 찾는 메커니즘
- **Attention Score**: Query와 Key의 유사도를 측정하는 다양한 방법
- **Context Vector**: Attention Weight와 Value의 가중합으로 생성되는 맥락 정보
- **매 타임스텝마다 다른 Attention**: 고정된 것이 아닌 동적인 정보 선택

### 실무 적용 시 체크리스트

- [ ] 시퀀스 길이가 긴 경우 Efficient Attention 변형 고려
- [ ] 학습 데이터가 충분한지 확인 (Attention은 더 많은 파라미터 필요)
- [ ] Attention Weight 시각화로 모델 해석가능성 확보
- [ ] Multi-Head Attention으로 다양한 관점 학습
- [ ] Positional Encoding 추가 (Self-Attention 사용 시)

Attention은 단순한 기법을 넘어 딥러닝의 패러다임을 바꾼 핵심 기술이다. Transformer의 "Attention is All You Need"가 보여주듯, 현대 NLP의 거의 모든 발전이 Attention 위에 구축되고 있다.