import requests

class QuantumKeyService:
    def generate_qrng_key(self, length=32):
        api_length = min(length, 1024)  # Max length per request is 1024
        api_url = f'https://qrng.anu.edu.au/API/jsonI.php?length={api_length}&type=uint8'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    random_numbers = data['data']
                    key_bytes = bytes(random_numbers)[:length]
                    return key_bytes
                else:
                    print('ANU QRNG API error:', data.get('message', 'Unknown error'))
                    return None
            else:
                print(f'HTTP Error: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error in generating quantum key: {e}')
            return None
