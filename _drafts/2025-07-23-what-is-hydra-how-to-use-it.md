---
title: "🐉 Hydra 로 딥러닝 실험 환경 정복하기: 설정 관리부터 하이퍼파라미터 튜닝까지"
date: 2025-07-23 16:31:00 +0900
categories: 
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- hydra-core==1.3.2
- omegaconf==2.3.0
- pytorch-lightning==2.1.0
- torch==2.1.0
- wandb==0.16.0
- optuna==3.4.0

## 🚀 TL;DR

- **Hydra**는 Facebook Research에서 개발한 **구성 관리 프레임워크**로, 복잡한 딥러닝 실험의 **설정을 체계적으로 관리**할 수 있게 해준다
- **YAML 기반 설정 파일**과 **명령행 오버라이드**를 통해 코드 수정 없이 다양한 실험 조건을 쉽게 변경할 수 있다
- **Config Groups**, **Multirun**, **Sweeps** 등의 기능으로 **하이퍼파라미터 튜닝**과 **실험 관리**를 자동화할 수 있다
- **PyTorch Lightning**과의 완벽한 통합으로 **MLOps 파이프라인** 구축이 용이하다
- **WandB**, **Optuna** 등 다른 ML 도구들과 원활하게 연동되어 **end-to-end 실험 환경**을 제공한다
- 대규모 실험에서 **재현 가능성**과 **추적 가능성**을 보장하여 **연구 효율성**을 크게 향상시킨다

## 📓 실습 Jupyter Notebook

- w.i.p

## 🔧 Hydra란 무엇인가?

**Hydra**는 Facebook Research(현 Meta AI)에서 개발한 **오픈소스 구성 관리 프레임워크**로, 복잡한 애플리케이션의 설정을 체계적으로 관리할 수 있게 해주는 도구다.

특히 **딥러닝 연구**에서는 모델 아키텍처, 하이퍼파라미터, 데이터셋 설정, 훈련 옵션 등 수많은 설정값들을 관리해야 하는데, Hydra는 이런 복잡한 설정들을 **구조화**하고 **자동화**할 수 있는 강력한 솔루션을 제공한다.

> Hydra의 핵심 철학은 **"코드는 변경하지 않고, 설정만 변경해서 다양한 실험을 수행한다"** 는 것이다. 이를 통해 실험의 재현성과 관리 효율성을 크게 향상시킬 수 있다.
{: .prompt-tip}

### 왜 Hydra가 필요한가?

딥러닝 연구에서 흔히 겪는 문제들을 살펴보자:

- **하드코딩된 설정값**: 코드 곳곳에 흩어진 하이퍼파라미터들
- **실험 추적의 어려움**: 어떤 설정으로 어떤 결과가 나왔는지 기억하기 어려움
- **설정 변경의 번거로움**: 작은 변경을 위해 코드를 수정하고 다시 실행
- **하이퍼파라미터 스윕의 복잡성**: 여러 조합을 테스트하기 위한 반복적인 작업
- **팀 협업의 어려움**: 설정을 공유하고 동기화하는 문제

```python
# 전통적인 방식의 문제점
def train_model():
    # 하드코딩된 설정들
    learning_rate = 0.001
    batch_size = 32
    hidden_dim = 256
    dropout = 0.1
    epochs = 100
    
    # 설정을 바꾸려면 코드를 직접 수정해야 함
    model = Model(hidden_dim=hidden_dim, dropout=dropout)
    optimizer = Adam(model.parameters(), lr=learning_rate)
    # ... 훈련 코드
```

Hydra는 이런 문제들을 **구성 기반 접근법**으로 해결한다.

## 🏗️ Hydra의 핵심 구성 요소

Hydra의 아키텍처는 다음과 같은 핵심 구성 요소들로 이루어져 있다:

```mermaid
graph TB
    A[Hydra App] --> B[Config Files]
    A --> C[Decorators]
    A --> D[OmegaConf]
    
    B --> E[Main Config]
    B --> F[Config Groups]
    B --> G[Defaults]
    
    C --> H[@hydra.main]
    C --> I[@hydra.compose]
    
    D --> J[Configuration Object]
    D --> K[Type Safety]
    D --> L[Interpolation]
    
    A --> M[Plugins]
    M --> N[Launcher Plugin]
    M --> O[Sweeper Plugin]
    M --> P[Logger Plugin]
```

### OmegaConf: 설정의 핵심

**OmegaConf** 는 Hydra의 기반이 되는 YAML 기반 구성 라이브러리다. 다음과 같은 특징을 가진다.

- **계층적 구성**: 중첩된 구조로 복잡한 설정 표현
- **타입 안정성**: 런타임에 타입 체크 수행
- **보간(Interpolation)**: 다른 설정값 참조 가능
- **병합**: 여러 설정 파일을 조합

```python
from omegaconf import OmegaConf

# YAML 형태의 설정
config_yaml = """
model:
  name: "ResNet50"
  hidden_dim: 512
  dropout: 0.1

training:
  learning_rate: 0.001
  batch_size: 32
  epochs: 100
  
data:
  dataset: "ImageNet"
  data_dir: "/data/imagenet"
  num_workers: 4

# 보간 사용 예시
logging:
  exp_name: "${model.name}_${training.learning_rate}"
  log_dir: "/logs/${logging.exp_name}"
"""

# OmegaConf 객체로 변환
cfg = OmegaConf.create(OmegaConf.load(config_yaml))

# 접근 방법들
print(cfg.model.hidden_dim)  # 512
print(cfg.logging.exp_name)  # ResNet50_0.001
print(cfg.logging.log_dir)   # /logs/ResNet50_0.001

# 타입 체크
cfg.training.epochs = "invalid"  # ValidationError 발생!
```

### Config Groups: 모듈화된 설정 관리

**Config Groups**는 관련된 설정들을 그룹화하여 모듈화하는 기능이다. 이를 통해 설정의 재사용성과 유지보수성을 높일 수 있다.

```
conf/
├── config.yaml                 # 메인 설정 파일
├── model/                       # 모델 관련 설정 그룹
│   ├── resnet.yaml
│   ├── transformer.yaml
│   └── efficientnet.yaml
├── optimizer/                   # 옵티마이저 설정 그룹
│   ├── adam.yaml
│   ├── sgd.yaml
│   └── adamw.yaml
├── dataset/                     # 데이터셋 설정 그룹
│   ├── imagenet.yaml
│   ├── cifar10.yaml
│   └── custom.yaml
└── experiment/                  # 실험 설정 그룹
    ├── baseline.yaml
    ├── large_model.yaml
    └── debug.yaml
```

```yaml
# conf/model/resnet.yaml
_target_: torchvision.models.resnet50
pretrained: true
num_classes: 1000

# conf/optimizer/adam.yaml
_target_: torch.optim.Adam
lr: 0.001
weight_decay: 1e-4
betas: [0.9, 0.999]

# conf/config.yaml
defaults:
  - model: resnet
  - optimizer: adam
  - dataset: imagenet
  - _self_

# 추가 설정들
training:
  epochs: 100
  save_every: 10
```

## 🚀 Hydra 기본 사용법

### 1. 기본 애플리케이션 설정

Hydra를 사용하는 가장 기본적인 방법은 **`@hydra.main`** 데코레이터를 사용하는 것이다.

```python
import hydra
from omegaconf import DictConfig, OmegaConf
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    # 설정 출력
    print(OmegaConf.to_yaml(cfg))
    
    # 모델 생성 (OmegaConf의 instantiate 기능 활용)
    model = hydra.utils.instantiate(cfg.model)
    
    # 옵티마이저 생성
    optimizer = hydra.utils.instantiate(cfg.optimizer, params=model.parameters())
    
    # 훈련 로직
    train_model(model, optimizer, cfg)

def train_model(model, optimizer, cfg):
    print(f"Training {cfg.model._target_} for {cfg.training.epochs} epochs")
    print(f"Learning rate: {cfg.optimizer.lr}")
    print(f"Batch size: {cfg.training.batch_size}")
    
    # 실제 훈련 코드는 여기에...
    for epoch in range(cfg.training.epochs):
        # 훈련 스텝들...
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{cfg.training.epochs}")

if __name__ == "__main__":
    my_app()
```

### 2. 명령행에서 설정 오버라이드

Hydra의 가장 강력한 기능 중 하나는 **명령행에서 설정을 동적으로 변경**할 수 있다는 것이다.

```bash
# 기본 실행
python train.py

# 하이퍼파라미터 변경
python train.py training.learning_rate=0.01 training.batch_size=64

# 모델 변경
python train.py model=transformer optimizer=adamw

# 여러 설정 동시 변경
python train.py model=efficientnet optimizer.lr=0.005 training.epochs=200

# 새로운 파라미터 추가
python train.py +training.warmup_steps=1000 +model.activation=gelu
```

### 3. Hydra Compose API 사용

**`@hydra.compose`** API를 사용하면 Jupyter Notebook이나 다른 스크립트에서도 Hydra를 활용할 수 있다.

```python
from hydra import compose, initialize
from omegaconf import OmegaConf

# Hydra 초기화
def setup_config():
    with initialize(version_base=None, config_path="conf"):
        # 기본 설정 로드
        cfg = compose(config_name="config")
        
        # 특정 설정으로 오버라이드
        cfg_override = compose(
            config_name="config", 
            overrides=[
                "model=transformer",
                "optimizer.lr=0.01",
                "training.batch_size=128"
            ]
        )
        
        return cfg, cfg_override

# Jupyter Notebook에서 사용 예시
def notebook_experiment():
    cfg, cfg_override = setup_config()
    
    print("기본 설정:")
    print(OmegaConf.to_yaml(cfg))
    
    print("\n오버라이드된 설정:")
    print(OmegaConf.to_yaml(cfg_override))
    
    # 실험 실행
    run_experiment(cfg_override)

def run_experiment(cfg):
    # 모델과 옵티마이저 생성
    model = hydra.utils.instantiate(cfg.model)
    optimizer = hydra.utils.instantiate(cfg.optimizer, params=model.parameters())
    
    print(f"실험 시작: {cfg.model._target_} 모델, LR={cfg.optimizer.lr}")
    # 실제 실험 코드...
```

## 🔤 Hydra 예약어와 특수 기능

Hydra는 설정 파일에서 사용할 수 있는 **다양한 예약어와 특수 기능**을 제공한다. 이러한 예약어들을 이해하면 **더 유연하고 강력한 설정 관리**가 가능해진다.

### 자주 사용하는 핵심 예약어

#### `defaults` - 설정 조합의 핵심

**`defaults`**는 Hydra에서 가장 중요한 예약어로, **다른 설정 파일들을 조합**하여 최종 설정을 만드는 데 사용된다.

```yaml
# config.yaml
defaults:
  - model: bert_base          # conf/model/bert_base.yaml 로드
  - data: glue_cola          # conf/data/glue_cola.yaml 로드  
  - training: full_training   # conf/training/full_training.yaml 로드
  - _self_                   # 현재 파일의 내용 (우선순위 지정)

# 여기서 정의한 값들이 위의 defaults보다 우선순위가 높음
experiment:
  name: my_experiment
```

#### `_self_` - 우선순위 제어

**`_self_`**는 **현재 파일의 설정이 언제 적용될지**를 결정한다. defaults 목록에서의 위치에 따라 우선순위가 달라진다.

```yaml
# _self_가 마지막에 있는 경우 (일반적)
defaults:
  - model: bert_base
  - data: glue_cola
  - _self_                   # 현재 파일이 마지막에 적용됨

model:
  learning_rate: 1e-4        # bert_base.yaml의 learning_rate를 오버라이드

---

# _self_가 처음에 있는 경우
defaults:
  - _self_                   # 현재 파일이 먼저 적용됨
  - model: bert_base         # bert_base.yaml이 현재 파일을 오버라이드

model:
  learning_rate: 1e-4        # bert_base.yaml에 의해 덮어써질 수 있음
```

#### `override` - 강제 오버라이드

**`override`** 키워드는 **명령줄에서 지정한 설정을 강제로 적용**할 때 사용한다.

```yaml
# config.yaml
defaults:
  - model: bert_base
  - override data: glue_cola  # 명령줄에서 data를 지정해도 glue_cola 사용

# 명령줄에서 다음과 같이 실행해도 glue_cola가 사용됨
# python train.py data=glue_sst2  
```

#### `+` (Plus) - 새로운 키 추가

**`+` 접두사**는 **존재하지 않는 새로운 키를 추가**할 때 사용한다.

```bash
# 새로운 설정 키 추가
python train.py +model.use_bias=true +training.save_optimizer=false

# 중첩된 새 키도 추가 가능
python train.py +logging.wandb.tags=[experiment,bert,cola]
```

```yaml
# config.yaml에서도 사용 가능
defaults:
  - model: bert_base
  - +experiment: baseline     # experiment 그룹이 없어도 추가

+new_section:                 # 완전히 새로운 섹션 추가
  custom_param: value
```

#### `~` (Tilde) - 키 삭제

**`~` 접두사**는 **기존 키를 삭제**할 때 사용한다.

```bash
# 특정 키 삭제
python train.py ~training.warmup_steps

# 중첩된 키 삭제
python train.py ~model.dropout ~data.cache_dir
```

```yaml
# config.yaml에서 사용
defaults:
  - model: bert_base
  - ~training: null           # training 그룹 전체 삭제

~unwanted_section: null       # 특정 섹션 삭제
```

### 변수 보간(Interpolation) 기능

#### `${}` - 기본 변수 보간

**`${}`** 구문을 사용하여 **다른 설정 값을 참조**할 수 있다.

```yaml
# config.yaml
model:
  name: bert-base-uncased
  hidden_size: 768

data:
  batch_size: 32
  max_length: 128

experiment:
  name: ${model.name}_${data.batch_size}batch    # "bert-base-uncased_32batch"
  output_dir: ./outputs/${experiment.name}       # "./outputs/bert-base-uncased_32batch"
  
training:
  total_steps: ${eval:${data.dataset_size}//${data.batch_size}*${training.num_epochs}}
```

#### `oc.env` - 환경변수 참조

**환경변수**를 설정에서 직접 사용할 수 있다.

```yaml
# config.yaml
data:
  cache_dir: ${oc.env:DATA_CACHE_DIR,/tmp/cache}  # 환경변수 사용, 기본값 지정
  
logging:
  wandb_api_key: ${oc.env:WANDB_API_KEY}          # 환경변수 필수

model:
  device: ${oc.env:CUDA_VISIBLE_DEVICES,0}        # GPU 지정
```

```bash
# 환경변수 설정 후 실행
export DATA_CACHE_DIR="/shared/cache"
export WANDB_API_KEY="your_api_key"
python train.py
```

#### `now` - 현재 시간 참조

**`now`** 예약어로 **현재 시간을 동적으로 생성**할 수 있다.

```yaml
# config.yaml
experiment:
  name: bert_experiment_${now:%Y%m%d_%H%M%S}      # "bert_experiment_20241225_143022"
  timestamp: ${now:%Y-%m-%d %H:%M:%S}             # "2024-12-25 14:30:22"
  
logging:
  log_file: logs/train_${now:%Y%m%d}.log          # "logs/train_20241225.log"
  
checkpoint:
  save_path: checkpoints/${experiment.name}_${now:%H%M%S}
```

### 고급 예약어 및 기능

#### `??` (Optional) - 선택적 키

**`??` 접미사**는 **키가 존재하지 않아도 오류가 발생하지 않도록** 한다.

```yaml
# config.yaml
model:
  name: ${model_name??bert-base-uncased}          # model_name이 없으면 기본값 사용
  dropout: ${model.dropout??0.1}                 # dropout이 정의되지 않으면 0.1 사용

data:
  custom_dataset_path: ${data.path??}             # path가 없으면 None/null
```

#### `_target_` - 객체 인스턴스화

**`_target_`**은 **Python 클래스나 함수를 동적으로 인스턴스화**할 때 사용한다.

```yaml
# config.yaml
optimizer:
  _target_: torch.optim.AdamW
  lr: ${model.learning_rate}
  weight_decay: 0.01
  
scheduler:
  _target_: torch.optim.lr_scheduler.CosineAnnealingLR
  T_max: ${training.num_epochs}
  
loss_function:
  _target_: torch.nn.CrossEntropyLoss
  label_smoothing: 0.1
```

```python
# Python 코드에서 사용
from hydra.utils import instantiate

@hydra.main(version_base=None, config_path="conf", config_name="config")
def train(cfg: DictConfig) -> None:
    # 설정에서 직접 객체 생성
    optimizer = instantiate(cfg.optimizer, params=model.parameters())
    scheduler = instantiate(cfg.scheduler, optimizer=optimizer)
    criterion = instantiate(cfg.loss_function)
    
    print(type(optimizer))  # <class 'torch.optim.adamw.AdamW'>
```

#### `@package` - 패키지 지정

**`@package`** 지시어는 **설정이 적용될 위치를 지정**한다.

```yaml
# conf/model/bert_with_optimizer.yaml
# @package model
name: bert-base-uncased
learning_rate: 2e-5

# @package optimizer  
_target_: torch.optim.AdamW
lr: ${model.learning_rate}
weight_decay: 0.01
```

```yaml
# conf/experiment/full_config.yaml
# @package _global_
defaults:
  - model: bert_with_optimizer

# 이 파일의 모든 내용이 전역 레벨에 적용됨
experiment_id: exp_001
debug_mode: false
```

### Hydra 자체 설정 예약어

#### `hydra` - Hydra 동작 제어

**`hydra`** 키를 통해 **Hydra 자체의 동작을 제어**할 수 있다.

```yaml
# config.yaml
hydra:
  # 출력 디렉토리 설정
  run:
    dir: outputs/${experiment.name}/${now:%Y-%m-%d}/${now:%H-%M-%S}
  
  # 스위프 설정
  sweep:
    dir: multirun/${experiment.name}/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}
  
  # 로깅 설정
  job_logging:
    level: INFO
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
  
  # 작업 설정
  job:
    chdir: true               # 출력 디렉토리로 이동
    name: ${experiment.name}
```

### 실무 활용 예시

```yaml
# conf/config.yaml - 모든 예약어를 활용한 종합 예시
defaults:
  - _self_
  - model: ${model_type:bert_base}        # 동적 모델 선택
  - data: ${dataset:glue_cola}            # 동적 데이터셋 선택  
  - training: full_training
  - override experiment: ${exp_name:baseline}

# 환경 기반 설정
environment:
  cache_dir: ${oc.env:CACHE_DIR,./cache}
  num_gpus: ${oc.env:CUDA_VISIBLE_DEVICES,0}
  
# 시간 기반 설정
experiment:
  name: ${model.name}_${data.task_name}_${now:%m%d_%H%M}
  output_dir: ${hydra:runtime.output_dir}
  log_file: ${experiment.output_dir}/train_${now:%Y%m%d}.log

# 선택적 고급 설정
advanced:
  model_parallel: ${training.model_parallel??false}
  gradient_checkpointing: ${model.gradient_checkpointing??false}
  
# 동적 객체 생성
optimizer:
  _target_: torch.optim.${training.optimizer_type:AdamW}
  lr: ${model.learning_rate}
  weight_decay: ${training.weight_decay??0.01}

# Hydra 동작 제어
hydra:
  run:
    dir: ./outputs/${experiment.name}
  job:
    chdir: true
    name: ${experiment.name}
```

```bash
# 명령줄에서 동적 설정 변경
python train.py \
  model_type=roberta_large \
  dataset=custom_data \
  +training.use_amp=true \
  ~model.dropout \
  experiment.name="roberta_custom_${now:%m%d}"
```

> Hydra의 예약어들을 효과적으로 활용하면 **설정의 유연성과 재사용성**을 크게 향상시킬 수 있다. 특히 **대규모 실험 환경**에서는 이러한 기능들이 **설정 관리의 복잡성을 크게 줄여준다**.
{: .prompt-tip}

## ⚡ PyTorch Lightning 과의 통합

**PyTorch Lightning** 과 Hydra를 함께 사용하면 더욱 강력한 실험 환경을 구축할 수 있다. Lightning 의 구조화된 코드와 Hydra의 설정 관리가 완벽하게 조화를 이룬다.

### 1. Lightning 모듈과 Hydra 설정

```python
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import hydra
from omegaconf import DictConfig
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import WandbLogger

class LitModel(pl.LightningModule):
    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.cfg = cfg
        self.save_hyperparameters()
        
        # 모델 구성
        self.model = hydra.utils.instantiate(cfg.model)
        self.criterion = hydra.utils.instantiate(cfg.loss)
        
    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        
        # 로깅
        self.log('train_loss', loss, on_step=True, on_epoch=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = (y_hat.argmax(dim=1) == y).float().mean()
        
        self.log('val_loss', loss, on_epoch=True)
        self.log('val_acc', acc, on_epoch=True)
        return loss
    
    def configure_optimizers(self):
        optimizer = hydra.utils.instantiate(
            self.cfg.optimizer, 
            params=self.parameters()
        )
        
        scheduler = None
        if "scheduler" in self.cfg:
            scheduler = hydra.utils.instantiate(
                self.cfg.scheduler, 
                optimizer=optimizer
            )
            return [optimizer], [scheduler]
        
        return optimizer

class LitDataModule(pl.LightningDataModule):
    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.cfg = cfg
        
    def setup(self, stage=None):
        # 데이터셋 로드
        self.train_dataset = hydra.utils.instantiate(self.cfg.dataset.train)
        self.val_dataset = hydra.utils.instantiate(self.cfg.dataset.val)
        
    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.cfg.training.batch_size,
            shuffle=True,
            num_workers=self.cfg.data.num_workers
        )
    
    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.cfg.training.batch_size,
            shuffle=False,
            num_workers=self.cfg.data.num_workers
        )

@hydra.main(version_base=None, config_path="conf", config_name="config")
def train(cfg: DictConfig):
    # 재현 가능성을 위한 시드 설정
    pl.seed_everything(cfg.training.seed, workers=True)
    
    # 데이터 모듈 및 모델 초기화
    datamodule = LitDataModule(cfg)
    model = LitModel(cfg)
    
    # 콜백 설정
    callbacks = []
    
    # 체크포인트 콜백
    if "checkpoint" in cfg:
        checkpoint_callback = ModelCheckpoint(
            dirpath=cfg.checkpoint.dirpath,
            filename=cfg.checkpoint.filename,
            monitor=cfg.checkpoint.monitor,
            mode=cfg.checkpoint.mode,
            save_top_k=cfg.checkpoint.save_top_k
        )
        callbacks.append(checkpoint_callback)
    
    # 조기 종료 콜백
    if "early_stopping" in cfg:
        early_stopping = EarlyStopping(
            monitor=cfg.early_stopping.monitor,
            patience=cfg.early_stopping.patience,
            mode=cfg.early_stopping.mode
        )
        callbacks.append(early_stopping)
    
    # 로거 설정
    logger = None
    if "logger" in cfg:
        logger = hydra.utils.instantiate(cfg.logger)
    
    # 트레이너 설정
    trainer = pl.Trainer(
        max_epochs=cfg.training.max_epochs,
        accelerator=cfg.training.accelerator,
        devices=cfg.training.devices,
        callbacks=callbacks,
        logger=logger,
        deterministic=True
    )
    
    # 훈련 시작
    trainer.fit(model, datamodule)
    
    # 테스트 (선택적)
    if "test" in cfg and cfg.test.run:
        trainer.test(model, datamodule)

if __name__ == "__main__":
    train()
```

### 2. Lightning 전용 설정 파일

```yaml
# conf/config.yaml
defaults:
  - model: resnet50
  - optimizer: adam
  - scheduler: cosine
  - dataset: imagenet
  - logger: wandb
  - callbacks: default
  - _self_

# 훈련 설정
training:
  max_epochs: 100
  batch_size: 32
  seed: 42
  accelerator: gpu
  devices: 1

# 데이터 설정
data:
  num_workers: 4
  pin_memory: true

# 체크포인트 설정
checkpoint:
  dirpath: "./checkpoints"
  filename: "{epoch:02d}-{val_loss:.2f}"
  monitor: "val_loss"
  mode: "min"
  save_top_k: 3

# 조기 종료 설정
early_stopping:
  monitor: "val_loss"
  patience: 10
  mode: "min"
```

```yaml
# conf/logger/wandb.yaml
_target_: pytorch_lightning.loggers.WandbLogger
project: "my-dl-project"
name: "${model._target_}_${optimizer.lr}"
save_dir: "./logs"
log_model: true

# conf/callbacks/default.yaml
model_checkpoint:
  _target_: pytorch_lightning.callbacks.ModelCheckpoint
  monitor: "val_acc"
  mode: "max"
  save_top_k: 1
  filename: "best-{epoch:02d}-{val_acc:.3f}"

learning_rate_monitor:
  _target_: pytorch_lightning.callbacks.LearningRateMonitor
  logging_interval: "step"
```

## 🔄 Multirun 과 하이퍼파라미터 스윕

Hydra 의 **Multirun** 기능을 사용하면 여러 설정 조합을 자동으로 실행할 수 있다. 이는 하이퍼파라미터 튜닝이나 모델 비교 실험에 매우 유용하다.

### 1. 기본 Multirun 사용법

```bash
# 여러 학습률로 실험
python train.py -m optimizer.lr=0.001,0.01,0.1

# 여러 모델과 옵티마이저 조합
python train.py -m model=resnet50,transformer optimizer=adam,sgd

# 범위 지정
python train.py -m training.batch_size=range(16,129,16)

# 다양한 조합
python train.py -m model=resnet50,efficientnet optimizer.lr=0.001,0.01 training.batch_size=32,64
```

### 2. Optuna 를 이용한 고급 하이퍼파라미터 최적화

```python
# conf/config.yaml에 추가
defaults:
  - override hydra/sweeper: optuna

hydra:
  sweeper:
    sampler:
      _target_: optuna.samplers.TPESampler
      seed: 42
    direction: maximize
    study_name: model_optimization
    storage: null
    n_trials: 100
    n_jobs: 1
    
    params:
      optimizer.lr: interval(0.0001, 0.1)
      training.batch_size: choice(16, 32, 64, 128)
      model.hidden_dim: range(128, 1024, step=128)
      training.dropout: uniform(0.1, 0.5)
```

```python
# Optuna 최적화를 위한 목적 함수 수정
@hydra.main(version_base=None, config_path="conf", config_name="config")
def train_optuna(cfg: DictConfig):
    # Lightning 훈련 코드 (이전과 동일)
    datamodule = LitDataModule(cfg)
    model = LitModel(cfg)
    
    trainer = pl.Trainer(
        max_epochs=cfg.training.max_epochs,
        accelerator=cfg.training.accelerator,
        devices=cfg.training.devices,
        enable_checkpointing=False,  # Optuna에서는 체크포인트 비활성화
        logger=False,  # 로깅도 비활성화 (선택적)
    )
    
    trainer.fit(model, datamodule)
    
    # Optuna에 반환할 메트릭 (최대화할 값)
    return trainer.callback_metrics["val_acc"].item()

# 실행
# python train.py -m hydra/sweeper=optuna
```

### 3. 병렬 실행과 자원 관리

```yaml
# conf/config.yaml - 병렬 실행 설정
defaults:
  - override hydra/launcher: joblib

hydra:
  launcher:
    n_jobs: 4  # 병렬 작업 수
    batch_size: 2  # 배치 크기
    
  # 또는 SLURM 사용시
  # launcher:
  #   _target_: hydra_plugins.hydra_submitit_launcher.submitit_launcher.SlurmLauncher
  #   timeout_min: 60
  #   cpus_per_task: 4
  #   gpus_per_node: 1
```

## 🔧 고급 기능과 실무 활용

### 1. 실험 추적과 결과 관리

```python
import wandb
from hydra.core.hydra_config import HydraConfig

@hydra.main(version_base=None, config_path="conf", config_name="config")
def train_with_tracking(cfg: DictConfig):
    # Hydra 실행 정보 가져오기
    hydra_cfg = HydraConfig.get()
    output_dir = hydra_cfg.runtime.output_dir
    
    # WandB 초기화 (설정 정보 포함)
    wandb.init(
        project=cfg.logger.project,
        config=OmegaConf.to_container(cfg, resolve=True),
        dir=output_dir
    )
    
    # 모델 및 훈련 설정
    model = LitModel(cfg)
    datamodule = LitDataModule(cfg)
    
    # WandB 로거 설정
    wandb_logger = WandbLogger(
        project=cfg.logger.project,
        save_dir=output_dir,
        log_model=True
    )
    
    trainer = pl.Trainer(
        max_epochs=cfg.training.max_epochs,
        logger=wandb_logger,
        callbacks=[
            ModelCheckpoint(
                dirpath=f"{output_dir}/checkpoints",
                filename="best-{epoch:02d}-{val_acc:.3f}",
                monitor="val_acc",
                mode="max",
                save_top_k=1
            )
        ]
    )
    
    # 훈련 시작
    trainer.fit(model, datamodule)
    
    # 최고 성능 로깅
    best_score = trainer.callback_metrics["val_acc"].item()
    wandb.log({"best_val_acc": best_score})
    
    # 모델 아티팩트 저장
    wandb.save(f"{output_dir}/checkpoints/*")
    
    wandb.finish()
    return best_score
```

### 2. 구조화된 설정(Structured Configs)

**Structured Configs**를 사용하면 타입 안정성과 IDE 지원을 받을 수 있다.

```python
from dataclasses import dataclass
from typing import Optional, List
from hydra.core.config_store import ConfigStore

@dataclass
class ModelConfig:
    name: str
    hidden_dim: int
    num_layers: int
    dropout: float
    activation: str = "relu"

@dataclass
class OptimizerConfig:
    name: str
    lr: float
    weight_decay: float = 1e-4
    betas: List[float] = None

@dataclass
class TrainingConfig:
    max_epochs: int
    batch_size: int
    seed: int = 42
    accelerator: str = "gpu"
    devices: int = 1

@dataclass
class Config:
    model: ModelConfig
    optimizer: OptimizerConfig
    training: TrainingConfig
    
    # 선택적 설정들
    scheduler: Optional[dict] = None
    callbacks: Optional[dict] = None

# Config Store에 등록
cs = ConfigStore.instance()

# 기본 설정 등록
cs.store(name="base_config", node=Config)

# 특정 모델 설정들
cs.store(group="model", name="resnet50", node=ModelConfig(
    name="resnet50",
    hidden_dim=2048,
    num_layers=50,
    dropout=0.1
))

cs.store(group="model", name="transformer", node=ModelConfig(
    name="transformer",
    hidden_dim=512,
    num_layers=6,
    dropout=0.1,
    activation="gelu"
))

# 옵티마이저 설정들
cs.store(group="optimizer", name="adam", node=OptimizerConfig(
    name="adam",
    lr=0.001,
    betas=[0.9, 0.999]
))

@hydra.main(version_base=None, config_path=None, config_name="base_config")
def my_structured_app(cfg: Config) -> None:
    # 타입 힌트와 자동 완성 지원!
    print(f"Model: {cfg.model.name}")
    print(f"Hidden dim: {cfg.model.hidden_dim}")
    print(f"Learning rate: {cfg.optimizer.lr}")
    
    # 유효성 검사 자동 수행
    assert cfg.training.batch_size > 0
    assert cfg.model.dropout >= 0.0 and cfg.model.dropout <= 1.0
```

### 3. 플러그인 시스템 활용

```python
# Custom Sweeper Plugin 예시
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra._internal.utils import create_config_search_path
from omegaconf import DictConfig

class CustomRandomSweeper(Sweeper):
    def __init__(self, max_trials: int = 10):
        self.max_trials = max_trials
    
    def sweep(self, arguments):
        # 사용자 정의 스윕 로직
        import random
        
        results = []
        for i in range(self.max_trials):
            # 랜덤 하이퍼파라미터 생성
            random_lr = random.uniform(0.0001, 0.1)
            random_batch = random.choice([16, 32, 64, 128])
            
            overrides = [
                f"optimizer.lr={random_lr}",
                f"training.batch_size={random_batch}"
            ]
            
            result = self.launcher.launch(arguments + overrides)
            results.extend(result)
            
        return results

# 플러그인 등록
Plugins.instance().register(CustomRandomSweeper)
```

## 📊 실무 베스트 프랙티스

### 1. 프로젝트 구조

```
project/
├── conf/                          # Hydra 설정 파일들
│   ├── config.yaml                # 메인 설정
│   ├── model/                     # 모델 설정들
│   │   ├── resnet.yaml
│   │   ├── transformer.yaml
│   │   └── efficientnet.yaml
│   ├── optimizer/                 # 옵티마이저 설정들
│   │   ├── adam.yaml
│   │   ├── sgd.yaml
│   │   └── adamw.yaml
│   ├── dataset/                   # 데이터셋 설정들
│   │   ├── imagenet.yaml
│   │   ├── cifar10.yaml
│   │   └── custom.yaml
│   ├── experiment/                # 실험별 설정들
│   │   ├── baseline.yaml
│   │   ├── ablation_study.yaml
│   │   └── production.yaml
│   └── hydra/                     # Hydra 자체 설정
│       ├── launcher/
│       └── sweeper/
├── src/                           # 소스 코드
│   ├── models/
│   ├── data/
│   ├── utils/
│   └── train.py
├── outputs/                       # Hydra 출력 (자동 생성)
├── multirun/                      # Multirun 결과 (자동 생성)
├── notebooks/                     # 실험용 노트북
└── scripts/                       # 실행 스크립트들
```

### 2. 설정 파일 작성 규칙

```yaml
# conf/config.yaml - 메인 설정 파일
defaults:
  - model: resnet50
  - optimizer: adam
  - dataset: imagenet
  - experiment: baseline
  - override hydra/launcher: basic
  - _self_

# 전역 설정
seed: 42
debug: false

# 하이드라 자체 설정
hydra:
  run:
    dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
  job:
    chdir: true  # 출력 디렉토리로 작업 디렉토리 변경
```

```yaml
# conf/experiment/baseline.yaml - 실험별 설정
# @package _global_

defaults:
  - override /model: resnet50
  - override /optimizer: adam

# 실험 특화 설정들
model:
  pretrained: true
  num_classes: 1000

training:
  max_epochs: 100
  batch_size: 32

optimizer:
  lr: 0.001
  weight_decay: 1e-4

# 실험 메타데이터
experiment:
  name: "baseline_resnet50"
  description: "Basic ResNet50 baseline experiment"
  tags: ["baseline", "resnet", "imagenet"]
```

### 3. 로깅 및 모니터링 통합

```python
import hydra
from omegaconf import DictConfig, OmegaConf
import wandb
import mlflow
from pathlib import Path

@hydra.main(version_base=None, config_path="conf", config_name="config")
def train_with_full_tracking(cfg: DictConfig):
    # 출력 디렉토리 설정
    output_dir = Path.cwd()
    
    # 설정 저장
    with open(output_dir / "config.yaml", "w") as f:
        OmegaConf.save(cfg, f)
    
    # 멀티 로거 설정
    loggers = []
    
    # WandB 로거
    if "wandb" in cfg.logging:
        wandb.init(
            project=cfg.logging.wandb.project,
            name=cfg.experiment.name,
            config=OmegaConf.to_container(cfg, resolve=True),
            dir=str(output_dir),
            tags=cfg.experiment.tags
        )
        loggers.append(WandbLogger())
    
    # MLflow 로거
    if "mlflow" in cfg.logging:
        mlflow.set_experiment(cfg.logging.mlflow.experiment_name)
        mlflow.start_run(run_name=cfg.experiment.name)
        mlflow.log_params(OmegaConf.to_container(cfg, resolve=True))
        loggers.append(MLFlowLogger())
    
    # 모델 및 훈련
    model = LitModel(cfg)
    datamodule = LitDataModule(cfg)
    
    trainer = pl.Trainer(
        max_epochs=cfg.training.max_epochs,
        logger=loggers,
        callbacks=setup_callbacks(cfg, output_dir),
        **cfg.trainer
    )
    
    trainer.fit(model, datamodule)
    
    # 결과 저장
    results = {
        "best_val_acc": trainer.callback_metrics.get("val_acc", 0.0).item(),
        "final_train_loss": trainer.callback_metrics.get("train_loss", 0.0).item()
    }
    
    # 결과 로깅
    with open(output_dir / "results.yaml", "w") as f:
        OmegaConf.save(results, f)
    
    if wandb.run:
        wandb.log(results)
        wandb.finish()
    
    if mlflow.active_run():
        mlflow.log_metrics(results)
        mlflow.end_run()
    
    return results["best_val_acc"]

def setup_callbacks(cfg: DictConfig, output_dir: Path):
    callbacks = []
    
    # 모델 체크포인트
    if "checkpoint" in cfg:
        callbacks.append(
            ModelCheckpoint(
                dirpath=output_dir / "checkpoints",
                **cfg.checkpoint
            )
        )
    
    # 조기 종료
    if "early_stopping" in cfg:
        callbacks.append(EarlyStopping(**cfg.early_stopping))
    
    # 학습률 모니터링
    callbacks.append(LearningRateMonitor(logging_interval="step"))
    
    return callbacks
```

### 4. CI/CD 통합

```yaml
# .github/workflows/ml_pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run unit tests
      run: |
        pytest tests/
    
    - name: Test config validation
      run: |
        python -c "
        import hydra
        from omegaconf import DictConfig
        
        @hydra.main(version_base=None, config_path='conf', config_name='config')
        def test_config(cfg: DictConfig):
            print('Config validation passed!')
            return cfg
        
        test_config()
        "
    
    - name: Run quick training test
      run: |
        python train.py experiment=debug training.max_epochs=1 training.batch_size=2
```

> Hydra를 실무에서 효과적으로 활용하려면 **일관된 설정 구조**, **명확한 명명 규칙**, **적절한 문서화**가 필수다. 특히 팀 프로젝트에서는 설정 파일의 변경 사항을 버전 관리하고, 실험 결과를 체계적으로 추적하는 것이 중요하다.
{: .prompt-tip}

## 🚨 주의사항과 트러블슈팅

### 1. 일반적인 문제와 해결책

```python
# 문제 1: Config 경로 문제
# 해결: 절대 경로 또는 상대 경로 명확히 설정
@hydra.main(version_base=None, config_path="../conf", config_name="config")

# 문제 2: Working Directory 변경
# 해결: hydra.job.chdir 설정 확인
hydra:
  job:
    chdir: false  # 작업 디렉토리 변경 비활성화

# 문제 3: Multirun 시 메모리 부족
# 해결: n_jobs 조정 및 배치 크기 제한
hydra:
  launcher:
    n_jobs: 2  # 병렬 작업 수 줄이기
    batch_size: 1
```

### 2. 성능 최적화

```python
# Config 로딩 최적화
from hydra import compose, initialize_config_store
from hydra.core.global_hydra import GlobalHydra

def optimized_config_loading():
    # Global Hydra 인스턴스 재사용
    if not GlobalHydra().is_initialized():
        initialize_config_store(config_path="conf")
    
    # 설정 캐싱
    cfg = compose(config_name="config")
    return cfg

# 대용량 설정 처리
def handle_large_configs(cfg: DictConfig):
    # 지연 로딩 활용
    if hasattr(cfg.dataset, '_target_'):
        dataset = hydra.utils.instantiate(cfg.dataset, _partial_=True)
        # 필요할 때만 실제 로딩
        actual_dataset = dataset()
```

### 3. 디버깅 팁

```python
# 설정 디버깅을 위한 유틸리티
def debug_config(cfg: DictConfig):
    print("=== Config Debug Info ===")
    print(f"Config keys: {list(cfg.keys())}")
    print(f"Config type: {type(cfg)}")
    
    # 해결된 설정 출력
    resolved_cfg = OmegaConf.to_container(cfg, resolve=True)
    print("Resolved config:")
    print(OmegaConf.to_yaml(resolved_cfg))
    
    # 보간 오류 체크
    try:
        OmegaConf.to_container(cfg, resolve=True, throw_on_missing=True)
        print("✅ No interpolation errors")
    except Exception as e:
        print(f"❌ Interpolation error: {e}")

# 실행 중 설정 변경 추적
def track_config_changes(cfg: DictConfig, step: str):
    config_hash = hash(str(OmegaConf.to_yaml(cfg)))
    print(f"Config hash at {step}: {config_hash}")
```

> Hydra를 사용할 때는 **설정 파일의 변경 사항을 Git으로 추적**하고, **실험 결과와 설정을 함께 저장**하는 것이 중요하다. 또한 **대규모 팀에서는 설정 스키마를 문서화**하여 일관성을 유지해야 한다.
{: .prompt-warning}

Hydra는 딥러닝 연구의 복잡한 설정 관리를 해결하는 강력한 도구다. PyTorch Lightning과 함께 사용하면 **재현 가능하고 확장 가능한 실험 환경**을 구축할 수 있으며, **체계적인 하이퍼파라미터 튜닝**과 **효율적인 실험 관리**가 가능하다. 특히 **대규모 연구 프로젝트**나 **프로덕션 환경**에서 그 진가를 발휘한다.