package main.penguindrop;

import android.app.Activity;
import android.os.Bundle;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;
import java.util.HashMap;
import android.graphics.Point;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.drawable.Drawable;
import android.view.Display;
import android.graphics.Color;
import android.view.View;
import android.widget.RelativeLayout;

public class MainActivity extends Activity {
	
	public Home home;
	public Ice ice;
	public Cannon cannon;
	public MyView myView;
	public float[] screen;
	public int[] angles;
	public Timer timer;
	public TimerTask task;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		//Get Screen size.
		Display display = getWindowManager().getDefaultDisplay();
		Point size = new Point();
		display.getSize(size);
		this.screen = new float[2];
		this.screen[0] = (float)size.x; this.screen[1] = (float)size.y;
		
		//Initialize drawables in Global.
		Global.PENGUIN = getResources().getDrawable(R.drawable.penguin);
		Global.PARACHUTE = getResources().getDrawable(R.drawable.parachute);
		Global.ICE = getResources().getDrawable(R.drawable.ice);
		this.angles = createCannons(screen); //angles are sorted.
		
	    this.myView = new MyView(this);
	    RelativeLayout layout = (RelativeLayout)findViewById(R.id.parent);
	    layout.addView(this.myView);
	    this.myView.setBackgroundColor(Color.rgb(159, 215, 251));
		
		init();
	}
	
	private void init() {
		//init gets called every restart.
		
		this.ice = new Ice(this.screen);
		this.home = new Home(this.ice);
		this.cannon = new Cannon(this.angles, this.home);
		
		this.myView.addIce(this.ice.getRect());
		this.myView.addCannon(this.cannon.getAngle());
		this.myView.drawCannon = true;
		
		//Set Interval to update.
		this.timer = new Timer();
		this.task = new TimerTask() {
			@Override
			public void run() {
				home.update();
				//Check if game is lost.
				if (ice.getNumPenguins() > Global.MAX_PENGUINS) {
					ice.fall();
					myView.addIce(ice.getRect());
					myView.drawCannon = false;
				}
				draw();
			}
		};
		this.timer.scheduleAtFixedRate(this.task, Global.SPEED, Global.SPEED);
		
		//Game Controls.
		View left = findViewById(R.id.left);
		View right = findViewById(R.id.right);
		View shoot = findViewById(R.id.shoot);
		View restart = findViewById(R.id.restart);
		left.setOnClickListener(new View.OnClickListener() {
			   @Override
			   public void onClick(View view) {
				   if (ice.getNumPenguins() <= Global.MAX_PENGUINS) {
					   cannon.rotateLeft();
					   myView.addCannon(cannon.getAngle());
				   }
			   }
			});
		right.setOnClickListener(new View.OnClickListener() {
			   @Override
			   public void onClick(View view) {
				   if (ice.getNumPenguins() <= Global.MAX_PENGUINS) {
					   cannon.rotateRight();
					   myView.addCannon(cannon.getAngle());
				   }
			   }
			});
		shoot.setOnClickListener(new View.OnClickListener() {
			   @Override
			   public void onClick(View view) {
				   if (ice.getNumPenguins() <= Global.MAX_PENGUINS) {
					   cannon.shootCannonball();
				   }
			   }
			});
		restart.setOnClickListener(new View.OnClickListener() {
			   @Override
			   public void onClick(View view) {
				   task.cancel();
				   timer.cancel();
				   timer.purge();
				   init();
			   }
			});
		findViewById(R.id.buttons).bringToFront();
		shoot.bringToFront();
		restart.bringToFront();
	}
	
	private void draw() {
		ArrayList<Rect> penRects = new ArrayList<Rect>();
		ArrayList<Rect> paraRects = new ArrayList<Rect>();
		ArrayList<RectF> canRects = new ArrayList<RectF>();
		
		for (Penguin pen : this.ice.penguins) {
			penRects.add(pen.getRect());
		}
		for (Penguin pen : this.home.penguins) {
			penRects.add(pen.getRect());
			paraRects.add(pen.parachute.getRect());
		}
		for (Cannonball ball : this.home.cannonballs) {
			canRects.add(ball.getRect());
		}
		
		this.myView.addPenguins(penRects);
		this.myView.addParachutes(paraRects);
		this.myView.addCannonballs(canRects);
		this.myView.addScore(this.home.score);
	}
	
	private int[] createCannons(float[] screen) {
//		//Create cannons.
		Global.CANNONS = new HashMap<Integer, Drawable>();
		Global.CANNONS.put(109, getResources().getDrawable(R.drawable.cannon109));
		Global.CANNONS.put(11, getResources().getDrawable(R.drawable.cannon11));
		Global.CANNONS.put(120, getResources().getDrawable(R.drawable.cannon120));
		Global.CANNONS.put(130, getResources().getDrawable(R.drawable.cannon130));
		Global.CANNONS.put(149, getResources().getDrawable(R.drawable.cannon149));
		Global.CANNONS.put(169, getResources().getDrawable(R.drawable.cannon169));
		Global.CANNONS.put(30, getResources().getDrawable(R.drawable.cannon30));
		Global.CANNONS.put(37, getResources().getDrawable(R.drawable.cannon37));
		Global.CANNONS.put(45, getResources().getDrawable(R.drawable.cannon45));
		Global.CANNONS.put(60, getResources().getDrawable(R.drawable.cannon60));
		Global.CANNONS.put(75, getResources().getDrawable(R.drawable.cannon75));
		Global.CANNONS.put(85, getResources().getDrawable(R.drawable.cannon85));
		Global.CANNONS.put(90, getResources().getDrawable(R.drawable.cannon90));
		Global.CANNONS.put(99, getResources().getDrawable(R.drawable.cannon99));
		
		//Scale Cannons and create angle array.
		float width = (float)Global.CANNONS.get(90).getIntrinsicWidth(); 
		float height = (float)Global.CANNONS.get(90).getIntrinsicHeight();
		float desiredH = Global.PERCENT_CANNON * screen[1];
		
		float[] size = Global.getScaledSize(width, height, desiredH);
		int w = (int)(size[0] / 2); int h = (int)(size[1] / 2);
		int x = (int)(screen[0] / 2); //middle x
		int y = (int)(screen[1]-(screen[1]*Global.PERCENT_ICE)); //middle y
		Rect bounds = new Rect(x-w, y-h, x+w, y+h);
		
		int[] f = new int[Global.CANNONS.size()];
		int i = 0;
		for (int a : Global.CANNONS.keySet()) {
			f[i] = a;
			i++;
			Global.CANNONS.get(a).setBounds(bounds);
		}
		Arrays.sort(f);
		return f;
	}
}
