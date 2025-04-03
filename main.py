from fastapi import FastAPI, Query
from typing import Optional
from scraper import obtener_brawlers_filtrados
from equipos_scraper import obtener_mejores_equipos  # 🚨 Nuevo import

app = FastAPI()

@app.get("/brawlers")
def get_brawlers(
    modo: str = Query(..., description="Modo de juego (ej. gem-grab)"),
    mapa: str = Query(..., description="Slug del mapa (ej. Double-Swoosh)"),
    powerplay: Optional[bool] = Query(None, description="true para clasificatorias, false para batallas regulares"),
    trophy_min: Optional[int] = Query(None, ge=0, le=18, description="Límite inferior de copas o rango (0-15 para copas, 1-18 para ranked)"),
    trophy_max: Optional[int] = Query(None, ge=0, le=18, description="Límite superior de copas o rango (0-15 para copas, 1-18 para ranked)"),
    season: Optional[str] = Query(None, description="Fecha de temporada (YYYY-MM-DD)")
):
    datos = obtener_brawlers_filtrados(modo, mapa, powerplay, trophy_min, trophy_max, season)
    if not datos:
        return {"error": "No se encontraron datos con esos parámetros."}
    return {
        "modo": modo,
        "mapa": mapa,
        "powerplay": powerplay,
        "trophy_min": trophy_min,
        "trophy_max": trophy_max,
        "season": season,
        "brawlers": datos
    }

@app.get("/equipos")
def get_equipos(
    modo: str = Query(..., description="Modo de juego (ej. gem-grab)"),
    mapa: str = Query(..., description="Slug del mapa (ej. Double-Swoosh)"),
    powerplay: Optional[bool] = Query(None, description="true para clasificatorias, false para batallas regulares"),
    trophy_min: Optional[int] = Query(None, ge=0, le=18),
    trophy_max: Optional[int] = Query(None, ge=0, le=18),
    season: Optional[str] = Query(None)
):
    datos = obtener_mejores_equipos(modo, mapa, powerplay, trophy_min, trophy_max, season)
    if not datos:
        return {"error": "No se encontraron equipos con esos parámetros."}
    return {
        "modo": modo,
        "mapa": mapa,
        "powerplay": powerplay,
        "trophy_min": trophy_min,
        "trophy_max": trophy_max,
        "season": season,
        "equipos": datos
    }
