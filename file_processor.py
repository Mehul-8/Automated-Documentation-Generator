import os
import zipfile
import base64
import shutil

ALLOWED_CODE_EXT = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.go', '.rb', '.php', '.html', '.css', '.json', '.yaml', '.yml',
    '.md', '.sql', '.sh', '.rs', '.swift', '.kt'
}

IGNORE_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build', '.idea', '.vscode'}

MAX_FILE_SIZE = 50000
MAX_TOTAL_SIZE = 150000

def process_zip(filepath):
    extract_dir = filepath + '_extracted'
    with zipfile.ZipFile(filepath, 'r') as z:
        z.extractall(extract_dir)

    file_tree = []
    combined_content = []
    total_size = 0

    for root, dirs, files in os.walk(extract_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for filename in files:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, extract_dir)
            ext = os.path.splitext(filename)[1].lower()

            file_tree.append(rel_path)

            if ext in ALLOWED_CODE_EXT and total_size < MAX_TOTAL_SIZE:
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if len(content) > MAX_FILE_SIZE:
                        content = content[:MAX_FILE_SIZE] + '\n... (truncated)'
                    combined_content.append(f'--- FILE: {rel_path} ---\n{content}\n')
                    total_size += len(content)
                except Exception:
                    pass

    shutil.rmtree(extract_dir)
    return file_tree, '\n'.join(combined_content)

def encode_image(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    media_type_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp'
    }
    media_type = media_type_map.get(ext, 'image/png')

    with open(filepath, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')

    return encoded, media_type