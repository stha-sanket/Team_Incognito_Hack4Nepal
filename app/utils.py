def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
