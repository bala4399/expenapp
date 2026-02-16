import json
from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route('/mock-fx-api', methods=['GET'])
def mock_fx_api():
    mock_fx_data = {
        "date": "20250701",
        "rates": {
            "USDEUR": 0.92,
            "GBPEUR": 1.17,
            "JPYEUR": 0.0064,
            "INREUR": 0.011,
            "AUDEUR": 0.61,
            "CADEUR": 0.69,
            "CHFEUR": 1.05,
            "CNYEUR": 0.13,
            "HKDEUR": 0.12,
            "SGDEUR": 0.68,
            "NZDEUR": 0.56,
            "SEKEUR": 0.087,
            "NOKEUR": 0.086,
            "PLNEUR": 0.23,
            "CZKEUR": 0.042,
            "HUFEUR": 0.0027,
            "RONEUR": 0.20,
            "TRYEUR": 0.035,
            "ZAREUR": 0.049,
            "BRLEUR": 0.19
        }
    }
    return jsonify(mock_fx_data)
    # return jsonify({"error": "Invalid request method"}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)