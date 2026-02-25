import requests
import json

class LlamaClient:
    def __init__(self, base_url="http://localhost:11434", model="llama3.1:8b"):
        self.base_url = base_url
        self.model = model

    def generate_response(self, prompt):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com o Llama: {e}")
            return None

if __name__ == "__main__":
    # Teste simples
    client = LlamaClient()
    resposta = client.generate_response("Olá, como você está?")
    print(f"Resposta do Llama: {resposta}")
