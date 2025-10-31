<%*
// 제목 입력 받기
const title = await tp.system.prompt("포스트 제목");
if (!title) throw new Error("제목이 필요합니다");

const post_filename = await tp.system.prompt("포스트 파일 이름을 간단한 영어로 적어주세요.");
if (!post_filename) throw new Error("포스트 파일 이름이 필요합니다");

// 파일명 생성 (YYYY-MM-DD-title.md 형식)
const fileDate = tp.date.now("YYYY-MM-DD");
const fileName = fileDate + "-" + post_filename.toLowerCase().replace(/\s+/g, '-');

// 템플릿 내용 생성
const frontMatter = `---
title: 🚣 (AI 부트캠프 13기) ${title}
date: ${tp.date.now("YYYY-MM-DD HH:mm:00 +0900")}
categories: [ "BOOTCAMP", "KERNEL_ACADEMY" ]
tags: [ "급발진거북이", "패스트캠퍼스", "패스트캠퍼스AI부트캠프", "패스트캠퍼스업스테이지부트캠프", "패스트캠퍼스업스테이지에이아이랩", "업스테이지패스트캠퍼스", "UpstageAILab", "국비지원", "후기", "UpstageAILab7기", "업스테이지에이아이랩", "커널아카데미", "AI부트캠프13기", GeekAndChill", "기깬칠" ]
toc: true
comments: false
mermaid: true
math: true
---`;

const content = `

![이미지](/assets/img/){: .w-75 .center}

## 📝 학습내용

## 🧠 강의 소감
`;

// 파일 이름 변경 및 내용 설정
await tp.file.rename(fileName);
tR = frontMatter + content;
-%>