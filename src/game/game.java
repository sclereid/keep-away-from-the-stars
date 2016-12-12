package game;

import java.awt.*;
import javax.swing.*;

public class game extends JFrame
{
	/**
	 * 
	 */
	
	private static final long serialVersionUID = 1L;
	
	int fps = 50;
	int speed = 120;
	int unit = 40;
	int []sizes;
	boolean []stats;
	
	enum block_status_class {_static, _up, _down, _left, _right};
	block_status_class [][]block_status;
	int [][]status_number;
	
	public static void main(String args[])
	{
		System.out.println("Expend: test");
		System.out.println("Created by virtualize at "+System.currentTimeMillis());
		System.out.println("");
		new game();
	}
	
	clock_class clock = new clock_class(this);
	
	game()
	{
		int tmp;
		sizes = new int[speed];
		stats = new boolean[speed];
		for(int i = 0; i < speed; i++)
		{
			tmp = (int)(Math.cos((double)(i*Math.PI*2/speed))*unit);
			if(tmp>0)
				stats[i] = true;
			else
				stats[i] = false;
			sizes[i] = (int)Math.abs(tmp);
		}
		
		this.setSize(1000, 700);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setResizable(false);
		this.setVisible(true);
		clock.start();
	}
	
	boolean started = false;
	
	String status1 = "started.", status2 = "", status3 = "";
	void showStatus(String msg)
	{
		status3 = status2;
		status2 = status1;
		status1 = msg;
	}
	
	long tmp2 = 0;
	
	
	Image iBuffer;
	Graphics gBuffer;
	boolean start_flag;
	
	public void update(Graphics g)
	{
		paint(g);
	}
	
	void draw()
	{
		if(start_flag)
		{
			iBuffer=createImage(this.getWidth(), this.getHeight()-20);
		    gBuffer=iBuffer.getGraphics();
		    start_flag = false;
		}
		//g.setColor(new Color(255,(int)(128+clock.c%128),0));
		/*
		int tmp = Math.abs((int)(200.0*Math.sin((double)clock.c/speed)));
				
		g.fillRect(50-tmp, 30, 2*tmp, 50);
		g.setColor(new Color(0,(int)(128+clock.c%128),tmp));
		g.fillRect(100, 200-tmp, 600, 2*tmp);
		*/
		gBuffer.clearRect(0, 0, this.getWidth(), this.getHeight()-20);
		int tmp = (int) (clock.c%speed);
		for(int i = 1; i < 10; i++)
		{
			for(int j = 1; j < 10; j++)
			{
				if(stats[tmp])
					gBuffer.setColor(Color.red);
				else
					gBuffer.setColor(Color.black);
				//g.fillRect(50*i-sizes[tmp], 50*j, 2*sizes[tmp], 50+unit/2);
				gBuffer.fillRect(60*i+10-sizes[tmp]/2, 60*j+10, sizes[tmp], unit);
			}
		}
	}
	
	
	public void paint(Graphics g)
	{
		if(!started)
			start_flag = true;
		//g.clearRect(0, 0, this.getWidth(), this.getHeight());
		
		g.drawImage(iBuffer, 0, 20, this);
		
		g.setFont(new Font("dialog", 10, 10));
		g.setXORMode(Color.darkGray);
		g.drawString(status1, 10, this.getHeight()-10);
		g.setXORMode(Color.gray);
		g.drawString(status2, 10, this.getHeight()-25);
		g.setXORMode(Color.lightGray);
		g.drawString(status3, 10, this.getHeight()-40);
		g.setPaintMode();
		started = true;
		//repaint();
	}
	
	class clock_class implements Runnable
	{
		/**clock:
		 * This is the handler of repainting.
		 */
		Thread t;
		long c;
		game ex;
		clock_class(game e)
		{
			ex = e;
			t = new Thread(this);
			c = 0;
		}
		public void run()
		{
			while(true)
			{
				try {
					Thread.sleep(1000/fps);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				c++;
				//System.out.println("clock: "+c);
				if(ex.started)
				{
					ex.draw();
					ex.repaint();
				}
			}
		}
		public void start()
		{
			t.start();
		}
	}
}