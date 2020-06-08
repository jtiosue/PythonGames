package main.distancetogreen;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.util.DisplayMetrics;
import android.view.MotionEvent;
import android.view.View;

public class MyView extends View implements View.OnTouchListener {

	private final static int NONE = 0;
	private final static int TOP = 1;
	private final static int BOTTOM = 2;
	
	//In inches. Both are scaled to pixels later with dpi.
	private final static float TEXT_SIZE = 0.2f;
	private final static float HEIGHT = 0.03f; //Thickness of lines. 0.25 the size of handles.
	
	private float dpi;
	private Rect top, bottom;
	private int current, textSize, height, radius;
	private Paint paint;
	private Drawable flag1, flag2, topBall, bottomBall;

	public MyView(Context context) {
		super(context);	
		DisplayMetrics metrics = context.getResources().getDisplayMetrics();	
		int w = metrics.widthPixels; int h = metrics.heightPixels;
		
		// #pixels / this.dpi = distance in inches.
		dpi = metrics.density * 160f;
		height = (int)(HEIGHT * dpi); //thickness of lines.
		textSize = (int)(TEXT_SIZE * dpi);
		
		// Initial y values don't really matter. They are adjusted by user.
		top = new Rect(0, h/4-height/2, w, h/4+height/2);
		bottom = new Rect(0, h/2-height/2, w, h/2+height/2);
		
		radius = 4 * height;
		Drawable ball = context.getResources().getDrawable(R.drawable.golfball);
		topBall = ball.getConstantState().newDrawable();
		topBall.setBounds(new Rect(w/2-radius, h/4-radius, w/2+radius, h/4+radius));
		bottomBall = ball.getConstantState().newDrawable();
		bottomBall.setBounds(new Rect(w/2-radius, h/2-radius, w/2+radius, h/2+radius));
		
		Drawable flag = context.getResources().getDrawable(R.drawable.flag);
		flag1 = flag.getConstantState().newDrawable();
		flag1.setBounds(new Rect(w/4-w/8, top.bottom, w/4+w/8, bottom.top));
		flag2 = flag.getConstantState().newDrawable();
		flag2.setBounds(new Rect(3*w/4-w/8, bottom.bottom, 3*w/4+w/8, top.top));
		
		paint = new Paint();
		paint.setColor(context.getResources().getColor(R.color.font));
		paint.setTextSize(textSize);
		
		current = NONE;		
		setOnTouchListener(this);
	}
	
	@Override
	protected void onDraw(Canvas canvas) {
		super.onDraw(canvas);
		//Update flags.
		Rect bounds;
		bounds = flag1.copyBounds();
		bounds.top = top.bottom; bounds.bottom = bottom.top;
		flag1.setBounds(bounds);
		bounds = flag2.copyBounds();
		bounds.top = bottom.bottom; bounds.bottom = top.top;
		flag2.setBounds(bounds);
		
		//The ordering is kind of important. Draw most important things last.
		flag1.draw(canvas);
		flag2.draw(canvas);
		canvas.drawRect(top, paint);
		topBall.draw(canvas);
		canvas.drawRect(bottom, paint);
		bottomBall.draw(canvas);
		canvas.drawText(computeDistance()+" yards", 0, textSize, paint);
	}
	
	@Override
	public boolean onTouch(View v, MotionEvent event) {
	    int x = (int)event.getX();
	    int y = (int)event.getY();
	    
	    switch (event.getAction()) {
	    case MotionEvent.ACTION_DOWN:
	    	current = hitTest(x, y);
	    	break;
	    case MotionEvent.ACTION_MOVE:
	    	if (current == TOP) {
	    		top.bottom = y + height/2;
	    		top.top = y - height/2;
	    		
	    		Rect bounds = topBall.copyBounds();
	    		bounds.top = y - radius;
	    		bounds.bottom = y + radius;
	    		topBall.setBounds(bounds);
	    		
	    		invalidate();
	    	} else if (current == BOTTOM) {
	    		bottom.bottom = y + height/2;
	    		bottom.top = y - height/2;	
	    		
	    		Rect bounds = bottomBall.copyBounds();
	    		bounds.top = y - radius;
	    		bounds.bottom = y + radius;
	    		bottomBall.setBounds(bounds);
	    		
	    		invalidate();
	    	}
	    	break;
	    case MotionEvent.ACTION_CANCEL:
	    	current = NONE;
	    	break;
	    }
	    
		return true;
	}
	
	private int hitTest(int x, int y) {
		//See if position (x, y) is on the golfball handles.
		Rect t = topBall.getBounds();
		Rect b = bottomBall.getBounds();
		if (x >= t.left && x <= t.right && y >= t.top && y <= t.bottom) {
			return TOP;
		} else if (x >= b.left && x <= b.right && y >= b.top && y <= b.bottom) {
			return BOTTOM;
		} else {
			return NONE;
		}
	}
	
	private int computeDistance() {
		// D_x/S_x = D_y/S_y
		float relHeight = Math.min(Math.abs(top.bottom - bottom.top),
								   Math.abs(top.top - bottom.bottom));
		
		float hYards = (relHeight / dpi) / 36f;
		
		return (int)Math.round(MainActivity.HOLD_DISTANCE * MainActivity.PIN_HEIGHT / hYards);
	}
}
