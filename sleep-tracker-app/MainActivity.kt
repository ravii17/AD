package com.example.sleeptrackerapp
import android.app.AlertDialog
import android.app.TimePickerDialog
import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.os.SystemClock
import android.widget.Button
import android.widget.Chronometer
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.edit
class MainActivity : AppCompatActivity() {
private lateinit var chronometer: Chronometer
private lateinit var tvSleepStage: TextView
private lateinit var tvGoal: TextView
private lateinit var tvSummary: TextView
private lateinit var btnStart: Button
private lateinit var btnStop: Button
private lateinit var btnReset: Button
private lateinit var btnSettings: Button
private var isTracking = false
private var sleepGoalMs: Long = 8 * 3600 * 1000L // Default 8 hours
private lateinit var sharedPrefs: SharedPreferences

override fun onCreate(savedInstanceState: Bundle?) {
super.onCreate(savedInstanceState)
setContentView(R.layout.activity_main)
sharedPrefs = getSharedPreferences("SleepTrackerPrefs", MODE_PRIVATE)
// Initialize UI components
chronometer = findViewById(R.id.chronometer)
tvSleepStage = findViewById(R.id.tvSleepStage)
tvGoal = findViewById(R.id.tvGoal)
tvSummary = findViewById(R.id.tvSummary)
btnStart = findViewById(R.id.btnStart)
btnStop = findViewById(R.id.btnStop)
btnReset = findViewById(R.id.btnReset)
btnSettings = findViewById(R.id.btnSettings)
loadData()
btnStart.setOnClickListener {
startTracking()
}
btnStop.setOnClickListener {
stopTracking()
}
btnReset.setOnClickListener {
resetTracking()
}
btnSettings.setOnClickListener {
openGoalSettings()
}
chronometer.setOnChronometerTickListener { chrono ->
val elapsedMs = SystemClock.elapsedRealtime() - chrono.base
// Deep sleep after 1.5 hours (1.5 * 3600 * 1000 = 5400000 ms)
if (elapsedMs >= 5400000L) {
tvSleepStage.text = "Deep Sleep"
} else {
tvSleepStage.text = "Light Sleep"
}
}
}
private fun startTracking() {
if (isTracking) return
chronometer.base = SystemClock.elapsedRealtime()
chronometer.start()
isTracking = true

btnStart.isEnabled = false
btnStop.isEnabled = true
tvSleepStage.text = "Light Sleep"
}
private fun stopTracking() {
if (!isTracking) {
Toast.makeText(this, "Tracking hasn't started yet!",

Toast.LENGTH_SHORT).show()

return
}
chronometer.stop()
isTracking = false
btnStart.isEnabled = true
btnStop.isEnabled = false
tvSleepStage.text = "Awake"
val elapsedMs = SystemClock.elapsedRealtime() - chronometer.base
saveSleepSession(elapsedMs)
showSleepSummary(elapsedMs)
}
private fun resetTracking() {
chronometer.stop()
chronometer.base = SystemClock.elapsedRealtime()
isTracking = false
btnStart.isEnabled = true
btnStop.isEnabled = false
tvSleepStage.text = "Not Sleeping"
Toast.makeText(this, "Session reset", Toast.LENGTH_SHORT).show()
}
private fun openGoalSettings() {
// Use TimePickerDialog to set duration goal (e.g. 8 hours 0 minutes)
val currentGoalHours = (sleepGoalMs / 3600000).toInt()
val currentGoalMinutes = ((sleepGoalMs % 3600000) / 60000).toInt()
val timePicker = TimePickerDialog(this, { _, hourOfDay, minute ->
if (hourOfDay == 0 && minute == 0) {
Toast.makeText(this, "Enter valid bedtime",

Toast.LENGTH_SHORT).show()
} else {
sleepGoalMs = (hourOfDay * 3600 + minute * 60) * 1000L
sharedPrefs.edit {
putLong("sleepGoalMs", sleepGoalMs)
}
updateGoalUI()
}
}, currentGoalHours, currentGoalMinutes, true)

timePicker.setTitle("Set Sleep Goal Duration")
timePicker.show()
}
private fun saveSleepSession(elapsedMs: Long) {
val totalSleepMs = sharedPrefs.getLong("totalSleepMs", 0L) + elapsedMs
val sleepSessions = sharedPrefs.getInt("sleepSessions", 0) + 1
sharedPrefs.edit {
putLong("totalSleepMs", totalSleepMs)
putInt("sleepSessions", sleepSessions)
}
updateSummaryUI(totalSleepMs, sleepSessions)
}
private fun showSleepSummary(elapsedMs: Long) {
val diff = elapsedMs - sleepGoalMs
val message = if (diff < 0) {
val lessMs = -diff
"You slept ${formatTime(lessMs)} less than your goal."
} else {
"Great job! You met your sleep goal."
}
AlertDialog.Builder(this)
.setTitle("Sleep Session Ended")
.setMessage("Duration: ${formatTime(elapsedMs)}\n$message")
.setPositiveButton("OK", null)
.show()
}
private fun loadData() {
sleepGoalMs = sharedPrefs.getLong("sleepGoalMs", 8 * 3600 * 1000L)
val totalSleepMs = sharedPrefs.getLong("totalSleepMs", 0L)
val sleepSessions = sharedPrefs.getInt("sleepSessions", 0)
updateGoalUI()
updateSummaryUI(totalSleepMs, sleepSessions)
}
private fun updateGoalUI() {
val hours = sleepGoalMs / 3600000
val minutes = (sleepGoalMs % 3600000) / 60000
tvGoal.text = "Bedtime Goal: ${hours}h ${minutes}m"
}
private fun updateSummaryUI(totalSleepMs: Long, sleepSessions: Int) {
if (sleepSessions == 0) {
tvSummary.text = "Avg. Sleep: 0h 0m"
return
}
val avgSleepMs = totalSleepMs / sleepSessions

tvSummary.text = "Avg. Sleep: ${formatTime(avgSleepMs)}"
}
private fun formatTime(ms: Long): String {
val hours = ms / 3600000
val minutes = (ms % 3600000) / 60000
return "${hours}h ${minutes}m"
}
}