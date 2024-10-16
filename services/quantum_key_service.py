import requests

class QuantumKeyService:
    def generate_qrng_key(self, length=32):
        num_values = length  
        api_url = f'https://qrng.anu.edu.au/API/jsonI.php?length=10&type=uint8'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    hex_numbers = data['data']
                    hex_string = ''.join(hex_numbers)
                    key_bytes = bytes.fromhex(hex_string)[:length]
                    return key_bytes
                else:
                    print('ANU QRNG API error:', data.get('message', 'Unknown error'))
                    return None
            else:
                print(f'HTTP Error: {response.status_code}')
                return None
        except Exception as e:
            print(f'Errore nella generazione della chiave quantistica: {e}')
            return None
