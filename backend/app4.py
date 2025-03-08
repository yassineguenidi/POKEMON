from flask import Flask, jsonify
import requests

app = Flask(__name__)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/api/pokemon/<name>')
def get_pokemon(name):
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
            return jsonify({"error": "Erreur lors de la récupération des informations du Pokémon"}), response.status_code


@app.route('/api/pokemon/<name>/abilities')
def get_pokemon_abilities(name):
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


@app.route('/api/pokemon/<name>/stats')
def get_pokemon_stats(name):
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


@app.route('/api/pokemon/<name>/evolutions')
def get_pokemon_evolutions(name):
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
