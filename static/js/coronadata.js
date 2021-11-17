const total_confirmed = parseInt(document.querySelector(".total_confirmed").innerText);
const total_deaths = parseInt(document.querySelector(".total_deaths").innerText);
const total_recovered = parseInt(document.querySelector(".total_recovered").innerText);
const new_confirmed = parseInt(document.querySelector(".new_confirmed").innerText);
const new_deaths = parseInt(document.querySelector(".new_deaths").innerText);
const new_recovered = parseInt(document.querySelector(".new_recovered").innerText);


function animate(obj, initVal, lastVal, duration) {

    let startTime = null;

    //get the current timestamp and assign it to the currentTime variable
    let currentTime = new Date.now();

    //pass the current timestamp to the step function
    const step = (currentTime ) => {

        //if the start time is null, assign the current time to startTime
        if (!startTime) {
              startTime = currentTime ;
        }

        //calculate the value to be used in calculating the number to be displayed
        const progress = Math.min((currentTime  - startTime) / duration, 1);

        //calculate what to be displayed using the value gotten above
        obj.innerHTML = Math.floor(progress * (lastVal - initVal) + initVal);

        //checking to make sure the counter does not exceed the last value (lastVal)
        if (progress < 1) {
              window.requestAnimationFrame(step);
        }
        else{
              window.cancelAnimationFrame(window.requestAnimationFrame(step));
        }
    };

    //start animating
    window.requestAnimationFrame(step);
}

let text1 = document.getElementByClassName('total_confirmed');
let text2 = document.getElementByClassName('total_deaths');
let text3 = document.getElementByClassName('total_recovered');
let text4 = document.getElementByClassName('new_confirmed');
let text5 = document.getElementByClassName('new_deaths');
let text6 = document.getElementByClassName('new_recovered');


animate(text1, 0, total_confirmed, 5000);
animate(text2, 0, total_deaths, 5000);
animate(text3, 0, total_recovered, 5000);
animate(text4, 0, new_confirmed, 5000);
animate(text5, 0, new_deaths, 5000);
animate(text6, 0, new_recovered, 5000);