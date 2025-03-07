from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
# Ativar o CORS para todos os endpoints

CORS(app)

# Caminho para o arquivo PDF base
PDF_PATH = "pdfs/FORM.pdf"  # Ajuste o caminho conforme necessário

@app.route("/gerar_json")
def gerar_json():
    try:
        # Caminho do arquivo JSON dentro da pasta /data
        file_path = os.path.join(os.getcwd(), "data", "base.json")

        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo JSON não encontrado"}), 404

        # Lê o conteúdo do arquivo JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return jsonify(data), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Erro ao decodificar JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {e}"}), 500
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=6002)
