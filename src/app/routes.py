from flask import Blueprint, request, jsonify, g, render_template
from app.decorators import auth_route
from app.db_client import *
from app import metrics
# from pdf_processor import PdfProcessor
from config import Config
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@main_bp.route('/upload', methods=['POST'])
@auth_route
def upload():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    if not file.filename:
        return 'No file selected for uploading', 400

    # temporary save file
    file_path = os.path.join(Config.UPLOAD_DIR, file.filename)
    file.save(file_path)

    id = g.user.get('username', 'User')

    # process and ingest document
    pdfProcessor = PdfProcessor(file_path, "")
    pdfProcessor.process()
    content = pdfProcessor.format_data(index_name=id)

    # delete file after processing
    os.remove(file_path)

    logger.info(json.dumps(content, indent=4))

    response = db_upload(id, content)

    # business metric
    metrics.PDF_UPLOAD_TOTAL.labels(
        status="success" if response else "error"
    ).inc()

    logger.info(json.dumps(response, indent=4))

    return jsonify({"content": response}), 200

@main_bp.route('/delete', methods=['POST'])
@auth_route
def delete():
    id = g.user.get('username', 'User')
    filename = request.form.get('filename')

    if not filename:
        return "No filename provided", 400

    response = db_delete(id, filename)

    metrics.PDF_DELETE_TOTAL.labels(
        status="success" if response else "error"
    ).inc()
    
    logger.info(json.dumps(response, indent=4))

    return jsonify({"content": response}), 200

@main_bp.route('/search', methods=['POST'])
@auth_route
def search():
    id = g.user.get('username', 'User')
    query = request.form.get('query')

    response = db_search(id, query)

    metrics.SEARCH_TOTAL.labels(
        status="success" if response else "error"
    ).inc()

    logger.info(json.dumps(response, indent=4))

    return jsonify({"content": response}), 200

@main_bp.route('/get-documents', methods=['GET'])
@auth_route
def get_documents():
    id = g.user.get('username', 'User')

    response = db_get_documents(id)

    logger.info("Documents fetched:")
    logger.info(json.dumps(response, indent=4))

    if not response:
        return jsonify({"documents": []}), 200

    return jsonify(response), 200

@main_bp.route('/profile', methods=['GET'])
@auth_route
def get_profile():
    id = g.user.get('username', 'User')

    return jsonify({ "username": id }), 200
