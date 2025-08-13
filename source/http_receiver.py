from http import HTTPStatus
import os
from flask import Flask, jsonify, request

import source.config as cfg

app = Flask(__name__)


@app.route("/collage")
def receive_collage():
    print(f"/collage ; method={request.method}")
    return jsonify(), HTTPStatus.NOT_IMPLEMENTED


@app.route("/totals")
def receive_totals():
    print(f"/totals ; method={request.method}")
    return jsonify(), HTTPStatus.NOT_IMPLEMENTED


@app.route("/tsv", methods=["POST", "OPTIONS"])
def receive_tsv():
    print(f"/tsv ; method={request.method}")
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    data = request.data

    data_out = (
        data.decode()
        .replace("\n", " ")
        .replace(",", "\n")
        .replace("\\t", ",")
        .replace("[", "")
        .replace("]", "")
        .replace('"', "")
        .replace("\n ", " ")
    )

    with open(os.path.join(cfg.SOURCE_DIR, cfg.OUTPUT_DIR, "test.csv"), "w") as file:
        file.write(data_out)
    print(data_out)

    return jsonify(), HTTPStatus.OK
