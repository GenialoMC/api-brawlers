import requests
from bs4 import BeautifulSoup

def obtener_brawlers_filtrados(
    modo_slug,
    mapa_slug,
    powerplay=None,
    trophy_min=None,
    trophy_max=None,
    season=None
):
    url = f"https://brawltime.ninja/es/tier-list/mode/{modo_slug}/map/{mapa_slug}"
    params = {}

    # Filtro de tipo de batalla (ranked o regulares)
    if powerplay is not None:
        params["filter[powerplay]"] = "true" if powerplay else "false"

    # Rango de copas o rango competitivo
    if trophy_min is not None:
        params["filter[trophyRangeGte]"] = trophy_min
    if trophy_max is not None:
        params["filter[trophyRangeLte]"] = trophy_max

    # Filtro de temporada (fecha)
    if season:
        params["filter[season]"] = season

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tabla = soup.find("table")
    if not tabla:
        return []

    brawlers = []
    filas = tabla.find_all("tr")[1:]  # Ignora encabezado

    for fila in filas:
        columnas = fila.find_all(["td", "th"])
        if len(columnas) < 4:
            continue

        # Obtener nombre del brawler desde el alt de la imagen
        brawler_img = columnas[1].find("img")
        nombre = brawler_img["alt"] if brawler_img and "alt" in brawler_img.attrs else "Desconocido"

        winrate = columnas[2].text.strip()
        popularidad = columnas[3].text.strip()

        brawlers.append({
            "brawler": nombre,
            "winrate": winrate,
            "popularidad": popularidad
        })

    return brawlers


