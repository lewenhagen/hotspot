var slides = document.querySelectorAll('#slides .slide');
var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var progress = document.getElementById("progress");
var currentSlide = 0;

var isPaused = true;
var backbtn = document.getElementById("back");
var playpausebtn = document.getElementById("playpause");
var nextbtn = document.getElementById("next");
var speedbtns = document.getElementsByClassName("speed");

var timer = 2000;
var slideInterval = setInterval(nextSlide, timer);
// progress.setAttribute("aria-valuemax", "12");

var progressStep = (100 / months.length);


function nextSlide() {
    if (!isPaused) {
        slides[currentSlide].className = 'slide';
        currentSlide = (currentSlide+1)%slides.length;
        slides[currentSlide].className = 'slide showing';
        progress.style.width = (progressStep * currentSlide) +'%';
    }
}

backbtn.addEventListener("click", function() {
    slides[currentSlide].className = 'slide';
    currentSlide = (currentSlide > 0) ? (currentSlide-1)%slides.length : 0;
    slides[currentSlide].className = 'slide showing';
    progress.style.width = (progressStep * currentSlide) +'%';
});

nextbtn.addEventListener("click", function() {
    slides[currentSlide].className = 'slide';
    currentSlide = (currentSlide+1)%slides.length;
    slides[currentSlide].className = 'slide showing';
    progress.style.width = (progressStep * currentSlide) +'%';
});

playpausebtn.addEventListener("click", function(event) {
    isPaused = true ? (!isPaused) : false;
    console.log(event.target);
    event.target.innerHTML = isPaused ? "Play" : "Pause";
});

for (var i = 0; i < speedbtns.length; i++) {
    speedbtns[i].addEventListener("click", function(event) {
        window.clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, parseInt(event.target.innerHTML) * 1000);
    });
}
