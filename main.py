from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from utils import as_json
from pydantic import BaseModel

app = FastAPI(title="Inazuma Eleven VR API")

# Carreguem el CSV
df_players = pd.read_csv("players.csv")
df_teams = pd.read_csv("teams.csv")


class Player(BaseModel):
    Id: int
    Imagen: str
    Nombre: str
    Apodo: str
    Juego: str
    Arquetipo: str
    Posicion: str
    Elemento: str
    Equipo: str
    Potencia: int
    Control: int
    Tecnica: int
    Presion: int
    Fisico: int
    Agilidad: int
    Inteligencia: int
    Total: int
    Grupo_de_Edad: str
    Ano_escolar: str
    Genero: str
    Rol: str

class Team(BaseModel):
    Imagen: str
    Equipo: str

# Endpoints de l'API

@app.get("/")
def home():
    return {"message": "La Api funcona"}

@app.get("/all")
def get_all():
    return as_json(df_players)

# /players endpoints
# Gets de jugadors

@app.get("/players")    
def get_all_players():
    return as_json(df_players["Nombre"])

@app.get("/players/{name}")
def get_player_by_name(name: str):
    nrml_name = name.title()
    player_rows = df_players[df_players["Nombre"] == nrml_name]
    if player_rows.empty:
        raise HTTPException(status_code=404, detail=f"Player {nrml_name} not found")
    return player_rows.to_dict(orient="records")  # devuelve una lista de diccionarios

@app.get("/players/apodo/{nickname}")
def get_player_by_nickname(nickname: str):
    nrml_nickname = nickname.title()
    player_rows = df_players[df_players["Apodo"] == nrml_nickname]
    if player_rows.empty:
        raise HTTPException(status_code=404, detail=f"El jugador con el apodo {nrml_nickname} no fue encontrado")
    return player_rows.to_dict(orient="records")

@app.get("/players/juego/{juego}")
def get_players_by_game(juego: str):
    players = df_players[df_players["Juego"].str.lower() == juego.lower()]
    if players.empty:
        raise HTTPException(status_code=404, detail=f"No players found for game {juego}")
    return as_json(players)

@app.get("/players/top/{n}")
def top_players(n: int = 10):
    top = df_players.sort_values("Total", ascending=False).head(n)
    return as_json(top)

#post de jugadors

@app.post("/players")
def add_player(player: Player):
    global df_players
    
    if player.Id in df_players['Id'].values:
        raise HTTPException(status_code=400, detail="El jugador con este Id ya existe")
    
    df_players.loc[len(df_players)] = pd.Series(player.dict())
    
    return {"mensaje": "Jugador agregado correctamente", "jugador": player.dict()}

# @app.post("/players")
# def add_player(player: Player):
#     global df_players
    
#     # Validar duplicado de Id
#     if player.Id in df_players['Id'].values:
#         raise HTTPException(status_code=400, detail="El jugador con este Id ya existe")
    
#     # Diccionario de validación
#     referencias = {
#         "Juego": df_juegos['Nombre'],
#         "Arquetipo": df_arquetipos['Nombre'],
#         "Posicion": df_posiciones['Nombre'],
#         "Elemento": df_elementos['Nombre'],
#         "Equipo": df_equipos['Nombre'],
#         "Grupo_de_Edad": df_grupos_edad['Nombre'],
#         "Ano_escolar": df_anos_escolares['Nombre'],
#         "Genero": df_generos['Nombre'],
#         "Rol": df_roles['Nombre']
#     }
    
#     # Validar campos referenciales
#     for campo, df_ref in referencias.items():
#         valor = getattr(player, campo)
#         if valor not in df_ref.values:
#             raise HTTPException(
#                 status_code=400, 
#                 detail=f"{campo} '{valor}' no existe"
#             )
    
#     # Agregar jugador al DataFrame
#     df_players.loc[len(df_players)] = pd.Series(player.dict())
    
#     # Guardar cambios en CSV
#     df_players.to_csv("players.csv", index=False)
    
#     return {"mensaje": "Jugador agregado correctamente", "jugador": player.dict()}

# /teams endpoints
# gets de teams
@app.get("/teams/")
def get_all_teams():
    teams = df_teams["Equipo"].unique().tolist()
    return as_json(teams)


@app.get("/teams/{team_name}")
def get_team_info(team_name: str):
    # Normalizamos el nombre para hacer case-insensitive
    team_name_norm = team_name.lower()
    
    # Buscamos el equipo en df_teams
    team_row = df_teams[df_teams["Equipo"].str.lower() == team_name_norm]
    
    if team_row.empty:
        raise HTTPException(status_code=404, detail=f"Equipo '{team_name}' no encontrado")
    
    # Obtenemos la imagen del equipo
    team_image = team_row.iloc[0]["Imagen"]
    
    # Obtenemos la lista de jugadores de ese equipo desde df_players
    players = df_players[df_players["Equipo"].str.lower() == team_name_norm.lower()]["Nombre"].tolist()
    
    return {
        "Equipo": team_name_norm.title(),
        "Imagen": team_image,
        "Jugadores": players
    }

@app.get("/teams/{team_name}/images")
def get_team_images(team_name: str):
    # Normalizamos el nombre para hacer case-insensitive
    team_name_norm = team_name.lower()
    
    # Buscamos el equipo en df_teams
    team_row = df_teams[df_teams["Equipo"].str.lower() == team_name_norm]
    
    if team_row.empty:
        raise HTTPException(status_code=404, detail=f"Equipo '{team_name}' no encontrado")
    
    # Obtenemos la imagen del equipo
    team_image = team_row.iloc[0]["Imagen"]
    
    return {"Imagen": team_image}

#post de teams

@app.post("/teams")
def add_team(team: Team):
    global df_teams
    
    if team.Equipo in df_teams["Equipo"].values:
        raise HTTPException(status_code=400, detail="El equipo ya existe")
    
    df_teams.loc[len(df_teams)] = pd.Series(team.dict())
    
    return {"mensaje": "Equipo agregado correctamente", "equipo": team.dict()}

# /elementos endpoints
# gets de elementos
@app.get("/elements/")    
def get_all_elements():
    elementos = df_players["Elemento"].unique().tolist()
    return as_json(elementos)

# /juegos endpoints
# gets de juegos
@app.get("/juegos/")
def get_all_games():
    juegos = df_players["Juego"].unique().tolist()
    return as_json(juegos)


