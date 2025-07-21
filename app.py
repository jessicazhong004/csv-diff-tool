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

        file1_path = os.path.join(UPLOAD_FOLDER, 'file1.csv')
        file2_path = os.path.join(UPLOAD_FOLDER, 'file2.csv')
        file1.save(file1_path)
        file2.save(file2_path)

        only_in_1, only_in_2 = compare_csv(file1_path, file2_path)

        result_path = os.path.join(UPLOAD_FOLDER, 'diff_result.csv')
        with open(result_path, 'w', encoding='utf-8', newline='') as f:
            f.write(f"Total rows only in File1: {len(only_in_1)}\n")
            f.write(f"Total rows only in File2: {len(only_in_2)}\n\n")

            f.write('Only in File1:\n')
            only_in_1.to_csv(f, index=False)
            f.write('\n\nOnly in File2:\n')
            only_in_2.to_csv(f, index=False)


        return send_file(result_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

