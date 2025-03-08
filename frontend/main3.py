# # # import streamlit as st
# # # import requests
# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # #
# # # API_URL = "http://127.0.0.1:5000/api/pokemon/"
# # # POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000"  # Récupère tous les Pokémon
# # #
# # # # Fonction pour récupérer les infos du Pokémon
# # # def get_pokemon_data(name):
# # #     response = requests.get(f"{API_URL}/{name}")
# # #     return response.json()
# # #
# # # # Fonction pour récupérer la liste des Pokémon
# # # @st.cache_data
# # # def get_pokemon_list():
# # #     response = requests.get(POKEAPI_LIST_URL)
# # #     if response.status_code == 200:
# # #         data = response.json()
# # #         return [pokemon["name"] for pokemon in data["results"]]
# # #     return []
# # #
# # # # Charger la liste des Pokémon
# # # pokemon_list = get_pokemon_list()
# # #
# # # # Interface utilisateur
# # # selected_pokemon = st.selectbox("Choisissez un Pokémon :", pokemon_list)
# # #
# # # if st.button("Rechercher"):
# # #     st.session_state.selected_pokemon = selected_pokemon
# # #     st.session_state.show_more = False
# # #
# # # if 'selected_pokemon' in st.session_state:
# # #     response = requests.get(f"{API_URL}{st.session_state.selected_pokemon.lower()}")
# # #     if response.status_code == 200:
# # #         data = response.json()
# # #         st.write(data)
# # #         # print(data)
# # #         st.subheader(f"Nom : {data['name'].capitalize()}")
# # #         st.write(f"**Taille :** {data['height']}")
# # #         st.write(f"**Poids :** {data['weight']}")
# # #         st.write(f"**Types :** {', '.join(data['types'])}")
# # #         st.image(data["image"], caption=data["name"].capitalize())
# # #
# # #         # Afficher les statistiques sous forme de graphique radar
# # #         # stats = data["stats"]
# # #         # labels = list(stats.keys())
# # #         # values = list(stats.values())
# # #         # #
# # #         # radar_fig = go.Figure()
# # #         # radar_fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=data['name'].capitalize()))
# # #         # radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
# # #         # st.subheader("Statistiques du Pokémon")
# # #         # st.plotly_chart(radar_fig)
# # #         #
# # #         # # Afficher les statistiques sous forme d'histogramme
# # #         # stats_df = pd.DataFrame({"Statistiques": labels, "Valeurs": values})
# # #         # bar_fig = px.bar(stats_df, x="Statistiques", y="Valeurs", title="Répartition des Statistiques", color="Statistiques")
# # #         # st.plotly_chart(bar_fig)
# # #
# # #         # Graphique en camembert pour les types de Pokémon
# # #         types = data['types']
# # #         type_counts = {t: types.count(t) for t in set(types)}
# # #         type_fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
# # #                           title="Répartition des Types de Pokémon")
# # #         st.plotly_chart(type_fig)
# # #
# # #         # Bouton "En savoir plus"
# # #         if st.button("En savoir plus"):
# # #             st.session_state.show_more = True
# # #
# # #     else:
# # #         st.error("Pokémon non trouvé !")
# # #
# # #     # Vérifier si "En savoir plus" est activé
# # #     if st.session_state.show_more and 'selected_pokemon' in st.session_state:
# # #         selected_pokemon = st.session_state.selected_pokemon.lower()
# # #
# # #         # Récupération des capacités
# # #         abilities_response = requests.get(f"{API_URL}{selected_pokemon}/abilities")
# # #         if abilities_response.status_code == 200:
# # #             abilities_data = abilities_response.json()
# # #             st.subheader("Capacités")
# # #             st.write(", ".join(abilities_data["abilities"]))
# # #         else:
# # #             st.error("Impossible de récupérer les capacités.")
# # #
# # #         # Récupération des évolutions
# # #         evolutions_response = requests.get(f"{API_URL}{selected_pokemon}/evolutions")
# # #         if evolutions_response.status_code == 200:
# # #             evolutions_data = evolutions_response.json()
# # #             st.subheader("Évolutions")
# # #             st.write(" → ".join(evolutions_data["evolutions"]))
# # #         else:
# # #             st.error("Impossible de récupérer les évolutions.")
# #
# #
# # import streamlit as st
# # import requests
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# #
# # API_URL = "http://127.0.0.1:5000/api/pokemon/"
# # POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000"  # Récupère tous les Pokémon
# #
# #
# # # Fonction pour récupérer les infos du Pokémon
# # def get_pokemon_data(name):
# #     response = requests.get(f"{API_URL}/{name}")
# #     return response.json()
# #
# #
# # # Fonction pour récupérer la liste des Pokémon
# # @st.cache_data
# # def get_pokemon_list():
# #     response = requests.get(POKEAPI_LIST_URL)
# #     if response.status_code == 200:
# #         data = response.json()
# #         return [pokemon["name"] for pokemon in data["results"]]
# #     return []
# #
# #
# # # Charger la liste des Pokémon
# # pokemon_list = get_pokemon_list()
# #
# # # Nombre de Pokémon à afficher par page
# # items_per_page = 10
# #
# #
# # # Fonction pour afficher les Pokémon en fonction de la page
# # def display_pokemon_page(page_num):
# #     global items_per_page
# #
# #     items_per_page = st.number_input(
# #         label="Donner le nombre de Pokémon à afficher",
# #         min_value=1,  # Pour éviter les valeurs nulles ou négatives
# #         value=10,  # Valeur par défaut
# #         step=1,  # Incrémentation par pas de 1
# #         format="%d"  # Affichage sous forme d'entier
# #     )
# #
# #     start_index = page_num * items_per_page
# #     end_index = start_index + items_per_page
# #     page_pokemon = pokemon_list[start_index:end_index]
# #
# #     pokemon_data = []
# #     # Récupérer les informations pour chaque Pokémon de la page
# #     for pokemon in page_pokemon:
# #         data = get_pokemon_data(pokemon)
# #         pokemon_data.append({
# #             "Nom": data['name'].capitalize(),
# #             "Poids": data['weight'],
# #             "Taille": data['height'],
# #             "Types": ", ".join(data['types'])
# #         })
# #
# #     # Convertir les données en DataFrame
# #     df = pd.DataFrame(pokemon_data)
# #     st.write(df)
# #
# #
# # # Interface utilisateur
# # st.title("Affichage des Pokémon")
# #
# # # Contrôles de pagination
# # if 'page_num' not in st.session_state:
# #     st.session_state.page_num = 0  # Initialiser la page à 0 (première page)
# #
# # # Afficher les Pokémon de la page actuelle
# # display_pokemon_page(st.session_state.page_num)
# #
# # # Contrôles pour la navigation entre les pages
# # col1, col2, col3 = st.columns([1, 2, 1])
# #
# # with col1:
# #     # Afficher un bouton pour la page précédente
# #     if st.session_state.page_num > 0:
# #         if st.button("Page précédente"):
# #             st.session_state.page_num -= 1
# #
# # with col3:
# #     # Afficher un bouton pour la page suivante
# #     if st.session_state.page_num < len(pokemon_list) // items_per_page:
# #         if st.button("Page suivante"):
# #             st.session_state.page_num += 1
# #
# # # Afficher un bouton "Afficher tous" pour afficher tous les Pokémon avec la pagination
# # # if st.button("Afficher tous"):
# # #     st.session_state.page_num = 0  # Réinitialiser à la première page
# # #     display_pokemon_page(st.session_state.page_num)
# #
# # # Section pour afficher les détails du Pokémon sélectionné
# # selected_pokemon = st.selectbox("Choisissez un Pokémon pour afficher les détails :", pokemon_list)
# #
# # if selected_pokemon:
# #     response = requests.get(f"{API_URL}{selected_pokemon.lower()}")
# #     if response.status_code == 200:
# #         data = response.json()
# #         st.subheader(f"Nom : {data['name'].capitalize()}")
# #         st.write(f"**Taille :** {data['height']}")
# #         st.write(f"**Poids :** {data['weight']}")
# #         st.write(f"**Types :** {', '.join(data['types'])}")
# #         st.image(data["image"], caption=data["name"].capitalize())
# #
# #         # Graphique en camembert pour les types de Pokémon
# #         types = data['types']
# #         type_counts = {t: types.count(t) for t in set(types)}
# #         type_fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
# #                           title="Répartition des Types de Pokémon")
# #         st.plotly_chart(type_fig)
# #
# #         # Bouton "En savoir plus"
# #         if st.button("En savoir plus"):
# #             st.session_state.show_more = True
# #
# #     else:
# #         st.error("Pokémon non trouvé !")
# #
# #     # Vérifier si "En savoir plus" est activé
# #     if st.session_state.show_more:
# #         selected_pokemon = st.session_state.selected_pokemon.lower()
# #
# #         # Récupération des capacités
# #         abilities_response = requests.get(f"{API_URL}{selected_pokemon}/abilities")
# #         if abilities_response.status_code == 200:
# #             abilities_data = abilities_response.json()
# #             st.subheader("Capacités")
# #             st.write(", ".join(abilities_data["abilities"]))
# #         else:
# #             st.error("Impossible de récupérer les capacités.")
# #
# #         # Récupération des évolutions
# #         evolutions_response = requests.get(f"{API_URL}{selected_pokemon}/evolutions")
# #         if evolutions_response.status_code == 200:
# #             evolutions_data = evolutions_response.json()
# #             st.subheader("Évolutions")
# #             st.write(" → ".join(evolutions_data["evolutions"]))
# #         else:
# #             st.error("Impossible de récupérer les évolutions.")
#
#
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
#
# API_URL = "http://127.0.0.1:5000/api/pokemon/"
# POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000"  # Récupère tous les Pokémon
#
# # Fonction pour récupérer les infos du Pokémon
# def get_pokemon_data(name):
#     response = requests.get(f"{API_URL}/{name}")
#     return response.json()
#
# # Fonction pour récupérer la liste des Pokémon
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
# # -------------------------------
# # Contrôle dynamique du nombre d'items
# # -------------------------------
# # Initialisation de la valeur dans session_state
# if "items_per_page" not in st.session_state:
#     st.session_state.items_per_page = 10
#
# # Widget pour saisir dynamiquement le nombre d'items par page
# st.session_state.items_per_page = st.number_input(
#     label="Donner le nombre de Pokémon à afficher",
#     min_value=1,
#     value=st.session_state.items_per_page,
#     step=1,
#     format="%d"
# )
#
# # -------------------------------
# # Pagination et affichage
# # -------------------------------
# def display_pokemon_page(page_num):
#     # Utilise la valeur dynamique saisie par l'utilisateur
#     items_per_page = st.session_state.items_per_page
#     start_index = page_num * items_per_page
#     end_index = start_index + items_per_page
#     page_pokemon = pokemon_list[start_index:end_index]
#
#     pokemon_data = []
#     # Récupération des informations pour chaque Pokémon de la page
#     for pokemon in page_pokemon:
#         data = get_pokemon_data(pokemon)
#         pokemon_data.append({
#             "Nom": data['name'].capitalize(),
#             "Poids": data['weight'],
#             "Taille": data['height'],
#             "Types": ", ".join(data['types'])
#         })
#
#     # Conversion en DataFrame et affichage
#     df = pd.DataFrame(pokemon_data)
#     st.write(df)
#
# st.title("Affichage des Pokémon")
#
# # Initialisation du numéro de page dans session_state
# if 'page_num' not in st.session_state:
#     st.session_state.page_num = 0
#
# # Affichage de la page courante
# display_pokemon_page(st.session_state.page_num)
#
# # Contrôles de navigation entre les pages
# col1, col2, col3 = st.columns([1, 2, 1])
# with col1:
#     if st.session_state.page_num > 0:
#         if st.button("Page précédente"):
#             st.session_state.page_num -= 1
#
# with col3:
#     # La limite de pages dépend maintenant de la valeur dynamique
#     if st.session_state.page_num < len(pokemon_list) // st.session_state.items_per_page:
#         if st.button("Page suivante"):
#             st.session_state.page_num += 1
#
# # -------------------------------
# # Détails du Pokémon sélectionné
# # -------------------------------
# selected_pokemon = st.selectbox("Choisissez un Pokémon pour afficher les détails :", pokemon_list)
#
# if selected_pokemon:
#     response = requests.get(f"{API_URL}{selected_pokemon.lower()}")
#     if response.status_code == 200:
#         data = response.json()
#         st.subheader(f"Nom : {data['name'].capitalize()}")
#         st.write(f"**Taille :** {data['height']}")
#         st.write(f"**Poids :** {data['weight']}")
#         st.write(f"**Types :** {', '.join(data['types'])}")
#         st.image(data["image"], caption=data["name"].capitalize())
#
#         # Graphique en camembert pour les types de Pokémon
#         types = data['types']
#         type_counts = {t: types.count(t) for t in set(types)}
#         type_fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
#                           title="Répartition des Types de Pokémon")
#         st.plotly_chart(type_fig)
#
#         if st.button("En savoir plus"):
#             st.session_state.show_more = True
#
#     else:
#         st.error("Pokémon non trouvé !")
#
#     # Affichage des détails supplémentaires si "En savoir plus" est activé
#     if st.session_state.get("show_more", False):
#         selected_pokemon = selected_pokemon.lower()
#
#         # Récupération des capacités
#         abilities_response = requests.get(f"{API_URL}{selected_pokemon}/abilities")
#         if abilities_response.status_code == 200:
#             abilities_data = abilities_response.json()
#             st.subheader("Capacités")
#             st.write(", ".join(abilities_data["abilities"]))
#         else:
#             st.error("Impossible de récupérer les capacités.")
#
#         # Récupération des évolutions
#         evolutions_response = requests.get(f"{API_URL}{selected_pokemon}/evolutions")
#         if evolutions_response.status_code == 200:
#             evolutions_data = evolutions_response.json()
#             st.subheader("Évolutions")
#             st.write(" → ".join(evolutions_data["evolutions"]))
#         else:
#             st.error("Impossible de récupérer les évolutions.")


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:5000/api/pokemon/"

API_URL = "http://127.0.0.1:5000/api/pokemon/"

POKEAPI_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=1304"  # Récupère tous les Pokémon


# Fonction pour récupérer les infos du Pokémon
def get_pokemon_data(name):
    response = requests.get(f"{API_URL}/{name}")
    return response.json()


# Fonction pour récupérer la liste des Pokémon
@st.cache_data
def get_pokemon_list():
    response = requests.get(POKEAPI_LIST_URL)
    if response.status_code == 200:
        data = response.json()
        return [pokemon["name"] for pokemon in data["results"]]
    return []


# Charger la liste des Pokémon
pokemon_list = get_pokemon_list()

# -------------------------------
# Navigation via la sidebar
# -------------------------------
page = st.sidebar.radio("Navigation", ["Liste des Pokémon", "Détails du Pokémon"])

# Initialisation de certaines variables dans session_state
if "items_per_page" not in st.session_state:
    st.session_state.items_per_page = 10
if "page_num" not in st.session_state:
    st.session_state.page_num = 0

# -------------------------------
# Page : Liste des Pokémon (affichage du DataFrame)
# -------------------------------
if page == "Liste des Pokémon":
    st.title("Liste des Pokémon")

    # Contrôle pour le nombre d'items par page (placé dans la sidebar pour la clarté)
    st.sidebar.header("Paramètres de la liste")
    st.session_state.items_per_page = st.sidebar.number_input(
        label="Donner le nombre de Pokémon à afficher",
        min_value=1,
        value=st.session_state.items_per_page,
        step=1,
        format="%d"
    )


    def display_pokemon_page(page_num):
        items_per_page = st.session_state.items_per_page
        start_index = page_num * items_per_page
        end_index = start_index + items_per_page
        page_pokemon = pokemon_list[start_index:end_index]

        pokemon_data = []
        # Récupérer les informations pour chaque Pokémon de la page
        for pokemon in page_pokemon:
            data = get_pokemon_data(pokemon)
            pokemon_data.append({
                "Nom": data['name'].capitalize(),
                "Poids": data['weight'],
                "Taille": data['height'],
                "Types": ", ".join(data['types'])
            })

        # Conversion en DataFrame et affichage
        df = pd.DataFrame(pokemon_data)
        st.write(df)


    # Afficher la page courante
    display_pokemon_page(st.session_state.page_num)

    # Contrôles pour la navigation entre les pages
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.page_num > 0:
            if st.button("Page précédente"):
                st.session_state.page_num -= 1

    with col3:
        if st.session_state.page_num < len(pokemon_list) // st.session_state.items_per_page:
            if st.button("Page suivante"):
                st.session_state.page_num += 1

# -------------------------------
# Page : Détails du Pokémon
# -------------------------------
elif page == "Détails du Pokémon":
    st.title("Détails du Pokémon")

    # Sélection du Pokémon
    selected_pokemon = st.selectbox("Choisissez un Pokémon pour afficher les détails :", pokemon_list)

    if selected_pokemon:
        response = requests.get(f"{API_URL}{selected_pokemon.lower()}")
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"Nom : {data['name'].capitalize()}")
            st.write(f"**Taille :** {data['height']}")
            st.write(f"**Poids :** {data['weight']}")
            st.write(f"**Types :** {', '.join(data['types'])}")
            st.image(data["image"], caption=data["name"].capitalize())

            # Graphique en camembert pour les types de Pokémon
            types = data['types']
            type_counts = {t: types.count(t) for t in set(types)}
            type_fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                              title="Répartition des Types de Pokémon")
            st.plotly_chart(type_fig)

            if st.button("En savoir plus"):
                st.session_state.show_more = True

        else:
            st.error("Pokémon non trouvé !")

        # Affichage des détails complémentaires si "En savoir plus" est activé
        if st.session_state.get("show_more", False):
            selected_pokemon = selected_pokemon.lower()

            # Récupération des capacités
            abilities_response = requests.get(f"{API_URL}{selected_pokemon}/abilities")
            if abilities_response.status_code == 200:
                abilities_data = abilities_response.json()
                st.subheader("Capacités")
                st.write(", ".join(abilities_data["abilities"]))
            else:
                st.error("Impossible de récupérer les capacités.")

            # Récupération des évolutions
            evolutions_response = requests.get(f"{API_URL}{selected_pokemon}/evolutions")
            if evolutions_response.status_code == 200:
                evolutions_data = evolutions_response.json()
                st.subheader("Évolutions")
                st.write(" → ".join(evolutions_data["evolutions"]))
            else:
                st.error("Impossible de récupérer les évolutions.")
