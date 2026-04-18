package com.halo.risk

import android.content.Context
import java.util.concurrent.atomic.AtomicReference

/**
 * Risk scoring engine mirroring src/halo/models/risk.py.
 *
 * Combines Layer 2 pattern score with Layer 3 metacognition signals into a
 * single 0..100 risk value.
 */
class RiskEngine private constructor(
    context: Context,
    private val weights: RiskWeights = RiskWeights(),
) {
    // TODO(M3): inject real metacognition probe state.

    fun compute(senderHash: String, result: ScamResult): Int {
        val overconfidence = 0.0
        val anomaly = 0.0
        val combined = weights.alpha * result.riskScore +
            weights.beta * overconfidence * 100.0 +
            weights.gamma * anomaly * 100.0
        return combined.toInt().coerceIn(0, 100)
    }

    companion object {
        private val REF = AtomicReference<RiskEngine?>(null)

        fun instance(context: Context): RiskEngine {
            REF.get()?.let { return it }
            val created = RiskEngine(context.applicationContext)
            return if (REF.compareAndSet(null, created)) created else REF.get()!!
        }
    }
}

data class RiskWeights(
    val alpha: Double = 0.5,
    val beta: Double = 0.3,
    val gamma: Double = 0.2,
)
