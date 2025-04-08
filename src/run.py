from app import create_app
import os

app = create_app()

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)