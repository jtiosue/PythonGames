package main.gameoflife;

import java.util.ArrayList;
import javax.swing.JFrame;

public class Home {
	private JFrame frame;
	private Grid grid;
	private Canvas can;
	private int count;
	
	public Home(JFrame frame) {
		this.frame = frame;
		this.can = new Canvas();
		this.frame.add(this.can);
		init();
	}
	
	public void init() {
		this.frame.setTitle("Conway's Game of Life");
		this.grid = new Grid();
		this.count = 0;
		draw();
	}
	
	public void draw(int[] position) {
		int i = this.grid.getIndex(position);
		if (i >= 0) {
			this.grid.makeLive(i);
			draw();
		}
	}
	
	public void update() {
		this.count++;
		this.frame.setTitle("Steps: "+this.count);
		this.grid.update();
		draw();
	}
	
	private void draw() {
		ArrayList<int[]> live = new ArrayList<int[]>();
		ArrayList<int[]> dead = new ArrayList<int[]>();
		
		for (int i=0;i<this.grid.tiles.length;i++) {
			if (this.grid.isTileLive(i)) {
				live.add(this.grid.rectDefs[i]);
			} else {
				dead.add(this.grid.rectDefs[i]);
			}
			
		this.can.draw(live, dead);
		}
	}
}
