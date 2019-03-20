package pegs;

import pegs.Pieces;

public class Board {
	public int rows, cols;
	public String[][] board; public int[] playerPos;
	
	public Board(String[][] board, int[] playerPos) {
		rows = board.length; cols = board[0].length;
		this.board = board; this.playerPos = playerPos;
	}
	
	public boolean onBoard(int[] pos) {
		int r = pos[0]; int c = pos[1];
		if(r >= 0 && r < rows && c >= 0 && c < cols) {
			return true;
		} else {
			return false;
		}
	}
	
	public String getValue(int[] pos) {
		if(onBoard(pos)) {
			int r = pos[0]; int c = pos[1];
			return board[r][c];
		} else {
			return Pieces.wal;
		}
	}
	
	public void setValue(int[] pos, String value) {
		if(onBoard(pos)) {
			int r = pos[0]; int c = pos[1];
			board[r][c] = value;
		}
	}
	
	private void updatePlayer(int[] pos) {
		setValue(playerPos, Pieces.bla);
		setValue(pos, Pieces.player);
		playerPos = pos;
	}
	
	private void collision(int[] p1, int[] p2) {
		String s1 = getValue(p1); String s2 = getValue(p2);
		if(s1 == Pieces.hol) {
			setValue(playerPos, Pieces.bla);
			playerPos[0] = -1; playerPos[1] = -1;
		} else {
			String v = Pieces.collision(s1, s2);
			if(v != null) {
				setValue(p2, v);
				updatePlayer(p1);
			}
		}
	}
	
	public void move(int[] direction) {
		int[] p1 = Pieces.nextPos(playerPos, direction);
		int[] p2 = Pieces.next2Pos(playerPos, direction);
		collision(p1, p2);
	}
	
	public String state() {
		if(!onBoard(playerPos)) {
			return "defeat";
		}
		int[] pos = new int[2];
		for(int r=0; r<rows; r++) {
			for(int c=0; c<cols; c++) {
				pos[0] = r; pos[1] = c;
				String v = getValue(pos);
				if(v == Pieces.box || v == Pieces.cir ||
						v == Pieces.plu || v == Pieces.tri || v == Pieces.uni) {
					return "ongoing";
				}
			}
		}
		
		return "victory";
	}
	
	public String prettify() {
		String s = "\n";
		for(int r=0; r<rows; r++) {
			s += "   ";
			for(int c=0; c<cols; c++) {
				s += " " + board[r][c];
			}
			s += "\n";
		}
		return s;
	}
}
