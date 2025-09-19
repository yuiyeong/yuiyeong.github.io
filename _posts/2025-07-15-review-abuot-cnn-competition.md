---
title: 🚣 (AI 부트캠프 13기) 대회를 치르면서 배운 CNN 모델링
date: 2025-07-15 09:00:00 +0900
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
  - GeekAndChill
  - 기깬칠
  - AI
  - 에이아이
  - AI부트캠프13기
  - UpstageAILab13기
toc: true
comments: false
mermaid: true
math: true
---

![이미지](/assets/img/2025-07-15/img_wandb.png){: .w-75 .center}

## 📝 나는 내 학습 목표를 달성하기 위해 무엇을 어떻게 했는가?

이번 문서 이미지 분류 대회를 시작하며 나는 세 가지 핵심 학습목표를 세웠다.

**_딥러닝 모델링을 위한 체계적인 이미지 분석 역량 습득_**

**_PyTorch Lightning + W&B를 활용한 실험 관리 체계 구축_**

**_Computer Vision 대회의 전체 파이프라인 경험_**

이러한 목표를 달성하기 위해 다음과 같은 활동을 진행했다.

### 딥러닝을 위한 이미지 EDA

이번 대회에서 가장 자부심을 느끼는 부분은 **체계적인 이미지 EDA**를 수행했다는 점이다. 단순히 이미지를 보는 것을 넘어서, 딥러닝 관점에서 의미 있는 32개의 특성을 추출하여 분석했다.

```python
# 추출한 주요 특성들
- 구조적 특성: width, height, aspect_ratio, total_pixels
- 품질 특성: brightness, contrast, sharpness, noise_level
- 문서 특성: text_density, white_space_ratio, margin_uniformity
- 변형 특성: skew_angle, is_rotated_90, has_black_borders
```

특히 Train-Test 데이터 간의 분포 차이를 정량적으로 분석한 결과, Test 데이터가 의도적으로 변형되었음을 발견했다.

- **Brightness**: Train(148.2) vs Test(172.2) - Test가 24포인트 더 밝음
- **Skew Angle**: Train(-1.1°±10.5°) vs Test(-2.8°±38.3°) - 표준편차가 3배 이상
- **Sharpness**: Train(1357.1) vs Test(688.3) - Test가 덜 선명함

### 개발 환경 구축

PyTorch Lightning과 Weights & Biases를 활용하여 체계적인 실험 관리 환경을 구축했다. 특히 Poetry를 통한 의존성 관리와 환경 변수 설정으로 재현 가능한 실험 환경을 만들었다.

```python
# 구축한 실험 관리 체계
- Poetry + pyproject.toml: 정확한 버전 관리
- PyTorch Lightning: 훈련 루프 추상화 및 멀티 GPU 지원
- Weights & Biases: 실시간 메트릭 추적 및 하이퍼파라미터 관리
- 모듈화된 코드 구조: config/, model/, training/, transforms/
```

## 🤝 나는 어떤 방식으로 팀으로서 대회를 참여하는 방식을 개선했는가?

### 체계적인 코드 구조화

팀원 간 협업을 위해 명확한 디렉토리 구조와 모듈화된 코드를 작성했다.

```
src/
├── config/         # 설정 관련 모듈
├── data/          # 데이터 로더 및 데이터셋
├── model/         # 모델 정의 및 구현
├── training/      # 훈련 관련 모듈  
├── transforms/    # 이미지 변환 및 증강
└── script/        # 실행 스크립트 (train.py, predict.py)
```

### 하이퍼파라미터 실험

다양한 하이퍼파라미터 조합으로 체계적인 실험을 진행했다.

|파라미터|실험 범위|최적값|
|---|---|---|
|Learning Rate|1e-4 ~ 5e-3|5e-4|
|Batch Size|16, 32, 64|16|
|Drop Rate|0.0 ~ 0.3|0.1|
|Label Smoothing|0.0 ~ 0.2|0.1|
|MixUp Alpha|0.0 ~ 0.4|0.2|

## 💡 내가 한 행동의 결과로 어떤 지점을 달성하고, 어떠한 깨달음을 얻었는가?

### 달성한 성과

1. **완성도 있는 파이프라인**: 데이터 로딩부터 예측까지 end-to-end 파이프라인 구축
2. **재현 가능한 실험**: 모든 실험이 seed 고정과 설정 파일로 재현 가능
3. **효율적인 코드**: PyTorch Lightning으로 boilerplate 코드 최소화

### 핵심 깨달음

**"Computer Vision 에서 데이터 이해가 모델 성능만큼 중요하다"**

32개 특성을 분석한 EDA는 Train-Test 분포 차이를 명확히 보여주었다. 하지만 아이러니하게도 이 인사이트를 실제 증강 전략으로 연결하지 못했다는 점에서, 분석과 실행 사이의 간극을 경험했다.

## 🔍 마주한 한계는 무엇이며, 아쉬웠던 점은 무엇인가?

### EDA 의 미활용

가장 큰 아쉬움은 공들여 수행한 EDA가 실제 모델링에 충분히 활용되지 못했다는 점이다. Test 데이터의 극단적 회전(-90°~90°)과 밝기 변화를 발견했음에도, 이를 반영한 증강 전략을 구현하지 못했다.

### Validation Set 구성의 실패

Train F1 score 와 Validation F1 score 간의 차이를 규명하지 못했다. 특히 Test 데이터의 분포를 반영한 적절한 Validation set 을 찾지 못해, 모델의 일반화 성능을 정확히 평가할 수 없었다.

### 시간 관리와 팀 협업

- 시간 부족으로 다양한 모델 아키텍처 실험 미진행
- 앙상블 기법 적용 실패
- 팀원 간 역할 분담과 지식 공유 부족
- 개인 작업 위주로 진행되어 시너지 효과 미흡

### 기술적 한계

- **Augraphy 라이브러리**: 문서 증강에 특화된 도구를 발견했지만, 충분한 실험 시간 부족
- **클래스 불균형**: 3개 소수 클래스(2.9%, 3.2%, 4.7%)에 대한 대응 전략 미수립
- **유사 클래스 처리**: 의료 문서 간 0.9 이상의 높은 유사도 문제 미해결

## 🚀 한계/교훈을 바탕으로 다음 경진대회에서 시도해보고 싶은 점은 무엇인가?

### 1. EDA 기반 증강 전략

```python
# Test 데이터 분포를 반영한 증강 파이프라인
augmentation_pipeline = A.Compose([
    A.Rotate(limit=90, p=0.5),  # Test의 극단적 회전 반영
    A.RandomBrightnessContrast(
        brightness_limit=0.2,  # Test가 더 밝은 특성 반영
        contrast_limit=0.1,
        p=0.5
    ),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),  # Test의 낮은 선명도 반영
])
```

### 2. Validation 전략 개선

- **Stratified K-Fold**: 클래스 불균형을 고려한 교차 검증
- **Domain Adaptation**: Test 분포를 추정하여 Validation set 구성
- **Pseudo Labeling**: Test 데이터의 고신뢰도 예측을 활용한 학습

### 3. 도메인 특화 기법

이번 대회가 문서 이미지에 관한 대회이다 보니 그 특성을 고려한, 다음과 같은 전처리를 했어야한다고 생각한다.

- Deskewing: 기울어진 문서 자동 보정
- Document Layout Analysis: 문서 구조 분석 활용
- OCR 기반 특징: 텍스트 정보를 보조 특징으로 활용
## 🏁 결론

이번 문서 이미지 분류 대회는 **Computer Vision의 전체 파이프라인을 경험**하는 귀중한 기회였다. 특히 체계적인 EDA와 실험 환경 구축은 큰 성과였지만, 이를 실제 성능 향상으로 연결하지 못한 점은 중요한 교훈이 되었다.

핵심은 **"분석은 실행으로 이어질 때 가치가 있다"** 는 것이다. 아무리 정교한 분석도 모델 개선으로 연결되지 않으면 의미가 없다. 또한 딥러닝 대회에서도 **팀워크와 체계적인 접근**이 개인의 기술력만큼 중요함을 깨달았다.

다음 대회에서는 이번 경험을 바탕으로 분석-실행-검증의 빠른 사이클을 구축하고, 팀원들과 더 긴밀히 협업하여 시너지를 만들어내고 싶다. 특히 EDA에서 발견한 인사이트를 즉시 실험으로 연결하는 민첩성을 갖추고자 한다.

## 🔗 Github Project

- [upstageailab-cv-classification-cv_3](https://github.com/AIBootcamp13/upstageailab-cv-classification-cv_3)