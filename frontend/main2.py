import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st
import requests

# URL de ton API Flask
API_URL = "http://127.0.0.1:5000/api/pokemon"

# Ton token d'authentification
TOKEN = "yassine_yassine"

# Fonction pour récupérer les infos du Pokémon
def get_pokemon_data(name):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_URL}/{name}", headers=headers)
    return response.json()

# Définir l'URL de l'API Flask pour l'authentification et Pokémon
FLASK_API_URL = "http://127.0.0.1:5000/api/pokemon/"
POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=1304"
LOGIN_URL = "http://127.0.0.1:5000/login"
LOGOUT_URL = "http://127.0.0.1:5000/logout"
CHECK_LOGIN_URL = "http://127.0.0.1:5000/check_login"

# Initialisation de session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_pokemon" not in st.session_state:
    st.session_state.selected_pokemon = None
if "show_more" not in st.session_state:
    st.session_state.show_more = False

# Fonction de connexion
def login(username, password):
    response = requests.post(LOGIN_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    else:
        st.session_state.logged_in = False
        return False

# Déconnexion
def logout():
    response = requests.post(LOGOUT_URL)
    if response.status_code == 200:
        st.session_state.logged_in = False
        del st.session_state.username
        return True
    return False

# Si l'utilisateur est connecté, afficher l'application Pokémon
if st.session_state.logged_in:
    st.title("Pokémon Info Dashboard")

    @st.cache_data
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
        st.session_state.show_more = False

    if st.session_state.selected_pokemon:
        response = requests.get(f"{FLASK_API_URL}{st.session_state.selected_pokemon.lower()}")
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"Nom : {data['name'].capitalize()}")
            st.write(f"**Taille :** {data['height']}")
            st.write(f"**Poids :** {data['weight']}")
            st.write(f"**Types :** {', '.join(data['types'])}")
            st.image(data["image"], caption=data["name"].capitalize())

            # Afficher les statistiques sous forme de graphique radar
            stats = data["stats"]
            labels = list(stats.keys())
            values = list(stats.values())

            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=data['name'].capitalize()))
            radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
            st.subheader("Statistiques du Pokémon")
            st.plotly_chart(radar_fig)

            # Afficher les statistiques sous forme d'histogramme
            stats_df = pd.DataFrame({"Statistiques": labels, "Valeurs": values})
            bar_fig = px.bar(stats_df, x="Statistiques", y="Valeurs", title="Répartition des Statistiques", color="Statistiques")
            st.plotly_chart(bar_fig)

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

    # Option de déconnexion
    if st.button("Se déconnecter"):
        if logout():
            st.success("Déconnexion réussie.")
            st.session_state.logged_in = False
            del st.session_state.username

# Si l'utilisateur n'est pas connecté, afficher le formulaire de connexion
else:
    st.title("Page de Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if login(username, password):
            st.success("Connexion réussie !")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
