import requests
import json
import os
from pypdf import PdfReader


class LlamaClient:
    def __init__(self, base_url="http://localhost:11434", model="llama3.1:8b",
                 context_file_path="documentacao/base_conhecimento.pdf"):
        self.base_url = base_url
        self.model = model
        self.context_file_path = context_file_path
        self.system_prompt = self._load_context()

    def _load_context(self):
        """Carrega o conteúdo do arquivo de contexto (PDF)."""
        if not os.path.exists(self.context_file_path):
            print(f"Aviso: Arquivo de contexto '{self.context_file_path}' não encontrado.")
            return ""

        try:
            reader = PdfReader(self.context_file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            # Instrução para o modelo agir como especialista e focar no contexto
            instruction = (
                "Você é um consultor e vendedor especialista neste produto.\n"
                "Use APENAS as informações abaixo para responder às perguntas.\n"
                "Se a resposta não estiver no contexto, diga que não sabe e ofereça contato humano.\n"
                "Não invente informações (alucinações).\n"
                "Responda de forma cordial e profissional.\n\n"
                "--- INÍCIO DO CONTEXTO (PDF) ---\n"
                f"{text}\n"
                "--- FIM DO CONTEXTO ---\n"
            )
            return instruction
        except Exception as e:
            print(f"Erro ao ler arquivo de contexto PDF: {e}")
            return ""

    def generate_response(self, prompt):
        url = f"{self.base_url}/api/generate"

        # Combina o prompt do sistema com a pergunta do usuário
        full_prompt = f"{self.system_prompt}\n\nPergunta do cliente: {prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1  # Baixa temperatura para reduzir criatividade/alucinações
            }
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
    # Certifique-se de ter um arquivo PDF válido em documentacao/base_conhecimento.pdf
    client = LlamaClient(context_file_path="documentacao/CatalogoFRM.pdf")

    print("--- Teste 1: Pergunta sobre o conteúdo do PDF ---")
    resposta = client.generate_response("Um engenheiro de manutenção precisa especificar um conjunto de mancal para um equipamento que opera sob serviço pesado, com um eixo de 30 mm de diâmetro, a uma rotação constante de 1.000 RPM.Identifique o modelo de mancal tipo Apoio (Pillow Block) de serviço pesado compatível com um eixo de 30 mm? seja mais especifco no modelo marcar e pagina ")
    print(f"Resposta: {resposta}\n")
