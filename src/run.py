from app import create_app
import os

app = create_app()

HOSTNAME = os.environ.get('HOSTNAME', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

if __name__ == '__main__':
    app.run(host=HOSTNAME, port=PORT, debug=True)