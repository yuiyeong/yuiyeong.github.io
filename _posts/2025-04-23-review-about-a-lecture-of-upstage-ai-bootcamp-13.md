---
title: "🚣 (AI 부트캠프 13기) 프로젝트를 위한 협업 Git 수업 후기: CLI에서 협업까지"
date: 2025-04-23 21:40:00 +0900
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
  - git
  - GeekAndChill
  - 기깬칠
  - AI
  - 에이아이
  - UpstageAILab7기
  - AI부트캠프13기
toc: true
comments: false
mermaid: true
math: true
---

![이미지](/assets/img/2025-04-24/img_result_of_git_lecture.png)
## 📝 학습내용

2일 동안 최우영 강사님의 **프로젝트를 위한 협업 Github** 강의를 들었다.

### Linux CLI 기본 명령어

```
cd, ls -la, mkdir, rm, cat, grep, find
```

### Vim 기본 사용법

```
i (삽입 모드), ESC (일반 모드), :wq (저장 후 종료), :q! (저장하지 않고 종료)
```

### Git 기본 명령어

```
git init
git add <file>
git commit -m "메시지"
git branch <branch_name>
git switch <branch_name>  # 새로운 명령어! (기존 checkout 대체)
git restore <file>
git push origin <branch>
git pull origin <branch>
git fetch
git merge <branch>
```

> Conventional Commit 도 배웠다. 매우 매우 중요한!!
> 1. commit의 제목은 commit을 설명하는 문장형이 아닌 구나 절의 형태로 작성
> 2. importanceofcapitalize `Importance of Capitalize`
> 3. prefix 꼭 달기
>   - feat: 기능 개발 관련
>   - fix: 오류 개선 혹은 버그 패치
>   - docs: 문서화 작업
>   - test: test 관련
>   - conf: 환경설정 관련
>   - build: 빌드 작업 관련
>   - ci: Continuous Integration 관련
>   - chore: 패키지 매니저, 스크립트 등
>   - style: 코드 포매팅 관련
{: .prompt-tip}

### Git 협업 방식

- **Git Flow**: main, develop, feature, release, hotfix 브랜치 활용
- **Github Flow**: main과 feature 브랜치 중심의 단순한 워크플로우
- **Gitlab Flow**: Github Flow에 환경별 브랜치 추가

## 🧠 강의 소감 (from 현직자의 시선)

### 솔직한 첫인상: "쉽고 심심했다"

솔직히 현직자로서 이 강의는 매우 쉽고 심심하게 느껴졌다. 하지만 이것은 어쩔 수 없는 일이다. 왜냐하면, 이미 여러 회사를 다니면서, 여러 형태의 git flow 및 github flow 를 체화했기 때문이다.

> 처음 배우는 사람과 이미 아는 사람의 학습 경험은 천지차이다. 내게 쉬운 것이 다른 사람에게는 어려울 수 있음을 항상 기억해야 한다.
{: .prompt-tip}

### 그럼에도 이 강의가 필요한 이유

그럼에도 이 강의는 꼭 필요하다고 생각했다. 우리 팀에서 과반수가 git 을 처음 봤다고 했기 때문이다. 그리고 제일 큰 문제는 git 이 무엇인지 알고, git 을 써봤지만 git 으로 협업하는 방식을 모르는 사람들이 꽤 있을 것이란 점이다.

이 수업의 진수는 "협업을 어떻게 체계적으로 할 것인가?"에 대한 실습이라고 생각한다. Test Repository를 만들고 사람들과 함께 작업해보니 실제로 매우 매우 힘들다는 것을 모두가 체감했다.

### 실습의 중요성

역시 실습이 중요하다는 것을 다시 한번 느꼈다. 그나마 다행이라면 팀장이 모든 초기 세팅을 담당한다는 것과 그 팀장이 git에 익숙하다는 점이다. 실제로 우리 팀 실습에서도,

- 처음에는 모두가 혼란스러워했다.
- 팀 repository 를 fork 하고, 본인 Repository 에서 작업한 뒤 PR 까지
- 마지막에는 PR을 만들고 리뷰하는 과정까지 원활하게 진행되었다.

## 🔍 아쉬웠던 점: CLI vs GUI

하지만 이 수업에서 가장 마음에 안 들었던 부분은, 모든 것을 CLI로만 진행했다는 점이다!

### git은 "도구"일 뿐이다

나는 git을 부수적인 "도구"라고 생각한다. 즉, 개발을 진행할 때 윤활유 역할을 할 수만 있으면 된다고 생각한다. 그래서 git 명령어들을 배웠고, 그것을 이해했다면, 그 다음 단계는 git GUI 도구로 생산성을 높이는 것이 당연하다.

### 실무에서 발생하는 복잡한 상황들

실제로 개발을 할 때는 정말 무궁무진한 상황이 발생한다.

- 복잡한 merge conflict
- 실수로 잘못된 branch에 commit한 경우
- 여러 branch의 변경사항을 선택적으로 적용해야 할 때
- commit history를 정리해야 할 때
- 동료의 PR을 검토할 때

이럴 때, CLI로만 그 문제를 해결하려고 하면... 정말 큰 재앙이 온다. 무조건 GUI를 쓰는 것이 답이다!

### GUI 도구의 장점

GitKraken, SourceTree, Fork, VS Code의 Git 확장 등 다양한 GUI 도구는 다음과 같은 장점이 있다.

1. 브랜치 관계를 시각적으로 확인 가능
2. 충돌을 직관적으로 해결 가능
3. 커밋 히스토리를 쉽게 탐색 가능
4. 복잡한 작업(rebase, cherry-pick 등)을 몇 번의 클릭으로 수행 가능

![Git GUI 도구 예시](assets/img/2025-04-24/img_git_gui_example.png)

### CLI의 역할은?

물론 EC2와 같은 Cloud Instance에서는 GUI 도구를 사용할 수 없으므로 git CLI 명령어를 알고 있어야 한다. 하지만 실제로는 매우 간단한 명령어로 모두 진행된다!

```
git pull
git add .
git commit -m "Update configuration"
git push
```

심지어 CI/CD 를 구축해두면 사실 이마저도 할 일이 거의 없다.

### AI의 시대에 명령어 외우기?

우리는 이제 ChatGPT나 Claude 같은 AI 도구에게 물어볼 수도 있다.

```
"Claude, git에서 마지막 3개의 커밋을 하나로 합치려면 어떻게 해야 해?"
```

이런 상황에서 모든 명령어를 외우는 것보다, git의 개념을 이해하고 필요할 때 도구(GUI나 AI)를 활용하는 능력이 더 중요하지 않을까?

## 📚 결론: 협업의 본질

결국 git은 협업을 위한 도구일 뿐이다. 가장 중요한 것은 팀원 간의 효과적인 커뮤니케이션과 일관된 워크플로우이다.

이번 부트캠프는 git 이라는 도구의 기본을 배울 수 있는 좋은 기회였다. 다만 실무에서는 이 기본을 바탕으로, 더 효율적인 방법을 찾아 적용하는 것이 중요하다.

마지막으로, 개발자로서 우리는 항상 더 좋은 도구와 방법을 찾아 발전해야 한다. git CLI 만 고집하기보다는, 상황에 맞는 최적의 도구를 선택하는 유연함이 필요하다. 그것이 진정한 개발자의 자세가 아닐까?

> 좋은 도구는 개발자의 생각을 코드로 옮기는 과정을 방해하지 않고 도와주는 것이다. git을 사용하는 데 시간을 너무 많이 쓴다면, 그것은 좋은 도구 사용법이 아니다.
{: .prompt-tip}