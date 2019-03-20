package main.penguindrop;

import java.util.ArrayList;

public class Home {

	public ArrayList<Penguin> penguins;
	public ArrayList<Cannonball> cannonballs;
	public int score;
	public float[] screen;
	
	private Ice ice;
	private float prob, increment;
	private int count, maxCount;
	
	public Home(Ice ice) {
		this.ice = ice; this.screen = ice.screen;
		
        //Starting probability of new penguins and how much to increase it by.
        this.prob = 0.01f; this.increment = 0.0025f;
        
        //Starting count and at what count to increment the probability.
        this.count = 0; this.maxCount = 1000;
		
        this.cannonballs = new ArrayList<Cannonball>();
		this.penguins = new ArrayList<Penguin>();
	}
	
	private void updateCannonballs() {
		int i = 0;
		while (i < this.cannonballs.size()) {
			this.cannonballs.get(i).update();
			if (this.cannonballs.get(i).offScreen()) {
				this.cannonballs.remove(i);
			} else {
				i++;
			}
		}
	}
	
	private void updatePenguins() {
		int[] iceRect = this.ice.getRectangularDefinition();
        int i = 0;
        while (i < this.penguins.size()) {
            Penguin p = this.penguins.get(i);
            p.update();
            int[] pRect = p.getRectangularDefinition();
            //if it's on the ice, add it to this.ice.
            if (Global.overlapping(pRect, iceRect)) {
                this.ice.addPenguin(p);
                this.penguins.remove(i);
                i--;
            } else if (p.offScreen()) {
                this.penguins.remove(i);
                i--;
            } else {
            	for (int n=0;n<this.cannonballs.size();n++) {
            		if (Global.overlapping(pRect, this.cannonballs.get(n).getRectangularDefinition())) {
            			this.score++;
            			this.cannonballs.remove(n);
            			this.penguins.remove(i);
            			i--;
            			break; //Only one cannonball is destroyed per penguin.
            		}
            	}
            }
            i++;
        }
	}
	
	public void update() {
		this.updateCannonballs();
		this.updatePenguins();

        // Update game difficulty and/or add penguins.
        
        this.count++;
        
        if (Math.random() <= this.prob) {
            this.penguins.add(new Penguin(this.screen));
        }
            
        if (this.count >= this.maxCount) {
            if (this.prob + this.increment < 1) {
                this.prob += this.increment;
            } else {
                this.prob = 1f;
            }
            this.count = 0;
        }
	}
	
	public void addCannonball(Cannonball cannonball) {
		this.cannonballs.add(cannonball);
	}
}
