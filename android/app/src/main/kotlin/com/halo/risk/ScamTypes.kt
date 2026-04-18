package com.halo.risk

/**
 * Shared types for the HALO risk pipeline.
 *
 * Mirrors src/halo/models/classifier.py on the Python side so that the
 * ONNX-exported model outputs are interpreted consistently.
 */

enum class ScamCategory(val apiName: String) {
    VOICE_PHISHING("voice_phishing"),
    ROMANCE_SCAM("romance_scam"),
    INVESTMENT_SCAM("investment_scam"),
    LOAN_SCAM("loan_scam"),
    SUBSIDY_SCAM("subsidy_scam"),
    FAMILY_IMPERSONATION("family_impersonation"),
    BENIGN("benign");

    companion object {
        fun fromApi(name: String): ScamCategory =
            values().firstOrNull { it.apiName == name } ?: BENIGN
    }
}

data class ScamResult(
    val category: ScamCategory,
    val riskScore: Int,
    val rationale: String,
    val keySignals: List<String>,
)

enum class InterventionLevel(val threshold: Int) {
    NONE(0),
    SOFT(50),
    MEDIUM(75),
    HARD(90);

    companion object {
        fun forRisk(risk: Int): InterventionLevel = when {
            risk >= HARD.threshold -> HARD
            risk >= MEDIUM.threshold -> MEDIUM
            risk >= SOFT.threshold -> SOFT
            else -> NONE
        }
    }
}
