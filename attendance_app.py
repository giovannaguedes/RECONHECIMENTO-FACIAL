from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__, template_folder='templates', static_folder='static')

# --- Carrega rostos do dataset ---
def load_encodings(dataset_path='dataset'):
    names = []
    encodings = []
    for filename in os.listdir(dataset_path):
        filepath = os.path.join(dataset_path, filename)
        img = cv2.imread(filepath)
        if img is None:
            continue
        names.append(os.path.splitext(filename)[0])
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encs = face_recognition.face_encodings(rgb_img)
        if face_encs:
            encodings.append(face_encs[0])
    return names, encodings

names, encodings = load_encodings()
attendance = []

@app.route('/')
def index():
    return render_template('index.html')

# --- Serve arquivos da pasta dataset (ex: Guedes.jpeg) ---
@app.route('/dataset/<path:filename>')
def dataset_static(filename):
    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
    return send_from_directory(dataset_path, filename)

# --- Rota de reconhecimento facial ---
@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'})

    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    if not face_encodings:
        return jsonify({'error': 'Nenhum rosto reconhecido'})

    face_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(encodings, face_encoding)
    distances = face_recognition.face_distance(encodings, face_encoding)
    best_match_index = np.argmin(distances)

    if matches[best_match_index] and distances[best_match_index] < 0.6:
        name = names[best_match_index]

        now = datetime.now()
        date_now = now.strftime('%Y-%m-%d')      # só a data
        time_now = now.strftime('%H:%M:%S')      # só a hora
        
        # Caminho relativo para frontend acessar a foto
        photo_url = url_for('dataset_static', filename=f"{name}.jpeg")  # ajuste extensão conforme seu arquivo

        if not any(record['Name'] == name for record in attendance):
            attendance.append({'Name': name, 'Time': time_now})
            pd.DataFrame(attendance).to_excel('attendance.xlsx', index=False)
        return jsonify({'name': name, 'time': time_now, 'date': date_now, 'photo': photo_url})
    else:
        return jsonify({'error': 'Nenhum rosto reconhecido'})

@app.route('/siem')
def siem_index():
    # Caminho correto para a nova pasta SIEM_mvp
    siem_path = os.path.join(os.path.dirname(__file__), '../SIEM_mvp')
    return send_from_directory(siem_path, 'siem.html')

# Serve arquivos dentro de SIEM_mvp (como imagens)
@app.route('/siem/<path:filename>')
def siem_static(filename):
    siem_path = os.path.join(os.path.dirname(__file__), '../SIEM_mvp')
    return send_from_directory(siem_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
