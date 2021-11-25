let categoryEl = document.querySelector('.information-content');

function categoryHandler(event) {
  if (event.target.getAttribute('class') === 'category-title') {
    event.target.nextElementSibling.classList.toggle('look');
  } else if (event.target.getAttribute('class') === 'click-guide') {
    event.target.parentElement.nextElementSibling.classList.toggle('look');
  }
}

categoryEl.addEventListener('click', categoryHandler);

$('.summary').on('click', function () {
  $('.category-group').removeClass('hidden');
  $('.all').addClass('hidden');
  $('.info-help div:first').html(
    '코로나 관련 <b>여행자 요약 정보</b>별로 확인해보세요.<br>❗꼭 전체 정보를 확인하세요'
  );
});
$('.allcontent').on('click', function () {
  $('.category-group').addClass('hidden');
  $('.all').removeClass('hidden');

  $('.info-help div:first').html(
    '코로나 관련 <b>여행자 전체 정보</b>를 확인해보세요.<br>요약정보를 보러면 요약을 클릭하세요'
  );
});

// 국기 추가하는 부분
let iso = window.location.pathname.slice(9, 11).toLowerCase();
let tag = `<img src="https://flagcdn.com/40x30/${iso}.png" alt="">`;
$('.flag').html(tag);

// 그래프
document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelector('#chart2Data1').textContent === '-1.0') {
    const containerEl = document.querySelector('#container');
    let containerDiv = document.createElement('div');
    containerDiv.setAttribute('class', 'notData');
    containerDiv.textContent = '백신 접종률에 대한 데이터가 없습니다.';
    containerEl.append(containerDiv);
  } else {
    Highcharts.setOptions({
      colors: ['#058DC7', '#64E572'],
      // #64E572
      // #6AF9C4
      // #50B432
    });
    const chart = Highcharts.chart('container', {
      chart: {
        type: 'column',
      },
      credits: { enabled: false },
      title: {
        text: '백신접종률',
      },
      xAxis: {
        categories: [''],
      },
      yAxis: {
        title: '',
      },
      tooltip: {
        formatter: function () {
          return this.series.name + ' : ' + this.y + '%';
        },
        hideDelay: 100,
      },
      plotOptions: {
        series: {
          dataLabels: {
            enabled: true,
            format: '{y} %',
          },
        },
      },

      series: [
        {
          name: `1차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data1').textContent)],
        },
        {
          name: `2차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data2').textContent)],
        },
      ],
    });
  }
});

// 숫자 애니메이션
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

var Endnum_list = document.querySelectorAll('.coronadata');
for (let i = 0; i < Endnum_list.length; i++) {
  endnum = parseInt(Endnum_list[i].innerText);
  if (endnum == -1) {
    Endnum_list[i].innerText = '정보가 없습니다!';
  } else {
    $({ val: 0 }).animate(
      { val: endnum },
      {
        duration: 1000,
        step: function () {
          var num = numberWithCommas(Math.floor(this.val));
          Endnum_list[i].innerText = num;
        },
        complete: function () {
          var num = numberWithCommas(Math.floor(this.val));
          Endnum_list[i].innerText = num;
        },
      }
    );
  }
}
// 환율 계산기
let rate = $('.rate').text();
rate = Number(rate.replace(/[^0-9.-]+/g, ''));

$('.exchangefrom').keyup(function () {
  let value = $('.exchangefrom').val();
  value = Number(value);
  let cal = value * (1 / rate);
  cal = cal.toFixed(3);
  $('.exchangeto').text(cal);
});
$('.reverse-cal').on('click', function () {
  const fromname = $('.calculator div:first p').text();
  const toname = $('.calculator div:last p:first').text();
  $('.calculator div:first p').text(toname);
  $('.calculator div:last p:first').text(fromname);
  rate = 1 / rate;
});


//댓글 입력창 자동크기 조절
function resize(obj) {
  obj.style.height = '1px';
  obj.style.height = 3 + obj.scrollHeight + 'px';
}

//댓글 버튼 활성화
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

// 댓글 보여 주기
function readComment(data) {
  const commentListEl = document.querySelector('.comment-list');
  data.forEach((el, i) => {
    // 댓글 루트
    if (el.index === el.parent) {
      let commentBoxDiv = document.createElement('div');
      commentBoxDiv.setAttribute('class', 'comment-box');
      commentBoxDiv.setAttribute('data-parent', el.index); // 댓글에 인덱스 표시
      commentBoxDiv.innerHTML = `
      <div class="box-head">
        <span class="comment-nickname">${el.nickname}</span>
        <span class="comment-period">${el.write_time}</span>
      </div>
      <div class="box-body">${el.text}</div>
      <div class="box-btn-group">
        <button class="btn btn-update-comment">수정</button>
        <button class="btn btn-delete-comment">삭제</button>
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
      inputGroupAddListener();
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
      <span class="show-comment">답글 ${count - 1}개 보기</span>
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
  commentBoxDiv.innerHTML = `
  <div class="box-head">
    <span class="comment-nickname">${plusComment.nickname}</span>
    <span class="comment-period">${plusComment.write_time}</span>
  </div>
  <div class="box-body">${plusComment.text}</div>
  <div class="box-btn-group">
    <button class="btn btn-update-comment">수정</button>
    <button class="btn btn-delete-comment">삭제</button>
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
// 입력창 추가 이벤트핸들러
function addInputGroup(event) {
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
  if (
    //예외 사항
    event.target.parentElement === safeInputEl ||
    event.target.parentElement.nextElementSibling ===
      document.querySelectorAll('.comment-input-group')[1] ||
    event.target.textContent === '취소'
  ) {
    return; //예외 사항은 pass
  } else {
    //그외의 경우는 입력상자 삭제
    if (document.querySelectorAll('.comment-input-group')[1] !== undefined) {
      document.querySelectorAll('.comment-input-group')[1].remove();
    }
  }
}
const body = document.querySelector('body');
body.addEventListener('click', removeInputGroup);

// 댓글 추가 기능
function addComment(i) {
  let iso_upper = window.location.pathname.slice(9, 11).toUpperCase();
  let inputNicknameEl = document.querySelectorAll('.input-nickname')[i];
  let inputCommentEl = document.querySelectorAll('.input-comment')[i];
  let inputPwEl = document.querySelectorAll('.input-pw')[i];
  let parentIndex =
    event.target.parentElement.parentElement.parentElement.dataset.parent !==
    undefined
      ? event.target.parentElement.parentElement.parentElement.dataset.parent
      : -1;
  console.log(parentIndex);
  console.log('닉네임:' + inputNicknameEl.value);
  console.log('내용:' + inputCommentEl.value);
  console.log('비밀번호:' + inputPwEl.value);
  let postData = {
    iso_code: iso_upper,
    parent: parseInt(parentIndex),
    text: inputNicknameEl.value,
    nickname: inputNicknameEl.value,
    password: inputPwEl.value,
  };
  $.ajax({
    type: 'POST',
    url: '/country/' + iso_upper,
    data: JSON.stringify(postData),
    contentType: 'application/json; charset=UTF-8',
    success: function () {
      alert('댓글이 등록되었습니다.');
    },
  });
  inputNicknameEl.value = '';
  inputCommentEl.value = '';
  inputPwEl.value = '';
  btnReset();
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
      commentCount(data);
      readComment(data);
    },
  });
}

callComment();
