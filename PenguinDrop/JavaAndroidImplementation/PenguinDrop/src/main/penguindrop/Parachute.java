package main.penguindrop;

import android.graphics.Rect;

public class Parachute {
	
	private float x, y;
	private float width, height;
	private float vy;
	
	public Parachute(float[] screen, float initial_x, float initial_y) {
		this.x = initial_x; this.y = initial_y;
		
		float w = (float)Global.PARACHUTE.getIntrinsicWidth(); float h = (float)Global.PARACHUTE.getIntrinsicHeight();
		float desiredH = Global.PERCENT_PARACHUTE * screen[1];
		float[] size = Global.getScaledSize(w, h, desiredH);
		this.width = size[0]; this.height = size[1];
		
		this.vy = Global.FALLING_SPEED * screen[1];
	}
	
	public void update() {
		this.y += this.vy;
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
}