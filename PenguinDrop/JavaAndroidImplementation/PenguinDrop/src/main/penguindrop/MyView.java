package main.penguindrop;

import android.content.Context;
import android.view.SurfaceView;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.drawable.Drawable;
import java.util.ArrayList;

public class MyView extends SurfaceView {
	
	private final static int TEXT_SIZE = 50;
	
	private Drawable[] penguin_images;
	private Drawable[] parachute_images;
	private Drawable ice;
	private Drawable cannon;
	
	private Paint paint;
	private ArrayList<RectF> cannonballs;
	private int score;
	
	public boolean drawCannon;
	
	public MyView(Context context) {
		super(context);
		this.ice = Global.ICE.getConstantState().newDrawable();
		
		//For cannonballs.
		this.paint = new Paint();
		this.paint.setColor(Color.WHITE);
		//For score text.
		this.paint.setTextSize(MyView.TEXT_SIZE);
	}
	
	@Override
	protected void onDraw(Canvas canvas) {
		super.onDraw(canvas);
		this.ice.draw(canvas);
		for (Drawable img : this.parachute_images) {
			try {
				img.draw(canvas);
			} catch (NullPointerException e) {}
		}
		for (Drawable img : this.penguin_images) {
			try {
				img.draw(canvas);
			} catch (NullPointerException e) {}
		}
		for (RectF r : this.cannonballs) {
			canvas.drawOval(r, this.paint);
		}
		if (this.drawCannon) {
			this.cannon.draw(canvas);
		}
		canvas.drawText(Integer.toString(this.score), 0, MyView.TEXT_SIZE, this.paint);
		this.invalidate();
	}
	
	public void addPenguins(ArrayList<Rect> penguins) {
		this.penguin_images = new Drawable[penguins.size()];
		for (int i=0;i<penguins.size();i++) {
			Drawable d = Global.PENGUIN.getConstantState().newDrawable();
			d.setBounds(penguins.get(i));
			this.penguin_images[i] = d;
		}
	}
	
	public void addParachutes(ArrayList<Rect> parachutes) {
		this.parachute_images = new Drawable[parachutes.size()];
		for (int i=0;i<parachutes.size();i++) {
			Drawable d = Global.PARACHUTE.getConstantState().newDrawable();
			d.setBounds(parachutes.get(i));
			this.parachute_images[i] = d;
		}
	}
	
	public void addCannonballs(ArrayList<RectF> cannonballs) {
		this.cannonballs = cannonballs;
	}
	
	public void addIce(Rect ice) {
		this.ice.setBounds(ice);
	}
	
	public void addScore(int score) {
		this.score = score;
	}
	
	public void addCannon(int angle) {
		this.cannon = Global.CANNONS.get(angle);
	}
}
