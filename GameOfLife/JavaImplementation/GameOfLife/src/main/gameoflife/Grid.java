package main.gameoflife;

import java.util.ArrayList;

public class Grid {
	public int[][] tiles;
	private boolean[] grid;
	public int[][] rectDefs;
	
	public Grid() {
		int dx = Global.screen[0] / Global.dimension[0];
		int dy = Global.screen[1] / Global.dimension[1];
		int w = dx * Global.dimension[0];
		int h = dy * Global.dimension[1];
		
		int arraySize = Global.dimension[0] * Global.dimension[1];
		tiles = new int[arraySize][2];
		grid = new boolean[arraySize];
		rectDefs = new int[arraySize][4];
		
		int x_grid, y_grid, index;
		y_grid = 0; index = 0;
		for (int y=0;y<h;y+=dy) {
			y_grid++; x_grid = 0;
			for (int x=0;x<w;x+=dx) {
				x_grid++;
				int[] position = {x_grid, y_grid};
				int[] rectDef = {x, y, x+dx, y+dy};
				tiles[index] = position;
				grid[index] = false;
				rectDefs[index] = rectDef;
				index++;
			}
		}
	}
	
	public boolean isTileLive(int index) {
		if (index < 0) {
			return false;
		} else {
			return grid[index];
		}
	}
	
	public int getIndex(int[] position) {
        int x = position[0]; int y = position[1];
        int[] rectDef;
        for (int index=0;index<tiles.length;index++) {
        	rectDef = rectDefs[index];
            if (x >= rectDef[0] && x <= rectDef[2]
            && y >= rectDef[1] && y <= rectDef[3]) {
                return index;
            }  	
        }
        return -1;
	}
	
	public void makeLive(int index) {
		grid[index] = true;
	}
	
	public void makeDead(int index) {
		grid[index] = false;
	}
	
	public int numLiveNeighbors(int index) {
		int total = 0;
		for (int[] n : Global.getNeighbors(tiles[index])) {
			if (isTileLive(Global.getIndexOf(n, tiles))) {
				total++;
			}
		}
		return total;
	}
	
	public void update() {
		ArrayList<Integer> toMakeDead = new ArrayList<Integer>();
		ArrayList<Integer> toMakeLive = new ArrayList<Integer>();
		
		for (int index=0;index<grid.length;index++) {
			int numLive = numLiveNeighbors(index);
			if (isTileLive(index)) {
				if (numLive < Global.minNeighbors || numLive > Global.maxNeighbors) {
					toMakeDead.add(index);
				}
			} else {
				if (numLive == Global.idealNeighbors) {
					toMakeLive.add(index);
				}
			}
		}
		for (int index : toMakeDead) {
			makeDead(index);
		}
		for (int index : toMakeLive) {
			makeLive(index);
		}
	}
}
