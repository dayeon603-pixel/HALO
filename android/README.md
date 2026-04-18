# HALO Android App

Y1 scope: SMS channel + Mi:dm 2.0 Mini on-device classifier + Soft
intervention. iOS is Phase 2.

## Prerequisites

- Android Studio Hedgehog (2023.1.1) or later.
- JDK 17.
- Android SDK Platform 34, Build Tools 34.0.0.
- NDK 26.1.10909125 (for ONNX Runtime native acceleration).
- Target device: Android 8.0 (API 26) minimum, Android 14 (API 34) target.

## Build

```bash
cd android
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

## Module structure

```
android/app/src/main/kotlin/com/halo/
├── HaloApp.kt                    # Application class, singletons
├── MainActivity.kt               # Compose host
├── services/
│   ├── SmsReceiver.kt            # BroadcastReceiver for SMS_RECEIVED
│   └── HaloForegroundService.kt  # Pipeline orchestrator
├── ml/
│   ├── MidmClassifier.kt         # ONNX Runtime + LoRA adapter
│   └── WhisperStt.kt             # Phase 2
├── risk/
│   ├── RiskEngine.kt             # Combines Layer 2 + Layer 3
│   └── MetacogProbe.kt           # Probe UI trigger
├── intervention/
│   ├── SoftInterventionActivity.kt  # Y1 only
│   ├── FamilyConnect.kt          # Phase 2
│   └── HardLock.kt               # Phase 2
├── ui/
│   └── MainScreen.kt             # Settings, history, status
└── data/
    ├── EventDao.kt               # Room DAO
    └── HaloDatabase.kt           # Room database
```

## Permissions

See AndroidManifest.xml. Minimum required for Y1:
- `READ_SMS`
- `RECEIVE_SMS`
- `POST_NOTIFICATIONS`
- `FOREGROUND_SERVICE`
- `INTERNET`

Phase 2 adds: `RECORD_AUDIO`, `BIND_ACCESSIBILITY_SERVICE`,
`FOREGROUND_SERVICE_MEDIA_PROJECTION`.

## Model deployment

1. Download Mi:dm 2.0 Mini ONNX from internal CDN on first run (~1.2 GB).
2. Cache in `files/models/midm_mini_int4.onnx`.
3. Apply LoRA adapter from `assets/lora_adapter_v0/adapter.safetensors`.
4. Delta adapter updates via OTA weekly (~10 MB each).
