// 모달 열기
  var modal = document.getElementById("myModal");

  // 모달 내용을 가져와서 modal-content-placeholder에 삽입
  var modalContentPlaceholder = document.getElementById("modal-content-placeholder");
  modalContentPlaceholder.innerHTML = "";  // 내용 초기화
  fetch('/path/to/add_quiz.html')  // 가져올 HTML 파일의 경로로 변경
    .then(response => response.text())
    .then(data => {
      modalContentPlaceholder.innerHTML = data;

      // 모달 열기
      modal.style.display = "block";
    });
// 모달 닫기
function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}

// 버튼 클릭 이벤트 처리
var openModalButton = document.getElementById("openModalButton");
openModalButton.addEventListener("click", function() {
  openModal();
});