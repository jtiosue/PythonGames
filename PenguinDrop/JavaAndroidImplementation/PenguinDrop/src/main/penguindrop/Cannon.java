package main.penguindrop;

public class Cannon {
	
	private Home home;
	private int index;
	private float middle_x, middle_y, length;
	private int[] angles;
	private float v0;

	public Cannon(int[] angles, Home home) {
		//angles must be sorted.
		this.index = angles.length / 2;
		
		this.length = Global.PERCENT_CANNON * home.screen[1] / 2f;
		
		this.middle_x = home.screen[0] / 2;
		this.middle_y = home.screen[1]-(home.screen[1]*Global.PERCENT_ICE);
		
		this.v0 = Global.START_VELOCITY * (home.screen[0] + home.screen[1]) / 2;
		
		this.home = home; this.angles = angles;
	}
	
	public int getAngle() {
		return this.angles[this.index];
	}
	
	public void rotateRight() {
		if (this.index > 0) {
			this.index--;
		}
	}
	
	public void rotateLeft() {
		if (this.index + 1 < this.angles.length) {
			this.index++;
		}
	}
	
	public void shootCannonball() {
		double angle = Math.toRadians(this.angles[this.index]);
		float vx = (float)(this.v0 * Math.cos(angle));
		float vy = (float)(this.v0 * Math.sin(angle) * -1);
		
		float x = this.middle_x + (float)Math.cos(angle) * this.length;
		float y = this.middle_y - (float)Math.sin(angle) * this.length / 2;
		
		this.home.addCannonball(new Cannonball(this.home.screen, x, y, vx, vy));
	}
}
