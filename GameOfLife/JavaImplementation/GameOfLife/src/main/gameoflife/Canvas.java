package main.gameoflife;

import java.awt.Dimension;
import java.awt.Graphics;
import java.util.ArrayList;
import javax.swing.JPanel;

public class Canvas extends JPanel {
	private ArrayList<int[]> live;
	private ArrayList<int[]> dead;
	
	public Canvas() {
		this.setPreferredSize(new Dimension(Global.screen[0], Global.screen[1]));
	}
	
	public void draw(ArrayList<int[]> live, ArrayList<int[]> dead) {
		this.live = live; this.dead = dead;
		repaint();
	}
	
	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g); //Super invokes parent class.
		g.setColor(Global.liveColor);
		for (int[] rectDef : this.live) {
			g.fillRect(rectDef[0], rectDef[1], rectDef[2]-rectDef[0], rectDef[3]-rectDef[1]);
		}
		g.setColor(Global.deadColor);
		for (int[] rectDef : this.dead) {
			g.fillRect(rectDef[0], rectDef[1], rectDef[2]-rectDef[0], rectDef[3]-rectDef[1]);
		}
	}
}
