$(document).ready(function(){
  $.ajax({
    url:'/safety_score',
    type:'GET',
    async:false,
    datatype:'json',
    success:function(res){
      let data = res['top3_score']
      data.forEach((el,i)=>{
        $(".ranking-body").append(
          `<a href="/country/${el.iso_code}" class="ranking-box">
              <img src="https://flagcdn.com/w640/${el.iso_code.toLowerCase()}.png" alt="">
              <div class="ranking-itmes">
                  <div class="star"><i class="fa fa-star"></i> ${i+1}위</div>
                  <div class="country-name">${el.country_kr}</div>
                  <div class="point">안전점수: <b>${el.score}점</b></div>
              </div>
          </a>`
        )
      })
    }
  })
})

