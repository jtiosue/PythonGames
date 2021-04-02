var CUSHION = 0.2;
var PLAYER_POS_0 = [10, 50];
var PLAYER_WIDTH = 2;
var INITIAL_V = -2;
var G = 0.12;
var SPEED = 20;
var WIDTH = 20;
var OBSTACLE_SPEED = -0.75;
var LINE_WIDTH = 2.5;
var FREQ = 60;
var FONTSIZE = 30;


function scaling_factor(screen) {
    return [screen[0]/100.0, screen[1]/100.0];
}

function apply_cushion(x0, x1, cushion) {
    if (x0 < x1) {
        x0 += cushion;
        x1 -= cushion;
    } else {
        x0 -= cushion;
        x1 += cushion;
    }
    return [x0, x1];
}

class Player {
    constructor(screen) {
        var scale = scaling_factor(screen);
        var xscale = scale[0]; var yscale = scale[1];
        this.xcushion = CUSHION*xscale; this.ycushion = CUSHION*yscale;
        
        this.x = PLAYER_POS_0[0]*xscale; this.y = PLAYER_POS_0[1]*yscale;
        
        this.w = PLAYER_WIDTH*yscale;
        
        this.v0 = INITIAL_V*yscale;
        this.vy = 0;
        this.g = G*yscale;
        
        this.screen = screen;
    }
    update() {
        this.vy += this.g;
        this.y += this.vy   
    }
    click() {
        this.vy = this.v0;
    }
    off_screen() {
        return this.y < -this.ycushion || this.y > this.screen[1]+this.ycushion;
    }
    draw(canvas) {
        canvas.beginPath();
        canvas.arc(this.x, this.y, this.w, 0, 2*Math.PI);
        canvas.stroke();
    }
    get_rectangular_definition() {
        var x0 = this.x - this.w; var y0 = this.y - this.w;
        var x1 = this.x + this.w; var y1 = this.y + this.w;
        
        var X = apply_cushion(x0, x1, this.xcushion);
        var Y = apply_cushion(y0, y1, this.ycushion);
        
        var x0 = X[0]; var x1 = X[1];
        var y0 = Y[0]; var y1 = Y[1];
        
        return [x0, y0, x1, y1];
    }
}

class Obstacle {
    constructor(screen) {
        var scale = scaling_factor(screen);
        var xscale = scale[0]; var yscale = scale[1];
        
        this.x = screen[0];
        this.w = WIDTH * yscale;
        
        this.vx = OBSTACLE_SPEED * xscale;
        
        this.opening = parseInt(Math.random()*(screen[1]-this.w));
        
        this.line_width = LINE_WIDTH*xscale;
        
        this.screen = screen;
    }
    update() {
        this.x += this.vx;
    }
    off_screen() {
        return this.x + this.line_width < 0;
    }
    draw(canvas) {
        canvas.fillRect(this.x, 0, this.line_width, this.opening);
        canvas.fillRect(
            this.x, this.opening + this.w,
            this.line_width, this.screen[1] - this.opening-this.w
        );
    }
    overlapping(rect_def) {
        var x0 = rect_def[0]; var y0 = rect_def[1];
        var x1 = rect_def[2]; var y1 = rect_def[3];
        if (x0 > x1) {
            var x0_temp = x0; var x1_temp = x1;
            x0 = x1_temp; x1 = x0_temp;
        }
        if (y0 > y1) {
            var y0_temp = y0; var y1_temp = y1;
            y0 = y1_temp; y1 = y0_temp;
        }
        if (y0 > this.opening && y1 < this.opening+this.w) {
            return false;
        } else {
            if (x1 < this.x || x0 > this.x+this.line_width) {
                return false;
            } else {
                return true;
            }
        }
    }
}

class Home {
    constructor(canvas, screen) {
        this.can = canvas;
        this.screen = screen;
        this.restart();
    }
    restart() {
        this.count = FREQ; this.score = 0;
        this.player = new Player(this.screen);
        this.player.draw(this.can);
        this.obstacles = [];
        this.running = true;
    }
    stop(interval) {
        clearInterval(interval);
        this.running = false;
    }
    click() {
        this.player.click();
    }
    clear_canvas() {
        this.can.clearRect(-100, -100, this.screen[0]+100, this.screen[1]+100);
    }
    update(interval) {
        this.clear_canvas();
        
        this.can.font = FONTSIZE+"px Arial";
        this.can.fillText(this.score, 0, FONTSIZE)
        
        this.player.update()
        this.player.draw(this.can);
        if (this.player.off_screen()) {this.stop(interval);}
        
        var rect_def = this.player.get_rectangular_definition();
        
        var i = 0;
        while (i < this.obstacles.length) {
            this.obstacles[i].update();
            this.obstacles[i].draw(this.can);
            if (this.obstacles[i].overlapping(rect_def)) {
                this.stop(interval);
            }
            if (this.obstacles[i].off_screen()) {
                this.obstacles.splice(i, 1);
                this.score += 1;
                i -= 1;
            }
            i += 1
        }
        
        this.count += 1;
        if (this.count >= FREQ) {
            this.obstacles.push(new Obstacle(this.screen));
            this.count = 0;
        }
    }
}

function play(screen) {
    var canvas = document.getElementById("canvas");
    canvas.width = screen[0]; canvas.height = screen[1];
    canvas.style = "background-color: #e6f9ff;";
    var ctx = canvas.getContext('2d');
    var main = new Home(ctx, screen);
    
    canvas.addEventListener("click", function(event) {
        if(main.running)
            main.click();
        else {
            main.restart();
            interval = setInterval(function() {main.update(interval);}, SPEED);
        }
    });
    
    var interval = setInterval(function() {main.update(interval);}, SPEED);
}

window.onload = function() {
    // screen = [700, 500];
    screen = [window.innerWidth/2, window.innerHeight/1.5];
    play(screen);
}
