from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import insert_image_blob, get_latest_image_blob, get_all_images_blob, delete_image_blob

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Gesture Transfer API!"}), 200

# mengirim/post data atau hasil ss ke database
@app.route("/api/image", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    image_blob = file.read()
    insert_image_blob(filename, image_blob)

    return jsonify({"status": "Image uploaded", "filename": filename}), 201

# mendapatkan data atau ss terakhir
@app.route("/api/image/last", methods=["GET"])
def latest_image():
    result = get_latest_image_blob()
    if result:
        result['image_data'] = result['image_data'].hex()
        return jsonify(result), 200
    return jsonify({"error": "No data"}), 404

# mendapatkan semua data atau hasil ss
@app.route("/api/image/all", methods=["GET"])
def all_images():
    return jsonify(get_all_images_blob()), 200

# menghapus data atau ss berdasarkan id
@app.route("/api/image/<int:id>", methods=["DELETE"])
def remove_image(id):
    deleted_count = delete_image_blob(id)
    if deleted_count == 0:
        return jsonify({"error": f"ID {id} not found"}), 404
    return jsonify({"status": "Deleted", "deleted_id": id}), 200


# menghapus semua data atau ss
@app.route("/api/image/deleteAll", methods=["DELETE"])
def remove_all_images():
    deleted_count = delete_image_blob(all_data=True)

    # 🔥 Tambahkan perintah reset auto_increment di sini
    from db import get_db_connection
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("ALTER TABLE screenshots AUTO_INCREMENT = 1")
    db.commit()
    db.close()

    return jsonify({"status": "All images deleted", "deleted_count": deleted_count}), 200

if __name__ == "__main__":
    app.run(debug=True)
