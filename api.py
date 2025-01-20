from flask import Flask, jsonify, send_file, request
from fillpdf import fillpdfs
import base64
from io import BytesIO
import os

app = Flask(__name__)

# Caminho para o arquivo PDF base
PDF_PATH = "pdfs/FORM.pdf"  # Ajuste o caminho conforme necessário

@app.route("/preencher", methods=["POST"])
def preencher_pdf():
    try:
        dados = request.json
        form_fields = list(fillpdfs.get_form_fields(PDF_PATH).keys())
        dict_preenchido = {}

        # Função para mapear campos dinamicamente
        def mapear_campos(payload, prefixo=""):
            for chave, valor in payload.items():
                # Adicionar o prefixo para diferenciar campos aninhados
                campo_pdf = f"{prefixo}{chave}"
                if isinstance(valor, dict):
                    # Recursão para campos aninhados
                    mapear_campos(valor, prefixo=f"{campo_pdf}_")
                else:
                    # Adicionar ao dict se o campo existe nos form_fields
                    if campo_pdf in form_fields:
                        dict_preenchido[campo_pdf] = valor

        # Mapear os campos do payload para o dict
        mapear_campos(dados)

        # Preencher o PDF com os dados
        pdf_output_path = 'preenchido.pdf'
        fillpdfs.write_fillable_pdf(PDF_PATH, pdf_output_path, dict_preenchido)

        # Abrir o PDF preenchido em modo binário
        with open(pdf_output_path, 'rb') as f:
            pdf_data = f.read()

        # Converter o conteúdo binário do PDF para base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Retornar o PDF preenchido como base64
        return {'status': 'PDF Gerado', 'pdf_base64': pdf_base64}
    
    except KeyError as e:
        return {'error': f"Chave não encontrada: {e}"}, 400
    except Exception as e:
        return {'error': f"Erro inesperado: {e}"}, 500
    
if __name__ == "__main__":
    app.run(debug=True)
