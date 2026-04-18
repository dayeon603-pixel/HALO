package com.halo.intervention

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * SOFT intervention full-screen activity.
 *
 * Triggered when risk >= 50. Shows the rationale from Layer 2 and three
 * options: continue, stop, notify family (Phase 2).
 */
class SoftInterventionActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val rationale = intent.getStringExtra(EXTRA_RATIONALE).orEmpty()
        val signals = intent.getStringArrayListExtra(EXTRA_KEY_SIGNALS).orEmpty()
        setContent {
            SoftInterventionScreen(rationale = rationale, keySignals = signals)
        }
    }

    companion object {
        const val EXTRA_RATIONALE = "extra_rationale"
        const val EXTRA_KEY_SIGNALS = "extra_key_signals"
    }
}

@Composable
private fun SoftInterventionScreen(rationale: String, keySignals: List<String>) {
    Surface(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("잠깐만요, 다시 확인해 주세요")
            Spacer(Modifier.height(16.dp))
            Text(rationale)
            Spacer(Modifier.height(16.dp))
            keySignals.forEach { signal ->
                Text("• $signal")
            }
            Spacer(Modifier.height(32.dp))
            Button(onClick = { /* TODO(M3): record user response */ }) {
                Text("확인했어요")
            }
        }
    }
}
