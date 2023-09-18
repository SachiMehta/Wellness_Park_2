function hover2(page, element) {
  // if page reference is nav access the nav folder 
    img_ID2.setAttribute('src', "/static/img/"+ page +"/nav" + element + ".png");
  }
  
  function unhover2(page) {
    // if the page reference is nav accesss the nav folder
    img_ID2.setAttribute('src', "/static/img/"+ page);
  }

  function sub(mood = "ignore", updat="ignore") {
    if (mood != "ignore")
    {document.getElementById('moodInput').value = mood;
    document.getElementById("moodsub").click();}
    else if (updat!= "ignore") 
    {document.getElementById('updateViewHid').value = updat;
      document.getElementById("updateView").click();}
    
  }

   if ( window.history.replaceState ) {
	window.history.replaceState( null, null, window.location.href );
     
   }

$(document).ready(function() {
    $('#secs').change(function() {
      var n = $(this).val();
      if (n < 0)
        $(this).val(0);
      if (n > 60)
        $(this).val(60);
    });
});

$(document).ready(function() {
    $('#mins').change(function() {
      var n = $(this).val();
      if (n < 0)
        $(this).val(0);
      if (n > 60)
        $(this).val(60);
    });
});
function startUp(){
// start up set up 
var savedDistance = 1500000;
var playing = "false";
  
//set starting time 
try {
  var savedDistance = JSON.parse(localStorage.getItem("distance"));
} catch (exceptionVar) {
  localStorage.setItem("distance", 1500000);
  var savedDistance = JSON.parse(localStorage.getItem("distance"));
}

//keep the timer going on reload
try {
  var playing = localStorage.getItem("playing");
} catch (exceptionVar) {
  localStorage.setItem("playing", "false");
  var playing = "false";
}
  
document.getElementById("demo").innerHTML = localStorage.getItem('playing');
var minutes = Math.floor(savedDistance / (1000 * 60));
var seconds = String(Math.floor((savedDistance % (1000 * 60)) / 1000)).padStart(2, '0');

document.getElementById("mins").value = minutes;
document.getElementById("secs").value = seconds;

showUpperRight(minutes, seconds)
var x = null

if (playing == "true")
{start();}
}

function reset()
  {
    stop();
    document.getElementById("demo").innerHTML = "reset";
    localStorage.setItem("distance", 1500000);
    localStorage.setItem("playing", "false");
    
    document.getElementById("mins").value = 25;
    document.getElementById("secs").value = String(0).padStart(2, '0');

    showUpperRight("25", String(0).padStart(2, '0'))
    
  }

window.onload = function(){
  startUp();
}


function stop(){
  localStorage.setItem('playing', "false");
  clearInterval(x);
  x = null
}

// Set the date we're counting down to
function start(){
localStorage.setItem('playing', "true");
  
var mins = document.getElementById("mins").value
var sec = document.getElementById("secs").value
var countTime = (sec*1000) + (mins*60000)
localStorage.setItem('distance', countTime);

//set end time 
var td = new Date().getTime();
var endTime = td + JSON.parse(localStorage.getItem('distance'));
document.getElementById("demo").innerHTML = localStorage.getItem('distance');

// Update the count down every 1 second
x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = endTime - now;

  // Time calculations for days, hours, minutes and seconds
  localStorage.setItem('distance', distance);
  var minutes = Math.floor(distance / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("mins").value = minutes;
  document.getElementById("secs").value = seconds;

  showUpperRight(minutes, seconds)
  //document.getElementById("demo").innerHTML = distance;
    
  // If the count down is over, write some text 
  if (distance <= 1000) {
    localStorage.setItem("distance", 0)
    document.getElementById("mins").value = 0;
    document.getElementById("secs").value = 0;
    showUpperRight("0", "0")
    
    stop()
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);
}

function showUpperRight(minsval, secsval)
{
   
  // select all elements with the class name "example"
var mins = document.getElementsByClassName("mins2");
var secs = document.getElementsByClassName("secs2");

// change the innerHTML of each selected element
for (var i = 0; i < mins.length; i++) {
  mins[i].innerHTML = minsval;
  secs[i].innerHTML = secsval;
}

}
//clear storage 
$(window).unload(function() {
  if (localStorage.getItem("playing") == "false")
  {localStorage.clear();}
});