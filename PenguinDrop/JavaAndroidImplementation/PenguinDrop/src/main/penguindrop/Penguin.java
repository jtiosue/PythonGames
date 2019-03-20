package main.penguindrop;

import android.graphics.Rect;

public class Penguin {
	
	private float x, y;
	private float width, height;
	private float[] screen;
	private float vy;
	public Parachute parachute;
	
	public Penguin(float[] screen) {		
		float w = (float)Global.PENGUIN.getIntrinsicWidth(); float h = (float)Global.PENGUIN.getIntrinsicHeight();
		float desiredH = Global.PERCENT_PENGUIN * screen[1];
		float[] size = Global.getScaledSize(w, h, desiredH);
		this.width = size[0]; this.height = size[1];
		
		this.x = (float)Math.random() * (screen[0]-this.width);
		this.y = -this.height;
		this.vy = Global.FALLING_SPEED * screen[1];
		
		this.parachute = new Parachute(screen, this.x, this.y-this.height);
		
		this.screen = screen;		
	}
	
	public void update() {
		this.y += this.vy;
		this.parachute.update();
	}

	public int[] getRectangularDefinition() {
		int[] f = new int[4];
		f[0] = (int)this.x; f[1] = (int)this.y;
		f[2] = (int)(this.x+this.width); f[3] = (int)(this.y+this.height);
		return f;
	}
	
	public Rect getRect() {
		int[] r = this.getRectangularDefinition();
		return new Rect(r[0], r[1], r[2], r[3]);
	}
	
	public boolean offScreen() {
		return this.y - Global.PERCENT_PARACHUTE*this.screen[1] > this.screen[1];
	}
}