from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.lacartoons.com"


def get_chapter_details(chapter_url: str) -> Dict[str, Any]:
    
    
    try:
        response = requests.get(chapter_url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"No se pudo conectar con la página: {e}"}

    soup = BeautifulSoup(response.content, "html.parser")

    # Extraer el título de la serie
    h2_elem = soup.select_one("h2.subtitulo-linea")
    series_title = ''.join(t.strip() for t in h2_elem.find_all(string=True, recursive=False)) if h2_elem else ""

    # Extraer el enlace de reproducción
    iframe = soup.select_one("div.serie-video-informacion iframe")
    video_url = iframe.get("src", "").strip() if iframe else ""

    # Extraer la información del episodio
    episode_info = {}
    try:
        h3_elem = soup.select_one("div.serie-video-informacion h3")
        number_info = h3_elem.contents[0].strip() if h3_elem and h3_elem.contents else ""
        ep_title = h3_elem.select_one("span").get_text(strip=True) if h3_elem and h3_elem.select_one("span") else ""
        episode_info = {"number_info": number_info, "title": ep_title}
    except Exception as e:
        print(f"Error obteniendo la información del episodio: {e}")

    # Extraer enlaces "Anterior" y "Siguiente"
    previous_url, next_url = "", ""
    try:
        controls = soup.select_one("div.controles-episodios")
        if controls:
            links = controls.find_all("a")
            if len(links) >= 2:
                previous_url = urljoin(BASE_URL, links[0].get("href", ""))
                next_url = urljoin(BASE_URL, links[1].get("href", ""))
    except Exception as e:
        print(f"Error obteniendo los enlaces de navegación: {e}")

    # Extraer la reseña
    review_text = ""
    try:
        review_elem = soup.select_one("div.resena-serie p")
        review_text = review_elem.get_text(strip=True) if review_elem else ""
    except Exception as e:
        print(f"Error obteniendo la reseña: {e}")

    return {
        "series_title": series_title,
        "video_url": video_url,
        "episode_info": episode_info,
        "previous_url": previous_url,
        "next_url": next_url,
        "review": review_text,
    }


def get_cartoon_details(base_url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': f"No se pudo conectar con la página: {e}"}

    soup = BeautifulSoup(response.content, 'html.parser')
    info_container = soup.select_one('.all-serie')
    episodes_container = soup.select_one('.contenedor-episodio-temporada')

    if not info_container or not episodes_container:
        return {'error': "No se pudo encontrar la información necesaria en la página"}

    try:
        backdrop = BASE_URL + info_container.select_one('img.fondo-serie-seccion')['src']
        titulo_container = info_container.select_one('h2.subtitulo-serie-seccion')
        titulo = titulo_container.contents[0].strip() if titulo_container else "Desconocido"
        canal = titulo_container.select_one('span').get_text(strip=True) if titulo_container else "N/A"
        poster = BASE_URL + info_container.select_one('.imagen-serie img')['src']
        episodios = info_container.select_one('.informacion-serie-seccion p:nth-of-type(1) span').get_text(strip=True)
        idioma = info_container.select_one('.informacion-serie-seccion p:nth-of-type(2) span').get_text(strip=True)
        ano = info_container.select_one('.marcador.marcador-año').get_text(strip=True)
        valoracion = info_container.select_one('.valoracion1').get_text(strip=True)
        resena = info_container.select_one('.informacion-serie-seccion p:nth-of-type(5) span').get_text(strip=True)
    except Exception as e:
        return {'error': f"Error extrayendo la información del cartoon: {e}"}

    seasons = []
    try:
        season_headers = episodes_container.select('h4.accordion')

        for header in season_headers:
            season_name = ''.join(t.strip() for t in header.find_all(string=True, recursive=False))

            panel = header.find_next_sibling('div', class_='episodio-panel')
            if not panel:
                continue  

            episode_list = panel.select_one('ul.listas-de-episodion')
            episode_items = episode_list.find_all('li') if episode_list else []

            episodes_data = []
            for li in episode_items:
                a_tag = li.select_one('a')
                if not a_tag:
                    continue
                episode_url = BASE_URL + a_tag.get('href', '')
                episode_number = a_tag.select_one('span').get_text(strip=True) if a_tag.select_one('span') else "N/A"
                full_text = a_tag.get_text(strip=True)
                episode_title = full_text.replace(episode_number, '', 1).strip(' -')

                episodes_data.append({
                    'url': episode_url,
                    'numero': episode_number,
                    'titulo': episode_title
                })

            seasons.append({'temporada': season_name, 'episodios': episodes_data})
    except Exception as e:
        print(f"Error obteniendo las temporadas: {e}")

    return {
        'backdrop': backdrop,
        'titulo': titulo,
        'canal': canal,
        'poster': poster,
        'episodios': episodios,
        'idioma': idioma,
        'ano': ano,
        'valoracion': valoracion,
        'resena': resena,
        'seasons': seasons
    }


def get_cartoons_series(base_url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': f"No se pudo conectar con la página: {e}"}

    soup = BeautifulSoup(response.content, 'html.parser')

    total_paginas = 1
    try:
        pagination_container = soup.select_one('ul.pagination')
        pages = [int(item.get_text(strip=True)) for item in pagination_container.find_all('li', class_='page-item') if item.get_text(strip=True).isdigit()]
        total_paginas = max(pages) if pages else 1
    except Exception as e:
        print(f"Error obteniendo total de páginas: {e}")

    series = []
    try:
        series_elements = soup.select('.conjuntos-series a')
        for serie in series_elements:
            url = BASE_URL + serie.get('href', '')
            nombre = serie.select_one('.nombre-serie').text.strip() if serie.select_one('.nombre-serie') else "Desconocido"
            canal = serie.select_one('.marcador.marcadorSeries').text.strip() if serie.select_one('.marcador.marcadorSeries') else "N/A"
            ano = serie.select_one('.marcador-ano').text.strip() if serie.select_one('.marcador-ano') else "N/A"
            valoracion = serie.select_one('.valoracion').text.strip() if serie.select_one('.valoracion') else "N/A"
            imagen = BASE_URL + serie.select_one('img')['src'] if serie.select_one('img') and 'src' in serie.select_one('img').attrs else "Sin imagen"

            series.append({'url': url, 'nombre': nombre, 'canal': canal, 'ano': ano, 'valoracion': valoracion, 'imagen': imagen})
    except Exception as e:
        print(f"Error obteniendo series: {e}")

    return {'paginas': total_paginas, 'cartoons': series}
