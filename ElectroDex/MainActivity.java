package com.example.electrodex;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

private AutoCompleteTextView searchInput;
private Button searchButton;
private ImageView componentImage;
private TextView componentName;
private TextView componentDescription;
private ProgressBar progressBar;

private RequestQueue requestQueue;

private static final String[] SUGGESTIONS = new String[]{

"Resistor", "Capacitor", "Diode", "Transistor", "MOSFET", "LED",

"Relay", "Inductor", "Integrated circuit", "Sensor"
};

@Override
protected void onCreate(Bundle savedInstanceState) {
super.onCreate(savedInstanceState);
EdgeToEdge.enable(this);
setContentView(R.layout.activity_main);

ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main),
(v, insets) -> {

Insets systemBars =

insets.getInsets(WindowInsetsCompat.Type.systemBars());

v.setPadding(systemBars.left, systemBars.top, systemBars.right,

systemBars.bottom);
return insets;
});

searchInput = findViewById(R.id.search_input);
searchButton = findViewById(R.id.search_button);
componentImage = findViewById(R.id.component_image);
componentName = findViewById(R.id.component_name);
componentDescription = findViewById(R.id.component_description);
progressBar = findViewById(R.id.progress_bar);

requestQueue = Volley.newRequestQueue(this);

// Set up AutoCompleteTextView

ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
android.R.layout.simple_dropdown_item_1line, SUGGESTIONS);
searchInput.setAdapter(adapter);

searchButton.setOnClickListener(v -> performSearch());
}

private void performSearch() {
String query = searchInput.getText().toString().trim();
if (query.isEmpty()) {
Toast.makeText(this, "Please enter a component name",

Toast.LENGTH_SHORT).show();

return;
}

// Hide previous results and show progress
clearDisplay();
progressBar.setVisibility(View.VISIBLE);

// Format query for Wikipedia API
String formattedQuery = query.replace(" ", "_");
String url = "https://en.wikipedia.org/api/rest_v1/page/summary/" +
formattedQuery;

JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET,
url, null,

response -> {
progressBar.setVisibility(View.GONE);
try {
String title = response.getString("title");

String description = response.getString("extract");

String imageUrl = null;
if (response.has("thumbnail")) {
JSONObject thumbnail =

response.getJSONObject("thumbnail");

if (thumbnail.has("source")) {
imageUrl = thumbnail.getString("source");
}
}

displayComponent(title, description, imageUrl);

} catch (JSONException e) {
Log.e("MainActivity", "JSON Parsing error", e);
Toast.makeText(MainActivity.this, "Error parsing

response", Toast.LENGTH_SHORT).show();

}
},
error -> {
progressBar.setVisibility(View.GONE);
Toast.makeText(MainActivity.this, "Component not found",

Toast.LENGTH_SHORT).show();

});

requestQueue.add(request);
}

private void displayComponent(String title, String description, String
imageUrl) {

componentName.setText(title);
componentDescription.setText(description);

if (imageUrl != null && !imageUrl.isEmpty()) {
Picasso.get().load(imageUrl)
.placeholder(android.R.drawable.ic_menu_gallery)
.error(android.R.drawable.ic_menu_report_image)
.into(componentImage);

} else {

componentImage.setImageResource(android.R.drawable.ic_menu_gallery);
}

componentName.setVisibility(View.VISIBLE);
componentDescription.setVisibility(View.VISIBLE);
componentImage.setVisibility(View.VISIBLE);
}

private void clearDisplay() {
componentName.setVisibility(View.GONE);
componentDescription.setVisibility(View.GONE);
componentImage.setVisibility(View.GONE);

componentName.setText("");
componentDescription.setText("");
componentImage.setImageDrawable(null);
}
}