package main.distancetogreen;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;
import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;

public class MainActivity extends Activity {
	
	public static float PIN_HEIGHT = 7 / 3f; // In yards.
	public static float HOLD_DISTANCE = 18 / 36f; //In yards.
	
	public View myView;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		createAd();		
		
	    myView = new MyView(this);
	    RelativeLayout layout = (RelativeLayout)findViewById(R.id.parent);
	    layout.addView(myView);
	    
	    //EditText stuff....
	    EditText pinHeight = (EditText)findViewById(R.id.pinHeight);
	    //Convert yards to feet for display.
	    pinHeight.setText(Float.toString(PIN_HEIGHT*3f));
	    pinHeight.setOnEditorActionListener(new OnEditorActionListener() {
	        @Override
	        public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                try {
                	//Convert feet to yards.
                	PIN_HEIGHT = Math.abs(Float.parseFloat(v.getText().toString()) / 3f);
                	myView.invalidate();
                } catch (NumberFormatException e) {}
	            return true;
	        }
	    });
	    EditText holdDistance = (EditText)findViewById(R.id.holdDistance);
	    //Convert yards to inches for display.
	    holdDistance.setText(Float.toString(HOLD_DISTANCE*36f));
	    holdDistance.setOnEditorActionListener(new OnEditorActionListener() {
	        @Override
	        public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                try {
                	//Convert inches to yards.
                	HOLD_DISTANCE = Math.abs(Float.parseFloat(v.getText().toString()) / 36f);
                	myView.invalidate();
                } catch (NumberFormatException e) {}
	            return true;
	        }
	    });
	    findViewById(R.id.text).bringToFront(); //Text contains both above EditText's.
	    
	    View v = findViewById(R.id.instructions); //Button.
	    v.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				AlertDialog.Builder builder = new AlertDialog.Builder(v.getContext());
				builder.setMessage(R.string.full_instructions);
				builder.setCancelable(true);	
				AlertDialog alert = builder.create();
				alert.show();	
			}
		});
	    v.bringToFront();
	}
	
	private void createAd() {
	    AdView adView = (AdView)findViewById(R.id.adView);
	    AdRequest adRequest = new AdRequest.Builder()
	        .build();
	    adView.loadAd(adRequest);
	}
}
