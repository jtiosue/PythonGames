package main.stupidbird;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Canvas;
import android.graphics.Color;
import android.content.Context;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.View;
import android.view.Display;
import android.view.MotionEvent;
import android.graphics.Point;
import java.util.Timer;
import java.util.TimerTask;
import java.util.ArrayList;

public class MainActivity extends Activity {
	
	public Timer timer;
	public TimerTask task;
	public float[] screen = new float[2];
	public Home home;
	public MyView view;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);		
		
		//Get Screen size.
		Display display = getWindowManager().getDefaultDisplay();
		Point size = new Point();
		display.getSize(size);
		this.screen[0] = (float)size.x;
		this.screen[1] = (float)size.y;
	
		this.home = new Home(this.screen);
		
		view = new MyView(this);
		setContentView(view);
		view.setBackgroundColor(Color.rgb(214, 214, 214));

		
		//Bind click to View.
		view.setOnTouchListener(new View.OnTouchListener() {
	        @Override
	        public boolean onTouch(View view, MotionEvent event) {
	        	if (home.is_current_valid()) {
	        		home.click();
	        	} else {
	        		home.restart();
	        		cancel_timer();
	        		set_timer();
	        	}
	            return true;
	        }
	    });
		
		//Start.
		this.set_timer();
	}
	
	public void set_timer() {
		this.timer = new Timer();
		
		this.task = new TimerTask() {
			@Override
			public void run() {
				home.update();
				
				//Draw Player.
				float x = home.player.x; float y = home.player.y;
				float w = home.player.w;
				RectF player = new RectF(x-w, y-w, x+w, y+w);
				view.addPlayer(player);
				
				//Draw Obstacles.
				ArrayList<RectF> obstacles = new ArrayList<RectF>();
				for (Obstacle obs : home.obstacles) {
					obstacles.add(new RectF(obs.x, 0, obs.x+obs.line_width, obs.opening));
					obstacles.add(new RectF(obs.x, obs.opening+obs.w, obs.x+obs.line_width, obs.screen[1]));
				}
				view.addObstacles(obstacles);
				
				if (home.is_current_valid()) {
					view.addScore(home.score);
				} else {
					cancel_timer();
				}
				view.postInvalidate();
			}
		};
		
		this.timer.scheduleAtFixedRate(this.task, Global.SPEED, Global.SPEED);
	}
	
	public void cancel_timer() {
		this.task.cancel();
		this.timer.cancel();
		this.timer.purge();
	}
	
	public class MyView extends View {
		
		public Paint paint;
		public RectF player;
		public ArrayList<RectF> obstacles;
		public int score;
		
		public MyView(Context context) {
			super(context);
			this.paint = new Paint();
			this.paint.setColor(Color.BLACK);
			this.paint.setTextSize(Global.TEXT_SIZE);
		}
		
		@Override
		protected void onDraw(Canvas canvas) {
			super.onDraw(canvas);
			canvas.drawOval(this.player, this.paint);
			for (RectF r : this.obstacles) {
				canvas.drawRect(r, this.paint);
			}
			canvas.drawText(Integer.toString(this.score), Global.TEXT_SIZE, Global.TEXT_SIZE, this.paint);
		}
		public void addPlayer(RectF rect) {
			this.player = rect;
		}
		public void addObstacles(ArrayList<RectF> obstacles) {
			this.obstacles = obstacles;
		}
		public void addScore(int score) {
			this.score = score;
		}
	}
}
