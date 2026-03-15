from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
# O CORS(app) é a mágica que permite o seu front-end ler a resposta sem ser bloqueado
CORS(app) 

@app.route('/', methods=['GET'])
def proxy():
    # Captura a URL da Globo que vem logo após a interrogação (?)
    target_url = request.query_string.decode('utf-8')
    
    if not target_url.startswith('http'):
        return jsonify({'error': 'URL inválida ou ausente.'}), 400

    # Adicionar headers ajuda a contornar proteções anti-bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        # Faz a requisição por debaixo dos panos para a Globo
        resp = requests.get(target_url, headers=headers)
        
        # Devolve exatamente o que a Globo respondeu (status, formato e conteúdo)
        return Response(
            resp.content, 
            status=resp.status_code, 
            content_type=resp.headers.get('Content-Type', 'application/json')
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Falha ao buscar dados', 'details': str(e)}), 500

if __name__ == '__main__':
    print("Proxy do Cartola rodando em: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
