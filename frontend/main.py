# import streamlit as st
# import requests
#
# # Définir l'URL de l'API Flask
# FLASK_API_URL = "http://127.0.0.1:5000/api/pokemon/"
# POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=1304"  # Récupère tous les Pokémon
#
# st.title("Pokémon Info App")
#
# # Initialiser session_state pour éviter la réinitialisation de la page
# if "show_more" not in st.session_state:
#     st.session_state.show_more = False
#
# @st.cache_data
# def get_pokemon_list():
#     response = requests.get(POKEAPI_LIST_URL)
#     if response.status_code == 200:
#         data = response.json()
#         return [pokemon["name"] for pokemon in data["results"]]
#     return []
#
# # Charger la liste des Pokémon
# pokemon_list = get_pokemon_list()
#
# # Interface utilisateur
# selected_pokemon = st.selectbox("Choisissez un Pokémon :", pokemon_list)
#
# if st.button("Rechercher"):
#     if selected_pokemon:
#         response = requests.get(f"{FLASK_API_URL}{selected_pokemon.lower()}")
#
#         if response.status_code == 200:
#             data = response.json()
#             st.subheader(f"Nom : {data['name'].capitalize()}")
#             st.write(f"**Taille :** {data['height']}")
#             st.write(f"**Poids :** {data['weight']}")
#             st.write(f"**Types :** {', '.join(data['types'])}")
#             st.image(data["image"], caption=data["name"].capitalize())
#             print('helloo')
#
#             # Afficher le bouton "En savoir plus"
#             if st.button("En savoir plus"):
#                 st.session_state.show_more = True  # Activer l'affichage des détails supplémentaires
#
# # Vérifier si "En savoir plus" a été cliqué
# if st.session_state.show_more and selected_pokemon:
#     # Récupération des capacités
#     abilities_response = requests.get(f"{FLASK_API_URL}{selected_pokemon.lower()}/abilities")
#     if abilities_response.status_code == 200:
#         abilities_data = abilities_response.json()
#         st.subheader("Capacités")
#         st.write(", ".join(abilities_data["abilities"]))
#         print("abilities")
#     else:
#         st.error("Impossible de récupérer les capacités.")
#
#     # Récupération des évolutions
#     evolutions_response = requests.get(f"{FLASK_API_URL}{selected_pokemon.lower()}/evolutions")
#     if evolutions_response.status_code == 200:
#         evolutions_data = evolutions_response.json()
#         st.subheader("Évolutions")
#         st.write(" → ".join(evolutions_data["evolutions"]))
#     else:
#         st.error("Impossible de récupérer les évolutions.")


import streamlit as st
import requests

# Définir l'URL de l'API Flask
FLASK_API_URL = "http://127.0.0.1:5000/api/pokemon/"
POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=1304"

st.title("Pokémon Info App")

# Initialisation des états dans session_state
if "selected_pokemon" not in st.session_state:
    st.session_state.selected_pokemon = None
if "show_more" not in st.session_state:
    st.session_state.show_more = False

@st.cache_data  # Utiliser la nouvelle version de cache
def get_pokemon_list():
    response = requests.get(POKEAPI_LIST_URL)
    if response.status_code == 200:
        data = response.json()
        return [pokemon["name"] for pokemon in data["results"]]
    return []

# Charger la liste des Pokémon
pokemon_list = get_pokemon_list()

# Interface utilisateur
selected_pokemon = st.selectbox("Choisissez un Pokémon :", pokemon_list)

if st.button("Rechercher"):
    st.session_state.selected_pokemon = selected_pokemon
    st.session_state.show_more = False  # Réinitialiser "En savoir plus"

# Vérifier si un Pokémon a été sélectionné
if st.session_state.selected_pokemon:
    response = requests.get(f"{FLASK_API_URL}{st.session_state.selected_pokemon.lower()}")

    if response.status_code == 200:
        data = response.json()
        st.subheader(f"Nom : {data['name'].capitalize()}")
        st.write(f"**Taille :** {data['height']}")
        st.write(f"**Poids :** {data['weight']}")
        st.write(f"**Types :** {', '.join(data['types'])}")
        st.image(data["image"], caption=data["name"].capitalize())

        # Bouton "En savoir plus"
        if st.button("En savoir plus"):
            st.session_state.show_more = True

    else:
        st.error("Pokémon non trouvé !")

# Vérifier si "En savoir plus" est activé
if st.session_state.show_more and st.session_state.selected_pokemon:
    selected_pokemon = st.session_state.selected_pokemon.lower()

    # Récupération des capacités
    abilities_response = requests.get(f"{FLASK_API_URL}{selected_pokemon}/abilities")
    if abilities_response.status_code == 200:
        abilities_data = abilities_response.json()
        st.subheader("Capacités")
        st.write(", ".join(abilities_data["abilities"]))
    else:
        st.error("Impossible de récupérer les capacités.")

    # Récupération des évolutions
    evolutions_response = requests.get(f"{FLASK_API_URL}{selected_pokemon}/evolutions")
    if evolutions_response.status_code == 200:
        evolutions_data = evolutions_response.json()
        st.subheader("Évolutions")
        st.write(" → ".join(evolutions_data["evolutions"]))
    else:
        st.error("Impossible de récupérer les évolutions.")
