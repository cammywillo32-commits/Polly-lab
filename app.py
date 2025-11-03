import os, time, requests
import streamlit as st

API = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🧪 Polly Lab — Control Room (Render)")

st.caption("Checking backend health…")
ok = False
for _ in range(15):
    try:
        r = requests.get(f"{API}/health", timeout=2)
        if r.ok:
            st.success(f"API health: {r.json()}")
            ok = True
            break
    except Exception:
        time.sleep(1)
if not ok:
    st.warning("Backend API not ready yet. Try again shortly.")

x = st.number_input("x", value=3)
y = st.number_input("y", value=5)

if st.button("Run addition job"):
    try:
        r = requests.post(f"{API}/jobs/add", params={"x": int(x), "y": int(y)}, timeout=8)
        payload = r.json()
        st.session_state["job_id"] = payload.get("job_id")
        if st.session_state["job_id"]:
            st.info(f"Queued job: {st.session_state['job_id']}")
        else:
            st.error(f"Backend response: {payload}")
    except Exception as e:
        st.error(f"Cannot reach API: {e}")

if st.session_state.get("job_id"):
    try:
        res = requests.get(f"{API}/jobs/{st.session_state['job_id']}", timeout=8).json()
        st.write("### Job Result", res)
    except Exception as e:
        st.error(f"Could not fetch result: {e}")

st.caption("Services: Streamlit UI + FastAPI + Celery worker + Managed Redis (Render).")
