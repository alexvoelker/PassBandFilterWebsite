from flask import Flask, render_template, abort
from flask import request as flask_request
import requests
import json

app = Flask(__name__)

API_URL = "https://tech120finalproject-ag4syvzubq-uc.a.run.app"


def perform_API_request(image_id: int, data: dict) -> str:
    """Performs an API request to the backend. Returns the file name of the created image."""
    file = open("geo.json")
    geo_file_json = json.load(file)

    request_data = {
        "Max Cloud Coverage": data['maxCloud'],
        "GeoJson": geo_file_json,
        "Filter": data['filterType'],
        "Boost Contrast": data['contrastLevel'],
    }

    # Validate request data input
    if not (isinstance(request_data["Max Cloud Coverage"], float)
            and isinstance(request_data["GeoJson"], dict)
            and isinstance(request_data["Filter"], str)
            and isinstance(request_data["Boost Contrast"], float)):
        return ''

    # TODO Add the ability to set specific geographic coordinates via geojson
    file_name = f"image_responses/image_{image_id}.jpg"

    out = requests.post(API_URL, json=request_data, timeout=None)

    with open(f"static/{file_name}", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(out.content)

    return file_name


@app.route('/', methods=["GET", "POST"])
def home_page():
    if flask_request.method == "POST":
        data = {'filterType': flask_request.form['filterType'],
                'contrastLevel': float(flask_request.form['contrastLevel']),
                'maxCloud': float(flask_request.form['maxCloud'])}

        # get the unique counter for the image file name
        with open('image_count', 'r') as image_count_file:
            image_count_raw = image_count_file.read()
            if image_count_raw == '':
                image_response_id = 0
            else:
                image_response_id = int(image_count_raw)
            image = perform_API_request(image_response_id, data)

            if len(image) == 0:  # Handling Invalid Inputs
                abort(400)

        # Write the updated image file counter to the file
        with open('image_count', 'w') as image_count_file:
            image_count_file.write(str(image_response_id + 1))

        # TODO get website to display full image
        return render_template('response.html', image=image)
    elif flask_request.method == "GET":
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(error):
    return render_template('400.html'), 400


if __name__ == '__main__':
    app.run(debug=False)
