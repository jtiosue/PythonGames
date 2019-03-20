package pegs;

import pegs.Pieces;
import pegs.Board;
import java.util.Scanner;

public class game {

	public static void main(String[] args) {
		int[] playerPos = {0, 0};
		String[][] b = {
				{"P", " ", " ", " "},
				{"B", "O", " ", " "},
				{"B", "O", " ", "W"}
		};
		
		Board board = new Board(b, playerPos);
		play(board);
	}
	
	public static void play(Board board) {
		Scanner reader = new Scanner(System.in);
		String move;
		while(board.state() == "ongoing") {
			System.out.println(board.prettify());
			System.out.println("Enter move: ");
			move = reader.next();
			for(char m : move.toCharArray()) {
				switch(String.valueOf(m)) {
				case "a": board.move(Pieces.left); break;
				case "d": board.move(Pieces.right); break;
				case "w": board.move(Pieces.up); break;
				case "s": board.move(Pieces.down); break;
				default: break;
				}
			}
		}
		System.out.println(board.prettify());
		System.out.println(board.state());
	}
}