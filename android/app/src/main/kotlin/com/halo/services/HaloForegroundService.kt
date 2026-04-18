package com.halo.services

import android.app.Notification
import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.halo.HaloApp
import com.halo.R
import timber.log.Timber

/**
 * HALO background service keeping the classifier warm and coordinating
 * Layer 1 through Layer 4 pipeline.
 *
 * Uses foregroundServiceType=dataSync so the service can survive Android
 * Doze and App Standby modes.
 */
class HaloForegroundService : Service() {

    override fun onCreate() {
        super.onCreate()
        startForeground(NOTIFICATION_ID, buildNotification())
        Timber.i("HaloForegroundService started")
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int = START_STICKY

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(): Notification =
        NotificationCompat.Builder(this, HaloApp.CHANNEL_ID_FOREGROUND)
            .setContentTitle("HALO가 보호 중입니다")
            .setContentText("의심스러운 메시지를 실시간으로 감지합니다")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

    companion object {
        const val NOTIFICATION_ID = 1001
    }
}
