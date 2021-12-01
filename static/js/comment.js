//댓글 입력창 자동크기 조절
function resize(obj) {
  obj.style.height = '1px';
  obj.style.height = 3 + obj.scrollHeight + 'px';
}

//댓글 버튼 활성화 -기본
function btnActive() {
  const inputNicknameEls = document.querySelectorAll('.input-nickname');
  const inputCommentEls = document.querySelectorAll('.input-comment');
  const inputPwEls = document.querySelectorAll('.input-pw');
  const btnSubmitEls = document.querySelectorAll('.btn-submit');
  for (let i = 0; i < inputNicknameEls.length; i++) {
    if (
      inputNicknameEls[i].value !== '' &&
      inputCommentEls[i].value !== '' &&
      inputPwEls[i].value !== ''
    ) {
      btnSubmitEls[i].removeAttribute('disabled');
    } else {
      btnReset();
    }
  }
}
function btnReset() {
  const btnSubmitEls = document.querySelectorAll('.btn-submit');
  btnSubmitEls.forEach((el) => {
    el.setAttribute('disabled', 'false');
  });
}
//댓글 버튼 활성화 - 수정
function btnActiveUpdate() {
  const inputCommentEls = document.querySelectorAll('.input-comment');
  const inputPwEls = document.querySelectorAll('.input-pw');
  const btnSubmitEls = document.querySelectorAll('.btn-submit');
  for (let i = 0; i < inputCommentEls.length; i++) {
    if (inputCommentEls[i].value !== '' && inputPwEls[i].value !== '') {
      btnSubmitEls[i].removeAttribute('disabled');
    } else {
      btnReset();
    }
  }
}
//댓글 버튼 활성화 - 삭제
function btnActiveDelete() {
  const inputPwEls = document.querySelectorAll('.input-pw');
  const btnSubmitEls = document.querySelectorAll('.btn-submit');
  for (let i = 0; i < inputPwEls.length; i++) {
    if (inputPwEls[i].value !== '') {
      btnSubmitEls[i].removeAttribute('disabled');
    } else {
      btnReset();
    }
  }
}

// 댓글 시간 계산 함수
function displayedAt(createdAt) {
  const milliSeconds = new Date() - createdAt;
  const seconds = milliSeconds / 1000;
  if (seconds < 60) return `방금 전`;
  const minutes = seconds / 60;
  if (minutes < 60) return `${Math.floor(minutes)}분 전`;
  const hours = minutes / 60;
  if (hours < 24) return `${Math.floor(hours)}시간 전`;
  const days = hours / 24;
  if (days < 7) return `${Math.floor(days)}일 전`;
  const weeks = days / 7;
  if (weeks < 5) return `${Math.floor(weeks)}주 전`;
  const months = days / 30;
  if (months < 12) return `${Math.floor(months)}개월 전`;
  const years = days / 365;
  return `${Math.floor(years)}년 전`;
}

// 댓글 보여 주기
function readComment(data) {
  const commentListEl = document.querySelector('.comment-list');
  data.forEach((el, i) => {
    // 댓글 루트
    // if (el.index === el.parent) {
    if (el.class == 0) {
      let commentBoxDiv = document.createElement('div');
      commentBoxDiv.setAttribute('class', 'comment-box');
      commentBoxDiv.setAttribute('data-parent', el.index); // 부모 댓글 표시
      commentBoxDiv.setAttribute('data-index', el.index); // 자기 index 표시
      let timeCalc = displayedAt(new Date(el.write_time));
      commentBoxDiv.innerHTML = `
      <div class="box-head">
        <span class="comment-nickname">${el.nickname}</span>
        <span class="comment-period">${timeCalc}</span>
      </div>
      <div class="box-body">${el.text}</div>
      <div class="box-btn-group">
        <button class="btn btn-update-comment" onclick="updateInputGroup()">수정</button>
        <button class="btn btn-delete-comment" onclick="deleteInputGroup()">삭제</button>
        <button class="btn-plus-comment">답글</button>
      </div>
      `;
      commentListEl.append(commentBoxDiv);
    }
    // 대댓글 루트
    else {
      readPlusCommentBtn(el, data);
      readPlusComment(el);
      plusCommentAddListener();
    }
  });
}
// 대댓글 버튼
function readPlusCommentBtn(plusComment, data) {
  // 현재 입력된 댓글들의 index 값들을 가져옴
  let commentBoxEls = document.querySelectorAll('[data-parent]');
  // 각 댓글들에 접근해서 현재 데이터의 parent와 일치하는 index의 댓글에 접근
  let commentBoxEl = '';
  for (let El of commentBoxEls) {
    if (El.dataset.parent == plusComment.parent) {
      commentBoxEl = El;
    }
  }
  // 일치하는 댓글에 대댓글 버튼이 없을 경우에만 대댓글 버튼 추가
  if (commentBoxEl.querySelector('.read-plus-comment') === null) {
    // 대댓글의 개수를 셈
    let count = 0;
    for (let i = 0; i < data.length; i++) {
      if (plusComment.parent === data[i].parent) {
        count++;
      }
    }
    let readPlusDiv = document.createElement('div');
    readPlusDiv.innerHTML = `
    <div class="read-plus-comment">
      <div class="triangle">▼</div>&ensp;
      <span class="show-comment">답글 ${count}개 보기</span>
      <div class="plus-comment-list hidden"></div>
    </div>
    `;
    commentBoxEl.append(readPlusDiv);
  }
}
// 대댓글 보여주기
function readPlusComment(plusComment) {
  let commentBoxEls = document.querySelectorAll('[data-parent]');
  let commentBoxEl = '';
  for (let El of commentBoxEls) {
    if (El.dataset.parent == plusComment.parent) {
      commentBoxEl = El;
    }
  }
  // 해당 index의 댓글에 대댓글 요소에 접근하여, 대댓글 추가
  let plusCommentListEl = commentBoxEl.querySelector('.plus-comment-list');
  let commentBoxDiv = document.createElement('div');
  commentBoxDiv.setAttribute('class', 'comment-box-plus');
  commentBoxDiv.setAttribute('data-index', plusComment.index); // 자기 index 표시
  let timeCalc = displayedAt(new Date(plusComment.write_time));
  commentBoxDiv.innerHTML = `
  <div class="box-head">
    <span class="comment-nickname">${plusComment.nickname}</span>
    <span class="comment-period">${timeCalc}</span>
  </div>
  <div class="box-body">${plusComment.text}</div>
  <div class="box-btn-group">
    <button class="btn btn-update-comment" onclick="updateInputGroup()">수정</button>
    <button class="btn btn-delete-comment" onclick="deleteInputGroup()">삭제</button>
  </div>
    `;
  plusCommentListEl.append(commentBoxDiv);
}

// 대댓글 보기,숨기기
function togglePlusComment(event) {
  event.target.nextElementSibling.classList.toggle('hidden');
  event.target.parentElement.firstElementChild.classList.toggle('rotate');
  // event.target.previousElementSiblling.classList.toggle('rotate');
}
function plusCommentAddListener() {
  const plusCommentEls = document.querySelectorAll('.show-comment');
  plusCommentEls.forEach((el) => {
    el.addEventListener('click', togglePlusComment);
  });
}

// 총 댓글 카운트
function commentCount(data) {
  let commentCountEl = document.querySelector('.comment-count');
  commentCountEl.textContent = `댓글 ${data.length}개`;
}

// 대댓글 입력 창
// 댓글 추가 입력창 이벤트핸들러
function addInputGroup() {
  if (document.querySelectorAll('.comment-input-group').length === 1) {
    let formEl = document.createElement('form');
    formEl.setAttribute('class', 'comment-input-group margin');
    formEl.innerHTML = `
    <input type="text" class="input-nickname" oninput="btnActive()" placeholder="닉네임 입력...">
    <textarea class="input-comment" oninput="btnActive()" onkeydown="resize(this)" onkeyup="resize(this)"  rows="1" type="text" placeholder="공개 댓글 추가..."></textarea>
    <input type="text" class="input-pw" oninput="btnActive()" placeholder="비밀번호 입력...">
    <div class="btn-group">
      <button type="reset" onclick="btnReset()" class="btn btn-reset">취소</button>
      <button type="button" onclick="addComment(1)" class="btn btn-submit" disabled>댓글</button>
    </div>
    `;
    event.target.parentElement.after(formEl);
  }
}
function inputGroupAddListener() {
  const btnPlusComments = document.querySelectorAll('.btn-plus-comment');
  btnPlusComments.forEach((el) => {
    el.addEventListener('click', addInputGroup);
  });
}
//입력창 삭제 이벤트핸들러
function removeInputGroup(event) {
  const safeInputEl = document.querySelectorAll('.comment-input-group')[1];
  if (event.target.textContent === '수정') {
    if (safeInputEl !== undefined) {
      safeInputEl.remove();
      updateInputGroup();
    }
  } else if (event.target.textContent === '삭제') {
    if (safeInputEl !== undefined) {
      safeInputEl.remove();
      deleteInputGroup();
    }
  } else if (event.target.textContent === '답글') {
    if (safeInputEl !== undefined) {
      safeInputEl.remove();
      addInputGroup();
    }
  } else if (
    //예외 사항
    event.target.parentElement === safeInputEl ||
    event.target.textContent === '취소'
  ) {
    return; //예외 사항은 pass
  } else {
    //그외의 경우는 입력상자 삭제
    if (safeInputEl !== undefined) {
      safeInputEl.remove();
    }
  }
}
const body = document.querySelector('body');
body.addEventListener('click', removeInputGroup);

// 댓글목록 초기화
function resetComment() {
  let commentListEl = document.querySelector('.comment-list');
  commentListEl.innerHTML = '';
}
// 댓글 추가 기능
function addComment(i) {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  let inputCommentEl = document.querySelectorAll('.input-comment')[i];
  let inputNicknameEl = document.querySelectorAll('.input-nickname')[i];
  let inputPwEl = document.querySelectorAll('.input-pw')[i];
  let parentIndex =
    event.target.parentElement.parentElement.parentElement.dataset.parent !==
    undefined
      ? event.target.parentElement.parentElement.parentElement.dataset.parent
      : -1;
  let classIndex = parentIndex == -1 ? 0 : 1;
  let postData = {
    iso_code: iso_upper,
    parent: parseInt(parentIndex),
    text: inputCommentEl.value,
    nickname: inputNicknameEl.value,
    password: inputPwEl.value,
    class: classIndex,
  };
  $.ajax({
    type: 'POST',
    url: '/country/' + iso_upper,
    data: JSON.stringify(postData),
    contentType: 'application/json; charset=UTF-8',
    success: function () {
      callComment();
    },
  });
  inputNicknameEl.value = '';
  inputCommentEl.value = '';
  inputPwEl.value = '';
  btnReset();
}
// 댓글 삭제
function deleteComment() {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  let inputPwEl = document.querySelectorAll('.input-pw')[1];
  let commentIndex =
    event.target.parentElement.parentElement.parentElement.dataset.index;
  console.log(commentIndex);
  console.log('비밀번호:' + inputPwEl.value);

  let deleteData = {
    index: parseInt(commentIndex),
    password: inputPwEl.value,
  };
  $.ajax({
    type: 'DELETE',
    url: '/country/' + iso_upper,
    data: JSON.stringify(deleteData),
    contentType: 'application/json; charset=UTF-8',
    success: function (res) {
      if (res.result === 'fail') {
        alert('비밀번호를 확인하세요.');
      } else if (res.result === 'success') {
        alert('성공했습니다.');
      }
      callComment();
    },
    error: function () {
      alert('알수 없는 오류 발생!');
    },
  });
  inputCommentEl.value = '';
  inputPwEl.value = '';
  btnReset();
}
// 댓글 수정 작업
function updateComment() {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  let inputCommentEl = document.querySelectorAll('.input-comment')[1];
  let inputPwEl = document.querySelectorAll('.input-pw')[1];
  let commentIndex =
    event.target.parentElement.parentElement.parentElement.dataset.index;
  let updateData = {
    index: parseInt(commentIndex),
    text: inputCommentEl.value,
    password: inputPwEl.value,
  };
  $.ajax({
    type: 'PATCH',
    url: '/country/' + iso_upper,
    data: JSON.stringify(updateData),
    contentType: 'application/json; charset=UTF-8',
    success: function (res) {
      if (res.result === 'fail') {
        alert('비밀번호를 확인하세요.');
      } else if (res.result === 'success') {
        alert('성공했습니다.');
      }
      callComment();
    },
    error: function () {
      alert('알수 없는 오류 발생!');
    },
  });
  inputCommentEl.value = '';
  inputPwEl.value = '';
  btnReset();
}
// 댓글 수정 입력창 이벤트핸들러
function updateInputGroup() {
  if (document.querySelectorAll('.comment-input-group').length === 1) {
    let originalText =
      event.target.parentElement.previousElementSibling.textContent;
    let formEl = document.createElement('form');
    formEl.setAttribute('class', 'comment-input-group margin');
    formEl.innerHTML = `
    <textarea class="input-comment" oninput="btnActiveUpdate()" onkeydown="resize(this)" onkeyup="resize(this)" rows="1" type="text" placeholder="공개 댓글 수정...(100글자 이내)">${originalText}</textarea>
    <input type="text" class="input-pw" oninput="btnActiveUpdate()" placeholder="비밀번호 입력...">
    <div class="btn-group">
      <button type="reset" onclick="btnReset()" class="btn btn-reset">취소</button>
      <button type="button" onclick="updateComment()" class="btn btn-submit" disabled>수정</button>
    </div>
    `;
    event.target.parentElement.after(formEl);
  }
}
// 댓글 삭제 입력창 이벤트핸들러
function deleteInputGroup() {
  if (document.querySelectorAll('.comment-input-group').length === 1) {
    let formEl = document.createElement('form');
    formEl.setAttribute('class', 'comment-input-group margin');
    formEl.innerHTML = `
    <input type="text" class="input-pw" oninput="btnActiveDelete()" placeholder="비밀번호 입력...">
    <div class="btn-group">
      <button type="reset" onclick="btnReset()" class="btn btn-reset">취소</button>
      <button type="button" onclick="deleteComment()" class="btn btn-submit" disabled>삭제</button>
    </div>
    `;
    event.target.parentElement.after(formEl);
  }
}

// 댓글 DB와 연동
function callComment() {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  $.ajax({
    type: 'get',
    url: `/country/${iso_upper}/comment`,
    dataType: 'json',
    async: false,
    success: function (data) {
      resetComment();
      commentCount(data);
      readComment(data);
      inputGroupAddListener();
    },
  });
}
callComment();

// 댓글 최신 감지
function commentResentActivition() {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  $.ajax({
    type: 'get',
    url: `/country/${iso_upper}/comment_update`,
    dataType: 'json',
    async: false,
    success: function (res) {
      const rensentIconEl = document.querySelector('.fa-history');
      const serverCount = res.count;
      const commentCountEl = document.querySelector('.comment-count');
      const commentCount = parseInt(
        commentCountEl.textContent.slice(
          3,
          commentCountEl.textContent.length - 1
        )
      );
      if (serverCount > commentCount) {
        rensentIconEl.classList.add('activity');
      }
    },
  });
}
// 댓글 감지 타이머
const commentResentActivityTimer = setInterval(() => {
  commentResentActivition();
}, 5000);
// 댓글 최신화 실행
function commentResentDeactivation() {
  const rensentIconEl = document.querySelector('.fa-history');
  rensentIconEl.classList.remove('activity');
  callComment();
}
