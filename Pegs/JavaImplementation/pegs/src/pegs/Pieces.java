package pegs;

public class Pieces {
	public final static String box = "B";
	public final static String cir = "O";
	public final static String plu = "+";
	public final static String tri = "T";
	public final static String uni = "U";
	public final static String hol = "H";
	public final static String wal = "W";
	public final static String player = "P";
	public final static String bla = " ";
	
	public final static int[] left = {0, -1};
	public final static int[] right = {0, 1};
	public final static int[] up = {-1, 0};
	public final static int[] down = {1, 0};
	
	public static int[] nextPos(int[] pos, int[] direction) {
		int x = pos[0]; int y = pos[1];
		int dx = direction[0]; int dy = direction[1];
		int[] f = {x+dx, y+dy};
		return f;
	}
	
	public static int[] next2Pos(int[] pos, int[] direction) {
		int x = pos[0]; int y = pos[1];
		int dx = direction[0]; int dy = direction[1];
		int[] f = {x+2*dx, y+2*dy};
		return f;
	}
	
	public static String collision(String p1, String p2) {
		if(p1 == bla) {
			return p2;
		} else if(p1 == box) {
			if(p2 == bla) {
				return p1;
			} else if(p2 == box || p2 == hol || p2 == uni) {
				return bla;
			}
		} else if(p1 == cir) {
			if(p2 == cir || p2 == uni) {
				return bla;
			} else if(p2 == hol) {
				return hol;
			} else if(p2 == bla) {
				return cir;
			}
		} else if(p1 == plu) {
			if(p2 == plu || p2 == uni) {
				return uni;
			} else if(p2 == hol) {
				return hol;
			} else if(p2 == bla) {
				return plu;
			}
		} else if(p1 == tri) {
			if(p2 == tri || p2 == uni) {
				return wal;
			} else if(p2 == hol) {
				return hol;
			} else if(p2 == bla) {
				return tri;
			}
		} else if(p1 == uni) {
			if(p2 == uni || p2 == tri) {
				return wal;
			} else if(p2 == hol || p2 == box || p2 == cir) {
				return bla;
			} else if(p2 == bla || p2 == plu) {
				return uni;
			}
		}
		return null;
	}
}