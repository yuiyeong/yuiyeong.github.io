---
title: 🔄 Alembic으로 시작하는 데이터베이스 마이그레이션
date: 2025-10-25 17:46:00 +0900
categories:
  - PYTHON
  - DB
tags:
  - 급발진거북이
  - GeekAndChill
  - 기깬칠
  - python
  - 파이썬
  - db
  - database
  - migration
  - alembic
  - postgresql
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 패키지/기술 버전 정보

- Python==3.12+
- SQLAlchemy==2.0.36
- alembic==1.14.0
- psycopg2-binary==2.9.10 (PostgreSQL 드라이버)
- PostgreSQL==17.x

## 🚀 TL;DR

- **Alembic**은 SQLAlchemy 기반의 데이터베이스 스키마 버전 관리 도구다
- Git처럼 데이터베이스 스키마 변경을 추적하고 관리할 수 있다
- **마이그레이션 파일**을 통해 스키마 변경을 단계별로 적용하거나 되돌릴 수 있다
- SQLAlchemy 모델로부터 **자동으로 마이그레이션 스크립트를 생성**할 수 있다
- PostgreSQL의 고유 기능(ENUM, Array, JSONB 등)을 완벽하게 지원한다
- **upgrade**(적용)와 **downgrade**(롤백) 함수로 양방향 마이그레이션 구현
- 팀 협업 시 데이터베이스 스키마 동기화를 자동화할 수 있다
- 프로덕션 환경에서 안전하게 스키마를 변경하는 표준 방법을 제공한다

## 📓 실습 Jupyter Notebook

- w.i.p.

## 🔍 Alembic이란?

**Alembic**은 SQLAlchemy를 위한 데이터베이스 마이그레이션 도구다. 쉽게 말해, 데이터베이스 스키마의 **"버전 관리 시스템"** 이라고 생각하면 된다.

### 왜 Alembic이 필요한가?

애플리케이션을 개발하다 보면 데이터베이스 스키마를 자주 변경하게 된다.

- 새로운 테이블 추가
- 기존 컬럼 수정 또는 삭제
- 인덱스나 제약 조건 변경
- 데이터 타입 변환

이러한 변경사항을 관리하지 않으면 다음과 같은 문제가 발생한다.

- 개발 환경과 프로덕션 환경의 스키마 불일치
- 팀원 간 데이터베이스 상태 동기화 어려움
- 배포 시 수동 SQL 실행으로 인한 실수 가능성
- 스키마 변경 히스토리 추적 불가

```mermaid
graph LR
    A[개발자 A의 DB] -->|동기화 어려움| B[개발자 B의 DB]
    B -->|배포 시 충돌| C[프로덕션 DB]
    
    style A fill:#ffebee
    style B fill:#ffebee
    style C fill:#ffebee
```

**Alembic을 사용하면,**

```mermaid
graph LR
    A[SQLAlchemy 모델] -->|자동 생성| B[마이그레이션 파일]
    B -->|버전 관리| C[Git 저장소]
    C -->|배포| D[모든 환경 동기화]
    
    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🎯 Alembic의 핵심 컨셉

### 1. 마이그레이션 (Migration)

데이터베이스 스키마의 **특정 변경사항을 나타내는 Python 스크립트**다. 각 마이그레이션 파일은 고유한 버전 ID를 가진다.

### 2. 리비전 (Revision)

각 마이그레이션 파일을 식별하는 **고유한 해시값**이다. Git의 커밋 해시와 유사하다.

```python
# 예시: versions/2a3b4c5d6e7f_add_user_table.py
"""add user table

Revision ID: 2a3b4c5d6e7f
Revises: 
Create Date: 2025-01-15 10:30:45.123456
"""
```

### 3. upgrade()와 downgrade()

- **upgrade()**: 스키마 변경을 **적용**하는 함수
- **downgrade()**: 스키마 변경을 **되돌리는** 함수

```python
def upgrade():
    # 테이블 생성
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )

def downgrade():
    # 테이블 삭제
    op.drop_table('users')
```

### 4. 리비전 체인 (Revision Chain)

마이그레이션들은 서로 연결되어 **체인 구조**를 형성한다.

```mermaid
graph LR
    A[초기 상태] --> B[Rev 1: users 테이블]
    B --> C[Rev 2: posts 테이블]
    C --> D[Rev 3: email 컬럼 추가]
    
    style A fill:#f5f5f5
    style B fill:#e3f2fd
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

## 🧩 Alembic의 핵심 구성요소

### 프로젝트 구조

```
my_project/
├── alembic/
│   ├── versions/          # 마이그레이션 파일들
│   │   ├── 001_initial.py
│   │   ├── 002_add_email.py
│   │   └── 003_add_index.py
│   ├── env.py            # 환경 설정
│   ├── script.py.mako    # 템플릿 파일
│   └── README
├── alembic.ini           # 메인 설정 파일
├── models.py             # SQLAlchemy 모델
└── main.py
```

### 1. alembic.ini

Alembic의 메인 설정 파일이다.

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .

# 데이터베이스 URL
sqlalchemy.url = postgresql://user:password@localhost/dbname

# 파일 템플릿
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# 로깅 설정
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

### 2. env.py

마이그레이션 실행 환경을 설정하는 파일이다. SQLAlchemy 엔진 설정과 메타데이터 연결을 담당한다.

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# SQLAlchemy 모델의 메타데이터 가져오기
from models import Base
target_metadata = Base.metadata

# Alembic Config 객체
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_online():
    """온라인 모드로 마이그레이션 실행"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
```

### 3. versions/ 디렉토리

생성된 모든 마이그레이션 파일이 저장되는 곳이다.

```python
# versions/20250115_1030_2a3b4c5d6e7f_add_user_table.py
"""add user table

Revision ID: 2a3b4c5d6e7f
Revises: 
Create Date: 2025-01-15 10:30:45
"""
from alembic import op
import sqlalchemy as sa

# 리비전 정보
revision = '2a3b4c5d6e7f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('users')
```

## 🚀 Alembic 설치 및 초기 설정

### 1단계: 설치

```bash
# Poetry 사용 시
poetry add alembic sqlalchemy psycopg2-binary

# pip 사용 시
pip install alembic sqlalchemy psycopg2-binary
```

### 2단계: Alembic 초기화

```bash
# 프로젝트 루트에서 실행
alembic init alembic

# 출력:
# Creating directory /path/to/project/alembic ... done
# Creating directory /path/to/project/alembic/versions ... done
# Generating /path/to/project/alembic.ini ... done
# Generating /path/to/project/alembic/env.py ... done
# Generating /path/to/project/alembic/README ... done
# Generating /path/to/project/alembic/script.py.mako ... done
```

### 3단계: 데이터베이스 URL 설정

```ini
# alembic.ini
[alembic]
sqlalchemy.url = postgresql://username:password@localhost:5432/mydatabase

# 환경변수 사용 (권장)
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

> **보안 팁**: 데이터베이스 URL을 환경변수로 관리하는 것이 좋습니다. `alembic.ini`는 Git에 커밋되지 않도록 `.gitignore`에 추가하거나, URL 부분만 환경변수로 처리하세요.
{: .prompt-warning}

### 4단계: SQLAlchemy 모델 연결

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")
```

```python
# alembic/env.py 수정
from models import Base  # 모델 import
target_metadata = Base.metadata  # 메타데이터 연결
```

## 📝 기본 사용법

### 마이그레이션 생성

#### 1. 자동 생성 (권장)

SQLAlchemy 모델의 변경사항을 자동으로 감지하여 마이그레이션 파일을 생성한다.

```bash
# 기본 형식
alembic revision --autogenerate -m "설명 메시지"

# 예시
alembic revision --autogenerate -m "add user and post tables"

# 출력:
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.autogenerate.compare] Detected added table 'users'
# INFO  [alembic.autogenerate.compare] Detected added table 'posts'
# Generating /path/to/alembic/versions/2a3b4c5d6e7f_add_user_and_post_tables.py ... done
```

> **자동 생성의 장점**: 수동으로 스키마 변경을 작성할 필요 없이, 모델 정의만 변경하면 Alembic이 차이를 감지하여 마이그레이션 코드를 생성해줍니다.
{: .prompt-tip}

#### 2. 수동 생성

```bash
# 빈 마이그레이션 파일 생성
alembic revision -m "custom migration"
```

생성된 파일을 직접 편집

```python
# versions/xxx_custom_migration.py
def upgrade():
    # 여기에 직접 작성
    op.execute("CREATE INDEX idx_username ON users(username)")

def downgrade():
    op.execute("DROP INDEX idx_username")
```

### 마이그레이션 적용 (Upgrade)

```bash
# 최신 버전으로 업그레이드
alembic upgrade head

# 출력:
# INFO  [alembic.runtime.migration] Running upgrade  -> 2a3b4c5d6e7f, add user and post tables
# INFO  [alembic.runtime.migration] Running upgrade 2a3b4c5d6e7f -> 3c4d5e6f7g8h, add email index

# 특정 리비전으로 업그레이드
alembic upgrade 2a3b4c5d6e7f

# 상대적 업그레이드 (현재부터 2단계 진행)
alembic upgrade +2
```

### 마이그레이션 롤백 (Downgrade)

```bash
# 한 단계 이전으로 롤백
alembic downgrade -1

# 특정 리비전으로 롤백
alembic downgrade 2a3b4c5d6e7f

# 처음 상태로 완전 롤백
alembic downgrade base
```

### 현재 상태 확인

```bash
# 현재 데이터베이스의 리비전 확인
alembic current

# 출력:
# 2a3b4c5d6e7f (head)

# 마이그레이션 히스토리 확인
alembic history

# 출력:
# 3c4d5e6f7g8h -> 4d5e6f7g8h9i (head), add email index
# 2a3b4c5d6e7f -> 3c4d5e6f7g8h, add posts table
# <base> -> 2a3b4c5d6e7f, add users table

# 상세 히스토리 (verbose)
alembic history --verbose
```

## 🎓 고급 활용법

### 1. 데이터 마이그레이션

- 스키마 변경과 함께 **데이터를 변환**해야 하는 경우

```python
# versions/xxx_migrate_user_data.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from models import User

def upgrade():
    # 1. 새 컬럼 추가
    op.add_column('users', sa.Column('full_name', sa.String(100)))
    
    # 2. 데이터 변환
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    
    # 기존 데이터에서 full_name 생성
    users = session.execute(sa.text("SELECT id, username FROM users")).fetchall()
    for user_id, username in users:
        full_name = username.replace('_', ' ').title()
        session.execute(
            sa.text("UPDATE users SET full_name = :full_name WHERE id = :id"),
            {"full_name": full_name, "id": user_id}
        )
    
    session.commit()
    
    # 3. NOT NULL 제약 추가
    op.alter_column('users', 'full_name', nullable=False)

def downgrade():
    op.drop_column('users', 'full_name')
```

### 2. 배치(Batch) 작업

- 여러 작업을 하나의 트랜잭션으로 묶어 처리

```python
def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer()))
        batch_op.add_column(sa.Column('city', sa.String(50)))
        batch_op.create_index('idx_city', ['city'])

def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('idx_city')
        batch_op.drop_column('city')
        batch_op.drop_column('age')
```

### 3. 브랜치 관리

- 여러 개발 브랜치에서 동시에 작업할 때

```bash
# 브랜치 생성
alembic revision -m "feature A" --branch-label=feature_a
alembic revision -m "feature B" --branch-label=feature_b

# 브랜치 병합
alembic merge -m "merge features" feature_a feature_b

# 브랜치 상태 확인
alembic branches
```

### 4. 조건부 마이그레이션

- 환경에 따라 다른 마이그레이션 적용

```python
import os

def upgrade():
    env = os.getenv('ENVIRONMENT', 'development')
    
    # 공통 변경사항
    op.add_column('users', sa.Column('status', sa.String(20)))
    
    # 프로덕션에만 인덱스 추가
    if env == 'production':
        op.create_index('idx_status', 'users', ['status'])

def downgrade():
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        op.drop_index('idx_status', 'users')
    
    op.drop_column('users', 'status')
```

### 5. 복잡한 제약 조건

```python
from sqlalchemy import CheckConstraint, UniqueConstraint

def upgrade():
    # CHECK 제약 조건
    op.create_check_constraint(
        'check_age_positive',
        'users',
        'age > 0'
    )
    
    # 복합 UNIQUE 제약 조건
    op.create_unique_constraint(
        'uq_user_email',
        'users',
        ['username', 'email']
    )
    
    # FOREIGN KEY 제약 조건
    op.create_foreign_key(
        'fk_post_author',
        'posts', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_post_author', 'posts', type_='foreignkey')
    op.drop_constraint('uq_user_email', 'users', type_='unique')
    op.drop_constraint('check_age_positive', 'users', type_='check')
```

## 🐘 PostgreSQL 특화 기능

PostgreSQL을 사용할 때 Alembic의 특별한 기능과 주의사항을 알아보자.

### 1. PostgreSQL ENUM 타입

```python
from sqlalchemy import Enum

# models.py
class User(Base):
    __tablename__ = 'users'
    
    status = Column(Enum('active', 'inactive', 'banned', name='user_status'))
```

- 마이그레이션에서 ENUM 처리

```python
# versions/xxx_add_user_status.py
from sqlalchemy.dialects import postgresql

def upgrade():
    # ENUM 타입 생성
    user_status = postgresql.ENUM('active', 'inactive', 'banned', 
                                   name='user_status', 
                                   create_type=True)
    user_status.create(op.get_bind())
    
    # 컬럼 추가
    op.add_column('users',
        sa.Column('status', user_status, server_default='active')
    )

def downgrade():
    op.drop_column('users', 'status')
    
    # ENUM 타입 삭제
    user_status = postgresql.ENUM('active', 'inactive', 'banned',
                                   name='user_status')
    user_status.drop(op.get_bind())
```

> **ENUM 값 추가/수정하기**: PostgreSQL은 ENUM 값을 직접 수정할 수 없다. 값을 추가하려면 `ALTER TYPE ... ADD VALUE` 명령을 사용해야 한다.
{: .prompt-warning}

```python
def upgrade():
    # ENUM에 새 값 추가
    op.execute("ALTER TYPE user_status ADD VALUE 'suspended'")

def downgrade():
    # ENUM 값 제거는 불가능 - 타입을 다시 만들어야 함
    pass
```

### 2. Array 타입

```python
from sqlalchemy.dialects.postgresql import ARRAY

# models.py
class User(Base):
    __tablename__ = 'users'
    
    tags = Column(ARRAY(String))
```

```python
# 마이그레이션
def upgrade():
    op.add_column('users',
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'tags')
```

### 3. JSON/JSONB 타입

```python
from sqlalchemy.dialects.postgresql import JSONB

# models.py
class User(Base):
    __tablename__ = 'users'
    
    metadata = Column(JSONB, default={})
```

```python
# 마이그레이션 with 인덱스
def upgrade():
    op.add_column('users',
        sa.Column('metadata', postgresql.JSONB, nullable=True)
    )
    
    # GIN 인덱스 추가 (JSONB 쿼리 성능 향상)
    op.create_index(
        'idx_user_metadata',
        'users',
        ['metadata'],
        postgresql_using='gin'
    )

def downgrade():
    op.drop_index('idx_user_metadata', 'users')
    op.drop_column('users', 'metadata')
```

### 4. PostgreSQL 전용 인덱스

```python
def upgrade():
    # BTREE 인덱스 (기본)
    op.create_index('idx_username_btree', 'users', ['username'])
    
    # HASH 인덱스
    op.create_index('idx_email_hash', 'users', ['email'],
                   postgresql_using='hash')
    
    # GIN 인덱스 (전체 텍스트 검색)
    op.create_index('idx_content_gin', 'posts', ['content'],
                   postgresql_using='gin',
                   postgresql_ops={'content': 'gin_trgm_ops'})
    
    # 부분 인덱스 (조건부)
    op.create_index('idx_active_users', 'users', ['created_at'],
                   postgresql_where=sa.text("status = 'active'"))

def downgrade():
    op.drop_index('idx_active_users', 'users')
    op.drop_index('idx_content_gin', 'posts')
    op.drop_index('idx_email_hash', 'users')
    op.drop_index('idx_username_btree', 'users')
```

> **전체 텍스트 검색**: GIN 인덱스를 사용하려면 PostgreSQL의 `pg_trgm` 확장을 먼저 활성화해야 한다.
{: .prompt-tip}

```python
def upgrade():
    # 확장 활성화
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    
    # 이후 GIN 인덱스 생성
    op.create_index('idx_content_gin', 'posts', ['content'],
                   postgresql_using='gin',
                   postgresql_ops={'content': 'gin_trgm_ops'})
```

### 5. 파티셔닝 (Partitioning)

- PostgreSQL 10+ 버전에서 테이블 파티셔닝 설정

```python
def upgrade():
    # 파티션 부모 테이블 생성
    op.execute("""
        CREATE TABLE logs (
            id SERIAL,
            log_date DATE NOT NULL,
            message TEXT,
            PRIMARY KEY (id, log_date)
        ) PARTITION BY RANGE (log_date)
    """)
    
    # 파티션 생성
    op.execute("""
        CREATE TABLE logs_2025_01 PARTITION OF logs
        FOR VALUES FROM ('2025-01-01') TO ('2025-02-01')
    """)
    
    op.execute("""
        CREATE TABLE logs_2025_02 PARTITION OF logs
        FOR VALUES FROM ('2025-02-01') TO ('2025-03-01')
    """)

def downgrade():
    op.execute("DROP TABLE logs_2025_02")
    op.execute("DROP TABLE logs_2025_01")
    op.execute("DROP TABLE logs")
```

### 6. 시퀀스(Sequence) 관리

```python
def upgrade():
    # 시퀀스 생성
    op.execute("CREATE SEQUENCE user_id_seq START 1000")
    
    # 컬럼의 기본값으로 시퀀스 사용
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN id 
        SET DEFAULT nextval('user_id_seq')
    """)

def downgrade():
    op.execute("ALTER TABLE users ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE user_id_seq")
```

### 7. 동시성 제어 (Concurrent Operations)

- 대용량 테이블에서 인덱스를 생성할 때 **CONCURRENTLY** 옵션 사용

```python
def upgrade():
    # 일반 인덱스 생성 - 테이블 락 발생
    # op.create_index('idx_username', 'users', ['username'])
    
    # CONCURRENTLY 옵션 - 락 없이 인덱스 생성
    op.execute("""
        CREATE INDEX CONCURRENTLY idx_username 
        ON users (username)
    """)

def downgrade():
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS idx_username")
```

> **주의**: `CONCURRENTLY` 옵션은 트랜잭션 밖에서 실행되어야 한다. Alembic에서는 `op.execute()`와 함께 사용하는 것이 좋다.
{: .prompt-warning}

### 8. UUID 타입

```python
from sqlalchemy.dialects.postgresql import UUID
import uuid

# models.py
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

```python
# 마이그레이션
def upgrade():
    # UUID 확장 활성화
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                 primary_key=True,
                 server_default=sa.text('uuid_generate_v4()'))
    )

def downgrade():
    op.drop_table('users')
```

## 💡 실무 팁과 베스트 프랙티스

### 1. 마이그레이션 파일명 규칙

```bash
# 날짜와 시간을 포함한 명명 규칙 설정
# alembic.ini
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# 결과: 20250115_1030_2a3b4c5d6e7f_add_user_table.py
```

### 2. 자동 생성 검증

```python
# alembic/env.py
def run_migrations_online():
    # ... 기존 코드 ...
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # 타입 변경 감지
            compare_server_default=True,  # 기본값 변경 감지
        )
```

> **자동 생성 후 반드시 확인**: Alembic의 자동 생성은 완벽하지 않다. 생성된 마이그레이션 파일을 반드시 검토하는 것이 좋다.
{: .prompt-warning}

### 3. 대용량 데이터 처리

```python
def upgrade():
    # 작은 배치로 나눠서 처리
    bind = op.get_bind()
    
    batch_size = 1000
    offset = 0
    
    while True:
        result = bind.execute(
            sa.text(f"""
                UPDATE users 
                SET processed = true 
                WHERE id IN (
                    SELECT id FROM users 
                    WHERE processed = false 
                    LIMIT {batch_size}
                )
            """)
        )
        
        if result.rowcount == 0:
            break
        
        offset += batch_size
        print(f"Processed {offset} rows...")
```

### 4. 롤백 가능성 보장

```python
def upgrade():
    # 데이터 백업
    op.execute("""
        CREATE TABLE users_backup AS 
        SELECT * FROM users
    """)
    
    # 실제 변경
    op.add_column('users', sa.Column('new_field', sa.String(100)))

def downgrade():
    # 백업에서 복원
    op.execute("DROP TABLE users")
    op.execute("ALTER TABLE users_backup RENAME TO users")
```

### 5. 환경별 설정 분리

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://dev:dev@localhost/dev_db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
```

```python
# alembic/env.py
from config import config as app_config
import os

env = os.getenv('ENVIRONMENT', 'development')
db_url = app_config[env].SQLALCHEMY_DATABASE_URI

# 설정에서 URL 가져오기
config.set_main_option('sqlalchemy.url', db_url)
```

### 6. 팀 협업 워크플로우

```mermaid
flowchart TD
    A[개발자가 모델 변경] --> B[alembic revision --autogenerate]
    B --> C[마이그레이션 파일 검토 및 수정]
    C --> D[Git commit & push]
    D --> E[다른 개발자가 pull]
    E --> F[alembic upgrade head]
    F --> G[로컬 DB 동기화 완료]
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style G fill:#e8f5e8
```

### 7. CI/CD 통합

```yaml
# .github/workflows/deploy.yml
name: Deploy with Migrations

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          alembic upgrade head
      
      - name: Deploy application
        run: |
          # 배포 스크립트 실행
```

### 8. 마이그레이션 테스트

```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config

@pytest.fixture
def alembic_config():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", "postgresql://test:test@localhost/test_db")
    return config

def test_upgrade_and_downgrade(alembic_config):
    # 최신 버전으로 업그레이드
    command.upgrade(alembic_config, "head")
    
    # 한 단계 다운그레이드
    command.downgrade(alembic_config, "-1")
    
    # 다시 최신 버전으로
    command.upgrade(alembic_config, "head")
```

## 🔧 트러블슈팅

### 문제 1: "Target database is not up to date"

```bash
# 현재 상태 확인
alembic current

# 강제로 현재 상태를 특정 리비전으로 설정
alembic stamp head
```

### 문제 2: 충돌하는 마이그레이션

```bash
# 두 브랜치의 마이그레이션이 충돌할 때
alembic merge -m "merge conflicting migrations" rev1 rev2
```

### 문제 3: PostgreSQL 권한 오류

```sql
-- 사용자에게 필요한 권한 부여
GRANT CREATE ON DATABASE mydb TO myuser;
GRANT USAGE ON SCHEMA public TO myuser;
GRANT CREATE ON SCHEMA public TO myuser;
```

### 문제 4: 마이그레이션 실행 중 에러

```python
# 트랜잭션 격리 수준 설정
# alembic/env.py
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        isolation_level="AUTOCOMMIT"  # DDL 명령에 필요
    )
```

## 📚 참고자료

- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
