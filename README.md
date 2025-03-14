# API de Scraping para LaCartoons

## Descripción
Esta API permite extraer información de la página web [LaCartoons](https://www.lacartoons.com/), proporcionando detalles sobre series animadas, capítulos y temporadas disponibles en el sitio.

## Tecnologías Utilizadas
- **FastAPI**: Framework para la construcción de la API.
- **BeautifulSoup**: Para el scraping de la web.
- **Requests**: Para realizar peticiones HTTP.
- **Python 3**: Lenguaje de programación principal.

## Instalación
### 1. Clonar el repositorio
```bash
git clone https://github.com/LuArtD/api_laCartoon.git
cd tu_repositorio
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso
### 1. Ejecutar el servidor
```bash
fastapi dev app.py

```


### 2. Documentación automática de la API
FastAPI genera automáticamente la documentación en los siguientes endpoints:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Disponibles
### 1. Obtener series animadas
**Endpoint:** `GET /cartoons`

**Parámetros:**
- `Titulo` (opcional): Texto para buscar en el título.
- `Categoria_id` (opcional, 1-8): ID de la categoría.
- `page` (opcional): Número de página.

**Ejemplo de uso:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/cartoons?Titulo=Batman&Categoria_id=2&page=1'
```

### 2. Obtener detalles de una serie
**Endpoint:** `GET /cartoons_details`

**Parámetros:**
- `url` (obligatorio): URL de la serie.

**Ejemplo de uso:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/cartoons_details?url=https://www.lacartoons.com/serie/8'
```

### 3. Obtener detalles de un episodio
**Endpoint:** `GET /chapter_details`

**Parámetros:**
- `url` (obligatorio): URL del episodio.

**Ejemplo de uso:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/chapter_details?url=https://www.lacartoons.com/serie/capitulo/485?t=2'
```

## Estructura del Proyecto
```
📁 tu_repositorio/
├── 📂 scrapper/
│   ├── la_cartoon_scrap.py  # Contiene las funciones de scraping
├── app.py                  # Archivo principal con los endpoints
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Documentación
```

## Contribución
1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva`).
3. Realiza tus cambios y haz un commit (`git commit -m 'Descripción del cambio'`).
4. Sube los cambios a tu fork (`git push origin feature-nueva`).
5. Crea un Pull Request en el repositorio principal.

## Derechos de la informacion
Los derechos de la informacion pertenecen a sus respectivos usuarios, este proyecto es solo con fines didacticos

## Licencia
Este proyecto está bajo la licencia MIT.

