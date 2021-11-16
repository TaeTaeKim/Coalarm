const categoryList = [
  {
    title: '입국관련',
    description: 	'목적, 외국인, 한국, 해외입국자,금지, 허용, 중단,허가,허용,불허,제한,통제,폐쇄,불가,관광,중지,통제'
  },
  {
    title: '필요서류',
    description: 	'확인서, 허가증, 신고서, 서약서,온라인,결과서,PCR,검사,카드,보험,증명서,QR,디지털,필수,결과지,서류,검진서,검사서,공인서'
  },
  {
    title: '격리관련',
    description: 	'격리~~~~~~~~~~~~~~'
  },
  {
    title: '비자관련',
    description: 	'비자~~~~~~~~~~~~~~'
  },
]

let categoryEl = document.querySelector('.information-content');

function categoryHandler(event){
  if (event.target.getAttribute('class') === 'category-title'){
    event.target.nextElementSibling.classList.toggle('look')
  }
}

categoryEl.addEventListener('click',categoryHandler)