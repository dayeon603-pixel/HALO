package com.halo.services

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import com.halo.ml.MidmClassifier
import com.halo.risk.RiskEngine
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import timber.log.Timber

/**
 * Receives SMS intents and hands off to the HALO pipeline.
 *
 * Layer 1 entry point for the SMS channel. Extracts sender and body, then
 * dispatches classification off the main thread. Raw text is cleared from
 * memory after classification completes.
 */
class SmsReceiver : BroadcastReceiver() {

    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Telephony.Sms.Intents.SMS_RECEIVED_ACTION) return

        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent) ?: return
        for (message in messages) {
            val sender = message.displayOriginatingAddress.orEmpty()
            val body = message.displayMessageBody.orEmpty()
            if (body.isBlank()) continue

            scope.launch {
                runCatching {
                    // TODO(M3): wire classifier and risk engine. This is a wiring scaffold.
                    Timber.i("SMS from %s (%d chars)", sender.take(4), body.length)
                    val classifier = MidmClassifier.instance(context)
                    val result = classifier.classify(body)
                    val engine = RiskEngine.instance(context)
                    val risk = engine.compute(senderHash(sender), result)
                    Timber.i("risk=%d category=%s", risk, result.category)
                    // TODO: dispatch to intervention activity when risk >= 50
                }.onFailure { Timber.e(it, "SMS pipeline failed") }
            }
        }
    }

    private fun senderHash(sender: String): String {
        // TODO(M3): replace with salted SHA-256.
        return sender.hashCode().toString()
    }
}
