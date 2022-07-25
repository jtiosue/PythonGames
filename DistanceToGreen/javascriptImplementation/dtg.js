function getDPI() {
  return parseFloat(document.getElementById("dpi").value);
}


function getHoldDistance() {
  return parseFloat(document.getElementById("holdDistance").value) / 36.;
}


function getPinHeight() {
  return parseFloat(document.getElementById("pinHeight").value) / 3.;
}


function calculateDistance(barHeightPixels) { // in yards
  var barHeightYards = barHeightPixels / (36.*getDPI());
  return getPinHeight() * getHoldDistance() / barHeightYards;
}


class Home {

  constructor(canvas, screen){
    this.canvas = canvas;
    this.screen = screen;
    this.bottom = 100;
    this.update(this.bottom);
  }

  update(bottom) {
    this.bottom = bottom;
    this.clearCanvas();
    this.canvas.fillRect(0, 0, this.screen[0], 20);
    this.canvas.fillRect(0, bottom, this.screen[0], 20);
    this.updateDistance(bottom);
  }

  updateDistance(bottom) {
    document.getElementById("distance").innerHTML = 
      Math.round(calculateDistance(bottom-20)) + " yards";
  }

  clearCanvas() {
    this.canvas.clearRect(-100, -100, this.screen[0]+100, this.screen[1]+100);
  }

  drag(location) {
    this.update(location-10);
  }

}


function main(screen) {
    var canvas = document.getElementById("canvas");
    canvas.width = screen[0]; canvas.height = screen[1];
    var ctx = canvas.getContext('2d');
    var home = new Home(ctx, screen);

    var offset = canvas.getBoundingClientRect();
    canvas.addEventListener("touchmove", function(event) {
      event.preventDefault();
      home.drag(event.pageY-offset.top-10);
    }, { passive: false });
    
    canvas.addEventListener("mousemove", function(event) {
      home.drag(event.offsetY-10);
    });
}

window.onload = function() {
    // screen = [700, 500];
    screen = [window.innerWidth, window.innerHeight/1.5];
    main(screen);
}

