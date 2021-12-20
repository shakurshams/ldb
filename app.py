import os
from flask import request, abort
from werkzeug.utils import secure_filename
from data_app import parser, tasks
from data_app.config import service, logger


@service.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files["csv_data"]
        filename = secure_filename(file.filename)
        file.save(filename)

        year = filename.split(".")[0].split("-")[1]
        uni_data = parser.parse(filename).to_json()
    except Exception as e:
        logger.exception(e)
        abort(404)

    tasks.add_url_description.delay(year, uni_data)
    os.remove(filename)

    return "OK", 200
