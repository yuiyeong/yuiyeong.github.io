---
title: "🎭 Poetry: Python 프로젝트의 의존성 관리와 패키징을 위한 모던 도구"
date: 2025-09-05 14:19:00 +0900
categories:
  - PYTHON
  - MANAGING
tags:
  - 급발진거북이
  - GeekAndChill
  - 기깬칠
  - poetry
  - 포에트리
  - 의존성
  - dependency
  - PEP621
  - pyproject_toml
  - pip
  - python
  - 파이썬
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 python package

- poetry==2.2.0
- python==3.12

## 🚀 TL;DR

- **Poetry**는 Python 프로젝트의 의존성 관리, 패키징, 가상환경 관리를 통합한 올인원 도구다
- `pyproject.toml` 파일 하나로 프로젝트 메타데이터와 의존성을 선언적으로 관리한다
- **의존성 잠금(lock)** 메커니즘으로 재현 가능한 빌드 환경을 보장한다
- 가상환경을 자동으로 생성/관리하여 pip + venv + setuptools의 복잡함을 해결한다
- **의존성 그룹**으로 개발/테스트/프로덕션 환경을 명확히 분리할 수 있다
- PyPI에 패키지를 배포하는 과정을 단순화하고 표준화한다
- **플러그인 시스템**과 **스크립트 정의**로 개발 워크플로우를 자동화할 수 있다
- **PEP 621 표준**을 준수하여 다른 도구와의 호환성을 확보할 수 있다

## 📓 실습 Jupyter Notebook

- w.i.p.

## 🌊 Poetry가 해결하는 문제들

Python 프로젝트를 개발하다 보면 다음과 같은 문제들을 마주치게 된다.

### 기존 도구들의 한계

- **pip + requirements.txt**: 의존성 버전 충돌, 재현성 부족
- **setuptools + setup.py**: 복잡한 설정, 표준화되지 않은 메타데이터
- **venv/virtualenv**: 수동 관리 필요, 프로젝트와 분리된 환경
- **여러 도구의 조합**: 학습 곡선이 높고 일관성 없는 워크플로우

Poetry는 이 모든 도구들의 기능을 하나로 통합하여 **일관된 개발 경험**을 제공한다.

```python
# 기존 방식: 여러 명령어와 파일 필요
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# pip install -r requirements-dev.txt
# python setup.py install

# Poetry 방식: 단일 명령어
# poetry install
```

## 📚 Poetry 설치와 기본 설정

### Poetry 설치하기

Poetry는 시스템 전역에 설치하는 것을 권장한다. pip로 설치하지 않고 독립적인 설치 스크립트를 사용하는 것이 좋다.

```bash
# macOS/Linux/WSL - 공식 설치 스크립트
curl -sSL https://install.python-poetry.org | python3 -

# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# 설치 확인
poetry --version
# 출력: Poetry (version 2.2.0)
```

### 전역 설정 구성

Poetry의 동작을 커스터마이징할 수 있는 주요 설정들이다.

```bash
# 가상환경을 프로젝트 디렉토리 내에 생성 (.venv 폴더)
poetry config virtualenvs.in-project true

# 가상환경 자동 생성 비활성화 (기존 환경 사용시)
poetry config virtualenvs.create false

# PyPI 외 추가 저장소 설정
poetry config repositories.private https://private.pypi.org/simple/

# 설정 확인
poetry config --list
```

## 🎯 프로젝트 초기화와 구조

### 새 프로젝트 생성

Poetry로 새 Python 프로젝트를 시작하는 두 가지 방법이 있다.

```bash
# 방법 1: 새 디렉토리와 함께 프로젝트 생성
poetry new my-project

# 방법 2: 기존 디렉토리에서 초기화
cd existing-project
poetry init  # 대화형 설정 프로세스 시작
```

### 프로젝트 구조

Poetry가 생성하는 표준 프로젝트 구조는 다음과 같다.

```
my-project/
├── pyproject.toml       # 프로젝트 설정과 의존성
├── README.md           # 프로젝트 문서
├── my_project/         # 소스 코드 디렉토리
│   └── __init__.py
└── tests/              # 테스트 디렉토리
    └── __init__.py
```

### pyproject.toml 파일 구조

**pyproject.toml**은 Poetry 프로젝트의 핵심 설정 파일이다. PEP 518과 PEP 621 표준을 따른다.

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A sample Python project managed by Poetry"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/username/my-project"
repository = "https://github.com/username/my-project"
keywords = ["sample", "poetry", "project"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"
pydantic = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
mypy = "^1.0.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.4.0"
mkdocs-material = "^9.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 🎨 PEP 621 표준 준수 방법

### PEP 621이란?

**PEP 621**은 Python 프로젝트 메타데이터를 `pyproject.toml`에 표준화된 방식으로 저장하는 방법을 정의한다. 이를 통해 서로 다른 빌드 도구 간의 호환성을 확보할 수 있다.

> **요즘은 PEP 621 준수 방식을 더 선호한다.** 이는 Poetry뿐만 아니라 pip, setuptools, flit, hatch 등 다른 도구들과도 호환되기 때문이다. 프로젝트를 Poetry에 종속시키지 않고 표준을 따르는 것이 장기적으로 더 유리하다. 
{: .prompt-tip}

### PEP 621 준수 pyproject.toml 구조

```toml
# PEP 621 표준 메타데이터 섹션
[project]
name = "my-project"
version = "0.1.0"
description = "A Python project following PEP 621"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"}
]
keywords = ["sample", "poetry", "pep621"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

# PEP 621 의존성 정의
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
    "click>=8.0.0",
]

# PEP 621 선택적 의존성 (extras)
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]
docs = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=9.0.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
]

# PEP 621 URL 정의
[project.urls]
Homepage = "https://github.com/username/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/username/my-project.git"
Issues = "https://github.com/username/my-project/issues"
Changelog = "https://github.com/username/my-project/blob/main/CHANGELOG.md"

# PEP 621 스크립트 엔트리포인트
[project.scripts]
my-cli = "my_project.cli:main"
my-tool = "my_project.tool:run"

# PEP 621 GUI 스크립트 (Windows용)
[project.gui-scripts]
my-gui = "my_project.gui:main"

# Poetry 특화 설정 (PEP 621과 별도)
[tool.poetry]
# Poetry만의 고급 기능 사용시
packages = [{include = "my_project"}]

# Poetry 의존성 관리 (PEP 621과 병행 사용)
[tool.poetry.dependencies]
python = "^3.8"
# Poetry의 고급 의존성 표현 사용 가능

[tool.poetry.group.dev.dependencies]
# Poetry 그룹 기능 활용

# 빌드 시스템 (Poetry 사용)
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### PEP 621과 Poetry 설정 혼용 전략

```toml
# 하이브리드 접근법: PEP 621 + Poetry 고급 기능

# 1. 기본 메타데이터는 PEP 621 사용
[project]
name = "hybrid-project"
version = "1.0.0"
description = "Best of both worlds"
dependencies = [
    "requests>=2.28.0",
    "fastapi>=0.100.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "black>=23.0.0"]

# 2. Poetry 고급 기능은 tool.poetry 사용
[tool.poetry.dependencies]
# Git 의존성, 로컬 패키지 등 복잡한 의존성
private-package = {git = "https://github.com/org/private.git", rev = "main"}
local-package = {path = "../local-package", develop = true}

# 3. Poetry 그룹 기능 활용
[tool.poetry.group.test.dependencies]
pytest-xdist = "^3.0.0"
pytest-timeout = "^2.1.0"

[tool.poetry.group.lint]
optional = true

[tool.poetry.group.lint.dependencies]
ruff = "^0.1.0"
pylint = "^3.0.0"
```

### PEP 621 준수의 장점

> PEP 621을 준수하면 다음과 같은 다양한 도구를 선택적으로 사용할 수 있다.
> 즉, 도구들이 모두 동일한 pyproject.toml 을 읽고 처리할 수 있다.
{: .prompt-tip}

- pip으로 직접 설치 (pip 23.0+)
	- `pip install .`
- build로 패키지 빌드
	- `python -m build`
- Poetry로 관리
	- `poetry install`
- PDM으로 전환
	- `pdm install`
- Hatch로 관리
	- `hatch env create`

### PEP 621 마이그레이션 가이드

- 기존 Poetry 전용 프로젝트를 PEP 621로 마이그레이션

```bash
# 1. 백업 생성
cp pyproject.toml pyproject.toml.backup

# 2. poetry-plugin-export 설치 (필요시)
poetry self add poetry-plugin-export

# 3. 현재 의존성 확인
poetry show --no-dev  # 런타임 의존성
poetry show --only dev  # 개발 의존성
```

### PEP 621과 Poetry 모범 사례

```toml
# best_practices.toml
# 모범 사례를 적용한 pyproject.toml

# ===== PEP 621 표준 섹션 =====
[project]
# 필수 메타데이터
name = "awesome-project"
version = "2.0.0"  # 또는 동적 버전 사용
description = "Production-ready Python project"

# 동적 버전 관리 (선택사항)
# dynamic = ["version"]  # version을 다른 곳에서 읽음

# 상세 메타데이터
readme = {file = "README.md", content-type = "text/markdown"}
requires-python = ">=3.8,<3.13"
license = {file = "LICENSE"}
authors = [
    {name = "Team Lead", email = "lead@example.com"},
]
maintainers = [
    {name = "Maintainer", email = "maintainer@example.com"},
]

# 분류 정보
keywords = ["fastapi", "async", "web", "api"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]

# 핵심 의존성 (범용적인 형식 사용)
dependencies = [
    "fastapi>=0.100.0,<1.0.0",
    "pydantic>=2.0.0,<3.0.0",
    "uvicorn[standard]>=0.23.0,<1.0.0",
    "httpx>=0.24.0,<1.0.0",
    "sqlalchemy>=2.0.0,<3.0.0",
    "alembic>=1.11.0,<2.0.0",
]

# 선택적 의존성 그룹
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.3.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.22.0",
]
test = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "faker>=19.0.0",
]
production = [
    "gunicorn>=21.0.0",
    "supervisor>=4.2.0",
    "python-json-logger>=2.0.0",
]

# 프로젝트 URL
[project.urls]
Homepage = "https://awesome-project.io"
Documentation = "https://docs.awesome-project.io"
Repository = "https://github.com/org/awesome-project"
Issues = "https://github.com/org/awesome-project/issues"
Changelog = "https://github.com/org/awesome-project/blob/main/CHANGELOG.md"
"Source Code" = "https://github.com/org/awesome-project"
"Bug Tracker" = "https://github.com/org/awesome-project/issues"

# CLI 엔트리포인트
[project.scripts]
awesome = "awesome_project.cli:main"
awesome-admin = "awesome_project.admin:cli"

# ===== Poetry 특화 섹션 =====
[tool.poetry]
# Poetry만의 고급 기능
packages = [
    {include = "awesome_project", from = "src"},
]

# Poetry 고급 의존성 (PEP 621로 표현 어려운 것들)
[tool.poetry.dependencies]
python = "^3.8"
# 프라이빗 패키지
internal-lib = {url = "https://private.pypi.org/packages/internal-lib-1.0.0.whl"}
# Git 의존성
edge-feature = {git = "https://github.com/org/edge.git", branch = "develop", optional = true}
# 로컬 개발 패키지
local-dev = {path = "../local-package", develop = true, optional = true}

# Poetry 개발 그룹
[tool.poetry.group.dev.dependencies]
ipython = "^8.14.0"
rich = "^13.5.0"

# Poetry 선택적 그룹
[tool.poetry.group.benchmark]
optional = true

[tool.poetry.group.benchmark.dependencies]
locust = "^2.15.0"
pytest-benchmark = "^4.0.0"

# ===== 빌드 시스템 =====
[build-system]
requires = ["poetry-core>=1.7.0"]
build-backend = "poetry.core.masonry.api"

# ===== 다른 도구 설정 =====
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.8"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-ra -q --strict-markers --cov=awesome_project"

[tool.coverage.run]
source = ["awesome_project"]
omit = ["*/tests/*", "*/migrations/*"]
```

## 🔧 의존성 관리

### 의존성 추가와 제거

Poetry는 의존성을 추가할 때 자동으로 호환 가능한 버전을 찾고 lock 파일을 업데이트한다.

```bash
# 런타임 의존성 추가
poetry add requests pandas numpy

# 특정 버전 지정
poetry add "django@^4.2"

# 개발 의존성 추가 (dev 그룹)
poetry add --group dev pytest black mypy

# 선택적 그룹에 추가
poetry add --group docs mkdocs

# Git 저장소에서 설치
poetry add git+https://github.com/user/repo.git

# 로컬 패키지 설치
poetry add --editable ../my-local-package

# 의존성 제거
poetry remove requests

# 개발 의존성 제거
poetry remove --group dev pytest
```

### 버전 지정 방식

Poetry는 **시맨틱 버전 관리**를 따르며, 다양한 버전 제약 표현을 지원한다.

```python
# pyproject.toml 예시
dependencies = {
    # 캐럿(^): 호환 가능한 버전 (가장 일반적)
    "django": "^4.2.0",     # >=4.2.0, <5.0.0
    
    # 틸드(~): 마이너 버전 고정
    "requests": "~2.28.0",  # >=2.28.0, <2.29.0
    
    # 정확한 버전
    "numpy": "1.24.3",
    
    # 범위 지정
    "pandas": ">=1.5,<2.0",
    
    # 와일드카드
    "pytest": "*",          # 최신 버전
    
    # 여러 제약 조합
    "python": ">=3.8,<3.12",
}
```

### poetry.lock 파일의 중요성

**poetry.lock** 파일은 모든 의존성의 정확한 버전을 기록하여 **재현 가능한 빌드**를 보장한다.

```python
# poetry.lock 파일 생성/업데이트
# poetry install 또는 poetry add 시 자동 생성

# lock 파일만 업데이트 (설치하지 않음)
# poetry lock

# lock 파일 무시하고 최신 버전으로 업데이트
# poetry update

# 특정 패키지만 업데이트
# poetry update requests pandas
```

> **poetry.lock 파일은 반드시 버전 관리 시스템에 커밋해야 한다.** 이를 통해 팀 전체가 동일한 의존성 버전을 사용할 수 있다.
{: .prompt-tip}

## 🎨 의존성 그룹 활용

Poetry 2.2에서는 **의존성 그룹** 기능이 강화되어 환경별 의존성 관리가 더욱 편리해졌다.

### 그룹 정의와 사용

```toml
# pyproject.toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-cov = "^4.0.0"
black = "^23.0.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.0.0"
tox = "^4.0.0"

# 선택적 그룹 (명시적으로 설치해야 함)
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
sphinx = "^6.0.0"
sphinx-rtd-theme = "^1.2.0"
```

### 그룹별 설치

```bash
# 기본 의존성 + 모든 필수 그룹
poetry install

# 특정 그룹 제외
poetry install --without dev,test

# 특정 그룹만 포함
poetry install --only main,docs

# 선택적 그룹 포함
poetry install --with docs

# 여러 조합
poetry install --without dev --with docs
```

## 🏃 가상환경과 명령어 실행

### 가상환경 관리

Poetry는 프로젝트별로 격리된 가상환경을 자동으로 관리한다.

```bash
# 가상환경 정보 확인
poetry env info

# 가상환경 경로 확인
poetry env info --path

# Python 버전 지정하여 환경 생성
poetry env use python3.11

# 가상환경 목록 보기
poetry env list

# 가상환경 삭제
poetry env remove python3.11

# 모든 가상환경 삭제
poetry env remove --all
```

### 명령어 실행

```bash
# 가상환경 내에서 명령어 실행
poetry run python script.py
poetry run pytest
poetry run black .

# 가상환경 쉘 활성화
poetry shell

# 스크립트 정의와 실행
# pyproject.toml에 정의
[tool.poetry.scripts]
my-cli = "my_project.cli:main"
serve = "my_project.server:run"

# 실행
poetry run my-cli
poetry run serve
```

## 📦 패키지 빌드와 배포

### 패키지 빌드

Poetry는 표준 Python 패키지 형식으로 프로젝트를 빌드할 수 있다.

```bash
# wheel과 sdist 빌드
poetry build

# 출력 예시:
# Building my-project (0.1.0)
#   - Building sdist
#   - Built my_project-0.1.0.tar.gz
#   - Building wheel
#   - Built my_project-0.1.0-py3-none-any.whl

# 특정 형식만 빌드
poetry build --format wheel
```

### PyPI 배포

```bash
# PyPI 자격증명 설정
poetry config pypi-token.pypi your-api-token

# 또는 사용자명/비밀번호
poetry config http-basic.pypi username password

# 패키지 배포
poetry publish

# 빌드와 배포를 한 번에
poetry publish --build

# 테스트 PyPI에 배포
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish --repository test-pypi
```

## 🚀 고급 기능과 팁

### 플러그인 시스템

Poetry 2.2는 플러그인을 통한 확장을 지원한다.

```bash
# 플러그인 설치
poetry self add poetry-plugin-export

# 설치된 플러그인 확인
poetry self show plugins

# requirements.txt 내보내기 (export 플러그인 사용)
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --dev --output requirements-dev.txt
```

### 환경 변수와 설정

```python
# .env 파일 사용
# poetry-dotenv-plugin 설치 필요
# poetry self add poetry-dotenv-plugin

# pyproject.toml에서 환경 변수 참조
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.8"
private-package = {url = "${PRIVATE_REPO_URL}/package.whl"}
```

### 모노레포 지원

Poetry는 여러 패키지를 포함하는 모노레포 구조를 지원한다.

```toml
# 워크스페이스 설정 (pyproject.toml)
[tool.poetry]
packages = [
    { include = "package_a", from = "packages" },
    { include = "package_b", from = "packages" },
]

[tool.poetry.dependencies]
package-a = {path = "packages/package_a", develop = true}
package-b = {path = "packages/package_b", develop = true}
```

### 스크립트와 태스크 자동화

```toml
# pyproject.toml
[tool.poetry.scripts]
test = "pytest:main"
format = "black:main"
lint = "my_project.scripts:lint"
serve = "my_project.server:run"

# 복잡한 태스크는 Python 스크립트로
[tool.poetry.scripts]
dev = "my_project.scripts:dev_server"
```

```python
# my_project/scripts.py
import subprocess
import sys

def dev_server():
    """개발 서버 실행 스크립트"""
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "my_project.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

def lint():
    """코드 품질 검사 실행"""
    commands = [
        ["black", "--check", "."],
        ["mypy", "my_project"],
        ["flake8", "my_project"],
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd)
        if result.returncode != 0:
            sys.exit(1)
```

## 🔍 문제 해결과 디버깅

### 일반적인 문제와 해결책

```bash
# 의존성 충돌 해결
poetry update --dry-run  # 실제 업데이트 없이 확인
poetry show --tree      # 의존성 트리 확인

# 캐시 문제 해결
poetry cache clear pypi --all
poetry install --no-cache

# lock 파일 충돌 해결
poetry lock --no-update  # 기존 버전 유지하며 lock 재생성

# 특정 패키지 문제 추적
poetry show package-name --tree

# 버전 충돌 상세 정보
poetry install -vvv  # 상세 로그 출력
```

### 성능 최적화

```bash
# 병렬 설치 설정
poetry config installer.parallel true

# 캐시 디렉토리 변경 (SSD 활용)
poetry config cache-dir /path/to/ssd/cache

# 설치 시간 단축
poetry install --no-root  # 현재 프로젝트 설치 제외
```

## 🔄 다른 도구와의 비교

### Poetry vs pip-tools

```python
# pip-tools 방식
# requirements.in -> pip-compile -> requirements.txt
# pip-sync requirements.txt

# Poetry 방식
# pyproject.toml -> poetry lock -> poetry.lock
# poetry install

# Poetry의 장점:
# - 통합된 도구 (가상환경, 빌드, 배포 포함)
# - 더 나은 의존성 해결 알고리즘
# - 표준화된 pyproject.toml 사용
```

### Poetry vs Pipenv

```python
# Pipenv과의 주요 차이점
differences = {
    "설정 파일": {
        "Poetry": "pyproject.toml (표준)",
        "Pipenv": "Pipfile (비표준)"
    },
    "성능": {
        "Poetry": "빠른 의존성 해결",
        "Pipenv": "느린 lock 생성"
    },
    "패키징": {
        "Poetry": "내장 지원",
        "Pipenv": "별도 도구 필요"
    },
    "스크립트": {
        "Poetry": "pyproject.toml에 정의",
        "Pipenv": "Pipfile에 정의"
    }
}
```

## 🎯 실무 활용 사례

### Django 프로젝트 설정

```toml
# Django 프로젝트용 pyproject.toml
[tool.poetry]
name = "django-app"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.11"
django = "^4.2"
psycopg2-binary = "^2.9"
redis = "^4.5"
celery = "^5.2"
gunicorn = "^20.1"

[tool.poetry.group.dev.dependencies]
django-debug-toolbar = "^4.0"
django-extensions = "^3.2"
ipython = "^8.12"
pre-commit = "^3.2"

[tool.poetry.scripts]
manage = "django.core.management:execute_from_command_line"
```

### FastAPI 마이크로서비스

```toml
# FastAPI 프로젝트용 pyproject.toml
[tool.poetry]
name = "fastapi-service"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100.0"
uvicorn = {extras = ["standard"], version = "^0.23.0"}
pydantic = "^2.0"
httpx = "^0.24.0"
sqlalchemy = "^2.0"
alembic = "^1.11"

[tool.poetry.group.test.dependencies]
pytest = "^7.4"
pytest-asyncio = "^0.21"
pytest-cov = "^4.1"
httpx = "^0.24"

[tool.poetry.scripts]
start = "uvicorn:main"
migrate = "alembic:main"
test = "pytest:main"
```

### 데이터 사이언스 프로젝트

```toml
# 데이터 분석 프로젝트용 pyproject.toml
[tool.poetry]
name = "data-analysis"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.0"
numpy = "^1.24"
scikit-learn = "^1.3"
matplotlib = "^3.7"
seaborn = "^0.12"
jupyter = "^1.0"
polars = "^0.18"  # 더 빠른 데이터프레임

[tool.poetry.group.ml.dependencies]
torch = "^2.0"
transformers = "^4.30"
wandb = "^0.15"

[tool.poetry.group.viz]
optional = true

[tool.poetry.group.viz.dependencies]
plotly = "^5.14"
dash = "^2.11"
streamlit = "^1.24"
```


> Poetry는 단순히 의존성 관리 도구가 아니라 **Python 프로젝트의 전체 생명주기를 관리하는 플랫폼**이다. 초기 학습 비용은 있지만, 장기적으로 보면 프로젝트 유지보수와 협업 효율성에서 큰 이득을 얻을 수 있다. 특히 PEP 621 표준을 따르면서 Poetry의 고급 기능을 활용하는 하이브리드 접근법을 사용하면, 도구에 종속되지 않으면서도 강력한 기능을 활용할 수 있다.
{: .prompt-tip}
