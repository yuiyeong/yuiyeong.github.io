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
title: ${title}
date: ${tp.date.now("YYYY-MM-DD HH:mm:00 +0900")}
categories: [ ]
tags: [ "급발진거북이", "GeekAndChill", "기깬칠", "에이아이", "업스테이지에이아이랩", "UpstageAILab", "UpstageAILab6기", "ML", "DL", "machinelearning", "deeplearning"]
toc: true
comments: false
mermaid: true
math: true
---`;

const content = `
## 🚀 TL;DR



## 📦 사용하는 python package

- 
- 

## 📓 실습 Jupyter Notebook

[GitHub 링크](#)


여기부터 본문을 작성하세요.`;

// 파일 이름 변경 및 내용 설정
await tp.file.rename(fileName);
tR = frontMatter + content;
-%>