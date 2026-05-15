import plotly.graph_objs as go
from flask import Flask
from api import api
from dashServer import createDash

from flask_cors import CORS
server = Flask(__name__)
CORS(server)
server.register_blueprint(api)
dash_app = createDash(server)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8050, debug=True)
