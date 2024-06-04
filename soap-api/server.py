from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Define a simple SOAP service
class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Create a Spyne application with the HelloWorldService
soap_app = Application([HelloWorldService], 'example.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# Wrap the Spyne application in a WSGI application
wsgi_app = WsgiApplication(soap_app)

# Create a Flask application
flask_app = Flask(__name__)

# Mount the SOAP service at the /soap endpoint
flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
    '/soap': wsgi_app
})

# Define a simple route for the home page
@flask_app.route('/')
def index():
    return 'Welcome to the SOAP API Server!'

# Run the Flask development server
if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, flask_app)
