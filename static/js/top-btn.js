// detail페이지 top버튼
$('.scroll-top-btn-detail').on('click', () => {
  $('body,html').animate({ scrollTop: $('.body-container').offset().top }, 100);
});
// main페이지 top버튼
$('.scroll-top-btn').on('click', () => {
  $('body,html').animate({ scrollTop: $('#map-container').offset().top }, 100);
});
