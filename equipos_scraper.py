import requests
from bs4 import BeautifulSoup

def obtener_mejores_equipos(
    modo_slug,
    mapa_slug,
    powerplay=None,
    trophy_min=None,
    trophy_max=None,
    season=None
):
    url = f"https://brawltime.ninja/es/tier-list/mode/{modo_slug}/map/{mapa_slug}"
    params = {}

    if powerplay is not None:
        params["filter[powerplay]"] = "true" if powerplay else "false"
    if trophy_min is not None:
        params["filter[trophyRangeGte]"] = trophy_min
    if trophy_max is not None:
        params["filter[trophyRangeLte]"] = trophy_max
    if season:
        params["filter[season]"] = season

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscamos la segunda tabla, que corresponde a "Mejores equipos"
    tablas = soup.find_all("table")
    if len(tablas) < 2:
        return []

    contenedor_tabla = tablas[1]  # Segunda tabla: equipos

    equipos = []
    filas = contenedor_tabla.find_all("tr")[1:]  # Ignorar encabezado

    for fila in filas:
        columnas = fila.find_all(["td", "th"])
        if len(columnas) < 3:
            continue

        brawler_imgs = columnas[1].find_all("img")
        nombres = [img["alt"] for img in brawler_imgs if img and "alt" in img.attrs]

        victorias = columnas[2].text.strip()
        try:
            victorias = int(victorias.replace(",", ""))
        except ValueError:
            victorias = 0

        equipos.append({
            "equipo": nombres,
            "victorias": victorias
        })

    return equipos

