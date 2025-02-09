document.getElementById('upload').addEventListener('change', async function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async function(e) {
        const img = new Image();
        img.src = e.target.result;

        img.onload = async function() {
            document.getElementById('spinner').style.display = 'block';
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            const preview = document.getElementById('preview');
            preview.src = url;
            preview.style.display = 'block';
            
            document.getElementById('spinner').style.display = 'none';
            document.getElementById('download').style.display = 'block';
            document.getElementById('download').onclick = function() {
                const a = document.createElement('a');
                a.href = url;
                a.download = 'processed_image.png';
                a.click();
            };
        };
    };
});
