import argparse
from flask import Flask, request, jsonify
import os
from functools import wraps

# parse command line arguments
parser = argparse.ArgumentParser(description="Simple File Management API")
parser.add_argument("--base_dir", required=True, help="Base directory for file storage")
parser.add_argument("--host", default="0.0.0.0", help="Host to run the API (default: 0.0.0.0)")
parser.add_argument("--port", type=int, default=5000, help="Port to run the API (default: 5000)")
parser.add_argument("--user", required=True, help="Username for authentication")
parser.add_argument("--password", required=True, help="Password for authentication")

args = parser.parse_args()

BASE_DIR = os.path.abspath(args.base_dir)
USER = args.user
PASSWORD = args.password

app = Flask(__name__)

# Check authentication
def check_auth(username, password):
    return username == USER and password == PASSWORD

# Decorator for authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated

@app.route("/list", methods=["GET"])
@requires_auth
def list_files():
    """ Retrieve a list of files in the directory (including subdirectories). """
    rel_dir = request.args.get("dir", "")
    abs_dir = os.path.abspath(os.path.join(BASE_DIR, rel_dir))

    if not abs_dir.startswith(BASE_DIR):  # prevent directory traversal
        return "Access Denied", 403

    if not os.path.exists(abs_dir):
        return "Directory not found", 404

    entries = []
    for entry in os.listdir(abs_dir):
        path = os.path.join(abs_dir, entry)
        entry_type = "dir" if os.path.isdir(path) else "file"
        entries.append({"name": entry, "type": entry_type})

    return jsonify(entries)

@app.route("/read", methods=["GET"])
@requires_auth
def read_file():
    """ Read a file """
    file_path = request.args.get("file")
    abs_path = os.path.abspath(os.path.join(BASE_DIR, file_path))

    if not abs_path.startswith(BASE_DIR):
        return "Access Denied", 403

    if os.path.exists(abs_path) and os.path.isfile(abs_path):
        with open(abs_path, "r") as f:
            return f.read()
    return "File not found", 404

@app.route("/write", methods=["POST"])
@requires_auth
def write_file():
    """ Write to a file """
    data = request.json
    file_path = data.get("file")
    content = data.get("content")

    if not file_path or not content:
        return "Invalid request", 400

    abs_path = os.path.abspath(os.path.join(BASE_DIR, file_path))

    if not abs_path.startswith(BASE_DIR):
        return "Access Denied", 403

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    with open(abs_path, "w") as f:
        f.write(content)

    return "File updated", 200

@app.route("/delete", methods=["DELETE"])
@requires_auth
def delete_file():
    """ Delete a file or an empty directory """
    file_path = request.args.get("file")
    abs_path = os.path.abspath(os.path.join(BASE_DIR, file_path))

    if not abs_path.startswith(BASE_DIR):
        return "Access Denied", 403

    if os.path.exists(abs_path):
        if os.path.isdir(abs_path):
            os.rmdir(abs_path)
        else:
            os.remove(abs_path)
        return "Deleted", 200
    return "Not found", 404

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=True)
