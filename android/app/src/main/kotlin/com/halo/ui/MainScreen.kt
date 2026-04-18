package com.halo.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Main settings and status screen.
 *
 * Y1 content:
 * - Status: HALO is protecting (service running indicator).
 * - History: recent classifications (last 7 days).
 * - Settings: opt-in toggles per channel.
 */
@Composable
fun MainScreen() {
    Surface(modifier = Modifier.fillMaxSize()) {
        Scaffold { padding ->
            Column(modifier = Modifier.padding(padding).padding(24.dp)) {
                Text("HALO")
                Text("어르신을 위한 AI 사기 방어")
                // TODO(M3): wire status indicator, history, settings.
            }
        }
    }
}
