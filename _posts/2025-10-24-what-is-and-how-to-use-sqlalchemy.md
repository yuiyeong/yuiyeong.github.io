---
title: "🗄️ SQLAlchemy v2 완벽 가이드: Python에서 PostgreSQL 사용하기"
date: 2025-10-24 19:43:00 +0900
categories:
  - PYTHON
  - DB
tags:
  - 급발진거북이
  - GeekAndChill
  - 기깬칠
  - python
  - 파이썬
  - sql
  - orm
  - sqlalchemy
toc: true
comments: false
mermaid: true
math: true
---
## 📦 사용하는 패키지/기술 버전 정보

- sqlalchemy==2.0.36
- psycopg2-binary==2.9.10
- python==3.12.0
- postgresql==16.0

## 🚀 TL;DR

- **SQLAlchemy**는 Python에서 가장 인기 있는 SQL 툴킷이자 ORM(Object-Relational Mapping) 라이브러리다
- **v2.0**에서 대대적인 변경이 있었으며, 더 명확하고 타입 안전한 API를 제공한다
- **ORM 방식**은 Python 객체로 데이터베이스를 다루고, **Core 방식**은 SQL에 가까운 저수준 제어를 제공한다
- **Engine**은 데이터베이스 연결을 관리하고, **Session**은 트랜잭션과 객체 생명주기를 관리한다
- **선언적 모델(Declarative Model)** 로 테이블 구조를 Python 클래스로 정의할 수 있다
- **관계(Relationship)** 설정으로 외래키 연결과 JOIN 쿼리를 직관적으로 처리할 수 있다
- **쿼리 빌더**는 타입 안전하고 재사용 가능한 데이터베이스 쿼리를 작성할 수 있게 해준다
- **Alembic**과 함께 사용하여 데이터베이스 스키마 마이그레이션을 관리할 수 있다

## 📓 실습 Jupyter Notebook

- w.i.p.

## 🤔 SQLAlchemy란?

**SQLAlchemy**는 Python에서 데이터베이스를 다루기 위한 가장 강력하고 유연한 도구다. 마치 Python과 SQL 사이의 통역사 역할을 한다고 생각하면 된다.

### SQLAlchemy의 두 가지 접근 방식

SQLAlchemy는 두 가지 사용 방식을 제공한다.

**1. ORM (Object-Relational Mapping)**

- Python 클래스와 객체를 사용하여 데이터베이스를 다루는 방식
- SQL을 직접 작성하지 않고도 데이터베이스 작업 수행
- 객체 지향적이고 직관적인 코드 작성 가능

**2. Core (SQL Expression Language)**

- SQL에 가까운 저수준 방식
- 더 세밀한 제어와 최적화 가능
- 복잡한 쿼리나 성능이 중요한 경우 유용

```mermaid
graph TB
    A[Python Application] --> B{SQLAlchemy}
    B --> C[ORM Layer]
    B --> D[Core Layer]
    C --> E[Engine]
    D --> E
    E --> F[Database Driver<br/>psycopg2]
    F --> G[(PostgreSQL)]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#f3e5f5
    style E fill:#fce4ec
    style G fill:#e1f5fe
```

> **왜 SQLAlchemy를 사용할까?**
> 
> - **데이터베이스 독립성**: PostgreSQL, MySQL, SQLite 등 다양한 DB를 같은 코드로 사용
> - **생산성 향상**: SQL 대신 Python 코드로 작업하여 개발 속도 증가
> - **타입 안전성**: IDE의 자동완성과 타입 체킹 지원
> - **보안**: SQL 인젝션 공격 자동 방어
> - **유지보수**: 객체 지향적 구조로 코드 관리 용이
{: .prompt-tip}

## 🏗️ SQLAlchemy v2의 핵심 컨셉

### v1에서 v2로의 주요 변화

SQLAlchemy v2.0은 이전 버전의 많은 문제점을 개선했다.

**1. 명확한 API**

- 애매모호한 동작 제거
- 명시적인 트랜잭션 관리
- 타입 힌트 강화

**2. 성능 개선**

- 더 효율적인 쿼리 실행
- 메모리 사용 최적화

**3. 현대적인 Python 활용**

- Type hints 완전 지원
- Async/await 네이티브 지원

```python
# v1.x 스타일 (레거시)
result = session.query(User).filter(User.name == 'Alice').first()

# v2.0 스타일 (권장)
from sqlalchemy import select

stmt = select(User).where(User.name == 'Alice')
result = session.scalar(stmt)
```

## 🔧 핵심 구성 요소

### 1. Engine - 데이터베이스 연결 관리자

**Engine**은 SQLAlchemy와 데이터베이스 사이의 연결을 관리하는 핵심 객체다. 마치 데이터베이스로 가는 전화선이라고 생각하면 된다.

```python
from sqlalchemy import create_engine

# PostgreSQL 연결 URL 형식
# postgresql://사용자명:비밀번호@호스트:포트/데이터베이스명
engine = create_engine(
    "postgresql://user:password@localhost:5432/mydb",
    echo=True,  # SQL 쿼리 로깅 (디버깅용)
    pool_size=5,  # 연결 풀 크기
    max_overflow=10  # 추가 연결 허용 개수
)

# 연결 테스트
with engine.connect() as conn:
    print("데이터베이스 연결 성공!")
```

**Engine의 주요 기능**

- **연결 풀링(Connection Pooling)**: 여러 연결을 재사용하여 성능 향상
- **방언(Dialect) 관리**: 각 데이터베이스의 특성에 맞게 SQL 변환
- **스레드 안전성**: 멀티스레드 환경에서 안전하게 사용

### 2. Session - 작업 단위 관리자

**Session**은 데이터베이스 작업의 작업 단위를 관리한다. 트랜잭션을 시작하고, 변경사항을 추적하고, 커밋 또는 롤백한다.

```python
from sqlalchemy.orm import Session

# Session 생성 (기본 방법)
session = Session(engine)

# 컨텍스트 매니저 사용 (권장)
with Session(engine) as session:
    # 여기서 데이터베이스 작업
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()  # 변경사항 저장
# session은 자동으로 닫힘

# SessionMaker를 사용한 세션 팩토리
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

> **Session의 생명주기**
> 
> 1. **시작**: Session 객체 생성
> 2. **작업**: 객체 추가, 수정, 삭제
> 3. **플러시(Flush)**: 변경사항을 SQL로 변환하여 전송 (자동 또는 수동)
> 4. **커밋(Commit)**: 트랜잭션 확정
> 5. **닫기(Close)**: 리소스 해제
{: .prompt-tip}

### 3. Declarative Base - 모델 정의의 기초

**Declarative Base**는 ORM 모델을 정의하기 위한 기본 클래스다. v2.0에서는 더 타입 안전한 방식으로 개선되었다.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from typing import Optional

# Base 클래스 정의
class Base(DeclarativeBase):
    pass

# 모델 정의
class User(Base):
    __tablename__ = "users"
    
    # v2.0 스타일: Mapped와 mapped_column 사용
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[Optional[int]]  # NULL 허용
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

# 테이블 생성
Base.metadata.create_all(engine)
```

### 4. Query Builder - 타입 안전한 쿼리

v2.0의 **select() 함수**는 타입 안전하고 명시적인 쿼리를 작성할 수 있게 해준다.

```python
from sqlalchemy import select, and_, or_

# 기본 SELECT
stmt = select(User)

# WHERE 조건
stmt = select(User).where(User.age > 18)

# 여러 조건 (AND)
stmt = select(User).where(
    and_(
        User.age > 18,
        User.name.like('A%')
    )
)

# 또는 (OR)
stmt = select(User).where(
    or_(
        User.name == 'Alice',
        User.name == 'Bob'
    )
)

# 정렬
stmt = select(User).order_by(User.name.desc())

# 제한
stmt = select(User).limit(10).offset(20)

# 실행
with Session(engine) as session:
    users = session.scalars(stmt).all()
    for user in users:
        print(user.name)
```

## 📝 기본 사용법: CRUD 작업

### Create - 데이터 생성

```python
from sqlalchemy.orm import Session

def create_user(name: str, email: str, age: int) -> User:
    """새로운 사용자 생성"""
    with Session(engine) as session:
        # 1. 객체 생성
        new_user = User(name=name, email=email, age=age)
        
        # 2. Session에 추가
        session.add(new_user)
        
        # 3. 커밋 (실제 DB에 저장)
        session.commit()
        
        # 4. 새로고침 (DB에서 생성된 ID 등을 가져옴)
        session.refresh(new_user)
        
        return new_user

# 사용 예시
user = create_user("Alice", "alice@example.com", 25)
print(f"생성된 사용자 ID: {user.id}")
# 출력: 생성된 사용자 ID: 1

# 여러 객체 한번에 추가
def create_multiple_users(users_data: list) -> None:
    with Session(engine) as session:
        users = [User(**data) for data in users_data]
        session.add_all(users)
        session.commit()

users_data = [
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 28}
]
create_multiple_users(users_data)
```

### Read - 데이터 조회

```python
from sqlalchemy import select

def get_user_by_id(user_id: int) -> Optional[User]:
    """ID로 사용자 조회"""
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        return session.scalar(stmt)

def get_all_users() -> list[User]:
    """모든 사용자 조회"""
    with Session(engine) as session:
        stmt = select(User)
        return list(session.scalars(stmt).all())

def get_users_by_age(min_age: int) -> list[User]:
    """나이 조건으로 조회"""
    with Session(engine) as session:
        stmt = select(User).where(User.age >= min_age)
        return list(session.scalars(stmt).all())

# 사용 예시
user = get_user_by_id(1)
print(f"조회된 사용자: {user.name}")
# 출력: 조회된 사용자: Alice

all_users = get_all_users()
print(f"전체 사용자 수: {len(all_users)}")
# 출력: 전체 사용자 수: 3

adults = get_users_by_age(25)
for user in adults:
    print(f"{user.name} (나이: {user.age})")
# 출력:
# Alice (나이: 25)
# Bob (나이: 30)
# Charlie (나이: 28)
```

### Update - 데이터 수정

```python
def update_user_email(user_id: int, new_email: str) -> bool:
    """사용자 이메일 업데이트"""
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalar(stmt)
        
        if user:
            user.email = new_email
            session.commit()
            return True
        return False

def increment_user_age(user_id: int) -> None:
    """사용자 나이 증가"""
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalar(stmt)
        
        if user:
            user.age = (user.age or 0) + 1
            session.commit()

# 사용 예시
success = update_user_email(1, "alice.new@example.com")
print(f"업데이트 {'성공' if success else '실패'}")
# 출력: 업데이트 성공

increment_user_age(1)
user = get_user_by_id(1)
print(f"Alice의 새로운 나이: {user.age}")
# 출력: Alice의 새로운 나이: 26
```

### Delete - 데이터 삭제

```python
def delete_user(user_id: int) -> bool:
    """사용자 삭제"""
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalar(stmt)
        
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

def delete_users_by_condition(min_age: int) -> int:
    """조건에 맞는 사용자들 삭제"""
    from sqlalchemy import delete
    
    with Session(engine) as session:
        stmt = delete(User).where(User.age < min_age)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount  # 삭제된 행 수

# 사용 예시
deleted = delete_user(1)
print(f"삭제 {'성공' if deleted else '실패'}")
# 출력: 삭제 성공

count = delete_users_by_condition(25)
print(f"{count}명의 사용자가 삭제되었습니다")
# 출력: 0명의 사용자가 삭제되었습니다 (25세 미만이 없음)
```

## 🔗 관계(Relationship) 설정

데이터베이스에서 테이블 간의 관계는 매우 중요하다. SQLAlchemy는 이러한 관계를 Python 객체로 직관적으로 표현할 수 있다.

### One-to-Many 관계

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "departments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # 관계 정의: 한 부서는 여러 직원을 가질 수 있음
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan"
    )

class Employee(Base):
    __tablename__ = "employees"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    
    # 역방향 관계: 각 직원은 하나의 부서에 속함
    department: Mapped["Department"] = relationship(back_populates="employees")

# 사용 예시
with Session(engine) as session:
    # 부서 생성
    it_dept = Department(name="IT")
    
    # 직원들 생성 및 부서에 추가
    emp1 = Employee(name="Alice", department=it_dept)
    emp2 = Employee(name="Bob", department=it_dept)
    
    session.add(it_dept)
    session.commit()
    
    # 부서의 직원들 조회
    print(f"{it_dept.name} 부서 직원:")
    for emp in it_dept.employees:
        print(f"  - {emp.name}")
    # 출력:
    # IT 부서 직원:
    #   - Alice
    #   - Bob
    
    # 직원의 부서 조회
    print(f"{emp1.name}의 부서: {emp1.department.name}")
    # 출력: Alice의 부서: IT
```

### Many-to-Many 관계

```python
from sqlalchemy import Table

# 연결 테이블 (Association Table)
student_course = Table(
    "student_course",
    Base.metadata,
    mapped_column("student_id", ForeignKey("students.id"), primary_key=True),
    mapped_column("course_id", ForeignKey("courses.id"), primary_key=True)
)

class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    # 다대다 관계
    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates="students"
    )

class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    
    # 역방향 다대다 관계
    students: Mapped[list["Student"]] = relationship(
        secondary=student_course,
        back_populates="courses"
    )

# 사용 예시
with Session(engine) as session:
    # 학생과 강좌 생성
    alice = Student(name="Alice")
    bob = Student(name="Bob")
    
    math = Course(title="Mathematics")
    physics = Course(title="Physics")
    
    # 학생에게 강좌 할당
    alice.courses.extend([math, physics])
    bob.courses.append(math)
    
    session.add_all([alice, bob, math, physics])
    session.commit()
    
    # 학생의 강좌 조회
    print(f"{alice.name}의 수강 과목:")
    for course in alice.courses:
        print(f"  - {course.title}")
    # 출력:
    # Alice의 수강 과목:
    #   - Mathematics
    #   - Physics
    
    # 강좌의 학생들 조회
    print(f"{math.title} 수강생:")
    for student in math.students:
        print(f"  - {student.name}")
    # 출력:
    # Mathematics 수강생:
    #   - Alice
    #   - Bob
```

## 🚀 고급 쿼리 기법

### JOIN 쿼리

```python
from sqlalchemy import select

def get_employees_with_departments():
    """직원과 부서 정보를 함께 조회"""
    with Session(engine) as session:
        # 명시적 JOIN
        stmt = (
            select(Employee, Department)
            .join(Employee.department)
            .where(Department.name == "IT")
        )
        
        results = session.execute(stmt).all()
        for emp, dept in results:
            print(f"{emp.name} - {dept.name}")

def get_departments_with_employee_count():
    """부서별 직원 수 조회"""
    from sqlalchemy import func
    
    with Session(engine) as session:
        stmt = (
            select(
                Department.name,
                func.count(Employee.id).label("employee_count")
            )
            .join(Department.employees)
            .group_by(Department.name)
        )
        
        results = session.execute(stmt).all()
        for dept_name, count in results:
            print(f"{dept_name}: {count}명")
        # 출력: IT: 2명
```

### 서브쿼리

```python
def get_departments_with_many_employees(min_count: int = 5):
    """직원이 많은 부서 조회"""
    from sqlalchemy import func
    
    with Session(engine) as session:
        # 서브쿼리: 부서별 직원 수
        subq = (
            select(
                Employee.department_id,
                func.count(Employee.id).label("emp_count")
            )
            .group_by(Employee.department_id)
            .having(func.count(Employee.id) >= min_count)
            .subquery()
        )
        
        # 메인 쿼리
        stmt = (
            select(Department)
            .join(subq, Department.id == subq.c.department_id)
        )
        
        departments = session.scalars(stmt).all()
        return departments
```

### 집계 함수

```python
from sqlalchemy import func

def get_statistics():
    """다양한 통계 정보 조회"""
    with Session(engine) as session:
        # 평균 나이
        avg_age = session.scalar(
            select(func.avg(User.age))
        )
        print(f"평균 나이: {avg_age:.1f}세")
        
        # 최대/최소 나이
        max_age = session.scalar(select(func.max(User.age)))
        min_age = session.scalar(select(func.min(User.age)))
        print(f"나이 범위: {min_age}세 ~ {max_age}세")
        
        # 전체 사용자 수
        total_users = session.scalar(
            select(func.count()).select_from(User)
        )
        print(f"전체 사용자: {total_users}명")
```

### Eager Loading (N+1 문제 해결)

```python
from sqlalchemy.orm import selectinload, joinedload

def get_departments_with_employees_efficient():
    """N+1 문제를 피하는 효율적인 조회"""
    with Session(engine) as session:
        # selectinload: 별도 쿼리로 관련 데이터 로드
        stmt = select(Department).options(
            selectinload(Department.employees)
        )
        
        departments = session.scalars(stmt).all()
        
        # 추가 쿼리 없이 employees 접근 가능
        for dept in departments:
            print(f"{dept.name}: {len(dept.employees)}명")

def get_employees_with_department_joined():
    """JOIN을 사용한 즉시 로딩"""
    with Session(engine) as session:
        # joinedload: JOIN으로 한 번에 로드
        stmt = select(Employee).options(
            joinedload(Employee.department)
        )
        
        employees = session.scalars(stmt).all()
        
        for emp in employees:
            print(f"{emp.name} - {emp.department.name}")
```

> **N+1 문제란?**
> 
> 부모 객체를 조회하는 쿼리 1개와 각 부모의 자식을 조회하는 쿼리 N개가 실행되는 성능 문제다.
> 
> - **문제**: 10개 부서 조회 시 11개 쿼리 실행 (부서 1개 + 각 부서의 직원 10개)
> - **해결**: `selectinload` 또는 `joinedload`로 2~3개 쿼리로 줄임
{: .prompt-warning}

## 🔄 트랜잭션 관리

### 기본 트랜잭션

```python
def transfer_money(from_account_id: int, to_account_id: int, amount: float):
    """계좌 이체 (트랜잭션 예시)"""
    with Session(engine) as session:
        try:
            # 송금 계좌에서 출금
            from_account = session.get(Account, from_account_id)
            if from_account.balance < amount:
                raise ValueError("잔액 부족")
            from_account.balance -= amount
            
            # 수신 계좌에 입금
            to_account = session.get(Account, to_account_id)
            to_account.balance += amount
            
            # 모두 성공 시 커밋
            session.commit()
            print(f"{amount}원 이체 완료")
            
        except Exception as e:
            # 오류 발생 시 롤백
            session.rollback()
            print(f"이체 실패: {e}")
            raise
```

### 중첩 트랜잭션 (Savepoint)

```python
def complex_operation():
    """복잡한 작업에서 부분 롤백"""
    with Session(engine) as session:
        # 메인 작업
        user = User(name="Alice")
        session.add(user)
        
        # Savepoint 생성
        savepoint = session.begin_nested()
        
        try:
            # 위험한 작업
            risky_user = User(name="Bob", email="invalid")
            session.add(risky_user)
            session.flush()
            
        except Exception:
            # 부분 롤백 (Alice는 유지)
            savepoint.rollback()
            print("위험한 작업만 롤백")
        
        # 전체 커밋
        session.commit()
```

## 🛠️ 실무 활용 패턴

### Repository 패턴

```python
from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    """기본 Repository 클래스"""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    def create(self, **kwargs) -> T:
        """객체 생성"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def get_by_id(self, id: int) -> Optional[T]:
        """ID로 조회"""
        return self.session.get(self.model, id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """전체 조회 (페이지네이션)"""
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """업데이트"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        """삭제"""
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False

# 사용 예시
class UserRepository(BaseRepository[User]):
    """User 전용 Repository"""
    
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)
    
    def get_adults(self) -> list[User]:
        stmt = select(User).where(User.age >= 18)
        return list(self.session.scalars(stmt).all())

# 실제 사용
with Session(engine) as session:
    user_repo = UserRepository(User, session)
    
    # 생성
    user = user_repo.create(name="Alice", email="alice@example.com", age=25)
    
    # 조회
    found_user = user_repo.get_by_email("alice@example.com")
    
    # 업데이트
    user_repo.update(user.id, age=26)
    
    # 삭제
    user_repo.delete(user.id)
```

### 의존성 주입 (FastAPI와 함께 사용)

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """데이터베이스 세션 제공 (컨텍스트 매니저)"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# FastAPI에서 사용
from fastapi import Depends

def get_db() -> Generator[Session, None, None]:
    """FastAPI 의존성"""
    with get_db_session() as session:
        yield session

# 라우터에서 사용
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/users/")
def create_user(
    name: str,
    email: str,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(User, db)
    return user_repo.create(name=name, email=email)
```


## 🎯 성능 최적화 팁

### 1. 인덱스 활용

```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True  # 인덱스 생성
    )
    name: Mapped[str] = mapped_column(String(50), index=True)
    
    # 복합 인덱스
    __table_args__ = (
        Index('idx_name_email', 'name', 'email'),
    )
```

### 2. 쿼리 최적화

```python
# 나쁜 예: 모든 컬럼 조회
def get_user_names_bad():
    with Session(engine) as session:
        users = session.scalars(select(User)).all()
        return [user.name for user in users]

# 좋은 예: 필요한 컬럼만 조회
def get_user_names_good():
    with Session(engine) as session:
        stmt = select(User.name)
        return list(session.scalars(stmt).all())
```

### 3. 벌크 작업

```python
def bulk_insert_users(users_data: list[dict]):
    """대량 삽입 최적화"""
    with Session(engine) as session:
        # 방법 1: bulk_insert_mappings (빠름)
        session.bulk_insert_mappings(User, users_data)
        session.commit()

def bulk_update_users(updates: list[dict]):
    """대량 업데이트 최적화"""
    with Session(engine) as session:
        # 방법 2: bulk_update_mappings
        session.bulk_update_mappings(User, updates)
        session.commit()
```

### 4. 커넥션 풀 튜닝

```python
engine = create_engine(
    "postgresql://user:password@localhost:5432/mydb",
    pool_size=20,  # 기본 연결 수
    max_overflow=0,  # 추가 연결 허용 안 함
    pool_pre_ping=True,  # 연결 유효성 사전 검사
    pool_recycle=3600,  # 1시간마다 연결 재활용
)
```

## 🔒 보안 모범 사례

### 1. SQL 인젝션 방지

```python
# 나쁜 예: 문자열 포맷팅 (절대 사용 금지!)
def unsafe_query(user_input: str):
    # SQL 인젝션 취약!
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    # 위험: user_input이 "'; DROP TABLE users; --" 같은 값이면?

# 좋은 예: 파라미터 바인딩
def safe_query(user_input: str):
    with Session(engine) as session:
        stmt = select(User).where(User.name == user_input)
        return session.scalars(stmt).all()
```

### 2. 비밀번호 저장

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]  # 해시된 비밀번호만 저장
    
    def set_password(self, password: str):
        """비밀번호 해싱"""
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """비밀번호 검증"""
        return pwd_context.verify(password, self.hashed_password)
```

### 3. 환경 변수로 DB 정보 관리

```python
import os
from dotenv import load_env

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/mydb"
)

engine = create_engine(DATABASE_URL)
```

## 🧪 테스트 작성

### 테스트용 데이터베이스 설정

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# 테스트용 인메모리 SQLite DB
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """각 테스트마다 새로운 DB 생성"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    Base.metadata.drop_all(engine)

def test_create_user(test_db):
    """사용자 생성 테스트"""
    user = User(name="Alice", email="alice@test.com", age=25)
    test_db.add(user)
    test_db.commit()
    
    # 검증
    found_user = test_db.scalar(
        select(User).where(User.email == "alice@test.com")
    )
    assert found_user is not None
    assert found_user.name == "Alice"
```

## 📚 참고자료

- [공식 문서](https://docs.sqlalchemy.org/en/20/)
- [마이그레이션 가이드 (v1→v2)](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Alembic 문서](https://alembic.sqlalchemy.org/)
