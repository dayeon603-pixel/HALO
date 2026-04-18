import { useState } from "react";

/**
 * HALO Family Companion Web root.
 *
 * Phase 2 entry point. Y1 scope is Android Soft intervention only.
 * This app enables Medium and Hard level interventions by connecting
 * family members to the protected HALO user.
 */
function App() {
  const [connected, setConnected] = useState(false);

  return (
    <main style={{ maxWidth: 640, margin: "40px auto", padding: 24, fontFamily: "system-ui" }}>
      <h1>HALO 가족 알림</h1>
      <p>보호 중인 가족의 실시간 안전 알림을 받을 수 있습니다.</p>
      <button onClick={() => setConnected(true)} disabled={connected}>
        {connected ? "연결됨" : "가족 연결 시작"}
      </button>
      <section style={{ marginTop: 32 }}>
        <h2>최근 알림</h2>
        <p>아직 알림이 없습니다.</p>
      </section>
    </main>
  );
}

export default App;
