package com.halo

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import timber.log.Timber

/**
 * HALO Application entry point.
 *
 * Responsibilities:
 * - Initialize Timber logging.
 * - Register notification channels.
 * - Hold DI container (to be added when Hilt or Koin is introduced).
 */
class HaloApp : Application() {

    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) {
            Timber.plant(Timber.DebugTree())
        }
        registerNotificationChannels()
    }

    private fun registerNotificationChannels() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        val foreground = NotificationChannel(
            CHANNEL_ID_FOREGROUND,
            "HALO 서비스 상태",
            NotificationManager.IMPORTANCE_LOW,
        ).apply {
            description = "HALO가 백그라운드에서 동작 중임을 알립니다."
        }

        val alerts = NotificationChannel(
            CHANNEL_ID_ALERTS,
            "HALO 사기 경고",
            NotificationManager.IMPORTANCE_HIGH,
        ).apply {
            description = "의심스러운 메시지나 통화가 감지되었을 때 표시됩니다."
        }

        nm.createNotificationChannel(foreground)
        nm.createNotificationChannel(alerts)
    }

    companion object {
        const val CHANNEL_ID_FOREGROUND = "halo_foreground"
        const val CHANNEL_ID_ALERTS = "halo_alerts"
    }
}
