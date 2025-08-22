from http import HTTPStatus
import os
import time
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

    data_for_filename = data_out.split("\n")
    if len(data_for_filename) > 1:
        location = data_for_filename[1].split(",")[0].split(".")[0]
        if not cfg.DISABLE_SHORTER_CSV:
            location = location.split("_")[1]
        stock_name = data_for_filename[1].split(",")[1] or "Public"
    else:
        location = f"{round(time.time(), 2)}"
        stock_name = ""
    filename = f"{location}_{stock_name}"

    with open(
        os.path.join(cfg.SOURCE_DIR, cfg.OUTPUT_DIR, f"{filename}.csv"), "w"
    ) as file:
        file.write(data_out)

    return jsonify(), HTTPStatus.OK
