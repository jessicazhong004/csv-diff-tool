from flask import Flask, render_template, request, send_file
import os
from diff_core import compare_csv

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        key_col = request.form.get('keyCol', 'id')
        print("Selected key column:", key_col)

        file1_path = os.path.join(UPLOAD_FOLDER, 'file1.csv')
        file2_path = os.path.join(UPLOAD_FOLDER, 'file2.csv')
        file1.save(file1_path)
        file2.save(file2_path)

        # compare
        only_in_1, only_in_2 = compare_csv(file1_path, file2_path, key_col)

        # save the two
        only1_path = os.path.join(UPLOAD_FOLDER, 'only_in_file1.csv')
        only2_path = os.path.join(UPLOAD_FOLDER, 'only_in_file2.csv')
        only_in_1.to_csv(only1_path, index=False)
        only_in_2.to_csv(only2_path, index=False)

        # visible button
        return render_template('index.html', show_download=True)

    return render_template('index.html', show_download=False)


# single download
@app.route('/download/file1')
def download_file1():
    return send_file(os.path.join(UPLOAD_FOLDER, 'only_in_file1.csv'), as_attachment=True)

@app.route('/download/file2')
def download_file2():
    return send_file(os.path.join(UPLOAD_FOLDER, 'only_in_file2.csv'), as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)