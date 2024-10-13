from flask import Flask, request, render_template, jsonify
import random
import string

app = Flask(__name__)

# Dictionnaire pour stocker les codes de vérification des joueurs
verification_codes = {}

# Générer un code de vérification aléatoire
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Page principale où le joueur entre son nom et code de vérification
@app.route('/')
def index():
    return render_template('index.html')

# Route pour générer un code pour un joueur
@app.route('/generate_code', methods=['POST'])
def generate_code_for_player():
    player_name = request.json.get('player_name')
    if not player_name:
        return jsonify({'error': 'Nom du joueur manquant'}), 400
    
    # Générer un nouveau code et l'enregistrer
    code = generate_code()
    verification_codes[player_name] = {'code': code, 'verified': False}
    return jsonify({'code': code})

# Route pour vérifier si le code est correct
@app.route('/verify_code', methods=['POST'])
def verify_code():
    player_name = request.form['player_name']
    code_entered = request.form['code']

    if player_name not in verification_codes:
        return "Joueur non trouvé.", 400

    if verification_codes[player_name]['code'] == code_entered:
        # Si le code est correct, le joueur est vérifié
        verification_codes[player_name]['verified'] = True
        return "Vérification réussie !", 200
    else:
        return "Code incorrect.", 403

# Route pour que Roblox vérifie si le joueur a été vérifié
@app.route('/is_verified', methods=['POST'])
def is_verified():
    player_name = request.json.get('player_name')
    
    if player_name not in verification_codes:
        return jsonify({'verified': False}), 400

    verified = verification_codes[player_name]['verified']
    return jsonify({'verified': verified}), 200

if __name__ == '__main__':
    app.run(debug=True)
