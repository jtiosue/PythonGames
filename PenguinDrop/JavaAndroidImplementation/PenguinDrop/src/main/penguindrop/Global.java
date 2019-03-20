package main.penguindrop;

import java.util.HashMap;
import android.graphics.drawable.Drawable;

public class Global {

	// Difficulty
	public static final int MAX_PENGUINS = 15;
	
	// Adjust movement of objects (these will be scaled based on screen size)
	public static final float FALLING_SPEED = 0.0025f;  //Speed that penguins fall (later * by screen height).
	public static final float G = 0.0005f;  //Acceleration of cannonball down due to gravity (later * by screen height).
	public static final float START_VELOCITY = 0.027f;  //Magnitude of velocity of cannonball when first shot (later * by sum(screen)).
	
	// Adjust relative sizes of objects
	public static final float PERCENT_ICE = 0.15f; //Ice height in terms of percent of screen.
	public static final float PERCENT_PENGUIN = 0.06f; //Penguin height in terms of percent of screen.
	public static final float PERCENT_PARACHUTE = 0.08f;//Parachute height in terms of percent of screen.
	public static final float PERCENT_CANNONBALL = 0.007f; //Cannonball radius in terms of percent of screen.
	public static final float PERCENT_CANNON = 0.08f; //Cannon height in terms of percent of screen.
	/* Penguin, parachute, and cannon images are scaled to keep their aspect ratios.
	   Ice image is set at size = (SCREEN[0], PERCENT_ICE*SCREEN[1]) */
	
	public static final int SPEED = 30; //Milliseconds between screen redraws.
	
	//////////////////////////////////////////////////////////////////////

	//Public drawables initialized in MainActivity at start only once.
	public static Drawable PENGUIN;
	public static Drawable PARACHUTE;
	public static Drawable ICE;
	public static HashMap<Integer, Drawable> CANNONS;
	
	//////////////////////////////////////////////////////////////////////

	public static float[] getScaledSize(float w, float h, float desiredH) {		
		float scale = desiredH / h;
		float[] f = new float[2];
		f[0] = w*scale; f[1] = h*scale;
		return f;
	}
	
	public static boolean overlapping(int[] rectDef1, int[] rectDef2) {
		if (rectDef1[0] >= rectDef2[0] && rectDef1[0] <= rectDef2[2]) {
			if (rectDef1[1] >= rectDef2[1] && rectDef1[1] <= rectDef2[3]) {
				return true;
			} else if (rectDef1[3] >= rectDef2[1] && rectDef1[3] <= rectDef2[3]) {
				return true;
			}
		} else if (rectDef1[2] >= rectDef2[0] && rectDef1[2] <= rectDef2[2]) {
			if (rectDef1[1] >= rectDef2[1] && rectDef1[1] <= rectDef2[3]) {
				return true;
			} else if (rectDef1[3] >= rectDef2[1] && rectDef1[3] <= rectDef2[3]) {
				return true;
			}
		}
		if (rectDef2[0] >= rectDef1[0] && rectDef2[0] <= rectDef1[2]) {
			if (rectDef2[1] >= rectDef1[1] && rectDef2[1] <= rectDef1[3]) {
				return true;
			} else if (rectDef2[3] >= rectDef1[1] && rectDef2[3] <= rectDef1[3]) {
				return true;
			}
		} else if (rectDef2[2] >= rectDef1[0] && rectDef2[2] <= rectDef1[2]) {
			if (rectDef2[1] >= rectDef1[1] && rectDef2[1] <= rectDef1[3]) {
				return true;
			} else if (rectDef2[3] >= rectDef1[1] && rectDef2[3] <= rectDef1[3]) {
				return true;
			}
		}
		return false;
	}
}
