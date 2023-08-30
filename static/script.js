
window.onload = function() {
  var ImageMap = function(map, img) {
    var n,
      areas = map.getElementsByTagName('area'),
      len = areas.length,
      coords = [],
      previousWidth = 1517;
    for (n = 0; n < len; n++) {
      coords[n] = areas[n].coords.split(',');
    }
    this.resize = function() {
      var n, m, clen,
        x = img.offsetWidth / previousWidth;
      for (n = 0; n < len; n++) {
        clen = coords[n].length;
        for (m = 0; m < clen; m++) {
          coords[n][m] *= x;
        }
        areas[n].coords = coords[n].join(',');
      }
      previousWidth = document.body.clientWidth;
      return true;
    };
    window.onresize = this.resize;
  },
    imageMap = new ImageMap(document.getElementById('map_ID'), document.getElementById('img_ID'));
  imageMap.resize();
  return;
}



// hover
function hover(page, element) {
// if page reference is nav access the nav folder 
  img_ID.setAttribute('src', "/static/img/"+ page +"/nav_" + element + ".png");
}

function unhover(page) {
  // if the page reference is nav accesss the nav folder
  img_ID.setAttribute('src', "/static/img/"+ page +"/nav.png");
}



// click
function openNav(id) {
  if (id != "mySidebar") { document.getElementById(id).style.width = "100%"; }
  else {
    document.getElementById(id).style.width = "350px";
    //document.getElementById("mainBody").style.marginLeft = "250px";
  }

  document.getElementById("mainBody").style.overflow = "hidden";
}

function closeNav(id) {
  document.getElementById(id).style.width = "0%";
  document.getElementById("mainBody").style.overflow = "visible";
  document.getElementById("mainBody").style.marginLeft = "0";
}


var button = document.getElementById("button");
var audio = document.getElementById("player");

function music() {
  if (audio.paused) {
    audio.play();
    button.innerHTML = "Mute";
  } else {
    audio.pause();
    button.innerHTML = "Play";
  }
};




// 
