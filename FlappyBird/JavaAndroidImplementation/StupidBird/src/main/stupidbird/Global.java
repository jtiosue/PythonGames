package main.stupidbird;

public class Global {
	
	// Global Variables to be used throughout
	// Most are in absolute scale and will be scaled later.
	// For example, PLAYER_POS_0[0] is the initial x position of the player.
	// On a screen that is 500px wide, it it will be scaled to be 50px
	public static float[] PLAYER_POS_0 = {10.0f, 50.0f};
	public static float PLAYER_WIDTH = 2.0f;

	public static float INITIAL_V = -1.8f; //Speed up when pressing the space bar before scaling.
	public static float G = 0.1f; //Acceleration down before scaling.

	public static float OBSTACLE_SPEED = -0.7f; ///before scaling.
	public static float LINE_WIDTH = 2.5f; //Width of obstacles before scaling.
	public static float WIDTH = 27.0f; //Width of openings before scaling.
	public static int SPEED = 20; //Milliseconds between screen redraw.
	public static int FREQ = 60; //How often new obstacles are initialized.
	public static float CUSHION = 0.3f; //Give leniency to player.
	
	public static int TEXT_SIZE = 50; //Size of score text.
	
	public static float[] scaling_factor(float[] screen) {
		float[] f = new float[2];
		f[0] = screen[0]/100.0f;
		f[1] = screen[1]/100.0f;
		return f;
	}
	
	public static float[] apply_cushion(float x0, float x1, float cushion) {
		if (x0 < x1) {
			x0 += cushion;
			x1 -= cushion;
		} else {
			x0 -= cushion;
			x1 += cushion;
		}
		float[] f = {x0, x1};
		return f;
	}
}