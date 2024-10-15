// dashboard/main.js

// Configurazione: inserisci il tuo tenantId e apiKey qui
const tenantId = 'd43d8235-1792-40f9-859b-6084ed753df5'; // Sostituisci con il tuo tenant_id
const apiKey = '7b50bbd4-1053-42ac-85c7-23c0da1f3869';     // Sostituisci con il tuo api_key

// URL di base per le API
const baseURL = 'http://localhost';
const encryptionAPI = `${baseURL}:5001`;
const keyManagementAPI = `${baseURL}:5003`;
const zkpAPI = `${baseURL}:5002`;

// Funzione per generare le chiavi
async function generateKeys() {
    const url = `${keyManagementAPI}/${tenantId}/keygen`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            alert('Chiavi generate con successo!');
        } else {
            const errorData = await response.json();
            alert('Errore nella generazione delle chiavi: ' + errorData.error);
        }
    } catch (error) {
        console.error('Errore nella richiesta:', error);
        alert('Errore nella richiesta: ' + error.message);
    }
}

// Funzione per cifrare un messaggio
async function encryptMessage() {
    const message = document.getElementById('messageToEncrypt').value;
    const url = `${encryptionAPI}/${tenantId}/encrypt`;

    try {
        const response = await fetch(url, {
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
        } else {
            const errorData = await response.json();
            alert('Errore nella cifratura: ' + errorData.error);
        }
    } catch (error) {
        console.error('Errore nella richiesta:', error);
        alert('Errore nella richiesta: ' + error.message);
    }
}

// Funzione per decifrare un messaggio
async function decryptMessage() {
    const encryptedMessage = document.getElementById('messageToDecrypt').value;
    const url = `${encryptionAPI}/${tenantId}/decrypt`;

    try {
        const response = await fetch(url, {
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
        } else {
            const errorData = await response.json();
            alert('Errore nella decifratura: ' + errorData.error);
        }
    } catch (error) {
        console.error('Errore nella richiesta:', error);
        alert('Errore nella richiesta: ' + error.message);
    }
}

// Event listeners per i pulsanti
document.getElementById('generateKeysButton').addEventListener('click', generateKeys);
document.getElementById('encryptButton').addEventListener('click', encryptMessage);
document.getElementById('decryptButton').addEventListener('click', decryptMessage);
