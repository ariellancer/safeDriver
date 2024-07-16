from flask import Flask
from mongoengine import connect

from Server.routes.model import model_bp
from Server.routes.statistics import get_statistics_bp, put_statistics_bp
from routes.user import register_bp
from Server.routes.token import login_bp

# Connect to MongoDB (replace with your own connection string)
connect('mydatabase', host='localhost', port=27017)

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')

app.register_blueprint(get_statistics_bp, url_prefix='/api')
app.register_blueprint(put_statistics_bp, url_prefix='/api')
app.register_blueprint(model_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# import http.server
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
# # class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
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
# # Create the server
# with socketserver.TCPServer(("127.0.0.1", PORT), MyHttpRequestHandler) as httpd:
#     print(f"Server running at http://127.0.0.1:{PORT}/")
#     # Start the server
#     httpd.serve_forever()
