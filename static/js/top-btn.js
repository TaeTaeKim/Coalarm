// main페이지 top버튼
const scrollTopBtn = document.querySelector('.scroll-top-btn');
scrollTopBtn.addEventListener('click', function () {
  window.scrollTo(0, 941);
});

// detail페이지 top버튼
const scrollTopBtnDetail = document.querySelector('.detail');
scrollTopBtnDetail.addEventListener('click', function () {
  window.scrollTo(0, 0);
});
