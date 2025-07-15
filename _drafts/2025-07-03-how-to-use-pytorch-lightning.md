---
title: "PyTorch Lightning: 딥러닝 모델 개발을 위한 고수준 프레임워크"
date: 2025-07-03 21:33:00 +0900
categories: 
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- torch==2.0.0+
- pytorch-lightning==2.0.0+
- torchvision==0.15.0+
- tensorboard==2.12.0+
- torchmetrics==0.11.0+
- wandb==0.15.0+

## 🚀 TL;DR

- PyTorch Lightning은 PyTorch의 **보일러플레이트 코드를 제거**하고 **연구와 프로덕션 모두에 적합한** 구조를 제공하는 프레임워크다
- **LightningModule**과 **Trainer**를 중심으로 학습 루프를 추상화하여 코드 재사용성과 가독성을 크게 향상시킨다
- **자동 배치 처리**, **멀티 GPU 학습**, **체크포인트 관리** 등이 내장되어 있어 복잡한 설정 없이 사용 가능하다
- **콜백 시스템**과 **로거 통합**으로 실험 관리와 모니터링이 편리하다
- **Weights & Biases (wandb)** 통합으로 실험 추적, 시각화, 협업이 매우 간편해진다
- 처음부터 모델을 학습하거나 **사전학습된 모델을 파인튜닝**하는 등 다양한 시나리오를 깔끔하게 구현할 수 있다

## 🌩️ PyTorch Lightning이란?

PyTorch Lightning은 PyTorch 코드를 구조화하고 확장 가능하게 만들어주는 고수준 프레임워크다. 연구자와 엔지니어가 **핵심 로직에만 집중**할 수 있도록 반복적인 보일러플레이트 코드를 제거하고, 모범 사례를 자동으로 적용해준다.

일반적인 PyTorch 코드에서는 학습 루프, 검증 루프, 디바이스 할당, 그래디언트 계산 등을 모두 수동으로 작성해야 한다. PyTorch Lightning은 이러한 부분을 **표준화된 인터페이스**로 추상화하여 코드의 재현성과 확장성을 높인다.

```python
# 일반 PyTorch 코드
for epoch in range(num_epochs):
    for batch in train_loader:
        optimizer.zero_grad()
        loss = model(batch)
        loss.backward()
        optimizer.step()
    # 검증, 로깅, 체크포인트 저장 등...

# PyTorch Lightning - 위의 모든 과정이 자동화됨
trainer = Trainer(max_epochs=num_epochs)
trainer.fit(model, train_loader)
```

## 🔧 핵심 컴포넌트

### LightningModule - 모델의 중심

**LightningModule**은 PyTorch의 `nn.Module`을 확장한 클래스로, 모델 아키텍처와 학습 로직을 하나로 묶는다. 모든 학습 관련 코드가 하나의 클래스에 체계적으로 정리되어 있어 관리가 용이하다.

주요 메서드:

- `__init__()`: 모델 레이어 정의
- `forward()`: 순전파 로직
- `training_step()`: 학습 단계 정의
- `validation_step()`: 검증 단계 정의
- `test_step()`: 테스트 단계 정의
- `configure_optimizers()`: 옵티마이저와 스케줄러 설정

```python
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F

class MyModel(pl.LightningModule):
    def __init__(self, input_dim=784, hidden_dim=128, output_dim=10):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log('train_loss', loss)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        acc = (logits.argmax(dim=1) == y).float().mean()
        self.log('val_loss', loss)
        self.log('val_acc', acc)
        
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

- log 함수
	- `self.log()`는 LightningModule에서 제공하는 메서드로, 훈련 과정에서 메트릭을 로깅하고 다양한 로거(Logger)에 자동으로 전송하는 역할을 합니다.
```python
def log(  
    self,  
    name: str,                    # 로깅할 메트릭 이름  
    value: Any,                   # 로깅할 값 (텐서, 숫자, torchmetrics 객체)  
    prog_bar: bool = False,       # 진행 표시줄에 표시할지 여부  
    logger: bool = True,          # 로거에 전송할지 여부  
    on_step: bool | None = None,  # 매 스텝마다 로깅할지 여부
    on_epoch: bool | None = None, # 에포크 끝에 로깅할지 여부
    reduce_fx: str = "mean",      # 분산 학습 시 값을 결합하는 방법  
    enable_graph: bool = False,   # 그래프 추적을 활성화할지 여부  
    sync_dist: bool = False,      # 분산 학습 시 동기화할지 여부  
    sync_dist_group: Any = None,  # 동기화할 프로세스 그룹  
    add_dataloader_idx: bool = True,  # 데이터로더 인덱스를 추가할지 여부  
    batch_size: int | None = None,    # 배치 크기 (가중 평균 계산용)  
    metric_attribute: str | None = None,  # 메트릭 속성 이름  
    rank_zero_only: bool = False,     # rank 0에서만 로깅할지 여부
)
```

### Trainer - 학습의 지휘자

**Trainer**는 실제 학습 과정을 관리하는 핵심 컴포넌트다. 에폭 반복, 배치 처리, 그래디언트 계산, 체크포인트 저장 등 모든 학습 관련 작업을 자동으로 처리한다.

주요 기능:

- **자동 배치 처리**: 데이터로더를 자동으로 순회
- **멀티 GPU/TPU 지원**: 간단한 플래그로 분산 학습 가능
- **자동 혼합 정밀도**: 메모리 효율성과 속도 향상
- **그래디언트 클리핑**: 학습 안정성 향상
- **조기 종료**: 과적합 방지

```python
from pytorch_lightning import Trainer

# 기본 Trainer
trainer = Trainer(
    max_epochs=10,
    accelerator='gpu',  # GPU 사용
    devices=1,          # GPU 개수
    precision=16        # 혼합 정밀도 학습
)

# 고급 설정
trainer = Trainer(
    max_epochs=100,
    accelerator='gpu',
    devices=4,                    # 4개 GPU 사용
    strategy='ddp',               # 분산 데이터 병렬 처리
    precision=16,                 # 16비트 혼합 정밀도
    gradient_clip_val=1.0,        # 그래디언트 클리핑
    accumulate_grad_batches=4,    # 그래디언트 누적
    val_check_interval=0.25,      # 에폭의 25%마다 검증
    log_every_n_steps=10          # 10 스텝마다 로깅
)

# 학습 실행
trainer.fit(model, train_dataloader, val_dataloader)
```

### LightningDataModule - 데이터 관리

**LightningDataModule**은 데이터 준비, 로딩, 변환을 캡슐화한다. 데이터 관련 코드를 모델과 분리하여 재사용성을 높인다.

```python
class MyDataModule(pl.LightningDataModule):
    def __init__(self, data_dir='./data', batch_size=32):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        
    def prepare_data(self):
        # 데이터 다운로드 (단일 프로세스에서만 실행)
        MNIST(self.data_dir, train=True, download=True)
        MNIST(self.data_dir, train=False, download=True)
        
    def setup(self, stage=None):
        # 데이터셋 생성 (각 프로세스에서 실행)
        transform = transforms.ToTensor()
        
        if stage == 'fit' or stage is None:
            mnist_full = MNIST(self.data_dir, train=True, transform=transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])
            
        if stage == 'test' or stage is None:
            self.mnist_test = MNIST(self.data_dir, train=False, transform=transform)
            
    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size, shuffle=True)
    
    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size)
    
    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size)
```

### Callbacks - 학습 과정 커스터마이징

**Callback**은 학습 과정의 특정 시점에 원하는 동작을 추가할 수 있게 해준다. 모델 체크포인트, 조기 종료, 학습률 스케줄링 등이 콜백으로 구현되어 있다.

```python
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor

# 모델 체크포인트 - 최고 성능 모델 저장
checkpoint_callback = ModelCheckpoint(
    monitor='val_loss',
    dirpath='checkpoints/',
    filename='best-model-{epoch:02d}-{val_loss:.2f}',
    save_top_k=3,
    mode='min'
)

# 조기 종료 - 과적합 방지
early_stop_callback = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min'
)

# 학습률 모니터링
lr_monitor = LearningRateMonitor(logging_interval='step')

# Trainer에 콜백 추가
trainer = Trainer(
    callbacks=[checkpoint_callback, early_stop_callback, lr_monitor]
)
```

### Loggers - 실험 추적

**Logger**는 학습 과정의 메트릭, 하이퍼파라미터, 모델 그래프 등을 기록한다. TensorBoard, WandB, MLflow 등 다양한 로깅 도구를 지원한다.

```python
from pytorch_lightning.loggers import TensorBoardLogger, WandbLogger

# TensorBoard 로거
tb_logger = TensorBoardLogger(
    save_dir='logs/',
    name='my_experiment'
)

# Weights & Biases 로거
wandb_logger = WandbLogger(
    project='my_project',
    name='experiment_1'
)

# 여러 로거 동시 사용
trainer = Trainer(
    logger=[tb_logger, wandb_logger]
)
```

[시각적 표현 넣기: PyTorch Lightning 컴포넌트 간의 관계를 보여주는 다이어그램]

## 📊 Weights & Biases (wandb) 통합

Weights & Biases는 머신러닝 실험 추적, 시각화, 협업을 위한 강력한 플랫폼이다. PyTorch Lightning과의 완벽한 통합으로 최소한의 코드 변경으로 강력한 실험 관리 기능을 사용할 수 있다.

### wandb 기본 설정

먼저 wandb를 설치하고 초기화한다.

```python
# 설치
# pip install wandb

import wandb
from pytorch_lightning.loggers import WandbLogger

# wandb 초기화 (처음 사용시 API 키 입력 필요)
wandb.login()

# WandbLogger 생성
wandb_logger = WandbLogger(
    project="my-lightning-project",     # 프로젝트 이름
    name="experiment-1",                # 실행 이름
    save_dir="./wandb",                 # 로컬 저장 디렉토리
    log_model=True,                     # 모델 체크포인트 자동 업로드
    offline=False,                      # 오프라인 모드
    tags=["baseline", "resnet18"],      # 실험 태그
    notes="Initial baseline experiment"  # 실험 설명
)

# Trainer에 로거 연결
trainer = Trainer(
    max_epochs=10,
    logger=wandb_logger
)
```

### 하이퍼파라미터 로깅

wandb는 모델의 하이퍼파라미터를 자동으로 추적하고 비교할 수 있게 해준다.

```python
class MyModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-3, hidden_dim=128, dropout=0.2):
        super().__init__()
        # 하이퍼파라미터 저장 - wandb가 자동으로 로깅
        self.save_hyperparameters()
        
        # 추가 설정 정보 로깅
        wandb.config.update({
            "architecture": "MLP",
            "dataset": "MNIST",
            "optimizer": "Adam"
        })
        
        self.model = nn.Sequential(
            nn.Linear(784, hidden_dim),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(hidden_dim, 10)
        )

# wandb에서 하이퍼파라미터 오버라이드
wandb.init(config={
    "learning_rate": 0.001,
    "hidden_dim": 256,
    "dropout": 0.3
})

model = MyModel(**wandb.config)
```

### 메트릭과 시각화

wandb는 다양한 형태의 데이터를 로깅하고 시각화할 수 있다.

```python
class AdvancedModel(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        
        # 기본 메트릭 로깅
        self.log('train_loss', loss)
        
        # wandb 전용 고급 로깅
        if batch_idx % 100 == 0:
            # 히스토그램 로깅
            wandb.log({
                "gradients": wandb.Histogram(self.fc1.weight.grad.cpu().numpy()),
                "weights": wandb.Histogram(self.fc1.weight.data.cpu().numpy())
            })
            
            # 이미지 로깅
            wandb.log({
                "examples": [wandb.Image(x[i]) for i in range(min(4, len(x)))]
            })
        
        return loss
    
    def validation_epoch_end(self, outputs):
        # 혼동 행렬 생성
        all_preds = []
        all_labels = []
        
        for output in outputs:
            all_preds.extend(output['preds'].cpu().numpy())
            all_labels.extend(output['labels'].cpu().numpy())
        
        # wandb에 혼동 행렬 로깅
        wandb.log({
            "conf_mat": wandb.plot.confusion_matrix(
                probs=None,
                y_true=all_labels,
                preds=all_preds,
                class_names=[str(i) for i in range(10)]
            )
        })
        
    def on_train_epoch_end(self):
        # 커스텀 차트 생성
        epoch_data = [[x, y] for x, y in enumerate(self.train_losses)]
        table = wandb.Table(data=epoch_data, columns=["step", "loss"])
        
        wandb.log({
            "loss_chart": wandb.plot.line(
                table, "step", "loss", title="Training Loss Progress"
            )
        })
```

### 아티팩트 관리

wandb Artifacts를 사용하여 데이터셋, 모델, 결과물을 버전 관리할 수 있다.

```python
# 데이터셋 아티팩트 생성
def create_dataset_artifact():
    artifact = wandb.Artifact('mnist-dataset', type='dataset')
    artifact.add_dir('data/mnist/')
    wandb.log_artifact(artifact)

# 모델 아티팩트 자동 저장
class ModelWithArtifacts(pl.LightningModule):
    def on_train_end(self):
        # 최종 모델을 아티팩트로 저장
        model_artifact = wandb.Artifact(
            f'model-{wandb.run.id}', 
            type='model',
            description='Final trained model',
            metadata={
                'accuracy': self.best_val_acc,
                'epoch': self.current_epoch
            }
        )
        model_artifact.add_file('best_model.ckpt')
        wandb.log_artifact(model_artifact)

# 아티팩트 사용
def load_from_artifact(artifact_name):
    artifact = wandb.use_artifact(artifact_name)
    artifact_dir = artifact.download()
    model = MyModel.load_from_checkpoint(f'{artifact_dir}/model.ckpt')
    return model
```

### 하이퍼파라미터 스윕

wandb Sweeps를 사용하여 자동 하이퍼파라미터 튜닝을 수행할 수 있다.

```python
# sweep_config.yaml
sweep_config = {
    'method': 'bayes',  # grid, random, bayes
    'metric': {
        'name': 'val_loss',
        'goal': 'minimize'
    },
    'parameters': {
        'learning_rate': {
            'min': 0.0001,
            'max': 0.1,
            'distribution': 'log_uniform_values'
        },
        'hidden_dim': {
            'values': [64, 128, 256, 512]
        },
        'dropout': {
            'min': 0.1,
            'max': 0.5
        },
        'batch_size': {
            'values': [32, 64, 128]
        }
    }
}

# Sweep 생성
sweep_id = wandb.sweep(sweep_config, project="my-project")

def train_sweep():
    # wandb가 하이퍼파라미터 제공
    wandb.init()
    
    # 하이퍼파라미터로 모델 생성
    model = MyModel(
        learning_rate=wandb.config.learning_rate,
        hidden_dim=wandb.config.hidden_dim,
        dropout=wandb.config.dropout
    )
    
    # 데이터 모듈 생성
    dm = MyDataModule(batch_size=wandb.config.batch_size)
    
    # WandbLogger 자동 생성됨
    trainer = Trainer(
        max_epochs=10,
        logger=WandbLogger()
    )
    
    trainer.fit(model, dm)

# Sweep 실행
wandb.agent(sweep_id, train_sweep, count=50)  # 50개 실험 실행
```

### 실시간 모니터링과 협업

```python
class CollaborativeModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        # 팀 멤버에게 알림 보내기
        wandb.alert(
            title="Training Started", 
            text=f"New experiment {wandb.run.name} has started"
        )
        
    def on_validation_epoch_end(self):
        # 특정 조건에서 알림
        if self.current_val_acc > 0.95:
            wandb.alert(
                title="High Accuracy Achieved!",
                text=f"Model reached {self.current_val_acc:.2%} accuracy",
                level=wandb.AlertLevel.INFO
            )
            
    def training_step(self, batch, batch_idx):
        # 실시간 메모 추가
        if batch_idx == 0 and self.current_epoch == 5:
            wandb.log({
                "notes": wandb.Html(
                    "<p>Learning rate decay started at epoch 5</p>"
                )
            })
```

### wandb와 PyTorch Lightning 통합 베스트 프랙티스

```python
class ProductionModel(pl.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.save_hyperparameters()
        
        # 모델 아키텍처 정의
        self.model = self._build_model(config)
        
        # 메트릭 추적을 위한 버퍼
        self.validation_step_outputs = []
        
    def on_fit_start(self):
        # 코드 저장
        wandb.save('*.py')
        
        # 환경 정보 로깅
        wandb.log({
            "pytorch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "gpu_count": torch.cuda.device_count()
        })
        
    def training_step(self, batch, batch_idx):
        loss = self._compute_loss(batch)
        
        # 주기적으로 상세 정보 로깅
        if self.global_step % 100 == 0:
            # 학습률 로깅
            lr = self.optimizers().param_groups[0]['lr']
            self.log('learning_rate', lr)
            
            # 메모리 사용량 로깅
            if torch.cuda.is_available():
                self.log('gpu_memory_used', 
                        torch.cuda.memory_allocated() / 1024**3)
                
        return loss
    
    def validation_step(self, batch, batch_idx):
        # 예측 결과 수집
        x, y = batch
        preds = self(x)
        
        # 첫 배치의 예시 저장
        if batch_idx == 0:
            # 예측 시각화
            fig = self._create_prediction_figure(x[:8], y[:8], preds[:8])
            wandb.log({"predictions": wandb.Image(fig)})
            
        self.validation_step_outputs.append({
            'preds': preds,
            'labels': y
        })
        
    def on_validation_epoch_end(self):
        # 에폭 레벨 메트릭 계산
        all_preds = torch.cat([x['preds'] for x in self.validation_step_outputs])
        all_labels = torch.cat([x['labels'] for x in self.validation_step_outputs])
        
        # 다양한 메트릭 계산 및 로깅
        metrics = self._calculate_metrics(all_preds, all_labels)
        wandb.log(metrics)
        
        # 정리
        self.validation_step_outputs.clear()
        
    def configure_optimizers(self):
        # 옵티마이저 설정을 wandb config에서 가져오기
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=wandb.config.learning_rate,
            weight_decay=wandb.config.weight_decay
        )
        
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=wandb.config.max_epochs
        )
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': scheduler,
            'monitor': 'val_loss'
        }

# 통합 실행 예시
if __name__ == "__main__":
    # wandb 실행 초기화
    wandb.init(
        project="lightning-wandb-integration",
        config={
            "learning_rate": 0.001,
            "weight_decay": 0.01,
            "max_epochs": 50,
            "batch_size": 64
        }
    )
    
    # 모델과 데이터 준비
    model = ProductionModel(wandb.config)
    datamodule = MyDataModule(batch_size=wandb.config.batch_size)
    
    # Trainer 설정
    trainer = Trainer(
        max_epochs=wandb.config.max_epochs,
        logger=WandbLogger(log_model='all'),  # 모든 체크포인트 저장
        callbacks=[
            ModelCheckpoint(
                monitor='val_loss',
                save_top_k=3,
                mode='min'
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=5
            )
        ]
    )
    
    # 학습 실행
    trainer.fit(model, datamodule)
    
    # 최종 테스트
    trainer.test(model, datamodule)
    
    # wandb 종료
    wandb.finish()
```

> wandb와 PyTorch Lightning의 조합은 머신러닝 실험을 체계적으로 관리하고 추적하는 가장 효과적인 방법 중 하나다. 실험 재현성, 협업, 그리고 모델 개발 과정의 투명성을 크게 향상시킬 수 있다. {: .prompt-tip}

## 🎯 다양한 학습 시나리오

### 처음부터 모델 학습하기

가장 기본적인 시나리오로, 랜덤 초기화된 가중치에서 시작하여 모델을 학습한다.

```python
import pytorch_lightning as pl
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F

# 1. 모델 정의
class SimpleClassifier(pl.LightningModule):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, num_classes)
        
        # 메트릭 저장용
        self.train_acc = []
        self.val_acc = []
        
    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        
        # 정확도 계산
        pred = logits.argmax(dim=1)
        acc = (pred == y).float().mean()
        
        # 로깅
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        
        # 정확도 계산
        pred = logits.argmax(dim=1)
        acc = (pred == y).float().mean()
        
        # 로깅
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)
        
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-3, weight_decay=0.01)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }

# 2. 데이터 준비
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST('data/', train=True, download=True, transform=transform)
val_dataset = datasets.MNIST('data/', train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=64, num_workers=4)

# 3. 학습 실행
model = SimpleClassifier()

trainer = pl.Trainer(
    max_epochs=10,
    accelerator='gpu' if torch.cuda.is_available() else 'cpu',
    callbacks=[
        ModelCheckpoint(monitor='val_acc', mode='max'),
        EarlyStopping(monitor='val_loss', patience=3)
    ]
)

trainer.fit(model, train_loader, val_loader)

# 4. 테스트
test_results = trainer.test(model, val_loader)
print(f"Test Accuracy: {test_results[0]['val_acc']:.4f}")
```

### 사전학습 모델 활용하기 (Transfer Learning)

사전학습된 모델을 가져와서 새로운 태스크에 맞게 파인튜닝하는 방법이다. 특히 데이터가 적을 때 효과적이다.

```python
import torchvision.models as models
from torchmetrics import Accuracy

class PretrainedClassifier(pl.LightningModule):
    def __init__(self, num_classes=10, learning_rate=1e-3):
        super().__init__()
        self.save_hyperparameters()
        
        # 사전학습된 ResNet18 로드
        self.backbone = models.resnet18(pretrained=True)
        
        # 백본 가중치 고정 (선택사항)
        for param in self.backbone.parameters():
            param.requires_grad = False
            
        # 마지막 레이어만 교체
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, num_classes)
        
        # 메트릭
        self.train_acc = Accuracy(task='multiclass', num_classes=num_classes)
        self.val_acc = Accuracy(task='multiclass', num_classes=num_classes)
        
    def forward(self, x):
        return self.backbone(x)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        
        # 메트릭 업데이트
        preds = torch.argmax(logits, dim=1)
        self.train_acc(preds, y)
        
        self.log('train_loss', loss, on_step=True, on_epoch=True)
        self.log('train_acc', self.train_acc, on_step=True, on_epoch=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        
        # 메트릭 업데이트
        preds = torch.argmax(logits, dim=1)
        self.val_acc(preds, y)
        
        self.log('val_loss', loss, on_epoch=True)
        self.log('val_acc', self.val_acc, on_epoch=True)
        
    def configure_optimizers(self):
        # 파인튜닝할 파라미터만 옵티마이저에 전달
        params_to_update = []
        for name, param in self.named_parameters():
            if param.requires_grad:
                params_to_update.append(param)
                
        optimizer = torch.optim.Adam(params_to_update, lr=self.hparams.learning_rate)
        
        # 학습률 스케줄러
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, 
            mode='min', 
            factor=0.5, 
            patience=2
        )
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }

# 사용 예시
model = PretrainedClassifier(num_classes=10)
trainer = pl.Trainer(max_epochs=5, accelerator='gpu')
trainer.fit(model, train_loader, val_loader)
```

### 점진적 언프리징 (Gradual Unfreezing)

사전학습 모델을 더 효과적으로 파인튜닝하기 위해 레이어를 점진적으로 언프리징하는 전략이다.

```python
class GradualUnfreezingModel(pl.LightningModule):
    def __init__(self, num_classes=10):
        super().__init__()
        self.backbone = models.resnet50(pretrained=True)
        
        # 초기에는 모든 레이어 고정
        self.freeze_backbone()
        
        # 분류 헤드
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
        self.unfreeze_epoch = 3  # 3 에폭 후 언프리징 시작
        
    def freeze_backbone(self):
        """백본 네트워크의 모든 파라미터 고정"""
        for param in self.backbone.parameters():
            param.requires_grad = False
            
        # 분류 헤드는 학습 가능하게 유지
        for param in self.backbone.fc.parameters():
            param.requires_grad = True
            
    def unfreeze_layers(self, num_layers):
        """마지막 num_layers개 레이어 언프리징"""
        # ResNet의 레이어 구조: layer1, layer2, layer3, layer4
        layers = [self.backbone.layer4, self.backbone.layer3, 
                 self.backbone.layer2, self.backbone.layer1]
        
        for i in range(min(num_layers, len(layers))):
            for param in layers[i].parameters():
                param.requires_grad = True
                
    def on_train_epoch_start(self):
        """에폭 시작 시 점진적 언프리징"""
        if self.current_epoch == self.unfreeze_epoch:
            print(f"Epoch {self.current_epoch}: Unfreezing layer4")
            self.unfreeze_layers(1)
        elif self.current_epoch == self.unfreeze_epoch + 2:
            print(f"Epoch {self.current_epoch}: Unfreezing layer3")
            self.unfreeze_layers(2)
        elif self.current_epoch == self.unfreeze_epoch + 4:
            print(f"Epoch {self.current_epoch}: Unfreezing all layers")
            for param in self.backbone.parameters():
                param.requires_grad = True
                
    def configure_optimizers(self):
        # 학습 가능한 파라미터만 옵티마이저에 전달
        params = filter(lambda p: p.requires_grad, self.parameters())
        
        optimizer = torch.optim.Adam(params, lr=1e-3)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
        
        return [optimizer], [scheduler]
```

### 모델 앙상블 구현

여러 모델을 함께 학습하고 예측을 결합하는 앙상블 방법이다.

```python
class EnsembleModel(pl.LightningModule):
    def __init__(self, model_configs, num_classes=10):
        super().__init__()
        self.models = nn.ModuleList()
        
        # 다양한 아키텍처의 모델들 생성
        for config in model_configs:
            if config['type'] == 'resnet18':
                model = models.resnet18(pretrained=True)
                model.fc = nn.Linear(model.fc.in_features, num_classes)
            elif config['type'] == 'efficientnet':
                model = models.efficientnet_b0(pretrained=True)
                model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
            elif config['type'] == 'mobilenet':
                model = models.mobilenet_v2(pretrained=True)
                model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
                
            self.models.append(model)
            
        # 앙상블 가중치 (학습 가능)
        self.ensemble_weights = nn.Parameter(torch.ones(len(self.models)))
        
    def forward(self, x):
        # 각 모델의 예측 수집
        outputs = []
        for model in self.models:
            outputs.append(model(x))
            
        # 가중 평균으로 결합
        weights = F.softmax(self.ensemble_weights, dim=0)
        ensemble_output = torch.zeros_like(outputs[0])
        
        for i, output in enumerate(outputs):
            ensemble_output += weights[i] * output
            
        return ensemble_output
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        
        # 개별 모델 손실 계산
        individual_losses = []
        for model in self.models:
            output = model(x)
            loss = F.cross_entropy(output, y)
            individual_losses.append(loss)
            
        # 앙상블 예측 및 손실
        ensemble_output = self(x)
        ensemble_loss = F.cross_entropy(ensemble_output, y)
        
        # 전체 손실 = 앙상블 손실 + 개별 손실의 평균
        total_loss = ensemble_loss + 0.1 * sum(individual_losses) / len(individual_losses)
        
        # 로깅
        self.log('train_loss', total_loss)
        self.log('ensemble_loss', ensemble_loss)
        
        return total_loss
    
    def configure_optimizers(self):
        # 다른 학습률 적용
        param_groups = [
            {'params': self.ensemble_weights, 'lr': 0.01},
            {'params': self.models.parameters(), 'lr': 0.001}
        ]
        
        optimizer = torch.optim.Adam(param_groups)
        return optimizer

# 사용 예시
model_configs = [
    {'type': 'resnet18'},
    {'type': 'efficientnet'},
    {'type': 'mobilenet'}
]

ensemble = EnsembleModel(model_configs, num_classes=10)
trainer = pl.Trainer(max_epochs=10)
trainer.fit(ensemble, train_loader, val_loader)
```

## 🚀 고급 기능 활용

### 분산 학습 설정

PyTorch Lightning은 다양한 분산 학습 전략을 간단한 설정으로 지원한다.

```python
# 데이터 병렬 처리 (DP)
trainer = Trainer(
    accelerator='gpu',
    devices=4,
    strategy='dp'  # 단일 노드, 다중 GPU
)

# 분산 데이터 병렬 처리 (DDP)
trainer = Trainer(
    accelerator='gpu',
    devices=4,
    strategy='ddp',  # 더 빠르고 확장성 있음
    num_nodes=2      # 멀티 노드 지원
)

# DeepSpeed 통합
trainer = Trainer(
    accelerator='gpu',
    devices=4,
    strategy='deepspeed',
    precision=16
)

# 모델 병렬 처리를 위한 커스텀 설정
class ModelParallelModule(pl.LightningModule):
    def __init__(self):
        super().__init__()
        # 모델을 여러 GPU에 분할
        self.layer1 = nn.Linear(1000, 1000).to('cuda:0')
        self.layer2 = nn.Linear(1000, 1000).to('cuda:1')
        
    def forward(self, x):
        x = self.layer1(x.to('cuda:0'))
        x = self.layer2(x.to('cuda:1'))
        return x
```

### 커스텀 학습 루프

특별한 학습 방법이 필요한 경우 학습 루프를 커스터마이징할 수 있다.

```python
class CustomTrainingLoop(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.automatic_optimization = False  # 자동 최적화 비활성화
        
    def training_step(self, batch, batch_idx):
        opt = self.optimizers()
        
        # 여러 번의 최적화 스텝
        for i in range(3):
            # Forward pass
            loss = self.compute_loss(batch)
            
            # Manual backward
            self.manual_backward(loss)
            
            # Gradient clipping
            self.clip_gradients(opt, gradient_clip_val=0.5, gradient_clip_algorithm="norm")
            
            # Update
            opt.step()
            opt.zero_grad()
            
        # 로깅
        self.log('train_loss', loss)
```

### 메모리 최적화 기법

대규모 모델 학습 시 메모리를 효율적으로 사용하는 방법이다.

```python
# 그래디언트 체크포인팅
class MemoryEfficientModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = models.resnet152()
        
        # 그래디언트 체크포인팅 활성화
        self.model = torch.utils.checkpoint_checkpoint_sequential(
            self.model, 
            segments=4
        )
        
# 혼합 정밀도 학습
trainer = Trainer(
    precision=16,  # FP16 사용
    amp_backend='native'  # PyTorch native AMP
)

# 그래디언트 누적
trainer = Trainer(
    accumulate_grad_batches=4,  # 4배치마다 업데이트
    precision=16
)
```

> PyTorch Lightning은 연구와 프로덕션 모두에서 딥러닝 개발을 가속화하는 강력한 도구다. 보일러플레이트 코드를 제거하고 모범 사례를 자동으로 적용함으로써, 개발자가 모델 아키텍처와 실험 설계에 더 집중할 수 있게 해준다. {: .prompt-tip}

## 📚 실무 활용 팁

### 실험 관리

```python
# 하이퍼파라미터 저장
class ExperimentModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-3, hidden_dim=128, dropout=0.2):
        super().__init__()
        self.save_hyperparameters()  # 자동으로 하이퍼파라미터 저장
        
        # self.hparams.learning_rate로 접근 가능
        self.model = nn.Sequential(
            nn.Linear(784, self.hparams.hidden_dim),
            nn.Dropout(self.hparams.dropout),
            nn.Linear(self.hparams.hidden_dim, 10)
        )

# 체크포인트에서 모델 로드
model = ExperimentModel.load_from_checkpoint(
    'checkpoints/best_model.ckpt',
    learning_rate=0.001  # 하이퍼파라미터 오버라이드 가능
)
```

### 프로덕션 배포

```python
# 모델을 ONNX로 내보내기
model.to_onnx('model.onnx', dummy_input, export_params=True)

# TorchScript로 변환
script = model.to_torchscript()
torch.jit.save(script, "model.pt")

# 추론 모드
model.eval()
model.freeze()  # 파라미터와 배치정규화 고정

with torch.no_grad():
    predictions = model(input_data)
```

> PyTorch Lightning을 마스터하면 딥러닝 프로젝트의 개발 속도를 크게 향상시킬 수 있다. 표준화된 구조와 풍부한 기능을 통해 연구에서 프로덕션까지 일관된 워크플로우를 구축할 수 있다. {: .prompt-tip}