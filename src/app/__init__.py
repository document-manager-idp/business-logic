from flask import Flask
import os
from dotenv import load_dotenv
import time
from flask import request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app import metrics

load_dotenv()

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB, adjust as needed

    # Load configuration
    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object('config.Config')

    # Import and register blueprint from routes
    from app.routes import main_bp
    app.register_blueprint(main_bp, url_prefix=os.environ.get('PREFIX'))

    @app.before_request
    def _start_timer():
        request._start_time = time.perf_counter()      # high-res timer

    @app.after_request
    def _record_metrics(response):
        elapsed = time.perf_counter() - getattr(request, "_start_time", 0)
        endpoint = request.endpoint or "unknown"

        metrics.HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint,
            http_status=response.status_code,
        ).inc()

        metrics.HTTP_REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(elapsed)

        return response

    @app.route("/metrics")
    def prometheus_metrics():
        """Prometheus scrape target"""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app