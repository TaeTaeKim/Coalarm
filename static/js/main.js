$('#arrowAnim').on('click', () => {
  $('body,html').animate({ scrollTop: $('#map-container').offset().top }, 1000);
});

const scrollTopBtn = document.querySelector('.scroll-top-btn');
scrollTopBtn.addEventListener('click', function () {
  window.scrollTo(0, 941);
});
