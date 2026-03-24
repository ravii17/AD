package com.helloworld.calculatorkiit;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
public class MainActivity extends AppCompatActivity {
TextView display;
String currentInput = &quot;&quot;;
String operator = &quot;&quot;;
int firstNumber = 0;
@Override
protected void onCreate(Bundle savedInstanceState) {
super.onCreate(savedInstanceState);
setContentView(R.layout.activity_main);
display = findViewById(R.id.display);
int[] numberButtons = {
R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3,
R.id.btn4, R.id.btn5, R.id.btn6,
R.id.btn7, R.id.btn8, R.id.btn9
};
for (int id : numberButtons) {
Button btn = findViewById(id);
btn.setOnClickListener(v -&gt; {
currentInput += btn.getText().toString();
display.setText(currentInput);
});
}
findViewById(R.id.btnAdd).setOnClickListener(v -&gt; setOperator(&quot;+&quot;));
findViewById(R.id.btnSub).setOnClickListener(v -&gt; setOperator(&quot;-&quot;));
findViewById(R.id.btnMul).setOnClickListener(v -&gt; setOperator(&quot;*&quot;));
findViewById(R.id.btnDiv).setOnClickListener(v -&gt; setOperator(&quot;/&quot;));

findViewById(R.id.btnClear).setOnClickListener(v -&gt; {
currentInput = &quot;&quot;;
operator = &quot;&quot;;
firstNumber = 0;
display.setText(&quot;0&quot;);
});
findViewById(R.id.btnEqual).setOnClickListener(v -&gt; calculate());
}
private void setOperator(String op) {
if (currentInput.isEmpty()) return;
firstNumber = Integer.parseInt(currentInput);
operator = op;
currentInput = &quot;&quot;;
}
private void calculate() {
if (currentInput.isEmpty() || operator.isEmpty()) return;
int secondNumber = Integer.parseInt(currentInput);
int result = 0;
switch (operator) {
case &quot;+&quot;:
result = firstNumber + secondNumber;
break;
case &quot;-&quot;:
result = firstNumber - secondNumber;
break;
case &quot;*&quot;:
result = firstNumber * secondNumber;
break;
case &quot;/&quot;:
if (secondNumber == 0) {
Toast.makeText(this, &quot;Cannot divide by zero&quot;, Toast.LENGTH_SHORT).show();
return;
}
result = firstNumber / secondNumber;
break;
}
display.setText(String.valueOf(result));
currentInput = String.valueOf(result);
operator = &quot;&quot;;
}
}