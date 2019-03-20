package main.penguindrop;

import android.graphics.Rect;
import java.util.ArrayList;

public class Ice {

	public float[] screen;
	private float y, vy, height;
	public ArrayList<Penguin> penguins;
	
	public Ice(float[] screen) {		
		this.screen = screen;
		this.penguins = new ArrayList<Penguin>();
		this.height = this.screen[1]*Global.PERCENT_ICE;
		this.y = this.screen[1] - this.height;
		this.vy = Global.FALLING_SPEED * this.screen[1];
	}
	
	public int[] getRectangularDefinition() {
		int[] f = new int[4];
		f[0] = 0; 
		f[1] = (int)this.y;
		f[2] = (int)this.screen[0]; 
		f[3] = (int)(this.y + this.height);
		return f;
	}
	
	public Rect getRect() {
		int[] r = this.getRectangularDefinition();
		return new Rect(r[0], r[1], r[2], r[3]);
	}
	
	public void fall() {
		if (this.y - this.height <= this.screen[1]) {
			this.y += this.vy;
		}
		for (Penguin pen : this.penguins) {
			if (!pen.offScreen()) {
				pen.update();
			}
		}
	}
	
	public int getNumPenguins() {
		return this.penguins.size();
	}
	
	public void addPenguin(Penguin penguin) {
		this.penguins.add(penguin);
	}
}