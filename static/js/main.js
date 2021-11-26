$('#arrowAnim').on('click', () => {
  $('body,html').animate({ scrollTop: $('#map-container').offset().top }, 1000);
});
