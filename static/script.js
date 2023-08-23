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

class Timer {
  constructor(root, root2) {
    root.innerHTML = Timer.getHTML();
    root2.innerHTML = Timer.getHTML();

    this.el = {
      minutes: root.querySelector(".timer__part--minutes"),
      seconds: root.querySelector(".timer__part--seconds"),
      control: root.querySelector(".timer__btn--control"),
      reset: root.querySelector(".timer__btn--reset")
    };

    this.interval = null;
    this.remainingSeconds = 0;

    this.el.control.addEventListener("click", () => {
      if (this.interval === null) {
        this.start();
      } else {
        this.stop();
      }
    });

    this.el.reset.addEventListener("click", () => {
      const inputMinutes = prompt("Enter number of minutes:");

      if (inputMinutes < 60) {
        this.stop();
        this.remainingSeconds = inputMinutes * 60;
        this.updateInterfaceTime();
      }
    });
  }

  updateInterfaceTime() {
    const minutes = Math.floor(this.remainingSeconds / 60);
    const seconds = this.remainingSeconds % 60;

    this.el.minutes.textContent = minutes.toString().padStart(2, "0");
    this.el.seconds.textContent = seconds.toString().padStart(2, "0");
  }

  updateInterfaceControls() {
    if (this.interval === null) {
      this.el.control.innerHTML = `<span class="material-icons">play_arrow</span>`;
      this.el.control.classList.add("timer__btn--start");
      this.el.control.classList.remove("timer__btn--stop");
    } else {
      this.el.control.innerHTML = `<span class="material-icons">pause</span>`;
      this.el.control.classList.add("timer__btn--stop");
      this.el.control.classList.remove("timer__btn--start");
    }
  }

  start() {
    if (this.remainingSeconds === 0) return;

    this.interval = setInterval(() => {
      this.remainingSeconds--;
      this.updateInterfaceTime();

      if (this.remainingSeconds === 0) {
        this.stop();
      }
    }, 1000);

    this.updateInterfaceControls();
  }

  stop() {
    clearInterval(this.interval);

    this.interval = null;

    this.updateInterfaceControls();
  }

  static getHTML() {
    return `
			<span class="timer__part timer__part--minutes">00</span>
			<span class="timer__part">:</span>
			<span class="timer__part timer__part--seconds">00</span>
			<button type="button" class="timer__btn timer__btn--control timer__btn--start">
				<span class="material-icons">play_arrow</span>
			</button>
			<button type="button" class="timer__btn timer__btn--reset">
				<span class="material-icons">timer</span>
			</button>
		`;
  }
}

new Timer(
  document.querySelector(".timer"),
  document.querySelector(".topcorner")
);

