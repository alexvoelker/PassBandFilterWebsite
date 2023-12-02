from flask import Flask, render_template, abort, session
from flask import request as flask_request
from flask_session import Session
import requests
import base64
import json
import lzma
import os

app = Flask(__name__)

SESSION_TYPE = 'filesystem'

with open('flask_secret_key', 'r') as FSK:
    app.secret_key = FSK.read()

app.config.from_object(__name__)
Session(app)

API_URL = "https://tech120finalproject-ag4syvzubq-uc.a.run.app"


def change_filter_request(id: str, data: dict) -> bytes:
    out = requests.get(API_URL + f"/v3/fetch?id={id}&filter={data['filterType']}&contrast={data['contrastLevel']}", stream=True)
    data = b''.join(out.iter_content())

    return data

def new_API_request(data: dict) -> str:
    """Performs an API request to the backend. Returns the file name of the created image."""

    # Validate request data input
    if not (isinstance(data["maxCloud"], float)
            and isinstance(data["filterType"], str)
            and isinstance(data["contrastLevel"], float)):
        return ''

    request_data = {
        "Max Cloud Coverage": data['maxCloud'],
        "GeoJson": data['GeoJson'],
    }

    # make request
    out = requests.post(API_URL + "/v3", json=request_data, timeout=None)

    image_id = json.loads(out.content)['id']
    image = change_filter_request(image_id, data)

    # uncompress image
    image_uncompressed = lzma.decompress(image)

    # save to file
    folder = f"image_responses/{id}/"
    file_name = f"{data['filterType']}.webp"

    d = f"static/{folder}"

    if not os.path.exists(d):
        os.makedirs(d)

    with open(d + file_name, "wb+") as binary_file:
        # Write bytes to file
        binary_file.write(image_uncompressed)

    return folder + file_name


def generate_GEO_JSON(x1: float, y1: float, x2: float, y2: float):
    json_data = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {}, "geometry": {"coordinates":
                                                                            [[[y1, x1], [y1, x2], [y2, x2], [y2, x1],
                                                                              [y1, x1]]], "type": "Polygon"}}]}
    return json_data


@app.route('/input-page/', methods=["GET", "POST"])
def input_page():
    if flask_request.method == "POST":
        geo_json_data = generate_GEO_JSON(float(flask_request.form['x1']), float(flask_request.form['y1']),
                                          float(flask_request.form['x2']), float(flask_request.form['y2']))
        data = {'filterType': flask_request.form['filterType'],
                'contrastLevel': float(flask_request.form['contrastLevel']),
                'maxCloud': float(flask_request.form['maxCloud']),
                'GeoJson': geo_json_data}

        # Save this request data as a cookie to be used in the image request later
        session['request_data'] = data
        return render_template('loading.html')
    elif flask_request.method == "GET":
        return render_template('input-page.html')


@app.route('/input-page/complete/')
def load_image():
    data = session.get('request_data')
    image = new_API_request(data)

    if len(image) == 0:  # Handling Invalid Inputs
        abort(400)

    return render_template('response.html', image=image, data=data)


@app.route('/tutorial-page/', methods=["GET"])
def tutorial_page():
    return render_template('tutorial-page.html')


@app.route('/', methods=["GET"])
def home_page():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(error):
    return render_template('400.html'), 400


if __name__ == '__main__':
    port = os.getenv("PORT")
    app.run(debug=False, port=port, host="0.0.0.0")