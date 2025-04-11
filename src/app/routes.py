from flask import Blueprint, request, jsonify, g, render_template_string
from app.decorators import auth_route, require_request_params
from app.db_client import *
from pdf_processor import PdfProcessor
from config import Config
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    html_content = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>PDF Operations</title>
      <style>
        .message { margin-top: 10px; font-weight: bold; }
        .error { color: red; }
        .success { color: green; }
      </style>
    </head>
    <body>
      <!-- File upload form -->
      <h1>Upload a PDF</h1>
      <form onsubmit="submitForm(event, '/upload')" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".pdf">
        <input type="submit" value="Upload">
      </form>
      <div id="upload-message" class="message"></div>
      <hr>
      
      <!-- Delete file form -->
      <h1>Delete a PDF</h1>
      <form onsubmit="submitForm(event, '/delete')" method="post">
        <input type="text" name="filename" placeholder="Enter filename" required>
        <input type="submit" value="Delete">
      </form>
      <div id="delete-message" class="message"></div>
      <hr>
      
      <!-- Search form -->
      <h1>Search</h1>
      <form onsubmit="submitForm(event, '/api/search')" method="post">
        <input type="text" name="query" placeholder="Enter query" required>
        <input type="submit" value="Search">
      </form>
      <div id="search-message" class="message"></div>
      
      <!-- JavaScript to send the form data with the bearer token -->
      <script>
        async function submitForm(event, url) {
          event.preventDefault();  // Prevent normal form submission
          
          const form = event.target;
          const formData = new FormData(form);
          const token = localStorage.getItem('cognitoToken');
          
          // Prepare headers with the Authorization header if token is provided.
          const headers = new Headers();
          if (token) {
            headers.append('Authorization', 'Bearer ' + token);
          }
          
          // Identify the message container based on the form url
          let messageDiv;
          if (url === '/api/upload') {
            messageDiv = document.getElementById('upload-message');
          } else if (url === '/api/delete') {
            messageDiv = document.getElementById('delete-message');
          } else if (url === '/api/search') {
            messageDiv = document.getElementById('search-message');
          } else {
            // Fallback generic message element
            messageDiv = document.getElementById('message');
          }
          
          try {
            const response = await fetch(url, {
              method: 'POST',
              body: formData,
              headers: headers
            });
            
            const result = await response.text();
            if (!response.ok) {
              messageDiv.innerHTML = `<span class="error">Error: ${result}</span>`;
            } else {
              messageDiv.innerHTML = `<span class="success">Response: ${result}</span>`;
            }
          } catch (error) {
            messageDiv.innerHTML = `<span class="error">Error: ${error}</span>`;
          }
        }
      </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

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
    content = pdfProcessor.format_data(id)

    # delete file after processing
    os.remove(file_path)

    logger.info(json.dumps(content, indent=4))

    response = db_upload(id, content)

    return jsonify({"content": response}), 200

@main_bp.route('/delete', methods=['DELETE'])
@auth_route
@require_request_params('filename')
def delete():
    data = request.get_json()
    id = g.user.get('username', 'User')
    filename = data.get('filename')

    response = db_delete(id, filename)

    return jsonify({"content": response}), 200

@main_bp.route('/search', methods=['GET'])
@auth_route
@require_request_params('query')
def search():
    data = request.get_json()
    id = g.user.get('username', 'User')
    query = data.get('query')

    response = db_search(id, query)

    return jsonify({"content": response}), 200
