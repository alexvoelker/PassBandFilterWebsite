from flask import Flask, render_template
from flask import request as flreq
import requests
import json

app = Flask(__name__)

image_response_id = 0

API_URL = "https://tech120finalproject-ag4syvzubq-uc.a.run.app"


def perform_API_request(data: dict) -> str:
    """Performs an API request to the backend. Returns the file name of the image created. """
    global image_response_id
    file = open("geo.json")
    geo_file_json = json.load(file)

    request_data = {
        "Max Cloud Coverage": data['maxCloud'],
        "GeoJson": geo_file_json,
        "Filter": data['filterType'],
        "Boost Contrast": data['contrastLevel'],
    }

    # TODO Add the ability to set specific geographic coordinates via geojson
    file_name = f"image_responses/image_{image_response_id}.jpg"
    image_response_id += 1

    out = requests.post(API_URL, json=request_data, timeout=None)

    with open(f"static/{file_name}", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(out.content)

    return file_name


@app.route('/', methods=["GET", "POST"])
def home_page():
    if flreq.method == "POST":
        data = {'filterType': flreq.form['filterType'],
                'contrastLevel': float(flreq.form['contrastLevel']),
                'maxCloud': float(flreq.form['maxCloud'])}
        image = perform_API_request(data)
        # TODO get website to display full image
        return render_template('response.html', image=image)
    elif flreq.method == "GET":
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False)
