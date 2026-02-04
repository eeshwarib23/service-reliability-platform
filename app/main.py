from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from app.simulator import SimConfig, handle_request
from app.store import MetricsStore

app = FastAPI(title="Service Reliability Platform (Mini)")

# In-memory metrics store
store = MetricsStore(maxlen=5000)

# Simulation config (runtime-tunable)
cfg = SimConfig()

# -----------------------
# Prometheus Metrics
# -----------------------
REQ_TOTAL = Counter(
    "srp_requests_total",
    "Total requests processed",
    ["result"]
)

LATENCY = Histogram(
    "srp_request_latency_ms",
    "Request latency in milliseconds",
    buckets=(50, 80, 120, 200, 350, 500, 800, 1200, 2000)
)

READY = True


# -----------------------
# Web Dashboard
# -----------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()


# -----------------------
# Health & Readiness
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"ready": READY}


# -----------------------
# API Endpoints
# -----------------------
@app.post("/api/request")
def api_request():
    ok, latency_ms = handle_request(cfg)

    store.add(ok=ok, latency_ms=latency_ms)
    LATENCY.observe(latency_ms)
    REQ_TOTAL.labels(result="success" if ok else "error").inc()

    if ok:
        return {"ok": True, "latency_ms": round(latency_ms, 2)}

    return JSONResponse(
        status_code=500,
        content={"ok": False, "latency_ms": round(latency_ms, 2)}
    )


@app.get("/api/summary")
def api_summary(window_sec: int = 300):
    return store.snapshot(window_sec=window_sec)


@app.post("/api/config")
def update_config(
    base_latency_ms: int = 80,
    jitter_ms: int = 120,
    error_rate: float = 0.05
):
    cfg.base_latency_ms = max(0, int(base_latency_ms))
    cfg.jitter_ms = max(0, int(jitter_ms))
    cfg.error_rate = min(max(float(error_rate), 0.0), 1.0)

    return {
        "base_latency_ms": cfg.base_latency_ms,
        "jitter_ms": cfg.jitter_ms,
        "error_rate": cfg.error_rate
    }


# -----------------------
# Prometheus Metrics Endpoint
# -----------------------
@app.get("/metrics")
def metrics():
    data = generate_latest()
    return PlainTextResponse(
        data.decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST
    )

