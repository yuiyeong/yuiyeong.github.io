---
title: PyTorch Custom Dataset 구현 가이드
date: 2025-07-05 20:22:00 +0900
categories: 
tags:
  - 급발진거북이
toc: true
comments: false
mermaid: true
math: true
---
## 📦 필수 구현 함수

PyTorch의 `torch.utils.data.Dataset`을 상속받아 커스텀 데이터셋을 만들 때 **반드시 구현해야 하는 함수**는 다음 2개입니다:

### 1. `__len__` 메서드

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

### 2. `__getitem__` 메서드

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

## 🔧 자주 구현되는 부가적인 함수들

### 1. `__init__` 생성자

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

### 2. `__repr__` 메서드

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

### 3. 클래스 정보 관련 메서드들

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

### 4. 데이터 분할 관련 메서드들

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

### 5. 통계 정보 메서드들

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

## 🎯 완전한 구현 예시

```python
import os
import torch
import pandas as pd
from PIL import Image
from typing import Any, Optional, Callable, Tuple, List, Dict
from torch.utils.data import Dataset
from collections import Counter
import numpy as np

class ImageClassificationDataset(Dataset):
    def __init__(
        self,
        csv_file: str,
        img_dir: str,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        class_to_idx: Optional[Dict[str, int]] = None
    ) -> None:
        """
        이미지 분류를 위한 커스텀 데이터셋
        
        Args:
            csv_file (str): 이미지 파일명과 레이블이 있는 CSV 파일 경로
            img_dir (str): 이미지들이 저장된 디렉토리 경로
            transform (Optional[Callable]): 이미지에 적용할 변환
            target_transform (Optional[Callable]): 레이블에 적용할 변환
            class_to_idx (Optional[Dict[str, int]]): 클래스명-인덱스 매핑
        """
        super().__init__()
        
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        
        # CSV 데이터 로딩
        self.data_frame = pd.read_csv(csv_file)
        
        # 클래스 정보 설정
        if class_to_idx is None:
            self.classes = sorted(self.data_frame['label'].unique().tolist())
            self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}
        else:
            self.class_to_idx = class_to_idx
            self.classes = list(class_to_idx.keys())
        
        self.idx_to_class = {idx: cls_name for cls_name, idx in self.class_to_idx.items()}
    
    def __len__(self) -> int:
        """데이터셋 크기 반환"""
        return len(self.data_frame)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        인덱스에 해당하는 (이미지, 레이블) 반환
        
        Args:
            idx (int): 데이터 인덱스
            
        Returns:
            Tuple[torch.Tensor, int]: (변환된 이미지, 레이블 인덱스)
        """
        if idx >= len(self.data_frame):
            raise IndexError(f"Index {idx} out of range for dataset of size {len(self.data_frame)}")
        
        # 이미지 로딩
        img_name = self.data_frame.iloc[idx]['filename']
        img_path = os.path.join(self.img_dir, img_name)
        image = Image.open(img_path).convert('RGB')
        
        # 레이블 가져오기
        label_name = self.data_frame.iloc[idx]['label']
        label = self.class_to_idx[label_name]
        
        # 변환 적용
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
            
        return image, label
    
    def __repr__(self) -> str:
        """데이터셋 정보 문자열 표현"""
        head = f"Dataset {self.__class__.__name__}"
        body = [
            f"Number of datapoints: {self.__len__()}",
            f"Image directory: {self.img_dir}",
            f"Number of classes: {self.num_classes}",
            f"Classes: {self.classes}",
            f"Transforms: {self.transform}",
            f"Target transforms: {self.target_transform}"
        ]
        lines = [head] + [" " * 4 + line for line in body]
        return '\n'.join(lines)
    
    def get_classes(self) -> List[str]:
        """클래스 이름 목록 반환"""
        return self.classes.copy()
    
    def get_class_to_idx(self) -> Dict[str, int]:
        """클래스명-인덱스 매핑 반환"""
        return self.class_to_idx.copy()
    
    @property
    def num_classes(self) -> int:
        """클래스 개수 반환"""
        return len(self.classes)
    
    def get_label_distribution(self) -> Dict[str, int]:
        """각 클래스별 샘플 개수 반환"""
        label_counts = Counter(self.data_frame['label'])
        return dict(label_counts)
    
    def get_sample_weights(self) -> torch.Tensor:
        """클래스 불균형 해결을 위한 샘플 가중치 계산"""
        label_counts = self.get_label_distribution()
        total_samples = len(self.data_frame)
        
        # 각 클래스의 가중치 = 1 / (클래스별 샘플 수 / 전체 샘플 수)
        class_weights = {
            label: total_samples / (len(self.classes) * count) 
            for label, count in label_counts.items()
        }
        
        # 각 샘플의 가중치
        sample_weights = [
            class_weights[self.data_frame.iloc[i]['label']] 
            for i in range(len(self.data_frame))
        ]
        
        return torch.tensor(sample_weights, dtype=torch.float)
    
    def split_dataset(
        self, 
        train_ratio: float = 0.8,
        stratify: bool = True,
        random_seed: Optional[int] = None
    ) -> Tuple['ImageClassificationDataset', 'ImageClassificationDataset']:
        """
        데이터셋을 훈련용과 검증용으로 분할
        
        Args:
            train_ratio (float): 훈련 데이터 비율
            stratify (bool): 클래스 비율을 유지할지 여부
            random_seed (Optional[int]): 랜덤 시드
            
        Returns:
            Tuple[ImageClassificationDataset, ImageClassificationDataset]: (훈련용, 검증용)
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        if stratify:
            # 클래스별로 분할
            train_indices = []
            val_indices = []
            
            for class_name in self.classes:
                class_indices = self.data_frame[self.data_frame['label'] == class_name].index.tolist()
                np.random.shuffle(class_indices)
                
                split_point = int(len(class_indices) * train_ratio)
                train_indices.extend(class_indices[:split_point])
                val_indices.extend(class_indices[split_point:])
        else:
            # 전체 데이터를 랜덤 분할
            indices = list(range(len(self.data_frame)))
            np.random.shuffle(indices)
            split_point = int(len(indices) * train_ratio)
            train_indices = indices[:split_point]
            val_indices = indices[split_point:]
        
        # 서브셋 생성
        train_dataset = self.get_subset(train_indices)
        val_dataset = self.get_subset(val_indices)
        
        return train_dataset, val_dataset
    
    def get_subset(self, indices: List[int]) -> 'ImageClassificationDataset':
        """주어진 인덱스들에 해당하는 서브셋 반환"""
        subset_dataset = ImageClassificationDataset.__new__(ImageClassificationDataset)
        
        # 기본 속성 복사
        subset_dataset.img_dir = self.img_dir
        subset_dataset.transform = self.transform
        subset_dataset.target_transform = self.target_transform
        subset_dataset.classes = self.classes.copy()
        subset_dataset.class_to_idx = self.class_to_idx.copy()
        subset_dataset.idx_to_class = self.idx_to_class.copy()
        
        # 서브셋 데이터프레임 생성
        subset_dataset.data_frame = self.data_frame.iloc[indices].reset_index(drop=True)
        
        return subset_dataset

# 사용 예시
if __name__ == "__main__":
    # 데이터셋 생성
    dataset = ImageClassificationDataset(
        csv_file="data/labels.csv",
        img_dir="data/images/",
        transform=None
    )
    
    # 기본 정보 출력
    print(dataset)
    print(f"\n클래스 분포: {dataset.get_label_distribution()}")
    
    # 데이터 분할
    train_dataset, val_dataset = dataset.split_dataset(train_ratio=0.8, random_seed=42)
    print(f"\n훈련 데이터: {len(train_dataset)}개")
    print(f"검증 데이터: {len(val_dataset)}개")
    
    # 샘플 데이터 확인
    image, label = dataset[0]
    print(f"\n첫 번째 샘플 - 레이블: {label} ({dataset.idx_to_class[label]})")
```

> **핵심 포인트**: `__len__`과 `__getitem__`만 구현하면 기본 동작은 하지만, 실무에서는 위의 부가적인 메서드들을 구현해야 데이터셋을 효율적으로 관리하고 디버깅할 수 있다. {: .prompt-tip}

> **주의사항**: `__getitem__`에서 인덱스 범위 검사를 하고, 적절한 에러 메시지와 함께 예외를 발생시키는 것이 좋다. 또한 멀티프로세싱 환경에서 안전하게 작동하도록 스레드 안전성을 고려해야 한다. {: .prompt-warning}

## 🔧 업데이트된 완전한 구현 예시

**Python 3.9+** 에서는 `typing` 모듈의 제네릭 타입들을 기본 내장 타입으로 대체할 수 있고, **Python 3.10+** 에서는 `Optional`과 `Union`을 `|` 연산자로 대체할 수 있습니다.

### 주요 변화사항

```python
# Python 3.8 이하 (기존 방식)
from typing import List, Dict, Tuple, Optional, Union, Callable, Any

# Python 3.9+ (새로운 방식)
from typing import Callable, Any  # 이것들만 import 필요
# List[str] → list[str]
# Dict[str, int] → dict[str, int] 
# Tuple[str, int] → tuple[str, int]

# Python 3.10+ (더 간단해짐)
# Optional[str] → str | None
# Union[str, int] → str | int
```

### 실제 구현

```python
import os
import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from collections import Counter
import numpy as np
from typing import Callable, Any  # 필요한 것만 import

class ImageClassificationDataset(Dataset):
    def __init__(
        self,
        csv_file: str,
        img_dir: str,
        transform: Callable | None = None,  # Optional[Callable] → Callable | None
        target_transform: Callable | None = None,
        class_to_idx: dict[str, int] | None = None  # Optional[Dict[str, int]] → dict[str, int] | None
    ) -> None:
        """
        이미지 분류를 위한 커스텀 데이터셋
        
        Args:
            csv_file (str): 이미지 파일명과 레이블이 있는 CSV 파일 경로
            img_dir (str): 이미지들이 저장된 디렉토리 경로
            transform (Callable | None): 이미지에 적용할 변환
            target_transform (Callable | None): 레이블에 적용할 변환
            class_to_idx (dict[str, int] | None): 클래스명-인덱스 매핑
        """
        super().__init__()
        
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        
        # CSV 데이터 로딩
        self.data_frame = pd.read_csv(csv_file)
        
        # 클래스 정보 설정
        if class_to_idx is None:
            self.classes = sorted(self.data_frame['label'].unique().tolist())
            self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}
        else:
            self.class_to_idx = class_to_idx
            self.classes = list(class_to_idx.keys())
        
        self.idx_to_class = {idx: cls_name for cls_name, idx in self.class_to_idx.items()}
    
    def __len__(self) -> int:
        """데이터셋 크기 반환"""
        return len(self.data_frame)
    
    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:  # Tuple[torch.Tensor, int] → tuple[torch.Tensor, int]
        """
        인덱스에 해당하는 (이미지, 레이블) 반환
        
        Args:
            idx (int): 데이터 인덱스
            
        Returns:
            tuple[torch.Tensor, int]: (변환된 이미지, 레이블 인덱스)
        """
        if idx >= len(self.data_frame):
            raise IndexError(f"Index {idx} out of range for dataset of size {len(self.data_frame)}")
        
        # 이미지 로딩
        img_name = self.data_frame.iloc[idx]['filename']
        img_path = os.path.join(self.img_dir, img_name)
        image = Image.open(img_path).convert('RGB')
        
        # 레이블 가져오기
        label_name = self.data_frame.iloc[idx]['label']
        label = self.class_to_idx[label_name]
        
        # 변환 적용
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
            
        return image, label
    
    def __repr__(self) -> str:
        """데이터셋 정보 문자열 표현"""
        head = f"Dataset {self.__class__.__name__}"
        body = [
            f"Number of datapoints: {self.__len__()}",
            f"Image directory: {self.img_dir}",
            f"Number of classes: {self.num_classes}",
            f"Classes: {self.classes}",
            f"Transforms: {self.transform}",
            f"Target transforms: {self.target_transform}"
        ]
        lines = [head] + [" " * 4 + line for line in body]
        return '\n'.join(lines)
    
    def get_classes(self) -> list[str]:  # List[str] → list[str]
        """클래스 이름 목록 반환"""
        return self.classes.copy()
    
    def get_class_to_idx(self) -> dict[str, int]:  # Dict[str, int] → dict[str, int]
        """클래스명-인덱스 매핑 반환"""
        return self.class_to_idx.copy()
    
    @property
    def num_classes(self) -> int:
        """클래스 개수 반환"""
        return len(self.classes)
    
    def get_label_distribution(self) -> dict[str, int]:  # Dict[str, int] → dict[str, int]
        """각 클래스별 샘플 개수 반환"""
        label_counts = Counter(self.data_frame['label'])
        return dict(label_counts)
    
    def get_sample_weights(self) -> torch.Tensor:
        """클래스 불균형 해결을 위한 샘플 가중치 계산"""
        label_counts = self.get_label_distribution()
        total_samples = len(self.data_frame)
        
        # 각 클래스의 가중치 = 1 / (클래스별 샘플 수 / 전체 샘플 수)
        class_weights = {
            label: total_samples / (len(self.classes) * count) 
            for label, count in label_counts.items()
        }
        
        # 각 샘플의 가중치
        sample_weights = [
            class_weights[self.data_frame.iloc[i]['label']] 
            for i in range(len(self.data_frame))
        ]
        
        return torch.tensor(sample_weights, dtype=torch.float)
    
    def split_dataset(
        self, 
        train_ratio: float = 0.8,
        stratify: bool = True,
        random_seed: int | None = None  # Optional[int] → int | None
    ) -> tuple['ImageClassificationDataset', 'ImageClassificationDataset']:  # Tuple[...] → tuple[...]
        """
        데이터셋을 훈련용과 검증용으로 분할
        
        Args:
            train_ratio (float): 훈련 데이터 비율
            stratify (bool): 클래스 비율을 유지할지 여부
            random_seed (int | None): 랜덤 시드
            
        Returns:
            tuple[ImageClassificationDataset, ImageClassificationDataset]: (훈련용, 검증용)
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        if stratify:
            # 클래스별로 분할
            train_indices = []
            val_indices = []
            
            for class_name in self.classes:
                class_indices = self.data_frame[self.data_frame['label'] == class_name].index.tolist()
                np.random.shuffle(class_indices)
                
                split_point = int(len(class_indices) * train_ratio)
                train_indices.extend(class_indices[:split_point])
                val_indices.extend(class_indices[split_point:])
        else:
            # 전체 데이터를 랜덤 분할
            indices = list(range(len(self.data_frame)))
            np.random.shuffle(indices)
            split_point = int(len(indices) * train_ratio)
            train_indices = indices[:split_point]
            val_indices = indices[split_point:]
        
        # 서브셋 생성
        train_dataset = self.get_subset(train_indices)
        val_dataset = self.get_subset(val_indices)
        
        return train_dataset, val_dataset
    
    def get_subset(self, indices: list[int]) -> 'ImageClassificationDataset':  # List[int] → list[int]
        """주어진 인덱스들에 해당하는 서브셋 반환"""
        subset_dataset = ImageClassificationDataset.__new__(ImageClassificationDataset)
        
        # 기본 속성 복사
        subset_dataset.img_dir = self.img_dir
        subset_dataset.transform = self.transform
        subset_dataset.target_transform = self.target_transform
        subset_dataset.classes = self.classes.copy()
        subset_dataset.class_to_idx = self.class_to_idx.copy()
        subset_dataset.idx_to_class = self.idx_to_class.copy()
        
        # 서브셋 데이터프레임 생성
        subset_dataset.data_frame = self.data_frame.iloc[indices].reset_index(drop=True)
        
        return subset_dataset

    def compute_mean_std(self) -> tuple[torch.Tensor, torch.Tensor]:  # Tuple[torch.Tensor, torch.Tensor] → tuple[torch.Tensor, torch.Tensor]
        """
        데이터셋의 평균과 표준편차 계산 (정규화용)
        
        Returns:
            tuple[torch.Tensor, torch.Tensor]: (평균, 표준편차)
        """
        # 임시로 정규화 없는 변환 적용
        temp_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])
        
        means = []
        stds = []
        
        for i in range(len(self)):
            # 원본 변환 임시 저장
            original_transform = self.transform
            self.transform = temp_transform
            
            image, _ = self[i]
            
            # 원본 변환 복원
            self.transform = original_transform
            
            means.append(image.mean(dim=[1, 2]))
            stds.append(image.std(dim=[1, 2]))
        
        mean = torch.stack(means).mean(dim=0)
        std = torch.stack(stds).mean(dim=0)
        
        return mean, std

    def filter_by_classes(self, class_names: list[str]) -> 'ImageClassificationDataset':  # List[str] → list[str]
        """
        특정 클래스들만 포함하는 데이터셋 반환
        
        Args:
            class_names (list[str]): 필터링할 클래스 이름들
            
        Returns:
            ImageClassificationDataset: 필터링된 데이터셋
        """
        filtered_indices = []
        for idx, row in self.data_frame.iterrows():
            if row['label'] in class_names:
                filtered_indices.append(idx)
        
        return self.get_subset(filtered_indices)

# 기타 유틸리티 함수들도 업데이트
def create_data_loaders(
    dataset: ImageClassificationDataset,
    batch_size: int = 32,
    train_ratio: float = 0.8,
    num_workers: int = 4,
    random_seed: int | None = None  # Optional[int] → int | None
) -> tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]:  # Tuple[...] → tuple[...]
    """
    데이터셋으로부터 훈련/검증 데이터로더 생성
    
    Args:
        dataset (ImageClassificationDataset): 입력 데이터셋
        batch_size (int): 배치 크기
        train_ratio (float): 훈련 데이터 비율
        num_workers (int): 데이터 로딩 워커 수
        random_seed (int | None): 랜덤 시드
        
    Returns:
        tuple[DataLoader, DataLoader]: (훈련용, 검증용) 데이터로더
    """
    train_dataset, val_dataset = dataset.split_dataset(
        train_ratio=train_ratio, 
        random_seed=random_seed
    )
    
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    return train_loader, val_loader
```

### 주요 변경사항 요약

| 기존 (Python 3.8 이하)     | 새로운 방식 (Python 3.9+)   | 새로운 방식 (Python 3.10+)  |
| ---------------------- | ---------------------- | ---------------------- |
| `List[str]`            | `list[str]`            | `list[str]`            |
| `Dict[str, int]`       | `dict[str, int]`       | `dict[str, int]`       |
| `Tuple[str, int]`      | `tuple[str, int]`      | `tuple[str, int]`      |
| `Optional[str]`        | `Optional[str]`        | `str \| None`          |
| `Union[str, int]`      | `Union[str, int]`      | `str \| int`           |
| `Callable[[int], str]` | `Callable[[int], str]` | `Callable[[int], str]` |

### 💡 추가 고려사항

```python
# Python 3.11+에서는 더 많은 개선사항이 있습니다
from typing import Self  # Python 3.11+에서 추가됨

class ImageClassificationDataset(Dataset):
    def get_subset(self, indices: list[int]) -> Self:  # 'Self' 사용 가능
        """자기 자신의 타입을 반환할 때 더 명확함"""
        # ...
        
    def filter_by_classes(self, class_names: list[str]) -> Self:
        """Self를 사용하면 상속받은 클래스에서도 올바른 타입 추론"""
        # ...
```

> **호환성 주의사항**: Python 3.9+ 기능을 사용할 때는 프로젝트의 최소 Python 버전 요구사항을 확인해야 한다. 하위 호환성이 필요한 경우 `from __future__ import annotations`를 사용하거나 기존 `typing` 모듈을 계속 사용하는 것이 안전하다. {: .prompt-warning}

> **성능상 이점**: 새로운 타입 힌팅 방식은 런타임 오버헤드가 적고, 더 읽기 쉬우며, IDE의 타입 추론 성능도 향상된다. {: .prompt-tip}