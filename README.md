# Business‑Logic Service

A lightweight micro‑service that ingests PDF files, extracts and chunks their contents (text + tables), then stores the result in a downstream document store for fast semantic search.  
It exposes a small REST/JSON API (and a simple HTML playground) guarded by an external auth service.

---

## Key Features
* **PDF ingestion & OCR** – powered by [unstructured‑io](https://unstructured.io/) and PyMuPDF
* **Sentence segmentation** – spaCy `ro_core_news_lg`
* **Chunking for embeddings** – Hugging Face `sentence‑transformers` tokenizer
* **Endpoints**
    * `POST   /upload`         – upload & index a PDF
    * `DELETE /delete`         – remove a previously indexed file
    * `GET    /search`         – query your indexed content
    * `GET    /get-documents`  – list all files for the authenticated user
* **HTML demo UI** at `/` (drag‑and‑drop a PDF, run queries, etc.)
* **Container‑ready** – single‑stage Dockerfile, multi‑arch image pushed to GHCR
* **CI/CD** – GitHub Actions workflow builds the image on every `main` push and bumps the tag in a separate k8s‑infra repo

---

## Tech Stack

| Layer            | Libraries / Tools                                            |
|------------------|--------------------------------------------------------------|
| Web/API          | **Flask**, `python-dotenv`, `requests`                       |
| Document parsing | **unstructured[pdf]**, **PyMuPDF**, **spaCy**, **bs4**  |
| Embeddings       | **transformers** (MiniLM‑L12‑v2), **tabulate**               |
| Logging          | Python `logging`                                             |
| Runtime / Ops    | **Docker**, GitHub Actions, GHCR, Kubernetes‑ready manifests |

Python 3.12 was used.

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/document-manager-idp/business-logic.git
cd business‑logic
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
# .env (example)
AUTH_HOST=auth-service       # host of auth API
AUTH_PORT=3000
DB_HOST=db-service           # host of db-service API
DB_PORT=5700
PREFIX=/api                  # route prefix for all JSON endpoints
HOSTNAME=0.0.0.0
PORT=5000
```
(You can also pass them on the command line or keep them in an .env file.)


### 3. Run locally
```python
python src/run.py
```

Browse to http://localhost:5000/ to open the demo UI.
### Running with Docker

```bash
# build the image
docker build -t business-logic:latest .

# run it
docker run --env-file .env -p 5000:5000 business-logic:latest
```

The container starts the Flask app on 0.0.0.0:5000.

## Development notes

* Hot‑reload – simply restart the python src/run.py process (Flask debug is on by default).

* Logs – structured files under ./logs/, plus console output.

* Uploads & temp files – saved to uploads/ and purged once the PDF has been processed.

* Extending parsers – add another DocumentProcessor subclass (e.g., WordProcessor) beside pdf_processor.py, then wire it in routes.py.

## CI / CD

The workflow in `.github/workflows/build-and-push.yml`:

1. Builds a multi‑arch image with Docker Buildx.

2. Pushes the image to ghcr.io.

3. Opens the k8s‑infrastructure repo, patches the image tag in the deployment manifest, and pushes to main.