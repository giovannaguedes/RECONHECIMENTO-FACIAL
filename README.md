# RECONHECIMENTO-FACIAL

◽️ Guia: Reconhecimento Facial com Flask + face_recognition

Esse software combina Flask (backend web), OpenCV e a biblioteca face_recognition para 
criar uma aplicação de login/identificação com base em fotos salvas em um dataset.

1. Frontend (index.html)
Página feita com Tailwind CSS para estilo responsivo.
Possui:

Câmera (Webcam API) para capturar o rosto.

Canvas Overlay para marcação da área.

Botão "Iniciar Reconhecimento" que envia a imagem para o servidor.

Crachá digital que mostra:

Foto do usuário (vinda do dataset)

Nome reconhecido

Data e hora de login

Palavra do dia

2. Backend (app.py)
Carregando Dataset
Lê cada arquivo da pasta dataset/.

Extrai o embedding facial com face_recognition.

Armazena o nome (arquivo) e o vetor facial (encoding).

3.Reconhecimento Facial (rota /start_recognition)

Recebe uma foto do usuário (request.files['image']).

Converte em array NumPy (cv2.imdecode).

Extrai face_encodings da imagem enviada.

Compara com o dataset usando:

compare_faces → booleano (match ou não).

face_distance → distância (quanto menor, mais parecido).

Se distância < 0.6, o usuário é reconhecido.

Retorna JSON para o frontend com:

Nome

Data

Hora

Foto original do dataset

4.Registro de Presença
if not any(record['Name'] == name for record in attendance):
    attendance.append({'Name': name, 'Time': time_now})
    pd.DataFrame(attendance).to_excel('attendance.xlsx', index=False)


Evita duplicar a presença do mesmo usuário.

Salva em um Excel (attendance.xlsx).

5. Fluxo Completo

Usuário acessa http://localhost:5000/.

O sistema pede imagem da webcam.

Foto é enviada via POST → /start_recognition.

Flask processa → compara com dataset.

Se reconhecido:

Mostra nome, foto e crachá digital.

Salva registro no Excel.

👉 O que você aprendeu

Como carregar dataset facial em Python.

Como usar face_recognition para comparar embeddings.

Como integrar Flask + HTML + JS para reconhecimento em tempo real.

Como salvar logs de presença em Excel.
