from flask import Flask, request, jsonify, send_file
from docxtpl import DocxTemplate
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ Server đang chạy!"

@app.route("/generate-docx", methods=["POST"])
def generate_docx():
    json_data = request.get_json()
    template_name = json_data.get("template")
    data = json_data.get("data")

    if not template_name or not data:
        return jsonify({"error": "Thiếu thông tin"}), 400

    try:
        doc = DocxTemplate(f"templates/{template_name}.docx")
        doc.render(data)

        os.makedirs("output", exist_ok=True)
        file_id = str(uuid.uuid4())
        output_path = f"output/{file_id}.docx"
        doc.save(output_path)

        return jsonify({
            "fileUrl": f"http://localhost:5000/download/{file_id}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    path = f"output/{file_id}.docx"
    if not os.path.exists(path):
        return jsonify({"error": "Không tìm thấy file"}), 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
