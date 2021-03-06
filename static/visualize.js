var slides = document.querySelectorAll('#slides .slide');
var months = [55, 98, 142, 187, 231, 275, 320, 365, 408, 453, 497, 541];

var currentSlide = 0;
var isPaused = true;
var progress = document.getElementById("progress");
var backbtn = document.getElementById("back");
var playpausebtn = document.getElementById("playpause");
var nextbtn = document.getElementById("next");
var speedbtns = document.getElementsByClassName("speed");

var timer = 2000;
var slideInterval = setInterval(nextSlide, timer);


var progressStep = (100 / months.length);

var marker = document.createElement("div");
marker.className = "marker";

document.getElementsByClassName("timeline_wrapper")[0].appendChild(marker);

function setMarker() {
    marker.style.left = months[currentSlide-1] + "px";
}

function nextSlide() {
    if (!isPaused) {
        slides[currentSlide].className = 'slide';
        currentSlide = (currentSlide+1)%slides.length;
        slides[currentSlide].className = 'slide showing';
        progress.style.width = (progressStep * currentSlide) +'%';
        setMarker();
    }
}

backbtn.addEventListener("click", function() {
    slides[currentSlide].className = 'slide';
    currentSlide = (currentSlide > 0) ? (currentSlide-1)%slides.length : 0;
    slides[currentSlide].className = 'slide showing';
    progress.style.width = (progressStep * currentSlide) +'%';
    setMarker();
});

nextbtn.addEventListener("click", function() {
    slides[currentSlide].className = 'slide';
    currentSlide = (currentSlide+1)%slides.length;
    slides[currentSlide].className = 'slide showing';
    progress.style.width = (progressStep * currentSlide) +'%';
    setMarker();
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
