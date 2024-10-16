// Configuration
const tenantId = 'your_tenantdId';
const apiKey = 'your_API_key';
const baseURL = 'http://localhost';
const encryptionAPI = `${baseURL}:5001`;
const keyManagementAPI = `${baseURL}:5003`;

document.addEventListener('DOMContentLoaded', function() {
    const generateKeysButton = document.getElementById('generateKeysButton');
    const encryptButton = document.getElementById('encryptButton');
    const decryptButton = document.getElementById('decryptButton');
    const fileToEncrypt = document.getElementById('fileToEncrypt');
    const fileToDecrypt = document.getElementById('fileToDecrypt');
    const fileName = document.getElementById('fileName');
    const fileNameDecrypt = document.getElementById('fileNameDecrypt');
    const downloadEncrypted = document.getElementById('downloadEncrypted');
    const downloadDecrypted = document.getElementById('downloadDecrypted');

    generateKeysButton.addEventListener('click', generateKeys);
    encryptButton.addEventListener('click', handleEncrypt);
    decryptButton.addEventListener('click', handleDecrypt);
    fileToEncrypt.addEventListener('change', updateFileName);
    fileToDecrypt.addEventListener('change', updateFileNameDecrypt);

    function updateFileName(e) {
        fileName.textContent = e.target.files[0] ? e.target.files[0].name : '';
    }

    function updateFileNameDecrypt(e) {
        fileNameDecrypt.textContent = e.target.files[0] ? e.target.files[0].name : '';
    }

    async function generateKeys() {
        const progressBar = document.querySelector('#keyGenerationProgress .progress');
        generateKeysButton.disabled = true;
        progressBar.style.width = '0%';

        try {
            // Simulate key generation process
            for (let i = 0; i <= 100; i += 10) {
                await new Promise(resolve => setTimeout(resolve, 200));
                progressBar.style.width = `${i}%`;
            }

            const response = await fetch(`${keyManagementAPI}/${tenantId}/keygen`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                showNotification('Keys generated successfully!', 'success');
            } else {
                const errorData = await response.json();
                showNotification('Error generating keys: ' + errorData.error, 'error');
            }
        } catch (error) {
            console.error('Error in request:', error);
            showNotification('Error in request: ' + error.message, 'error');
        } finally {
            generateKeysButton.disabled = false;
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 1000);
        }
    }

    async function handleEncrypt() {
        const message = document.getElementById('messageToEncrypt').value;
        const file = fileToEncrypt.files[0];

        if (file) {
            await encryptFile(file);
        } else if (message) {
            await encryptMessage(message);
        } else {
            showNotification('Please enter a message or choose a file to encrypt.', 'error');
        }
    }

    async function handleDecrypt() {
        const message = document.getElementById('messageToDecrypt').value;
        const file = fileToDecrypt.files[0];

        if (file) {
            await decryptFile(file);
        } else if (message) {
            await decryptMessage(message);
        } else {
            showNotification('Please enter a message or choose a file to decrypt.', 'error');
        }
    }

    async function encryptMessage(message) {
        try {
            const response = await fetch(`${encryptionAPI}/${tenantId}/encrypt`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('encryptedMessage').value = data.encrypted_message;
                showNotification('Message encrypted successfully!', 'success');
            } else {
                const errorData = await response.json();
                showNotification('Error encrypting: ' + errorData.error, 'error');
            }
        } catch (error) {
            console.error('Error in request:', error);
            showNotification('Error in request: ' + error.message, 'error');
        }
    }

    async function decryptMessage(encryptedMessage) {
        try {
            const response = await fetch(`${encryptionAPI}/${tenantId}/decrypt`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ encrypted_message: encryptedMessage })
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('decryptedMessage').value = data.decrypted_message;
                showNotification('Message decrypted successfully!', 'success');
            } else {
                const errorData = await response.json();
                showNotification('Error decrypting: ' + errorData.error, 'error');
            }
        } catch (error) {
            console.error('Error in request:', error);
            showNotification('Error in request: ' + error.message, 'error');
        }
    }

    async function encryptFile(file) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            const fileContent = e.target.result;
            try {
                const response = await fetch(`${encryptionAPI}/${tenantId}/encrypt`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: fileContent })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('encryptedMessage').value = 'File encrypted. Use download button to save.';
                    downloadEncrypted.style.display = 'inline-flex';
                    downloadEncrypted.href = URL.createObjectURL(new Blob([data.encrypted_message], {type: 'application/octet-stream'}));
                    downloadEncrypted.download = 'encrypted_' + file.name;
                    showNotification('File encrypted successfully!', 'success');
                } else {
                    const errorData = await response.json();
                    showNotification('Error encrypting file: ' + errorData.error, 'error');
                }
            } catch (error) {
                console.error('Error in request:', error);
                showNotification('Error in request: ' + error.message, 'error');
            }
        };
        reader.readAsDataURL(file);
    }

    async function decryptFile(file) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            const fileContent = e.target.result;
            try {
                const response = await fetch(`${encryptionAPI}/${tenantId}/decrypt`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ encrypted_message: fileContent })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('decryptedMessage').value = 'File decrypted. Use download button to save.';
                    downloadDecrypted.style.display = 'inline-flex';
                    downloadDecrypted.href = data.decrypted_message;
                    downloadDecrypted.download = 'decrypted_' + file.name;
                    showNotification('File decrypted successfully!', 'success');
                } else {
                    const errorData = await response.json();
                    showNotification('Error decrypting file: ' + errorData.error, 'error');
                }
            } catch (error) {
                console.error('Error in request:', error);
                showNotification('Error in request: ' + error.message, 'error');
            }
        };
        reader.readAsText(file);
    }

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }
});
