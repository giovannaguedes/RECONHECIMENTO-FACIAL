const video = document.getElementById('webcam');
const canvas = document.getElementById('overlay');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startRecognition');

// Acessa webcam
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
})
.catch(err => {
    alert('Não foi possível acessar a webcam.');
    console.error(err);
});

// Ajusta canvas quando o vídeo carrega
video.onloadedmetadata = () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    drawOverlay();
};

// Desenha overlay contínuo (para debug)
function drawOverlay() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, canvas.width, canvas.height); // mostra o contorno do canvas
    requestAnimationFrame(drawOverlay);
}

// Captura a imagem e envia ao backend
startButton.addEventListener('click', () => {
    if (!video.videoWidth || !video.videoHeight) {
        alert('Vídeo ainda não carregou. Tente novamente.');
        return;
    }

    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);

    tempCanvas.toBlob(blob => {
        if (!blob) {
            alert('Erro ao capturar a imagem.');
            return;
        }

        const formData = new FormData();
        formData.append('image', blob, 'snapshot.png');

    
        fetch('/start_recognition', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
           
             // Atualiza informações do crachá
             document.getElementById('userName').innerText = data.name;
             document.getElementById('userId').innerText = data.id;
             // Divide data e hora
             document.getElementById('loginDate').innerText = data.date; // só a data
             document.getElementById('loginTime').innerText = data.time; // só a hora
         
             const words = [
                "Coragem",
                "Inovação",
                "Persistência",
                "Criatividade",
                "Resiliência"
            ];
            
            // Escolhe uma palavra aleatória
            const randomWord = words[Math.floor(Math.random() * words.length)];
            
            // Mostra no crachá
            document.getElementById('wordOfTheDay').innerText = randomWord;
            
            // Atualiza a foto (se o backend retornar)
        if (data.photo) {
          document.getElementById('userPhoto').src = data.photo;
        }

            // Exibe o crachá só depois do reconhecimento
         document.getElementById('result').classList.remove('hidden');

            
      // Redireciona para siem.html após um pequeno atraso
            setTimeout(() => {
                window.location.href = '/siem';
            }, 80000);
        })
        .catch(err => {
            console.error(err);
            alert('Erro ao tentar reconhecer o rosto.');
        });
    }, 'image/png');
});