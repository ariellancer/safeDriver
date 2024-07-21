import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from flask import Flask
from mongoengine import connect

from routes.model import model_bp
from routes.statistics import get_statistics_bp, put_statistics_bp
from routes.user import register_bp
from routes.token import login_bp

# from controllers.user import add_user_controller
# Connect to MongoDB (replace with your own connection string)
connect('mydatabase', host='localhost', port=27017)

app = Flask(__name__)
# Register the blueprints

# app.route('/api/Register', methods=['post'])(add_user_controller)


app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(get_statistics_bp, url_prefix='/api')
app.register_blueprint(put_statistics_bp, url_prefix='/api')
app.register_blueprint(model_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# import http.Server
# import socketserver
# from flask import Flask
# from mongoengine import connect
#
# from Server.routes.token import login_bp
# from routes.user import register_bp
#
# # Define the port number
# PORT = 5000
#
# # Connect to MongoDB (replace with your own connection string)
# connect('mydatabase', host='localhost', port=27017)
#
# app = Flask(__name__)
#
# # Register the blueprint
# app.register_blueprint(register_bp, url_prefix='/api')
# app.register_blueprint(login_bp, url_prefix='/api')
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
# # Create a request handler
# # class MyHttpRequestHandler(http.Server.SimpleHTTPRequestHandler):
# #     def do_GET(self):
# #         # Set the response status code and headers
# #         self.send_response(200)
# #         self.send_header("Content-type", "text/plain")
# #         self.end_headers()
# #
# #         # Send the response body
# #         self.wfile.write(b"Hello, World!\n")
#
#
# # Create the Server
# with socketserver.TCPServer(("127.0.0.1", PORT), MyHttpRequestHandler) as httpd:
#     print(f"Server running at http://127.0.0.1:{PORT}/")
#     # Start the Server
#     httpd.serve_forever()
