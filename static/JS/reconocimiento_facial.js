let stream = null;
let rostroCapturado = null;
let isDetectionActive = false;

document.addEventListener('DOMContentLoaded', function() {
    const startCameraBtn = document.getElementById('startCamera');
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const preview = document.getElementById('preview');
    const cameraContainer = document.getElementById('cameraContainer');
    const previewContainer = document.getElementById('previewContainer');
    const retakePhotoBtn = document.getElementById('retakePhoto');
    const rostroDataInput = document.getElementById('rostro_data');
    const faceGuide = document.getElementById('faceGuide');
    const facialError = document.getElementById('facialError');

    if (!startCameraBtn) return;

    startCameraBtn.addEventListener('click', async function() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'user',
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                }
            });

            video.srcObject = stream;
            cameraContainer.style.display = 'block';
            previewContainer.style.display = 'none';
            startCameraBtn.style.display = 'none';
            isDetectionActive = true;

            video.onloadedmetadata = () => {
                video.play();
                const ajustarYDetectar = () => {
                    if (video.readyState >= 2) {
                        ajustarGuiaRostro();
                        setTimeout(ajustarGuiaRostro, 100);
                        setTimeout(ajustarGuiaRostro, 300);
                        detectarRostro();
                    } else {
                        setTimeout(ajustarYDetectar, 50);
                    }
                };
                setTimeout(ajustarYDetectar, 200);
            };

            window.addEventListener('resize', ajustarGuiaRostro);
        } catch (error) {
            console.error('Error al acceder a la cámara:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error de cámara',
                text: 'No se pudo acceder a la cámara. Verifica los permisos o usa otro navegador.',
                confirmButtonText: 'Entendido'
            });
        }
    });

    function ajustarGuiaRostro() {
        if (!faceGuide || !video || !cameraContainer) return;
        
        const videoRect = video.getBoundingClientRect();
        const containerRect = cameraContainer.getBoundingClientRect();
        
        if (videoRect.width === 0 || videoRect.height === 0) {
            setTimeout(ajustarGuiaRostro, 100);
            return;
        }

        const videoLeftRelative = videoRect.left - containerRect.left;
        const videoTopRelative = videoRect.top - containerRect.top;
        const videoCenterX = videoLeftRelative + (videoRect.width / 2);
        const videoCenterY = videoTopRelative + (videoRect.height / 2);
        
        faceGuide.style.width = '150px';
        faceGuide.style.height = '150px';
        faceGuide.style.left = videoCenterX + 'px';
        faceGuide.style.top = videoCenterY + 'px';
        faceGuide.style.transform = 'translate(-50%, -50%)';
        faceGuide.style.position = 'absolute';
        faceGuide.style.margin = '0';
        faceGuide.style.padding = '0';
        faceGuide.style.display = 'block';
    }

    function detectarRostro() {
        if (!isDetectionActive || !video.videoWidth) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const detectionSize = 150;
        
        const imageData = ctx.getImageData(
            centerX - detectionSize / 2,
            centerY - detectionSize / 2,
            detectionSize,
            detectionSize
        );

        let hasContent = false;
        let totalBrightness = 0;
        for (let i = 0; i < imageData.data.length; i += 4) {
            const r = imageData.data[i];
            const g = imageData.data[i + 1];
            const b = imageData.data[i + 2];
            const brightness = (r + g + b) / 3;
            totalBrightness += brightness;
            if (brightness > 30) {
                hasContent = true;
            }
        }

        const avgBrightness = totalBrightness / (imageData.data.length / 4);

        if (hasContent && avgBrightness > 40) {
            facialError.style.display = 'none';
            faceGuide.style.borderColor = 'rgba(0, 255, 0, 0.8)';
            faceGuide.classList.add('detected');
        } else {
            facialError.textContent = 'Coloca tu rostro en el centro del círculo.';
            facialError.style.display = 'block';
            faceGuide.style.borderColor = 'rgba(128, 128, 128, 0.8)';
            faceGuide.classList.remove('detected');
        }

        if (isDetectionActive) {
            setTimeout(detectarRostro, 500);
        }
    }

    video.addEventListener('click', function() {
        capturarFoto();
    });

    if (cameraContainer) {
        const captureBtn = document.createElement('button');
        captureBtn.type = 'button';
        captureBtn.className = 'btn btn-primary btn-sm mt-2';
        captureBtn.innerHTML = '<i class="bi bi-camera-fill"></i> Capturar';
        captureBtn.addEventListener('click', capturarFoto);
        cameraContainer.appendChild(captureBtn);
    }

    function capturarFoto() {
        if (!video.videoWidth || !video.videoHeight) {
            Swal.fire({
                icon: 'warning',
                title: 'Espera un momento',
                text: 'La cámara aún se está inicializando...',
                timer: 2000
            });
            return;
        }

        if (!faceGuide.classList.contains('detected')) {
            Swal.fire({
                icon: 'warning',
                title: 'Rostro no detectado',
                text: 'Por favor, coloca tu rostro en el centro del círculo verde antes de capturar.',
                confirmButtonText: 'Entendido'
            });
            return;
        }

        isDetectionActive = false;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const cropSize = 150;
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        
        const cropCanvas = document.createElement('canvas');
        cropCanvas.width = cropSize;
        cropCanvas.height = cropSize;
        const cropCtx = cropCanvas.getContext('2d');
        
        cropCtx.drawImage(
            canvas,
            centerX - cropSize / 2,
            centerY - cropSize / 2,
            cropSize,
            cropSize,
            0,
            0,
            cropSize,
            cropSize
        );
        
        const imageData = cropCanvas.toDataURL('image/jpeg', 0.8);
        rostroCapturado = imageData;

        preview.src = imageData;
        previewContainer.style.display = 'block';
        cameraContainer.style.display = 'none';

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }

        if (rostroDataInput) {
            rostroDataInput.value = imageData;
        }

        Swal.fire({
            icon: 'success',
            title: 'Foto capturada',
            text: 'Tu foto facial ha sido registrada correctamente.',
            timer: 2000,
            showConfirmButton: false
        });
    }

    retakePhotoBtn.addEventListener('click', function() {
        previewContainer.style.display = 'none';
        startCameraBtn.style.display = 'block';
        rostroCapturado = null;
        isDetectionActive = false;
        if (rostroDataInput) {
            rostroDataInput.value = '';
        }
        if (faceGuide) {
            faceGuide.style.display = 'none';
        }
    });

    window.addEventListener('beforeunload', function() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });
});

function obtenerRostroData() {
    const rostroDataInput = document.getElementById('rostro_data');
    return rostroDataInput ? rostroDataInput.value : null;
}
