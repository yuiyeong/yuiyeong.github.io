---
title: "🌟 Python Celery: 비동기 작업 처리의 완벽 가이드"
date: 2025-10-12 13:59:00 +0900
categories:
  - PYTHON
  - CELERY
tags:
  - 급발진거북이
  - GeekAndChill
  - 기깬칠
  - python
  - 파이썬
  - Celery
  - backgound
  - backgroundTask
  - task
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 패키지/기술 버전 정보

- celery==5.4.0
- redis==5.2.0
- fastapi==0.115.0
- uvicorn==0.32.0
- flower==2.0.1 (모니터링 도구)
- kombu==5.4.0 (메시징 라이브러리)
- python==3.12
- pydantic==2.9.0

## 🚀 TL;DR

- **Celery**는 Python에서 비동기 작업(백그라운드 작업)을 처리하는 분산 작업 큐 시스템이다
- **메시지 브로커**(Redis, RabbitMQ)를 통해 작업을 전달하고, **Worker**가 이를 실행한다
- 시간이 오래 걸리는 작업(이메일 발송, 데이터 처리, 리포트 생성 등)을 백그라운드에서 처리할 수 있다
- **FastAPI**와 통합하면 API 응답 속도를 크게 개선할 수 있다
- **Celery Beat**를 사용하면 주기적인 작업(크론잡)을 쉽게 스케줄링할 수 있다
- **Flower**로 작업 모니터링과 관리가 가능하다
- Task의 재시도, 우선순위, 체이닝, 그룹화 등 다양한 고급 기능을 제공한다
- 프로덕션 환경에서는 적절한 worker 수, timeout 설정, 에러 핸들링이 필수적이다
- Task 상태는 PENDING → STARTED → SUCCESS/FAILURE로 전이된다
- 분산 시스템으로 확장 가능하며, 고가용성 아키텍처 구성이 가능하다

## 📓 실습 Jupyter Notebook


- w.i.p.

## 🎯 Celery란 무엇인가?

**Celery**는 Python으로 작성된 **분산 작업 큐(Distributed Task Queue)** 시스템이다.

웹 애플리케이션에서 다음과 같은 상황을 생각해보자:

- 사용자가 회원가입을 하면 환영 이메일을 보내야 한다
- 대용량 엑셀 파일을 업로드하면 데이터를 처리해야 한다
- 매일 밤 12시에 일일 리포트를 생성해야 한다
- 동영상 파일을 다양한 해상도로 변환해야 한다
- 수천 명의 사용자에게 푸시 알림을 보내야 한다

이런 작업들을 **동기적으로 처리**하면 사용자는 작업이 완료될 때까지 기다려야 한다. 이메일 발송에 5초가 걸린다면, 사용자는 5초를 기다려야 회원가입이 완료된다. 동영상 변환에 10분이 걸린다면 API는 10분 동안 응답하지 않는다.

Celery는 이런 작업들을 **백그라운드에서 비동기적으로 처리**할 수 있게 해준다. 사용자에게는 즉시 응답을 주고, 실제 작업은 나중에 처리하는 것이다.

```mermaid
sequenceDiagram
    participant User as 사용자
    participant API as API 서버
    participant Queue as 작업 큐
    participant Worker as Celery Worker
    
    User->>API: 회원가입 요청
    API->>Queue: 이메일 발송 작업 추가
    API->>User: 즉시 응답 (0.1초)
    
    Note over Queue,Worker: 백그라운드에서 처리
    Worker->>Queue: 작업 가져오기
    Worker->>Worker: 이메일 발송 (5초)
    Worker->>Queue: 작업 완료 보고
```

> Celery는 **"일을 나중에 처리하겠다"** 는 약속을 하고, 그 약속을 지키는 시스템이다. 사용자는 즉시 응답을 받고, 실제 작업은 백그라운드에서 조용히 처리된다.
{: .prompt-tip}

## 🏗️ Celery의 핵심 아키텍처

Celery는 여러 컴포넌트가 협력하여 작동하는 분산 시스템이다. 각 컴포넌트의 역할과 상호작용을 이해하는 것이 중요하다.

```mermaid
graph TB
    subgraph "클라이언트 레이어"
        A[FastAPI/Django<br/>클라이언트]
        A1[스케줄러<br/>Celery Beat]
    end
    
    subgraph "메시지 브로커"
        B[Redis/RabbitMQ<br/>메시지 큐]
        B1[Priority Queue]
        B2[Default Queue]
        B3[Email Queue]
    end
    
    subgraph "Worker 레이어"
        C1[Worker 1<br/>4 processes]
        C2[Worker 2<br/>4 processes]
        C3[Worker 3<br/>4 processes]
    end
    
    subgraph "결과 저장소"
        D[Redis/DB<br/>Result Backend]
    end
    
    subgraph "모니터링"
        E[Flower<br/>웹 대시보드]
    end
    
    A -->|작업 발행| B
    A1 -->|주기적 작업 발행| B
    B --> B1
    B --> B2
    B --> B3
    
    B1 -->|작업 배분| C1
    B2 -->|작업 배분| C2
    B3 -->|작업 배분| C3
    
    C1 -->|결과 저장| D
    C2 -->|결과 저장| D
    C3 -->|결과 저장| D
    
    C1 -.->|상태 정보| E
    C2 -.->|상태 정보| E
    C3 -.->|상태 정보| E
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C1 fill:#e8f5e8
    style C2 fill:#e8f5e8
    style C3 fill:#e8f5e8
    style D fill:#f3e5f5
    style E fill:#fce4ec
```

### 컴포넌트 상세 설명

#### 1. Client (작업 요청자)

클라이언트는 Celery에게 작업을 요청하는 주체다. 웹 애플리케이션, API 서버, 또는 다른 스크립트가 될 수 있다.

```python
# FastAPI 엔드포인트에서 작업 요청
@app.post("/send-email")
async def send_email(email: str):
    # Celery에게 이메일 발송 작업 요청
    task = send_welcome_email.delay(email)
    return {
        "task_id": task.id,
        "status": "작업이 큐에 추가되었습니다",
        "eta": "약 5초 후 완료 예정"
    }
```

**클라이언트의 역할**

- 작업 생성 및 파라미터 전달
- 작업 우선순위 설정
- 작업 스케줄링 (지연 실행, 특정 시간 실행)
- 작업 ID 반환

#### 2. Message Broker (메시지 브로커)

브로커는 작업 요청을 **큐(Queue)** 에 저장하는 중간 매개체다. 클라이언트와 Worker 사이의 통신을 담당한다.

```mermaid
graph LR
    subgraph "메시지 브로커 내부"
        A[수신 레이어] --> B{라우팅}
        B -->|우선순위 높음| C[High Priority Queue]
        B -->|일반| D[Default Queue]
        B -->|우선순위 낮음| E[Low Priority Queue]
        
        C --> F[Worker Pool]
        D --> F
        E --> F
    end
    
    style C fill:#ffcdd2
    style D fill:#fff9c4
    style E fill:#c8e6c9
```

**주요 브로커 옵션**

**Redis** (권장, 간단하고 빠름)

```python
# Redis를 브로커로 사용
app = Celery('tasks', broker='redis://localhost:6379/0')

# Redis 설정 옵션
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 10
```

**RabbitMQ** (고급 기능, 더 안정적)

```python
# RabbitMQ를 브로커로 사용
app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

# RabbitMQ 고급 설정
app.conf.broker_heartbeat = 30
app.conf.broker_pool_limit = 10
```

> **브로커 선택 기준**
> 
> - **Redis**: 설정이 간단하고 성능이 좋다. 대부분의 경우 충분하다.
> - **RabbitMQ**: 더 복잡한 라우팅이 필요하거나, 메시지 손실을 절대 허용할 수 없는 경우 사용한다.
{: .prompt-tip}

#### 3. Worker (작업 처리자)

Worker는 실제로 작업을 수행하는 프로세스다. 여러 개의 Worker를 동시에 실행할 수 있으며, 각 Worker는 여러 프로세스나 스레드를 가질 수 있다.

```mermaid
graph TB
    subgraph "Worker 프로세스"
        W[Worker Main]
        W --> P1[Process 1]
        W --> P2[Process 2]
        W --> P3[Process 3]
        W --> P4[Process 4]
        
        P1 --> T1[Task 실행]
        P2 --> T2[Task 실행]
        P3 --> T3[Task 실행]
        P4 --> T4[Idle]
    end
    
    Q[Message Queue] -->|작업 가져오기| W
    T1 -->|결과 저장| R[Result Backend]
    T2 -->|결과 저장| R
    T3 -->|결과 저장| R
    
    style W fill:#e3f2fd
    style P1 fill:#c8e6c9
    style P2 fill:#c8e6c9
    style P3 fill:#c8e6c9
    style P4 fill:#ffecb3
```

**Worker 실행 옵션**

```bash
# 기본 Worker 시작
celery -A tasks worker --loglevel=info

# CPU 코어 수만큼 프로세스 생성
celery -A tasks worker --concurrency=4

# Autoscale: 부하에 따라 자동 조절 (최소 2, 최대 8)
celery -A tasks worker --autoscale=8,2

# 특정 큐만 처리
celery -A tasks worker -Q high_priority,default

# 로그 파일 저장
celery -A tasks worker --logfile=/var/log/celery/worker.log

# 메모리 누수 방지: 1000개 작업 후 재시작
celery -A tasks worker --max-tasks-per-child=1000
```

**Worker 풀 타입**

```python
# Prefork (기본값, 멀티프로세싱)
celery -A tasks worker --pool=prefork

# Gevent (경량 코루틴, I/O 바운드 작업에 적합)
celery -A tasks worker --pool=gevent --concurrency=1000

# Solo (단일 프로세스, 개발/디버깅용)
celery -A tasks worker --pool=solo

# Threads (멀티스레딩)
celery -A tasks worker --pool=threads --concurrency=10
```

> **풀 타입 선택 가이드**
> 
> - **CPU 집약적 작업**: prefork (기본값)
> - **I/O 집약적 작업** (네트워크 요청, 파일 I/O): gevent 또는 threads
> - **디버깅**: solo
{: .prompt-tip}

#### 4. Result Backend (결과 저장소)

작업의 실행 결과와 상태를 저장하는 곳이다. 선택적으로 사용할 수 있다.

```python
# Redis를 결과 저장소로 사용
app = Celery('tasks', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

# 결과를 저장하지 않는 경우
app = Celery('tasks', 
             broker='redis://localhost:6379/0',
             backend=None)

# PostgreSQL을 결과 저장소로 사용
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='db+postgresql://user:pass@localhost/dbname')
```

**Backend 옵션 비교**

|Backend|장점|단점|사용 사례|
|---|---|---|---|
|Redis|빠르고 간단|메모리 기반, 영속성 제한|임시 결과, 빠른 조회|
|RabbitMQ|브로커와 통합|상대적으로 느림|간단한 설정|
|Database|영속적, 복잡한 쿼리|느림, 부하 증가|장기 보관, 감사 로그|
|MongoDB|유연한 스키마|추가 인프라 필요|대용량 결과 저장|

## 📝 Task 상태 전이 다이어그램

Celery Task는 생명주기 동안 여러 상태를 거친다. 이 상태 전이를 이해하면 작업 모니터링과 디버깅이 쉬워진다.

```mermaid
stateDiagram-v2
    [*] --> PENDING: 작업 생성
    PENDING --> STARTED: Worker가 작업 시작
    STARTED --> RETRY: 실패 & 재시도 가능
    STARTED --> PROGRESS: 진행 중
    PROGRESS --> PROGRESS: 진행률 업데이트
    PROGRESS --> SUCCESS: 완료
    PROGRESS --> FAILURE: 실패
    STARTED --> SUCCESS: 완료
    STARTED --> FAILURE: 실패
    RETRY --> STARTED: 재시도 실행
    RETRY --> FAILURE: 재시도 한도 초과
    SUCCESS --> [*]
    FAILURE --> [*]
    
    note right of PENDING
        큐에 대기 중
        아직 Worker가 받지 않음
    end note
    
    note right of STARTED
        Worker가 작업 시작
        task_track_started=True 필요
    end note
    
    note right of PROGRESS
        진행률 정보 포함
        self.update_state() 호출
    end note
    
    note right of SUCCESS
        작업 성공 완료
        결과가 Backend에 저장됨
    end note
    
    note right of FAILURE
        작업 실패
        예외 정보 포함
    end note
```

**상태별 상세 설명**

```python
from celery import Celery, states
from celery.result import AsyncResult

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, track_started=True)
def process_with_progress(self, data):
    """진행률을 업데이트하는 작업"""
    
    # 상태: STARTED (Worker가 작업 시작)
    self.update_state(state='STARTED', meta={'step': 'initialization'})
    
    total_steps = 100
    for i in range(total_steps):
        # 상태: PROGRESS (진행 중)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_steps,
                'percent': int((i + 1) / total_steps * 100),
                'status': f'Processing item {i + 1}'
            }
        )
        # 실제 작업 수행
        time.sleep(0.1)
    
    # 상태: SUCCESS (자동으로 설정됨)
    return {'result': 'completed', 'processed': total_steps}

# 상태 확인
def check_task_status(task_id):
    result = AsyncResult(task_id, app=app)
    
    state_info = {
        'state': result.state,
        'info': result.info
    }
    
    if result.state == states.PENDING:
        state_info['message'] = '작업이 아직 시작되지 않았습니다'
    
    elif result.state == states.STARTED:
        state_info['message'] = 'Worker가 작업을 시작했습니다'
    
    elif result.state == 'PROGRESS':
        info = result.info
        state_info['message'] = f"진행 중: {info.get('percent', 0)}%"
        state_info['current'] = info.get('current')
        state_info['total'] = info.get('total')
    
    elif result.state == states.SUCCESS:
        state_info['message'] = '작업이 완료되었습니다'
        state_info['result'] = result.result
    
    elif result.state == states.FAILURE:
        state_info['message'] = '작업이 실패했습니다'
        state_info['error'] = str(result.info)
    
    return state_info
```

## 🚀 Celery 기본 사용법 - 단계별 가이드

### 1. 설치 및 환경 설정

```bash
# Celery와 Redis 설치
pip install celery redis

# Redis 서버 시작 (Docker 사용)
docker run -d -p 6379:6379 --name redis redis:latest

# Redis 정상 동작 확인
redis-cli ping
# 응답: PONG
```

### 2. 프로젝트 구조 설정

실무에서 사용하는 권장 프로젝트 구조

```
project/
├── celery_app/
│   ├── __init__.py
│   ├── celery.py          # Celery 앱 설정
│   ├── config.py          # 설정 파일
│   └── tasks/
│       ├── __init__.py
│       ├── email_tasks.py
│       ├── report_tasks.py
│       └── data_tasks.py
├── api/
│   ├── __init__.py
│   └── main.py            # FastAPI 앱
├── requirements.txt
└── .env
```

### 3. Celery 앱 생성 및 설정

**celery_app/config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis 설정
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # Celery 설정
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # Worker 설정
    worker_concurrency: int = 4
    worker_prefetch_multiplier: int = 1
    
    # Task 설정
    task_soft_time_limit: int = 300  # 5분
    task_time_limit: int = 360       # 6분
    task_acks_late: bool = True
    task_reject_on_worker_lost: bool = True
    
    # 결과 설정
    result_expires: int = 3600  # 1시간
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**celery_app/celery.py**

```python
from celery import Celery
from celery.signals import worker_ready, worker_shutdown
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Celery 앱 생성
celery_app = Celery(
    'project',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        'celery_app.tasks.email_tasks',
        'celery_app.tasks.report_tasks',
        'celery_app.tasks.data_tasks',
    ]
)

# Celery 설정
celery_app.conf.update(
    # 직렬화
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # 시간대
    timezone='Asia/Seoul',
    enable_utc=True,
    
    # 작업 추적
    task_track_started=True,
    task_send_sent_event=True,
    
    # 타임아웃
    task_soft_time_limit=settings.task_soft_time_limit,
    task_time_limit=settings.task_time_limit,
    
    # Worker 설정
    worker_prefetch_multiplier=settings.worker_prefetch_multiplier,
    worker_max_tasks_per_child=1000,
    
    # ACK 설정
    task_acks_late=settings.task_acks_late,
    task_reject_on_worker_lost=settings.task_reject_on_worker_lost,
    
    # 결과 저장
    result_expires=settings.result_expires,
    result_compression='gzip',
    
    # 재시도 설정
    task_publish_retry=True,
    task_publish_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },
)

# Worker 시작/종료 이벤트 핸들러
@worker_ready.connect
def on_worker_ready(**kwargs):
    logger.info("Worker가 시작되었습니다")

@worker_shutdown.connect
def on_worker_shutdown(**kwargs):
    logger.info("Worker가 종료됩니다")

# Task 자동 검색
celery_app.autodiscover_tasks()
```

### 4. Task 작성 - 실용적인 예제들

**celery_app/tasks/email_tasks.py**

```python
from celery import Task
from celery_app.celery import celery_app
from celery.utils.log import get_task_logger
import smtplib
from email.mime.text import MIMEText
import time

logger = get_task_logger(__name__)

class EmailTask(Task):
    """이메일 발송을 위한 베이스 Task 클래스"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """작업 실패 시 호출"""
        logger.error(f"이메일 발송 실패: {exc}")
        # 실패 알림 전송 (Slack, Discord 등)
        
    def on_success(self, retval, task_id, args, kwargs):
        """작업 성공 시 호출"""
        logger.info(f"이메일 발송 성공: {retval}")
        
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """재시도 시 호출"""
        logger.warning(f"이메일 발송 재시도: {exc}")

@celery_app.task(
    base=EmailTask,
    bind=True,
    name='email.send_welcome',
    max_retries=3,
    default_retry_delay=60,  # 1분 후 재시도
    autoretry_for=(smtplib.SMTPException,),
    retry_backoff=True,  # 지수 백오프
    retry_backoff_max=600,  # 최대 10분
    retry_jitter=True,  # 재시도 시간에 랜덤성 추가
)
def send_welcome_email(self, email: str, username: str):
    """환영 이메일 발송"""
    try:
        logger.info(f"환영 이메일 발송 시작: {email}")
        
        # 이메일 발송 로직
        message = f"환영합니다, {username}님!"
        
        # 실제 SMTP 로직 (여기서는 시뮬레이션)
        time.sleep(2)
        
        if email == "fail@example.com":
            raise smtplib.SMTPException("SMTP 연결 실패")
        
        logger.info(f"환영 이메일 발송 완료: {email}")
        return {
            'email': email,
            'status': 'sent',
            'timestamp': time.time()
        }
        
    except smtplib.SMTPException as exc:
        logger.error(f"SMTP 에러: {exc}")
        raise self.retry(exc=exc)
    
    except Exception as exc:
        logger.error(f"예상치 못한 에러: {exc}", exc_info=True)
        raise

@celery_app.task(
    name='email.send_batch',
    bind=True,
    rate_limit='10/m',  # 분당 10개로 제한
)
def send_batch_emails(self, email_list: list, message: str):
    """대량 이메일 발송 (속도 제한 적용)"""
    results = []
    
    for idx, email in enumerate(email_list):
        try:
            logger.info(f"이메일 발송 중 ({idx+1}/{len(email_list)}): {email}")
            
            # 진행률 업데이트
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': idx + 1,
                    'total': len(email_list),
                    'percent': int((idx + 1) / len(email_list) * 100)
                }
            )
            
            # 이메일 발송
            time.sleep(0.5)
            results.append({'email': email, 'status': 'sent'})
            
        except Exception as e:
            logger.error(f"이메일 발송 실패 ({email}): {e}")
            results.append({'email': email, 'status': 'failed', 'error': str(e)})
    
    return {
        'total': len(email_list),
        'sent': len([r for r in results if r['status'] == 'sent']),
        'failed': len([r for r in results if r['status'] == 'failed']),
        'results': results
    }
```

**celery_app/tasks/data_tasks.py**

```python
from celery_app.celery import celery_app
from celery.utils.log import get_task_logger
from celery import group, chain, chord
import pandas as pd
import time

logger = get_task_logger(__name__)

@celery_app.task(
    name='data.process_chunk',
    bind=True,
    time_limit=600,  # 10분
    soft_time_limit=540,  # 9분
)
def process_data_chunk(self, chunk_id: int, data: list):
    """데이터 청크 처리"""
    try:
        logger.info(f"청크 {chunk_id} 처리 시작 ({len(data)}개 항목)")
        
        # 데이터 처리 로직
        processed_count = 0
        for idx, item in enumerate(data):
            # 실제 처리
            time.sleep(0.1)
            processed_count += 1
            
            # 진행률 업데이트
            if (idx + 1) % 10 == 0:
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'chunk_id': chunk_id,
                        'processed': processed_count,
                        'total': len(data),
                        'percent': int(processed_count / len(data) * 100)
                    }
                )
        
        logger.info(f"청크 {chunk_id} 처리 완료")
        return {
            'chunk_id': chunk_id,
            'processed': processed_count,
            'status': 'completed'
        }
        
    except Exception as e:
        logger.error(f"청크 {chunk_id} 처리 실패: {e}", exc_info=True)
        raise

@celery_app.task(name='data.merge_results')
def merge_chunk_results(results: list):
    """청크 처리 결과 병합"""
    logger.info(f"{len(results)}개 청크 결과 병합 시작")
    
    total_processed = sum(r['processed'] for r in results)
    
    return {
        'total_chunks': len(results),
        'total_processed': total_processed,
        'status': 'completed'
    }

def process_large_dataset(data: list, chunk_size: int = 100):
    """대용량 데이터를 병렬로 처리"""
    # 데이터를 청크로 분할
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    # 병렬 처리 후 결과 병합
    workflow = chord(
        group(
            process_data_chunk.s(idx, chunk)
            for idx, chunk in enumerate(chunks)
        )
    )(merge_chunk_results.s())
    
    return workflow
```

**celery_app/tasks/report_tasks.py**

```python
from celery_app.celery import celery_app
from celery.utils.log import get_task_logger
from datetime import datetime
import time

logger = get_task_logger(__name__)

@celery_app.task(
    name='report.generate_daily',
    bind=True,
    ignore_result=False,  # 결과 저장
    expires=86400,  # 24시간 후 만료
)
def generate_daily_report(self, report_date: str = None):
    """일일 리포트 생성"""
    try:
        if report_date is None:
            report_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"일일 리포트 생성 시작: {report_date}")
        
        # 단계별 처리
        steps = [
            ('데이터 수집', 3),
            ('데이터 분석', 5),
            ('차트 생성', 2),
            ('PDF 생성', 3),
            ('저장', 1)
        ]
        
        total_steps = len(steps)
        for idx, (step_name, duration) in enumerate(steps):
            logger.info(f"{step_name} 중...")
            
            self.update_state(
                state='PROGRESS',
                meta={
                    'current_step': idx + 1,
                    'total_steps': total_steps,
                    'step_name': step_name,
                    'percent': int((idx + 1) / total_steps * 100)
                }
            )
            
            time.sleep(duration)
        
        report_url = f"https://cdn.example.com/reports/{report_date}.pdf"
        
        logger.info(f"일일 리포트 생성 완료: {report_url}")
        return {
            'report_date': report_date,
            'report_url': report_url,
            'generated_at': datetime.now().isoformat(),
            'status': 'completed'
        }
        
    except Exception as e:
        logger.error(f"리포트 생성 실패: {e}", exc_info=True)
        raise
```

### 5. Worker 실행 및 관리

```bash
# 개발 환경: 기본 실행
celery -A celery_app.celery worker --loglevel=info

# 프로덕션 환경: 자세한 설정
celery -A celery_app.celery worker \
  --loglevel=info \
  --concurrency=4 \
  --max-tasks-per-child=1000 \
  --time-limit=300 \
  --soft-time-limit=270 \
  --logfile=/var/log/celery/worker.log \
  --pidfile=/var/run/celery/worker.pid

# 특정 큐만 처리
celery -A celery_app.celery worker \
  -Q email,default \
  --loglevel=info

# Daemonize (백그라운드 실행)
celery -A celery_app.celery worker \
  --detach \
  --logfile=/var/log/celery/worker.log \
  --pidfile=/var/run/celery/worker.pid
```

## 🔗 FastAPI와 Celery 완벽 통합

### 프로젝트 구조

```
project/
├── celery_app/
│   ├── __init__.py
│   ├── celery.py
│   ├── config.py
│   └── tasks/
│       ├── __init__.py
│       ├── email_tasks.py
│       ├── report_tasks.py
│       └── data_tasks.py
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       └── reports.py
├── tests/
│   ├── __init__.py
│   ├── test_tasks.py
│   └── test_api.py
├── requirements.txt
├── .env
└── docker-compose.yml
```

### FastAPI 애플리케이션 구성

**api/dependencies.py**

```python
from fastapi import Depends, HTTPException, status
from celery.result import AsyncResult
from celery_app.celery import celery_app
from typing import Optional

def get_celery_app():
    """Celery 앱 의존성"""
    return celery_app

def get_task_result(task_id: str) -> AsyncResult:
    """Task 결과 조회"""
    return AsyncResult(task_id, app=celery_app)

async def verify_task_exists(task_id: str) -> AsyncResult:
    """Task가 존재하는지 확인"""
    result = AsyncResult(task_id, app=celery_app)
    if result.state == 'PENDING' and not result.info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id}를 찾을 수 없습니다"
        )
    return result
```

**api/routers/tasks.py**

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from celery.result import AsyncResult
from celery import states
from typing import Optional, List
from datetime import datetime

from celery_app.tasks.email_tasks import send_welcome_email, send_batch_emails
from celery_app.tasks.data_tasks import process_data_chunk, process_large_dataset
from api.dependencies import get_task_result, verify_task_exists

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Request/Response 모델
class EmailRequest(BaseModel):
    email: EmailStr
    username: str

class BatchEmailRequest(BaseModel):
    emails: List[EmailStr]
    message: str

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    state: str
    info: Optional[dict] = None
    result: Optional[dict] = None
    error: Optional[str] = None

class DataProcessRequest(BaseModel):
    data: List[dict]
    chunk_size: int = 100

# 이메일 발송 엔드포인트
@router.post("/email/welcome", response_model=TaskResponse)
async def send_welcome_email_endpoint(request: EmailRequest):
    """환영 이메일 발송 작업 생성"""
    task = send_welcome_email.delay(request.email, request.username)
    
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message=f"{request.email}로 환영 이메일이 발송될 예정입니다"
    )

@router.post("/email/batch", response_model=TaskResponse)
async def send_batch_emails_endpoint(request: BatchEmailRequest):
    """대량 이메일 발송 작업 생성"""
    task = send_batch_emails.delay(request.emails, request.message)
    
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message=f"{len(request.emails)}명에게 이메일이 발송될 예정입니다"
    )

# 데이터 처리 엔드포인트
@router.post("/data/process", response_model=TaskResponse)
async def process_data_endpoint(request: DataProcessRequest):
    """대량 데이터 처리 작업 생성"""
    workflow = process_large_dataset(request.data, request.chunk_size)
    
    return TaskResponse(
        task_id=workflow.id,
        status="queued",
        message=f"{len(request.data)}개 항목이 처리될 예정입니다"
    )

# Task 상태 조회
@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    result: AsyncResult = Depends(verify_task_exists)
):
    """Task 상태 조회"""
    response = TaskStatusResponse(task_id=task_id, state=result.state)
    
    if result.state == states.PENDING:
        response.info = {'status': '작업이 대기 중입니다'}
    
    elif result.state == states.STARTED:
        response.info = {'status': '작업이 시작되었습니다'}
    
    elif result.state == 'PROGRESS':
        response.info = result.info
    
    elif result.state == states.SUCCESS:
        response.result = result.result
    
    elif result.state == states.FAILURE:
        response.error = str(result.info)
    
    else:
        response.info = {'status': f'알 수 없는 상태: {result.state}'}
    
    return response

# Task 취소
@router.delete("/{task_id}")
async def cancel_task(
    task_id: str,
    result: AsyncResult = Depends(verify_task_exists)
):
    """Task 취소"""
    result.revoke(terminate=True, signal='SIGKILL')
    
    return {
        "task_id": task_id,
        "message": "작업 취소가 요청되었습니다",
        "timestamp": datetime.now().isoformat()
    }

# Task 재시작
@router.post("/{task_id}/retry")
async def retry_task(
    task_id: str,
    result: AsyncResult = Depends(verify_task_exists)
):
    """실패한 Task 재시작"""
    if result.state != states.FAILURE:
        raise HTTPException(
            status_code=400,
            detail="실패한 작업만 재시작할 수 있습니다"
        )
    
    # 원래 작업의 인자를 가져와서 새로 실행
    # 주의: 이는 간단한 예시이며, 실제로는 작업 타입에 따라 다르게 처리해야 함
    raise HTTPException(
        status_code=501,
        detail="재시작 기능은 구현 중입니다"
    )

# 실행 중인 작업 목록
@router.get("/")
async def list_active_tasks():
    """실행 중인 작업 목록 조회"""
    from celery_app.celery import celery_app
    
    inspect = celery_app.control.inspect()
    
    active = inspect.active()
    scheduled = inspect.scheduled()
    reserved = inspect.reserved()
    
    return {
        "active": active or {},
        "scheduled": scheduled or {},
        "reserved": reserved or {},
        "timestamp": datetime.now().isoformat()
    }
```

**api/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import tasks

app = FastAPI(
    title="Celery Integration API",
    description="FastAPI와 Celery를 통합한 비동기 작업 처리 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(tasks.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "FastAPI + Celery Integration",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    from celery_app.celery import celery_app
    
    try:
        # Celery 연결 확인
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        if stats:
            return {
                "status": "healthy",
                "celery": "connected",
                "workers": len(stats)
            }
        else:
            return {
                "status": "degraded",
                "celery": "no workers",
                "workers": 0
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "celery": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Docker Compose로 전체 스택 실행

**docker-compose.yml**

```yaml
version: '3.8'

services:
  # Redis 서비스
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # FastAPI 서비스
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app

  # Celery Worker 서비스
  worker:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
    command: celery -A celery_app.celery worker --loglevel=info --concurrency=4
    volumes:
      - .:/app

  # Celery Beat 서비스
  beat:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
    command: celery -A celery_app.celery beat --loglevel=info
    volumes:
      - .:/app

  # Flower 모니터링
  flower:
    build: .
    ports:
      - "5555:5555"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
    command: celery -A celery_app.celery flower --port=5555
    volumes:
      - .:/app

volumes:
  redis_data:
```

**Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경변수 설정
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

실행

```bash
# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f worker

# 특정 서비스만 재시작
docker-compose restart worker

# 정리
docker-compose down -v
```

## ⏰ Celery Beat: 주기적 작업 스케줄링

Celery Beat는 크론잡처럼 주기적으로 작업을 실행할 수 있게 해주는 스케줄러다.

```mermaid
sequenceDiagram
    participant Beat as Celery Beat
    participant Queue as Message Queue
    participant Worker as Celery Worker
    participant Task as Task 실행
    
    loop 매 분마다
        Beat->>Beat: 스케줄 확인
        Beat->>Queue: 실행할 작업 전송
    end
    
    Worker->>Queue: 작업 가져오기
    Worker->>Task: 작업 실행
    Task->>Worker: 완료
    Worker->>Queue: 결과 저장
```

### Beat 설정

**celery_app/celery.py**에 스케줄 추가

```python
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

celery_app = Celery(
    'project',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Beat 스케줄 설정
celery_app.conf.beat_schedule = {
    # === 시간 기반 스케줄 ===
    
    # 30초마다 실행
    'health-check-every-30-seconds': {
        'task': 'tasks.health_check',
        'schedule': 30.0,
    },
    
    # 5분마다 실행
    'cleanup-every-5-minutes': {
        'task': 'tasks.cleanup_temp_files',
        'schedule': timedelta(minutes=5),
    },
    
    # === Crontab 스케줄 ===
    
    # 매일 오전 9시
    'daily-report-at-9am': {
        'task': 'report.generate_daily',
        'schedule': crontab(hour=9, minute=0),
        'args': (),  # 인자 없음
    },
    
    # 매일 자정
    'daily-cleanup-at-midnight': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(hour=0, minute=0),
    },
    
    # 매주 월요일 오전 8시
    'weekly-summary-monday-8am': {
        'task': 'report.send_weekly_summary',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
    
    # 매월 1일 오전 9시
    'monthly-billing-1st-9am': {
        'task': 'billing.process_monthly',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
    },
    
    # 평일(월-금) 오후 6시
    'weekday-backup-6pm': {
        'task': 'backup.daily_backup',
        'schedule': crontab(hour=18, minute=0, day_of_week='1-5'),
    },
    
    # 10분마다, 하지만 업무시간(9-18시)에만
    'business-hours-sync': {
        'task': 'sync.external_data',
        'schedule': crontab(minute='*/10', hour='9-18'),
    },
    
    # === 복잡한 스케줄 ===
    
    # 매 15분마다 (0, 15, 30, 45분)
    'quarter-hourly-task': {
        'task': 'tasks.quarter_hour_task',
        'schedule': crontab(minute='*/15'),
    },
    
    # 홀수 시간마다 (1, 3, 5, 7...)
    'odd-hours-task': {
        'task': 'tasks.odd_hour_task',
        'schedule': crontab(minute=0, hour='1,3,5,7,9,11,13,15,17,19,21,23'),
    },
    
    # 특정 시간대에 여러 번
    'multi-time-task': {
        'task': 'tasks.important_task',
        'schedule': crontab(hour='8,12,17,21', minute=0),
    },
}

# Beat 설정
celery_app.conf.beat_schedule_filename = '/var/run/celery/celerybeat-schedule'
celery_app.conf.beat_max_loop_interval = 5  # 5초마다 스케줄 확인
```

### 동적 스케줄 관리

데이터베이스를 사용한 동적 스케줄 관리

```python
# django-celery-beat를 사용한 예시
# pip install django-celery-beat

from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# 새로운 주기 작업 생성
def create_periodic_task(name, task, crontab_expr, args=None):
    """동적으로 주기 작업 생성"""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        hour=crontab_expr.get('hour', '*'),
        minute=crontab_expr.get('minute', '*'),
        day_of_week=crontab_expr.get('day_of_week', '*'),
        day_of_month=crontab_expr.get('day_of_month', '*'),
        month_of_year=crontab_expr.get('month_of_year', '*'),
    )
    
    PeriodicTask.objects.create(
        name=name,
        task=task,
        crontab=schedule,
        args=json.dumps(args or []),
        enabled=True,
    )

# 사용 예시
create_periodic_task(
    name='user-report-123',
    task='report.generate_user_report',
    crontab_expr={'hour': '9', 'minute': '0'},
    args=[123]  # user_id
)
```

### Beat 실행

```bash
# Beat 스케줄러 시작
celery -A celery_app.celery beat --loglevel=info

# 특정 스케줄 파일 사용
celery -A celery_app.celery beat \
  --schedule=/var/run/celery/celerybeat-schedule \
  --loglevel=info

# 데이터베이스 기반 스케줄 사용 (django-celery-beat)
celery -A celery_app.celery beat \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler \
  --loglevel=info
```

> Worker와 Beat는 별도의 프로세스로 실행해야 한다. Worker는 작업을 실행하고, Beat는 스케줄에 따라 작업을 큐에 넣는다.
{: .prompt-warning}

## 🎨 고급 기능 및 패턴

### 1. Task 재시도 메커니즘

```mermaid
flowchart TD
    A[Task 시작] --> B{성공?}
    B -->|Yes| C[결과 반환]
    B -->|No| D{재시도 가능?}
    D -->|No| E[실패 처리]
    D -->|Yes| F[재시도 대기]
    F --> G[지수 백오프 계산]
    G --> H[대기 시간만큼 지연]
    H --> I[재시도 횟수 증가]
    I --> J{최대 횟수?}
    J -->|Yes| E
    J -->|No| A
    
    style C fill:#c8e6c9
    style E fill:#ffcdd2
    style F fill:#fff9c4
```

**재시도 전략**

```python
from celery import Task
from celery.utils.log import get_task_logger
import requests
from requests.exceptions import RequestException

logger = get_task_logger(__name__)

# 1. 기본 재시도
@celery_app.task(bind=True, max_retries=3)
def basic_retry_task(self, url):
    """기본 재시도"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as exc:
        # 60초 후 재시도
        raise self.retry(exc=exc, countdown=60)

# 2. 지수 백오프 (Exponential Backoff)
@celery_app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=10,  # 초기 지연: 10초
)
def exponential_backoff_task(self, url):
    """지수 백오프 재시도"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as exc:
        # 재시도 횟수에 따라 지연 시간 증가
        # 10초, 20초, 40초, 80초, 160초
        retry_count = self.request.retries
        countdown = 10 * (2 ** retry_count)
        
        logger.warning(
            f"재시도 {retry_count + 1}/{self.max_retries}, "
            f"{countdown}초 후 재시도"
        )
        
        raise self.retry(exc=exc, countdown=countdown)

# 3. 자동 재시도 (autoretry_for)
@celery_app.task(
    bind=True,
    autoretry_for=(RequestException,),  # 특정 예외 발생 시 자동 재시도
    retry_kwargs={'max_retries': 3, 'countdown': 5},
    retry_backoff=True,  # 지수 백오프 활성화
    retry_backoff_max=600,  # 최대 10분
    retry_jitter=True,  # 재시도 시간에 랜덤성 추가 (thundering herd 방지)
)
def auto_retry_task(self, url):
    """자동 재시도"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

# 4. 커스텀 재시도 로직
class CustomRetryTask(Task):
    """커스텀 재시도 로직을 가진 Task 클래스"""
    
    def retry(self, args=None, kwargs=None, exc=None, **options):
        """재시도 전 커스텀 로직"""
        logger.warning(f"재시도 시도: {self.name}")
        
        # 재시도 전 정리 작업
        self.cleanup()
        
        # 알림 전송
        if self.request.retries >= 2:
            self.send_alert(f"작업 {self.name}이 {self.request.retries}번 실패")
        
        return super().retry(args, kwargs, exc, **options)
    
    def cleanup(self):
        """재시도 전 정리 작업"""
        pass
    
    def send_alert(self, message):
        """알림 전송"""
        logger.error(message)

@celery_app.task(base=CustomRetryTask, bind=True, max_retries=5)
def custom_retry_task(self, data):
    """커스텀 재시도 작업"""
    # 작업 로직
    pass
```

### 2. Task 체이닝 (Chaining)

여러 작업을 순차적으로 실행:

```mermaid
graph LR
    A[Task 1: 데이터 수집] -->|결과 전달| B[Task 2: 데이터 처리]
    B -->|결과 전달| C[Task 3: 결과 저장]
    C -->|결과 전달| D[Task 4: 알림 발송]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#f3e5f5
```

```python
from celery import chain, group, chord

# Task 정의
@celery_app.task
def fetch_data(url):
    """데이터 가져오기"""
    import requests
    response = requests.get(url)
    return response.json()

@celery_app.task
def process_data(data):
    """데이터 처리"""
    processed = [item * 2 for item in data]
    return processed

@celery_app.task
def save_data(data):
    """데이터 저장"""
    # DB에 저장
    return {'saved': len(data), 'data': data}

@celery_app.task
def send_notification(result):
    """알림 발송"""
    print(f"작업 완료! {result['saved']}개 항목 저장됨")
    return "알림 발송 완료"

# 1. 기본 체인
workflow = chain(
    fetch_data.s('https://api.example.com/data'),
    process_data.s(),
    save_data.s(),
    send_notification.s()
)
result = workflow.apply_async()

# 2. 파이프 연산자 사용 (더 직관적)
workflow = (
    fetch_data.s('https://api.example.com/data') |
    process_data.s() |
    save_data.s() |
    send_notification.s()
)
result = workflow.apply_async()

# 3. 조건부 체인
@celery_app.task
def check_data(data):
    """데이터 검증"""
    if len(data) > 100:
        return {'status': 'large', 'data': data}
    return {'status': 'small', 'data': data}

@celery_app.task
def process_large_data(result):
    """대용량 데이터 처리"""
    return result['data'][:100]  # 첫 100개만 처리

@celery_app.task
def process_small_data(result):
    """소량 데이터 처리"""
    return result['data']  # 전체 처리

# 조건에 따라 다른 작업 실행
def create_conditional_workflow(data):
    result = check_data.apply_async(args=[data]).get()
    
    if result['status'] == 'large':
        workflow = process_large_data.s(result) | save_data.s()
    else:
        workflow = process_small_data.s(result) | save_data.s()
    
    return workflow.apply_async()
```

### 3. Task 그룹화 (Grouping)

여러 작업을 병렬로 실행

```mermaid
graph TB
    A[시작] --> B{작업 분할}
    B --> C[Task 1]
    B --> D[Task 2]
    B --> E[Task 3]
    B --> F[Task 4]
    
    C --> G[모든 결과 수집]
    D --> G
    E --> G
    F --> G
    
    G --> H[결과 병합]
    
    style A fill:#e1f5fe
    style G fill:#fff3e0
    style H fill:#e8f5e8
```

```python
from celery import group

# 1. 기본 그룹
@celery_app.task
def process_item(item_id):
    """개별 항목 처리"""
    time.sleep(1)
    return {'item_id': item_id, 'processed': True}

# 여러 항목을 병렬로 처리
items = [1, 2, 3, 4, 5]
job = group(process_item.s(item_id) for item_id in items)
result = job.apply_async()

# 모든 결과 대기
results = result.get(timeout=10)
print(results)  # [{'item_id': 1, ...}, {'item_id': 2, ...}, ...]

# 2. Chord: 그룹 + 콜백
@celery_app.task
def merge_results(results):
    """모든 결과 병합"""
    total = sum(r['item_id'] for r in results)
    return {'total': total, 'count': len(results)}

# 병렬 처리 후 결과 병합
callback = merge_results.s()
workflow = chord(
    (process_item.s(i) for i in range(10)),
    callback
)
result = workflow.apply_async()
final_result = result.get()
print(final_result)  # {'total': 45, 'count': 10}
```

### 4. Map-Reduce 패턴

```python
from celery import group

@celery_app.task
def map_task(item):
    """Map 단계: 개별 항목 처리"""
    return item * 2

@celery_app.task
def reduce_task(results):
    """Reduce 단계: 결과 집계"""
    return sum(results)

# Map-Reduce 실행
items = range(100)
map_group = group(map_task.s(item) for item in items)
workflow = (map_group | reduce_task.s())
result = workflow.apply_async()
total = result.get()
print(f"총합: {total}")  # 총합: 9900
```

### 5. 우선순위 큐

```python
# 큐 설정
from kombu import Queue

celery_app.conf.task_routes = {
    'tasks.critical_task': {'queue': 'critical'},
    'tasks.high_priority_task': {'queue': 'high'},
    'tasks.normal_task': {'queue': 'default'},
    'tasks.low_priority_task': {'queue': 'low'},
}

celery_app.conf.task_queues = (
    Queue('critical', priority=10),
    Queue('high', priority=5),
    Queue('default', priority=0),
    Queue('low', priority=-5),
)

# Task 정의
@celery_app.task(queue='critical')
def critical_task():
    """긴급 작업"""
    pass

@celery_app.task(queue='high')
def high_priority_task():
    """높은 우선순위 작업"""
    pass

# 동적 우선순위 설정
@celery_app.task
def flexible_task():
    """우선순위를 동적으로 설정 가능한 작업"""
    pass

# 사용 시 우선순위 지정
flexible_task.apply_async(args=[], priority=9)
```

### 6. 에러 핸들링 패턴

```mermaid
flowchart TD
    A[Task 실행] --> B{에러 발생?}
    B -->|No| C[성공]
    B -->|Yes| D{에러 타입 확인}
    
    D -->|일시적 에러| E[재시도]
    D -->|영구적 에러| F[에러 로깅]
    D -->|알 수 없음| G[관리자 알림]
    
    E --> H{재시도 성공?}
    H -->|Yes| C
    H -->|No| I{재시도 한도?}
    I -->|남음| E
    I -->|초과| F
    
    F --> J[실패 처리]
    G --> J
    
    J --> K[보상 트랜잭션]
    K --> L[정리 작업]
    
    style C fill:#c8e6c9
    style J fill:#ffcdd2
    style E fill:#fff9c4
```

```python
from celery import Task
from celery.utils.log import get_task_logger
import traceback

logger = get_task_logger(__name__)

class RobustTask(Task):
    """견고한 에러 핸들링을 가진 Task"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """성공 시 호출"""
        logger.info(f"Task {task_id} 성공: {retval}")
        # 성공 메트릭 기록
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """실패 시 호출"""
        logger.error(
            f"Task {task_id} 실패\n"
            f"예외: {exc}\n"
            f"인자: {args}\n"
            f"키워드 인자: {kwargs}\n"
            f"에러 정보: {einfo}"
        )
        
        # 에러 타입에 따라 다른 처리
        if isinstance(exc, ValueError):
            # 데이터 유효성 에러
            self.log_data_error(args, kwargs, exc)
        elif isinstance(exc, ConnectionError):
            # 연결 에러
            self.notify_ops_team(exc)
        else:
            # 알 수 없는 에러
            self.send_alert(f"예상치 못한 에러: {exc}")
        
        # 실패 메트릭 기록
        
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """재시도 시 호출"""
        logger.warning(f"Task {task_id} 재시도: {exc}")
        # 재시도 메트릭 기록
    
    def log_data_error(self, args, kwargs, exc):
        """데이터 에러 로깅"""
        logger.error(f"데이터 유효성 에러: {exc}")
    
    def notify_ops_team(self, exc):
        """운영팀 알림"""
        logger.critical(f"시스템 에러 발생: {exc}")
        # Slack, Email 등으로 알림
    
    def send_alert(self, message):
        """긴급 알림"""
        logger.critical(message)
        # PagerDuty, Opsgenie 등으로 알림

@celery_app.task(base=RobustTask, bind=True, max_retries=3)
def robust_task(self, data):
    """견고한 작업"""
    try:
        # 작업 로직
        result = process(data)
        return result
        
    except ValueError as e:
        # 데이터 유효성 에러는 재시도하지 않음
        logger.error(f"유효하지 않은 데이터: {e}")
        raise
        
    except ConnectionError as e:
        # 연결 에러는 재시도
        raise self.retry(exc=e, countdown=60)
        
    except Exception as e:
        # 기타 에러는 로깅 후 재시도
        logger.error(f"예상치 못한 에러: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=120)
```

## 🌸 Flower: Celery 모니터링

Flower는 Celery를 위한 실시간 웹 기반 모니터링 도구다.

```mermaid
graph TB
    subgraph "Flower 대시보드"
        A[Task 목록]
        B[Worker 상태]
        C[통계 & 그래프]
        D[Task 상세 정보]
        E[Worker 제어]
    end
    
    F[Celery 시스템] -->|실시간 데이터| A
    F -->|실시간 데이터| B
    F -->|실시간 데이터| C
    
    A --> D
    B --> E
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#f3e5f5
    style E fill:#fce4ec
```

### 설치 및 실행

```bash
# 설치
pip install flower

# 기본 실행
celery -A celery_app.celery flower --port=5555

# 인증 추가
celery -A celery_app.celery flower \
  --port=5555 \
  --basic_auth=admin:password

# 설정 파일 사용
celery -A celery_app.celery flower \
  --conf=flowerconfig.py
```

### Flower 설정 파일

**flowerconfig.py**

```python
# 기본 설정
port = 5555
address = '0.0.0.0'

# 인증
basic_auth = ['admin:secretpassword', 'user:userpassword']

# 데이터베이스 (작업 히스토리 저장)
db = 'flower.db'

# 작업 히스토리 유지 기간 (일)
max_tasks = 10000

# 로깅
logging = 'INFO'

# SSL 설정
# certfile = '/path/to/cert.pem'
# keyfile = '/path/to/key.pem'

# 커스텀 헤더
xheaders = True

# API 활성화
enable_events = True

# 자동 새로고침 간격 (밀리초)
auto_refresh = True
```

### Flower 주요 기능

**1. 실시간 모니터링**

- 실행 중인 작업 목록
- Worker 상태 (온라인/오프라인)
- 작업 처리 속도
- 큐 상태

**2. 작업 관리**

- 작업 취소
- 작업 재시작
- 작업 결과 조회
- 작업 상세 정보 (인자, 실행 시간 등)

**3. 통계 & 그래프**

- 시간별 작업 처리량
- 성공/실패 비율
- Worker별 부하
- 큐별 작업 분포

**4. Worker 제어**

- Worker 시작/중지
- Worker 풀 크기 조정
- Worker 설정 변경

### API를 통한 프로그래밍 방식 접근

```python
import requests

# Flower API 엔드포인트
FLOWER_URL = "http://localhost:5555"

def get_workers():
    """Worker 목록 조회"""
    response = requests.get(f"{FLOWER_URL}/api/workers")
    return response.json()

def get_tasks():
    """Task 목록 조회"""
    response = requests.get(f"{FLOWER_URL}/api/tasks")
    return response.json()

def get_task_info(task_id):
    """특정 Task 정보 조회"""
    response = requests.get(f"{FLOWER_URL}/api/task/info/{task_id}")
    return response.json()

def revoke_task(task_id):
    """Task 취소"""
    response = requests.post(
        f"{FLOWER_URL}/api/task/revoke/{task_id}",
        params={'terminate': True}
    )
    return response.json()

# 사용 예시
workers = get_workers()
print(f"활성 Worker 수: {len(workers)}")

tasks = get_tasks()
print(f"총 Task 수: {len(tasks)}")
```

## 💡 프로덕션 환경 베스트 프랙티스

### 1. Worker 설정 최적화

```python
# celery_app/production.py
class ProductionConfig:
    """프로덕션 환경 설정"""
    
    # === Worker 설정 ===
    worker_concurrency = 8  # CPU 코어 수에 맞춰 조정
    worker_prefetch_multiplier = 1  # 작업을 하나씩만 가져옴
    worker_max_tasks_per_child = 1000  # 1000개 작업 후 재시작
    worker_disable_rate_limits = False
    
    # === Task 설정 ===
    task_acks_late = True  # 작업 완료 후 ACK
    task_reject_on_worker_lost = True  # Worker 종료 시 작업 거부
    task_time_limit = 3600  # 1시간
    task_soft_time_limit = 3300  # 55분
    
    # === 브로커 설정 ===
    broker_connection_retry_on_startup = True
    broker_connection_retry = True
    broker_connection_max_retries = 10
    broker_heartbeat = 30
    broker_pool_limit = 10
    
    # === 결과 설정 ===
    result_expires = 86400  # 24시간
    result_compression = 'gzip'
    result_extended = True
    
    # === 로깅 ===
    worker_redirect_stdouts_level = 'INFO'
```

### 2. 모니터링 및 알림 설정

```python
from celery.signals import (
    task_failure,
    task_success,
    worker_shutdown,
    worker_ready
)
import logging

logger = logging.getLogger(__name__)

@task_failure.connect
def task_failure_handler(sender, task_id, exception, args, kwargs, **kw):
    """작업 실패 시 알림"""
    logger.error(
        f"Task {sender.name} failed: {task_id}\n"
        f"Exception: {exception}\n"
        f"Args: {args}\n"
        f"Kwargs: {kwargs}"
    )
    
    # Slack 알림
    send_slack_alert(
        f"🚨 Task 실패: {sender.name}\n"
        f"에러: {exception}"
    )
    
    # 심각한 에러는 PagerDuty로 전송
    if isinstance(exception, CriticalException):
        trigger_pagerduty_incident(
            title=f"Critical Task Failure: {sender.name}",
            details=str(exception)
        )

@task_success.connect
def task_success_handler(sender, result, **kwargs):
    """작업 성공 메트릭 기록"""
    # Prometheus 메트릭
    task_success_counter.labels(task=sender.name).inc()
    task_duration_histogram.labels(task=sender.name).observe(
        result.get('duration', 0)
    )

@worker_shutdown.connect
def worker_shutdown_handler(sender, **kwargs):
    """Worker 종료 알림"""
    logger.warning(f"Worker {sender} is shutting down")
    send_slack_alert(f"⚠️ Worker {sender} 종료")

@worker_ready.connect
def worker_ready_handler(sender, **kwargs):
    """Worker 시작 알림"""
    logger.info(f"Worker {sender} is ready")
    send_slack_alert(f"✅ Worker {sender} 시작됨")

def send_slack_alert(message):
    """Slack 알림 전송"""
    import requests
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    requests.post(webhook_url, json={'text': message})

def trigger_pagerduty_incident(title, details):
    """PagerDuty 인시던트 생성"""
    # PagerDuty API 호출
    pass
```

### 3. 로깅 설정

```python
# logging_config.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/celery/celery.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/celery/celery_errors.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery.task': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 4. Systemd 서비스 설정

**celery-worker.service**

```ini
[Unit]
Description=Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/celery/celery.conf
WorkingDirectory=/app
ExecStart=/usr/local/bin/celery -A celery_app.celery worker \
    --loglevel=info \
    --logfile=/var/log/celery/worker.log \
    --pidfile=/var/run/celery/worker.pid \
    --detach \
    --concurrency=8 \
    --max-tasks-per-child=1000

ExecStop=/usr/local/bin/celery -A celery_app.celery control shutdown
ExecReload=/usr/local/bin/celery -A celery_app.celery control pool_restart

Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

**celery-beat.service**

```ini
[Unit]
Description=Celery Beat
After=network.target redis.service

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/celery/celery.conf
WorkingDirectory=/app
ExecStart=/usr/local/bin/celery -A celery_app.celery beat \
    --loglevel=info \
    --logfile=/var/log/celery/beat.log \
    --pidfile=/var/run/celery/beat.pid \
    --detach

Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

**설치 및 실행**

```bash
# 서비스 파일 복사
sudo cp celery-worker.service /etc/systemd/system/
sudo cp celery-beat.service /etc/systemd/system/

# 서비스 리로드
sudo systemctl daemon-reload

# 서비스 시작
sudo systemctl start celery-worker
sudo systemctl start celery-beat

# 부팅 시 자동 시작
sudo systemctl enable celery-worker
sudo systemctl enable celery-beat

# 상태 확인
sudo systemctl status celery-worker
sudo systemctl status celery-beat

# 로그 확인
sudo journalctl -u celery-worker -f
```

### 5. 분산 시스템 아키텍처

```mermaid
graph TB
    subgraph "로드 밸런서"
        LB[Nginx/HAProxy]
    end
    
    subgraph "API 서버"
        API1[FastAPI 1]
        API2[FastAPI 2]
        API3[FastAPI 3]
    end
    
    subgraph "메시지 브로커 클러스터"
        R1[Redis Master]
        R2[Redis Replica 1]
        R3[Redis Replica 2]
    end
    
    subgraph "Worker 풀 1"
        W1[Worker 1-1]
        W2[Worker 1-2]
        W3[Worker 1-3]
    end
    
    subgraph "Worker 풀 2"
        W4[Worker 2-1]
        W5[Worker 2-2]
        W6[Worker 2-3]
    end
    
    subgraph "결과 저장소"
        DB[(PostgreSQL)]
    end
    
    subgraph "모니터링"
        F[Flower]
        P[Prometheus]
        G[Grafana]
    end
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> R1
    API2 --> R1
    API3 --> R1
    
    R1 -.복제.-> R2
    R1 -.복제.-> R3
    
    R1 --> W1
    R1 --> W2
    R1 --> W3
    R1 --> W4
    R1 --> W5
    R1 --> W6
    
    W1 --> DB
    W2 --> DB
    W3 --> DB
    W4 --> DB
    W5 --> DB
    W6 --> DB
    
    R1 -.->F
    W1 -.-> P
    W2 -.-> P
    W3 -.-> P
    P --> G
    
    style LB fill:#e3f2fd
    style R1 fill:#fff3e0
    style DB fill:#e8f5e8
    style F fill:#f3e5f5
```

## 🚨 트러블슈팅 가이드

### 일반적인 문제들

#### 1. Worker가 작업을 가져오지 않음

**증상**

- 작업이 큐에 쌓이지만 처리되지 않음
- Worker는 실행 중이지만 아무 일도 하지 않음

**원인 및 해결**

```bash
# 1. Worker가 올바른 큐를 보고 있는지 확인
celery -A celery_app.celery inspect active_queues

# 2. 브로커 연결 확인
celery -A celery_app.celery inspect ping

# 3. Worker 재시작
celery -A celery_app.celery control shutdown
celery -A celery_app.celery worker --loglevel=info

# 4. 큐에 쌓인 작업 확인 (Redis)
redis-cli LLEN celery

# 5. 작업 제거 (필요한 경우)
celery -A celery_app.celery purge
```

#### 2. 메모리 누수

**증상**

- Worker 메모리 사용량이 계속 증가
- 시간이 지나면 Worker가 응답하지 않음

**해결책**

```python
# 1. max_tasks_per_child 설정
celery_app.conf.worker_max_tasks_per_child = 1000

# 2. Worker 시작 시 옵션 추가
# celery -A celery_app.celery worker --max-tasks-per-child=1000

# 3. 메모리 사용량 모니터링
@celery_app.task
def memory_intensive_task(data):
    import psutil
    import gc
    
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # 작업 수행
    result = process_data(data)
    
    # 명시적 가비지 컬렉션
    gc.collect()
    
    final_memory = process.memory_info().rss / 1024 / 1024
    logger.info(f"메모리 사용: {initial_memory:.2f}MB → {final_memory:.2f}MB")
    
    return result
```

#### 3. Task 결과를 가져올 수 없음

**증상**

- `result.get()`이 타임아웃되거나 영원히 기다림
- Task는 완료되었지만 결과를 찾을 수 없음

**해결책**

```python
# 1. Backend 설정 확인
print(celery_app.conf.result_backend)

# 2. Task에 ignore_result=True가 설정되어 있는지 확인
@celery_app.task(ignore_result=False)  # 명시적으로 False 설정
def important_task():
    return "result"

# 3. 타임아웃 설정
result = task.apply_async()
try:
    value = result.get(timeout=10)
except TimeoutError:
    logger.error("Task 타임아웃")

# 4. Task 상태 확인
print(result.state)  # PENDING, STARTED, SUCCESS, FAILURE
print(result.ready())  # 완료 여부
```

#### 4. Redis 연결 문제

**증상**

- `redis.exceptions.ConnectionError`
- Worker가 시작되지 않음

**해결책**

```python
# 1. Redis 연결 확인
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.ping()  # True가 반환되어야 함

# 2. Celery 설정에 재시도 옵션 추가
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_connection_retry = True
celery_app.conf.broker_connection_max_retries = 10

# 3. Redis 최대 연결 수 확인
# redis-cli CONFIG GET maxclients
# redis-cli CONFIG SET maxclients 10000
```

### 디버깅 팁

```python
# 1. Solo 모드로 실행 (동기 실행, 디버깅 용이)
celery -A celery_app.celery worker --pool=solo --loglevel=debug

# 2. 특정 Task만 실행
@celery_app.task
def debug_task():
    print(f"Request: {debug_task.request}")
    print(f"Task ID: {debug_task.request.id}")
    print(f"Args: {debug_task.request.args}")
    print(f"Kwargs: {debug_task.request.kwargs}")

# 3. Task 실행 정보 출력
result = task.apply_async(args=[1, 2])
print(f"Task ID: {result.id}")
print(f"Task Name: {result.task_name}")
print(f"State: {result.state}")

# 4. IPython으로 대화형 디버깅
# pip install ipython
from IPython import embed

@celery_app.task
def interactive_task(data):
    # 여기서 디버깅
    embed()  # IPython 쉘 시작
    return process(data)
```
