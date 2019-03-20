package main.stupidbird;

public class Player {
	
	public float x = Global.PLAYER_POS_0[0];
	public float y = Global.PLAYER_POS_0[1];
	public float w = Global.PLAYER_WIDTH;
	public float g = Global.G;
	public float v0 = Global.INITIAL_V;
	public float xcushion = Global.CUSHION;
	public float ycushion = Global.CUSHION;
	
	public float vy; public float[] screen;
	
	Player(float[] screen) {
		float[] scale = Global.scaling_factor(screen);
		float xscale = scale[0]; float yscale = scale[1];
		
		this.xcushion *= xscale; this.ycushion *= yscale;
		
		this.x *= xscale; this.y *= yscale;
		
		this.w *= yscale; this.g *= yscale; this.v0 *= yscale;
		
		this.vy = 0.0f;
		
		this.screen = screen;
	}
	public void click() {
		this.vy = this.v0;
	}
	public boolean off_screen() {
		return (this.y - this.w > this.screen[1] || this.y + this.w < 0.0);
	}
	public float[] get_rectangle_definition() {
		float x0 = this.x - this.w; float y0 = this.y - this.w;
		float x1 = this.x + this.w; float y1 = this.y + this.w;
		
		float[] x_temp = Global.apply_cushion(x0, x1, this.xcushion);
		float[] y_temp = Global.apply_cushion(y0, y1, this.ycushion);
		
		float[] f = {x_temp[0], y_temp[0], x_temp[1], y_temp[1]};
		return f;
	}
		
	public void update() {
		this.vy += this.g;
		this.y += this.vy;
	}
}