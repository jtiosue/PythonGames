package main.penguindrop;

import android.graphics.RectF;

public class Cannonball {

	private float[] screen;
	private float x, y, vx, vy;
	private float r; //radius.
	private float a;
	
	public Cannonball(float[] screen, float initial_x, float initial_y, float initial_vx, float initial_vy) {
		this.x = initial_x; this.y = initial_y;
		this.vx = initial_vx; this.vy = initial_vy;
		this.screen = screen;
		
		this.r = Global.PERCENT_CANNONBALL * this.screen[1];
		this.a = Global.G * this.screen[1];
	}
	
	public void update() {
		this.x += this.vx;
		this.vy += this.a;
		this.y += this.vy;
	}
	
	public int[] getRectangularDefinition() {
		int[] f = new int[4];
		f[0] = (int)(this.x-this.r); f[1] = (int)(this.y-this.r);
		f[2] = (int)(this.x+this.r); f[3] = (int)(this.y+this.r);
		return f;
	}
	
	public RectF getRect() {
		//Ovals use RectF not Rect.
		int[] r = this.getRectangularDefinition();
		return new RectF((float)r[0], (float)r[1], (float)r[2], (float)r[3]);
	}
	
	public boolean offScreen() {
		return this.x - this.r > this.screen[0] || this.x + this.r < 0 ||
				this.y - this.r > this.screen[1] || this.y + this.r < 0;
	}
}
