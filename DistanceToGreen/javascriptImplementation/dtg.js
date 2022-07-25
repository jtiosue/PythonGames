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

  drag(event) {
    // if (this.bottom <= event.offsetY && event.offsetY <= this.bottom+20) {
      // this.update(event.offsetY-10);
    this.update(event.pageY-10);
    // }
  }

}


function main(screen) {
    var canvas = document.getElementById("canvas");
    canvas.width = screen[0]; canvas.height = screen[1];
    var ctx = canvas.getContext('2d');
    var home = new Home(ctx, screen);

    var mousedown = false;
    // canvas.addEventListener("mousedown", function(event) {
      mousedown = true;
    // });
    // canvas.addEventListener("mouseup", function(event) {
    //  mousedown = false;
    // });
    canvas.addEventListener("touchmove", function(event) {
      if (mousedown) {home.drag(event);}
    });
}

window.onload = function() {
    // screen = [700, 500];
    screen = [window.innerWidth, window.innerHeight/1.5];
    main(screen);
}

