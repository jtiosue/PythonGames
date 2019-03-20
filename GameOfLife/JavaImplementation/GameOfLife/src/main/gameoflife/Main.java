package main.gameoflife;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionListener;
import java.util.Timer;
import java.util.TimerTask;
import javax.swing.JFrame;

public class Main {
	
	private Timer timer;
	private TimerTask task;
	private Home home;
	private boolean playing;
	
	public Main(JFrame frame) {
		this.home = new Home(frame);
		this.playing = false;
		
		frame.addKeyListener(new KeyListener() {
			public void keyTyped(KeyEvent e) { }
			public void keyReleased(KeyEvent e) { }
			public void keyPressed(KeyEvent e) {
				int key = e.getKeyCode();
				if (key == KeyEvent.VK_ENTER) {
					if (playing) {
						playing = false;
						cancelTimer();
					}
					home.init();
				} else if (key == KeyEvent.VK_SPACE) {
					if (playing) {
						playing = false;
						cancelTimer();
					} else {
						playing = true;
						setTimer();
					}
				}
			}		
		});
		frame.addMouseMotionListener(new MouseMotionListener() {
			public void mouseMoved(MouseEvent me) {
			}
			public void mouseDragged(MouseEvent me) {
				int[] position = {me.getX(), me.getY()};
				home.draw(position);
			}
		});
	}
	
	public void setTimer() {
		this.timer = new Timer();
		
		this.task = new TimerTask() {
			@Override
			public void run() {
				home.update();
			}
		};
		
		this.timer.scheduleAtFixedRate(this.task, Global.speed, Global.speed);
	}
	
	public void cancelTimer() {
		this.task.cancel();
		this.timer.cancel();
		this.timer.purge();
	}
	
	public static void main(String[] args) {
		JFrame frame = new JFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//		frame.setResizable(false);
		frame.setSize(Global.screen[0], Global.screen[1]);
//		frame.setExtendedState(java.awt.Frame.MAXIMIZED_BOTH);
		frame.setLocationRelativeTo(null);
		frame.setVisible(true);
		
		new Main(frame);
	}
}