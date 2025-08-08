---
title: 🚣 (AI 부트캠프 13기) 첫 NLP 경진 대회와 참혹한 실패
date: 2025-08-08 16:17:00 +0900
categories:
  - BOOTCAMP
  - KERNEL_ACADEMY
tags:
  - 급발진거북이
  - 패스트캠퍼스
  - 패스트캠퍼스AI부트캠프
  - 패스트캠퍼스업스테이지부트캠프
  - 패스트캠퍼스업스테이지에이아이랩
  - 업스테이지패스트캠퍼스
  - UpstageAILab
  - 국비지원
  - 후기
toc: true
comments: false
mermaid: true
math: true
---

![이미지](/assets/img/2025-08-08/img_leaderboard_of_nlp_competition.png){: .w-75 .center}


## 📝 솔직한 고백: 이번 대회에서 나는 무엇을 했는가?

이번 대화 요약(Dialogue Summarization) 경진대회는 나에게 **실패와 반성**의 시간이었다. 솔직히 말하면, 팀원으로서 제대로 된 기여를 하지 못했고, 실질적인 실험 결과도 거의 내지 못했다.

**_내가 실제로 한 일들_**

- ✅ 개발 환경 구축 (PyTorch, Transformers 설치)
- ✅ 강의 수강 (Transformer 아키텍처, BART vs GPT 비교)
- ✅ 개인 공부 (Encoder-Decoder vs Decoder-only 모델 차이점 학습)
- ❌ 실질적인 모델 실험
- ❌ 팀 프로젝트에 기여
- ❌ 대회 결과 향상

**_팀원이 한 일_**

팀원분은 나와 달리 BART 계열 사전훈련 모델로 체계적인 실험을 진행하셨다. KoBART, mBART 등 다양한 모델을 시도하며 하이퍼파라미터 튜닝까지 수행하는 모습을 보며, 내가 얼마나 기여하지 못했는지 뼈저리게 느꼈다.

## 🤦‍♂️ 왜 제대로 참여하지 못했는가?

### 1. 잘못된 시간 관리

**2주라는 짧은 대회 기간에 휴가를 다녀온 것**이 가장 큰 실수였다. 경진대회가 진행 중인데도 개인 일정을 우선시한 결과, 팀에 민폐를 끼쳤다.

### 2. 비현실적인 목표 설정

**Decoder-only 모델(GPT 계열)로 실험해보겠다는 욕심**이 오히려 독이 되었다.

```python
# 내가 시도했던 것들
- KoGPT-2 (175M): 메모리 부족으로 훈련 실패
- Polyglot-Ko-1.3B: 로딩조차 안됨
- SOLAR-10.7B: 꿈도 꾸지 못함

# 현실적인 선택지였던 것들
- KoBART (140M): 팀원이 이미 실험 중
- KoT5 (220M): 시도해볼 만했지만 도전하지 않음
```

### 3. 기술적 한계와 경험 부족

서버 리소스는 충분했지만(RTX 3090 24GB), **모델 최적화 기법에 대한 지식 부족**으로 큰 모델을 효율적으로 다루지 못했다.

- Gradient Checkpointing
- Model Parallelism
- DeepSpeed ZeRO
- LoRA, QLoRA 등 Parameter-Efficient Fine-tuning

이런 기법들을 제대로 이해하지 못한 채 무작정 큰 모델만 고집했다.

## 💡 그래도 얻은 것들: 이론적 이해의 심화

비록 실험은 실패했지만, **모델 아키텍처에 대한 이해**는 크게 늘었다.

### Encoder-Decoder vs Decoder-only 모델 비교

|특성|BART (Encoder-Decoder)|GPT (Decoder-only)|
|---|---|---|
|**아키텍처**|Bidirectional Encoder + Autoregressive Decoder|Autoregressive Decoder Only|
|**사전훈련**|Denoising (마스킹, 순서 변경)|Next Token Prediction|
|**요약 성능**|전통적으로 우수|최근 In-context Learning으로 역전|
|**메모리 효율성**|상대적으로 효율적|KV-cache로 인한 메모리 부담|
|**산업 트렌드**|레거시|ChatGPT, Claude 등 주류|

### 코드 차이점 이해

```python
# BART 방식 (Fine-tuning)
model = BartForConditionalGeneration.from_pretrained("kobart")
tokenizer = BartTokenizer.from_pretrained("kobart")

# 훈련용 데이터 준비
inputs = tokenizer(dialogue, max_length=512, truncation=True, return_tensors="pt")
targets = tokenizer(summary, max_length=128, truncation=True, return_tensors="pt")

# Forward pass
outputs = model(input_ids=inputs.input_ids, labels=targets.input_ids)
loss = outputs.loss

# GPT 방식 (Few-shot Learning)
prompt = f"""다음 대화를 요약해주세요:

대화: {dialogue}

요약:"""

response = model.generate(prompt, max_new_tokens=128)
```

### 현실과 대회의 괴리감

이번 대회에서 가장 **흥미를 잃게 된 요소**는 현실과의 괴리였다.

- **현실**: GPT-4, Claude, Gemini 등 Decoder-only 모델이 요약 작업 주도
- **대회**: BART, T5 등 Encoder-Decoder 모델로 제한
- **산업 트렌드**: In-context Learning, Few-shot Learning
- **대회 방식**: Traditional Fine-tuning

물론 교육 목적에서는 Fine-tuning 경험이 중요하지만, **시대적 흐름과 반대 방향**으로 가는 느낌이 들어 동기부여가 어려웠다.

## 🔍 마주한 한계와 깊은 반성

### 팀워크의 실패

가장 큰 반성점은 **팀원에게 민폐를 끼쳤다**는 것이다.

- 초기 환경 구축 외에는 실질적 기여 없음
- 개인 공부에만 몰두하여 팀 목표 외면
- 휴가로 인한 소통 단절
- 결과적으로 팀원 혼자서 모든 실험 부담

### 목표 설정의 실패

**"Decoder-only 모델로 도전해보자"** 라는 목표 자체는 나쁘지 않았지만, 현실적 제약을 고려하지 않았다.

- 메모리 제약 분석 부족
- 대안 기법 학습 부족
- 백업 플랜 부재
- 팀 목표와의 정렬 실패

## 🚀 앞으로의 계획: 개인 프로젝트로 설욕

이번 대회의 아쉬움을 개인 프로젝트로 해결하고자 한다.

### Parameter-Efficient Fine-tuning 마스터

```python
# LoRA를 활용한 대화 요약 프로젝트
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(base_model, config)
# 전체 파라미터의 1% 미만만 학습하여 메모리 효율성 극대화
```

### Decoder-only 모델 요약 실험

- **SOLAR-10.7B + QLoRA**: 메모리 효율적 파인튜닝
- **Few-shot Learning**: GPT 스타일 프롬프트 엔지니어링
- **In-context Learning**: 예시 기반 요약 생성

## 🏁 결론: 실패도 성장의 밑거름

이번 대화 요약 경진대회는 **완전한 실패**였다. 팀에 기여하지 못했고, 실험 결과도 없으며, 대회 목표도 달성하지 못했다.

하지만 **실패 자체가 중요한 학습**이었다고 생각한다:

1. **시간 관리의 중요성**: 짧은 대회 기간에는 모든 것을 집중해야 함
2. **현실적 목표 설정**: 이상과 현실의 균형점 찾기
3. **팀워크의 가치**: 개인 성장도 중요하지만 팀 기여가 우선
4. **기술적 한계 인정**: 모르는 것은 빨리 배우거나 다른 방법 모색

**가장 큰 깨달음은 "완벽한 이해보다는 실행 가능한 실험이 더 가치 있다"** 는 것이다.

다음 경진대회에서는,

- 팀 목표에 맞는 현실적 계획 수립
- 개인 공부와 팀 기여의 균형
- 빠른 프로토타입 → 점진적 개선 전략
- 백업 플랜을 항상 준비

이번 실패를 발판 삼아, 개인 프로젝트에서는 반드시 **Decoder-only 모델로 대화 요약 태스크를 정복**하겠다는 다짐으로 이 회고를 마친다.
