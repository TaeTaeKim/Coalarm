
let rankingEl = $('.ranking-body');

data = [
  {
    link: "#",
    flag: '../static/img/한국.jpg',
    country: '한국',
    point: 90,
    isolation: 3,
    continent: 'East Asia'
  },
  {
    link: "#",
    flag: '../static/img/미국.png',
    country: '미국',
    point: 80,
    isolation: 7,
    continent: 'America'
  },
  {
    link: "#",
    flag: '../static/img/싱가폴.png',
    country: '싱가폴',
    point: 70,
    isolation: 10,
    continent: 'East Asia'
  }
]

data.forEach((el, i)=>{
  $(rankingEl).append(
    `<a href=${el.link} class="ranking-box">
        <img src=${el.flag} alt="국기사진${i+1}">
        <div class="ranking-itmes">
            <div class="star"><i class="fa fa-star"></i> ${i+1}위</div>
            <div class="country-name">${el.country}</div>
            <div class="point">안전점수: <b>${el.point}point</b></div>
        </div>
        <div class="ranking-line"></div>
        <div class="ranking-info">
            <div class="period"><i class="fa fa-clock"></i> 자가격리 기간: ${el.isolation}일</div>
            <div class="continent"><i class="fa fa-globe"></i> 대륙: ${el.continent}</div>
        </div>
    </a>`
  );
})