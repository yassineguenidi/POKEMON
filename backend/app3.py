from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement à partir du fichier .env

SECRET_KEY = os.getenv("SECRET_KEY")

import jwt
import datetime
from flask import Flask, jsonify, request
import requests
from functools import wraps

app = Flask(__name__)

# Clé secrète pour encoder le token
SECRET_KEY = "votre_cle_secrete"

# Clé de base de l'API Pokémon
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEAPI_BASE_URL = "http://127.0.0.1:5000/api/pokemon/"


# Décorateur pour vérifier le token JWT
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # On récupère le token dans l'en-tête Authorization
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # Récupère le token après "Bearer"

        if not token:
            return jsonify({"message": "Token manquant!"}), 403

        try:
            # Vérifie le token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data["user"]  # Assumes que 'user' est stocké dans le token
        except Exception as e:
            return jsonify({"message": "Token invalide!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated_function


# Endpoint de connexion pour générer un token
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.json
    username = auth_data.get("username")
    password = auth_data.get("password")

    # Vérifie les identifiants
    if username == "utilisateur" and password == "motdepasse":
        # Génère le token JWT
        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Identifiants incorrects!"}), 401


# Endpoint pour récupérer un Pokémon (protégé par JWT)
@app.route('/api/pokemon/<name>')
@token_required
def get_pokemon(current_user, name):
    """Récupère les informations de base d'un Pokémon."""
    url = f"{POKEAPI_BASE_URL}{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "image": data["sprites"]["front_default"]
        })
    else:
        if response.status_code == 404:
            return jsonify({"error": f"Pokémon '{name}' non trouvé"}), 404
        else:
            return jsonify(
                {"error": "Erreur lors de la récupération des informations du Pokémon"}), response.status_code


# Endpoint pour récupérer les capacités d'un Pokémon (protégé par JWT)
@app.route('/api/pokemon/<name>/abilities')
@token_required
def get_pokemon_abilities(current_user, name):
    """Récupère les capacités d'un Pokémon."""
    url = f"{POKEAPI_BASE_URL}{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        abilities = [a["ability"]["name"] for a in data["abilities"]]
        return jsonify({"name": data["name"], "abilities": abilities})
    else:
        if response.status_code == 404:
            return jsonify({"error": f"Pokémon '{name}' non trouvé"}), 404
        else:
            return jsonify({"error": "Erreur lors de la récupération des capacités"}), response.status_code


# Endpoint pour récupérer les statistiques d'un Pokémon (protégé par JWT)
@app.route('/api/pokemon/<name>/stats')
@token_required
def get_pokemon_stats(current_user, name):
    """Récupère les statistiques d'un Pokémon."""
    url = f"{POKEAPI_BASE_URL}{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        return jsonify({"name": data["name"], "stats": stats})
    else:
        if response.status_code == 404:
            return jsonify({"error": f"Pokémon '{name}' non trouvé"}), 404
        else:
            return jsonify({"error": "Erreur lors de la récupération des statistiques"}), response.status_code


# Endpoint pour récupérer tous les Pokémon (non protégé)
@app.route('/api/pokemon')
def get_all_pokemon():
    """Récupère la liste de tous les Pokémon disponibles dans l'API."""
    url = f"{POKEAPI_BASE_URL}?limit=1302"  # Nombre total de Pokémon dans l'API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_list = [{"name": p["name"], "url": p["url"]} for p in data["results"]]
        return jsonify({"count": len(pokemon_list), "pokemon": pokemon_list})
    else:
        return jsonify({"error": "Impossible de récupérer la liste des Pokémon"}), response.status_code


# Endpoint pour récupérer les évolutions d'un Pokémon (protégé par JWT)
@app.route('/api/pokemon/<name>/evolutions')
@token_required
def get_pokemon_evolutions(current_user, name):
    """Récupère la chaîne d'évolution d'un Pokémon."""
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    response = requests.get(species_url)

    if response.status_code == 200:
        species_data = response.json()
        evolution_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_url)

        if evolution_response.status_code == 200:
            evolution_data = evolution_response.json()
            evolutions = []

            def get_evolutions(chain):
                evolutions.append(chain["species"]["name"])
                if "evolves_to" in chain and len(chain["evolves_to"]) > 0:
                    for evo in chain["evolves_to"]:
                        get_evolutions(evo)

            get_evolutions(evolution_data["chain"])

            return jsonify({"name": name, "evolutions": evolutions})
        else:
            return jsonify({"error": "Chaîne d'évolution introuvable pour ce Pokémon"}), 404
    else:
        return jsonify({"error": f"Pokémon '{name}' non trouvé"}), 404


if __name__ == '__main__':
    app.run(debug=True)
