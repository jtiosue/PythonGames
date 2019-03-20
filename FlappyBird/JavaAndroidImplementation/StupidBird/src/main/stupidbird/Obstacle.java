package main.stupidbird;

public class Obstacle {
	
	public float x;
	public float opening;
	
	public float w = Global.WIDTH;
	public float vx = Global.OBSTACLE_SPEED;
	public float line_width = Global.LINE_WIDTH;
	
	public float[] screen;
	
	Obstacle(float[] screen) {
		float[] scale = Global.scaling_factor(screen);
		float xscale = scale[0]; float yscale = scale[1];
		
		this.x = screen[0];
		this.w *= yscale;
		
		this.vx *= xscale;
		this.line_width *= xscale;
		
		this.opening = (float)Math.random()*(screen[1]-this.w);
		
		this.screen = screen;
	}
	public boolean off_screen() {
		return this.x + this.line_width < 0;
	}
	public void update() {
		this.x += this.vx;
	}
	public boolean overlapping(float[] rect_def) {
		// rect_def is the rectangular definition of the player.
		float x0 = rect_def[0]; float y0 = rect_def[1];
		float x1 = rect_def[2]; float y1 = rect_def[3];
		
		// Make sure x0 < x1 and y0 < y1
		if (x0 > x1) {
			float x0_temp = x0; float x1_temp = x1;
			x0 = x1_temp; x1 = x0_temp;
		}
		if (y0 > y1) {
			float y0_temp = y0; float y1_temp = y1;
			y0 = y1_temp; y1 = y0_temp;
		}
		
		if (y0 > this.opening && y1 < this.opening + this.w) {
			return false;
		} else {
			if (x1 < this.x || x0 > this.x + this.line_width) {
				return false;
			} else {
				return true;
			}
		}
	}
}