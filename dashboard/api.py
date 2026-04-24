from flask import Blueprint, jsonify, request
import pandas as pd

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health")
def health():
    return jsonify({"status": "ok"})

