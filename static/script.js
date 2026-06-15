const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const generateBtn = document.getElementById('generateBtn');
const outputSection = document.getElementById('outputSection');
const outputContent = document.getElementById('outputContent');
const statusText = document.getElementById('statusText');
const downloadBtn = document.getElementById('downloadBtn');

let uploadedData = null;

fileInput.addEventListener('change', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    fileLabel.textContent = file.name;
    generateBtn.disabled = true;
    statusText.textContent = 'Processing file...';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/upload', { method: 'POST', body: formData });
        const data = await res.json();

        if (data.error) {
            fileLabel.textContent = data.error;
            return;
        }

        uploadedData = data;
        generateBtn.disabled = false;
        fileLabel.textContent = `${file.name} ready`;
    } catch (err) {
        fileLabel.textContent = 'Upload failed';
    }
});

generateBtn.addEventListener('click', async () => {
    if (!uploadedData) return;

    generateBtn.disabled = true;
    outputSection.style.display = 'block';
    outputContent.innerHTML = '';
    downloadBtn.style.display = 'none';
    statusText.textContent = 'Generating...';

    let fullText = '';

    const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(uploadedData)
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop();

        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const payload = JSON.parse(line.slice(6));

            if (payload.text) {
                fullText += payload.text;
                outputContent.innerHTML = marked.parse(fullText);
            }

            if (payload.done) {
                statusText.textContent = 'Done';
                downloadBtn.style.display = 'inline-block';
            }
        }
    }

    generateBtn.disabled = false;

    downloadBtn.onclick = () => {
        const blob = new Blob([fullText], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'documentation.md';
        a.click();
        URL.revokeObjectURL(url);
    };
});