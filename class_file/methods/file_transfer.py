import os
import glob
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


# --- HELPER FUNCTION (Fixes the NameError) ---
def find_file_by_id(user_id):
    """Loops through extensions to find if the file exists on disk."""
    for ext in ALLOWED_EXTENSIONS:
        potential_file = f"{user_id}{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], potential_file)
        if os.path.exists(file_path):
            return potential_file, file_path
    return None, None


# 1. CREATE (POST) - Upload a new ID file
@app.route('/upload_id', methods=['POST'])
def upload_id_file():
    if 'file' not in request.files or 'id' not in request.form:
        return jsonify({'error': 'Missing file or ID in form-data'}), 400

    file = request.files['file']
    id_from_form = request.form['id']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'}), 400

    # Prevent overwriting if user already exists
    filename, _ = find_file_by_id(id_from_form)
    if filename:
        return jsonify({'error': 'ID already exists. Use PUT to update'}), 409

    secure_filename = f"{id_from_form}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
    file.save(file_path)

    return jsonify({'message': 'Uploaded successfully', 'id': id_from_form}), 201


# 2. SHOW / RETRIEVE (GET) - View/Download a specific ID file
@app.route('/upload_id/<user_id>', methods=['GET'])
def get_user_id_data(user_id):
    filename, _ = find_file_by_id(user_id)
    
    if not filename:
        return jsonify({'error': f'Image file not found for ID {user_id}'}), 404
        
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 3. REPLACE / UPDATE (PUT) - Completely replace an existing ID file
@app.route('/upload_id/<user_id>', methods=['PUT'])
def replace_id_file(user_id):
    if 'file' not in request.files:
        return jsonify({'error': 'Missing file in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_extension = os.path.splitext(file.filename)[1].lower() 
    if file_extension not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'}), 400

    filename, old_file_path = find_file_by_id(user_id)
    if not filename:
        return jsonify({'error': 'ID does not exist to update. Use POST to create'}), 404

    # Safe file replacement (removes old file even if extension changes)
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    new_filename = f"{user_id}{file_extension}"
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    file.save(new_file_path)

    return jsonify({'message': 'ID replaced successfully', 'id': user_id}), 200


# 4. PARTIAL UPDATE (PATCH) - Update file if sent, otherwise pass
@app.route('/upload_id/<user_id>', methods=['PATCH'])
def patch_id_file(user_id):
    filename, old_file_path = find_file_by_id(user_id)
    if not filename:
        return jsonify({'error': 'ID file not found'}), 404

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                return jsonify({'error': 'Invalid file type'}), 400
            
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
                
            new_filename = f"{user_id}{file_extension}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            return jsonify({'message': 'ID file updated via PATCH', 'id': user_id}), 200

    return jsonify({'message': 'No file provided, no changes made', 'id': user_id}), 200


# 5. DELETE (DELETE) - Permanently remove an ID file
@app.route('/upload_id/<user_id>', methods=['DELETE'])
def delete_id_file(user_id):
    filename, file_path = find_file_by_id(user_id)
    if not filename:
        return jsonify({'error': f'ID file not found for ID {user_id}'}), 404

    if os.path.exists(file_path):
        os.remove(file_path)
        
    return jsonify({'message': 'ID file deleted successfully', 'id': user_id}), 200


# 6. LIST ALL (GET) - View all uploaded IDs in the folder
@app.route('/upload_id', methods=['GET'])
def list_id_files():
    files_list = []
    for ext in ALLOWED_EXTENSIONS:
        for path in glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], f"*{ext}")):
            filename = os.path.basename(path)
            user_id = os.path.splitext(filename)[0]
            files_list.append({
                'id': user_id,
                'filename': filename,
                'size_bytes': os.path.getsize(path)
            })
    return jsonify({'total_count': len(files_list), 'files': files_list}), 200


if __name__ == '__main__':
    app.run(debug=True)