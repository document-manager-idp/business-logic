from prometheus_client import Counter, Histogram

# ── generic HTTP stats ────────────────────────────────────────────────────────
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

HTTP_REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

# ── business specific counters ────────────────────────────────────────────────
PDF_UPLOAD_TOTAL     = Counter("pdf_upload_total",     "Number of PDF uploads",     ["status"])
PDF_DELETE_TOTAL     = Counter("pdf_delete_total",     "Number of PDF deletions",  ["status"])
SEARCH_TOTAL         = Counter("search_total",         "Number of /search calls",  ["status"])
CHUNKS_CREATED_TOTAL = Counter("chunks_created_total", "Chunks produced from docs")