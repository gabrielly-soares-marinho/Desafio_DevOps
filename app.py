from flask import Flask, jsonify, redirect, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para o Swagger funcionar
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Para testes, tokens não expiram
jwt = JWTManager(app)

# Swagger
from flask import send_from_directory

SWAGGER_URL = '/swagger'
# Serve the swagger spec from a simple endpoint to avoid static/blueprint path issues
API_DOC_URL = '/swagger.json'

@app.route('/swagger.json', methods=['GET'])
def swagger_spec():
    # Use Flask's static folder to serve the swagger.json reliably
    return send_from_directory(app.static_folder, 'swagger.json')

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_DOC_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Middleware para corrigir o formato do token automaticamente
@app.before_request
def fix_authorization_header():
    import re
    # Pega o header do environ diretamente (antes do Flask processar)
    auth_header = request.environ.get('HTTP_AUTHORIZATION', '') or request.headers.get('Authorization', '')
    
    if auth_header and not auth_header.startswith('Bearer '):
        # Remove "Bearer " se já tiver (para evitar duplicação)
        token = auth_header.replace('Bearer ', '').strip()
        
        # Se o header contém JSON com access_token, extrai apenas o token
        if 'access_token' in auth_header:
            try:
                import json
                # Tenta extrair do JSON
                if auth_header.strip().startswith('{'):
                    data = json.loads(auth_header)
                    token = data.get('access_token', token)
                else:
                    # Extrai usando regex
                    match = re.search(r'"access_token"\s*:\s*"([^"]+)"', auth_header)
                    if match:
                        token = match.group(1)
            except:
                pass
        
        # Se ainda não tem token válido, tenta extrair JWT diretamente
        if not token or len(token) < 20:
            match = re.search(r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', auth_header)
            if match:
                token = match.group(0)
        
        # Garante que o token não está vazio e adiciona "Bearer"
        if token and len(token) > 10:  # Tokens JWT são longos
            # Modifica o environ ANTES do Flask-JWT processar
            request.environ['HTTP_AUTHORIZATION'] = f'Bearer {token}'

@app.route('/', methods=['GET'])
def index():
    return {"mensagem": "Ola, bem-vindo ao Desafio Final!"}, 200

@app.route('/docs', methods=['GET'])
def docs():
    return redirect('/swagger/')


# Accept common misspelling from client requests and redirect to the correct URL
@app.route('/swgger', methods=['GET'])
@app.route('/swgger/', methods=['GET'])
def swgger_redirect():
    return redirect('/swagger/')

@app.route('/items', methods=['GET'])
def get_items():
    items = [{"id": 1, "name": "item1"},
             {"id": 2, "name": "item2"},
             {"id": 3, "name": "item3"}]
    return jsonify(items=items), 200

@app.route('/login', methods=['POST'])
def login():
    """Rota de login que gera um token JWT"""
    # Pode receber dados do usuário, mas para simplificar sempre gera token
    user_data = request.get_json() if request.is_json else {}
    user_identity = user_data.get('username', 'user')
    
    access_token = create_access_token(identity=user_identity)
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Rota protegida que requer autenticação JWT"""
    current_user = get_jwt_identity()
    return jsonify(message="Protected route", user=current_user), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 1313))
    app.run(host='0.0.0.0', port=port)
