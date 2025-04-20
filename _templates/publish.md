<%*
// 현재 파일 경로 가져오기
const currentPath = tp.file.path();

// 현재 파일이 _drafts 폴더에 있는지 확인
if (!currentPath.includes('_drafts')) {
  await tp.system.suggester(["예"], ["yes"], false, "이 명령어는 _drafts 폴더의 파일에서만 사용할 수 있습니다.")
  return;
}

// 발행 확인
const publish = await tp.system.suggester(["예", "아니오"], ["yes", "no"], false, "이 포스트를 발행하시겠습니까?");
if (publish !== "yes") {
  await tp.system.suggester(["예"], ["yes"], false, "발행이 취소되었습니다.")
  return;
}

// _posts 폴더로 이동
const fileName = currentPath.split('/').pop();
await tp.file.move("_posts/" + fileName);
-%>