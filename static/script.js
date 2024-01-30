document.addEventListener("DOMContentLoaded", function () {
  var startFloorDropdown = document.getElementById("start_Floor_Dropdown");
  var startNodeDropdown = document.getElementById("start_node_Dropdown");

  var selectedStartFloor = "";
  var selectedStartNode = "";

  startFloorDropdown.addEventListener("change", function () {
    selectedStartFloor = startFloorDropdown.value;
  });

  startNodeDropdown.addEventListener("change", function () {
    selectedStartNode = startNodeDropdown.value;
  });

  // start_node_Dropdown의 값이 변경되면 이벤트 처리 로직 추가
  var startNodeSubmitButton = document.getElementById("start_node_SubmitButton");
  startNodeSubmitButton.addEventListener("click", function () {
    // 선택된 값이 있는지 확인
    if (selectedStartNode !== "") {
      // AJAX 요청을 통해 /start_info 경로로 POST 요청 보내기
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/start_info", true);
      xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
          // 응답을 받으면 현재 페이지 갱신
          window.location.reload();
        }
      };
      xhr.send("start_node=" + encodeURIComponent(selectedStartNode));
    }
  });

  var endFloorDropdown = document.getElementById("end_Floor_Dropdown");
  var endNodeDropdown = document.getElementById("end_node_Dropdown");

  var selectedEndFloor = "";
  var selectedEndNode = "";

  endFloorDropdown.addEventListener("change", function () {
    selectedEndFloor = endFloorDropdown.value;
  });

  endNodeDropdown.addEventListener("change", function () {
    selectedEndNode = endNodeDropdown.value;
  });
});

document.addEventListener("DOMContentLoaded", (event) => {
  const imgs = document.querySelectorAll(".img");
  const modals = document.querySelectorAll(".modal");
  const modalContents = document.querySelectorAll(".modal_content");
  const closeButtons = document.querySelectorAll(".close");
  const rotateButtons = document.querySelectorAll(".right_rotate");

  imgs.forEach((img, index) => {
    img.addEventListener("click", () => {
      modals[index].style.display = "block";
      modalContents[index].src = img.src;
      modalContents[index].style.transform = "rotate(0deg)";
    });
  });

  closeButtons.forEach((closeButton, index) => {
    closeButton.addEventListener("click", () => {
      modals[index].style.display = "none";
    });
  });

  rotateButtons.forEach((rotateButton, index) => {
    rotateButton.addEventListener("click", () => {
      let currentAngle = modalContents[index].style.transform.match(/rotate\(([0-9]+)deg\)/)[1];
      let newAngle = (parseInt(currentAngle) + 90) % 360;
      modalContents[index].style.transform = "rotate(" + newAngle + "deg)";

      if (newAngle === 90 || newAngle === 270) {
        modalContents[index].style.width = "auto";
        modalContents[index].style.height = "100%";
      } else {
        modalContents[index].style.width = "100%";
        modalContents[index].style.height = "auto";
      }
    });
  });

  modals.forEach((modal, index) => {
    modal.addEventListener("click", (evt) => {
      if (evt.target === modals[index]) {
        modals[index].style.display = "none";
      }
    });
  });
});
