import time
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

print(Path("../frontend/dist").resolve())
app = Flask("prova_gui", static_url_path="/web", static_folder="/frontend/dist")


@app.route("/", methods=["POST"])
def test():
    args = request.json.get('args')
    print("ARGS", args)
    json = request.json.get("value")
    print("JSON", json)
    return jsonify(dict(msg="Hello extensions!"))


@app.route("/files", methods=["POST"])
def test2():
    file = request.files['file']
    fname = file.filename
    print("You have uploaded a file called:", fname)
    return jsonify(dict(msg=f"Hello extensions, you have uploaded the file: {fname}!"))


@app.get("/content")
def content():
    return f"Hello {time.time()}"


CORS(app)

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
