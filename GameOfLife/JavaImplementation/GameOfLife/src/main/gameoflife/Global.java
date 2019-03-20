package main.gameoflife;

import java.awt.Color;

public class Global {
	// Rules
	public final static int maxNeighbors = 3;
	public final static int minNeighbors = 2;
	public final static int idealNeighbors = 3;
	
	// Settings
	public final static int[] dimension = {50, 40};
	public final static int[] screen = {1000, 800};
	public final static Color liveColor = Color.GREEN;
	public final static Color deadColor = Color.WHITE;
	public final static int speed = 500;
	
	public static int[][] getNeighbors(int[] position) {
		int[][] f = new int[8][2];
		
		int i = 0;
		for (int x=-1;x<=1;x++) {
			for (int y=-1;y<=1;y++) {
				if (x != 0 || y != 0) {
					f[i][0] = position[0] + x;
					f[i][1] = position[1] + y;
					i++;
				}
			}
		}
		return f;
	}
	
	public static int getIndexOf(int[] tile, int[][] tiles) {
		for (int i=0;i<tiles.length;i++) {
			if (tiles[i][0] == tile[0] && tiles[i][1] == tile[1]) {
				return i;
			}
		}
		return -1;
	}
	
}
