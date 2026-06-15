import os
from flask import Flask, render_template, request, Response, jsonify
from file_processor import process_zip, encode_image
from claude_service import stream_codebase_docs, stream_schematic_docs

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ext = filename.rsplit('.', 1)[-1].lower()

    if ext == 'zip':
        file_tree, combined_content = process_zip(filepath)
        os.remove(filepath)
        return jsonify({
            'type': 'codebase',
            'file_tree': file_tree,
            'content': combined_content
        })
    elif ext in ['png', 'jpg', 'jpeg', 'webp']:
        image_data, media_type = encode_image(filepath)
        os.remove(filepath)
        return jsonify({
            'type': 'schematic',
            'image_data': image_data,
            'media_type': media_type
        })
    else:
        os.remove(filepath)
        return jsonify({'error': 'Unsupported file type'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    doc_type = data.get('type')

    if doc_type == 'codebase':
        generator = stream_codebase_docs(data.get('file_tree'), data.get('content'))
    elif doc_type == 'schematic':
        generator = stream_schematic_docs(data.get('image_data'), data.get('media_type'))
    else:
        return jsonify({'error': 'Invalid type'}), 400

    return Response(generator, mimetype='text/event-stream', headers={'Cache-Control': 'no-cache'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)