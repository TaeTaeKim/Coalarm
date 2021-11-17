let categoryEl = document.querySelector('.information-content');

function categoryHandler(event){
  if (event.target.getAttribute('class') === 'category-title'){
    event.target.nextElementSibling.classList.toggle('look')
  }
}

categoryEl.addEventListener('click',categoryHandler)

$('.summary').on('click',function(){
  $('.category-group').removeClass('hidden')
  $('.all').addClass('hidden')
  $('.info-help div:first').html('코로나 관련 <b>여행자 요약 정보</b>별로 확인해보세요.<br>❗꼭 전체 정보를 확인하세요')
})
$('.allcontent').on('click',function(){
  
  $('.category-group').addClass('hidden')
  $('.all').removeClass('hidden')
  $('.info-help div:first').html('코로나 관련 <b>여행자 전체 정보</b>를 확인해보세요.<br>요약정보를 보러면 요약을 클릭하세요')
})


// 국기 추가하는 부분
let iso = window.location.pathname.slice(9,11).toLowerCase();
let tag = `<img src="https://flagcdn.com/40x30/${iso}.png" alt="">`
$(".flag").html(tag)