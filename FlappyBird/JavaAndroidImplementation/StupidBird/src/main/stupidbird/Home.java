package main.stupidbird;

import java.util.ArrayList;

public class Home {
	
	public Player player;
	public ArrayList<Obstacle> obstacles;
	public float[] screen = new float[2];
	public int count = Global.FREQ;
	public int score = 0;
	
	Home(float[] screen) {
		this.player = new Player(screen);
		this.obstacles = new ArrayList<Obstacle>();
		this.screen = screen;
	}
	
	public void click() {
		this.player.click();
	}
	
	public void update() {
		// update player
		this.player.update();
		
		// update obstacles
		int i = 0;
		while (i < this.obstacles.size()) {
			this.obstacles.get(i).update();
			if (this.obstacles.get(i).off_screen()) {
				this.score++;
				this.obstacles.remove(i);
			} else {i++;}
		}
		
		// Add new obstacles if it's time
		this.count += 1;
		if (this.count >= Global.FREQ) {
			this.obstacles.add(new Obstacle(this.screen));
			this.count = 0;
		}
	}
	
	public void restart() {
		while (this.obstacles.size() > 0) {
			this.obstacles.remove(0);
			this.player = new Player(this.screen);
			this.score = 0; this.count = Global.FREQ;
		}
	}
	
	public boolean is_current_valid() {
		if (this.player.off_screen()) {
			return false;
		} else if (this.obstacles.size() > 0 && this.obstacles.get(0).overlapping(this.player.get_rectangle_definition())) {
			return false;
		} else {
			return true;
		}
	}
}