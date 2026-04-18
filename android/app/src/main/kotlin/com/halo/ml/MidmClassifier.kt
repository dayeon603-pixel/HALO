package com.halo.ml

import android.content.Context
import com.halo.risk.ScamCategory
import com.halo.risk.ScamResult
import java.util.concurrent.atomic.AtomicReference

/**
 * On-device Layer 2 classifier wrapping ONNX Runtime Mobile with KT Mi:dm
 * 2.0 Mini + LoRA adapter.
 *
 * Y1: stub returns benign with risk 0 for wiring tests. M2 replaces with
 * real ONNX session.
 */
class MidmClassifier private constructor(context: Context) {

    // TODO(M2): load ONNX session with QNN or NNAPI delegate.

    fun classify(text: String): ScamResult {
        // TODO(M2): tokenize with Mi:dm tokenizer, run ONNX inference, parse JSON.
        return ScamResult(
            category = ScamCategory.BENIGN,
            riskScore = 0,
            rationale = "classifier not loaded",
            keySignals = emptyList(),
        )
    }

    companion object {
        private val REF = AtomicReference<MidmClassifier?>(null)

        fun instance(context: Context): MidmClassifier {
            REF.get()?.let { return it }
            val created = MidmClassifier(context.applicationContext)
            return if (REF.compareAndSet(null, created)) created else REF.get()!!
        }
    }
}
