from fastapi import  Query, FastAPI
from typing import Optional
from urllib.parse import urlencode
from scrapper.la_cartoon_scrap import get_cartoons_series, get_cartoon_details, get_chapter_details

app = FastAPI()

BASE_URL = "https://www.lacartoons.com/"

@app.get("/cartoons")
def get_cartoons(
    Titulo: Optional[str] = Query(None, description="Texto para buscar en el título"),
    Categoria_id: Optional[int] = Query(None, ge=1, le=8, description="ID de la categoría (1-8)"),
    page: Optional[int] = Query(None, ge=1, description="Número de página")
):
    # Construcción dinámica de la URL con parámetros
    params = {}
    if Titulo:
        params["utf8"] = "%E2%9C%93"  # Código para el check utf-8
        params["Titulo"] = Titulo
    if Categoria_id:
        params["Categoria_id"] = Categoria_id
    if page:
        params["page"] = page
    
    url = BASE_URL + "?" + urlencode(params)
    
    return get_cartoons_series(url)

@app.get("/cartoons_details")
def get_cartoons_details(url: str = Query(..., description="URL de la serie ej : https://www.lacartoons.com/serie/8")):
    return get_cartoon_details(url)

@app.get("/chapter_details")
def get_chapter_info(url: str = Query(..., description="URL del episodio ej: https://www.lacartoons.com/serie/capitulo/485?t=2")):
    return get_chapter_details(url)