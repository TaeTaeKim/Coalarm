let modalEl = document.querySelector('.modalBox');
let modalBackground = document.querySelector('.backgroundModal');
let modalBtn = document.querySelector('modalBtn');

function closeModal(){
  modalEl.classList.add('hidden');
  modalBackground.classList.add('hidden');
}

modalEl.addEventListener('click', closeModal);