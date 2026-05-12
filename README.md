# 🌤️ Weather API

API REST profesional para consultar información meteorológica utilizando OpenWeatherMap, con sistema de caché en Redis, rate limiting, manejo robusto de errores y arquitectura por capas.

---

## 🚀 Stack Tecnológico

- **Python 3.12**
- **FastAPI** - Framework web moderno y de alto rendimiento
- **Pydantic** - Validación de datos y settings management
- **Redis** - Sistema de caché para optimizar rendimiento
- **httpx** - Cliente HTTP asíncrono
- **slowapi** - Rate limiting
- **Uvicorn** - Servidor ASGI

---

## ✨ Características Principales

- ✅ **API REST asíncrona** con endpoints documentados automáticamente (OpenAPI/Swagger)
- ✅ **Sistema de caché con Redis** (TTL de 12 horas, reduce latencia de ~600ms a ~11ms)
- ✅ **Rate limiting** (10 requests por minuto por IP)
- ✅ **Manejo robusto de errores** con excepciones personalizadas y handlers globales
- ✅ **Seguridad mejorada** con sanitización de logs y URLs (no expone API keys)
- ✅ **Arquitectura por capas** (Router → Service → Client)
- ✅ **Logging profesional** con niveles configurables
- ✅ **Validación de entrada** (nombres de ciudad, caracteres permitidos)
- ✅ **Graceful degradation** (continúa funcionando si Redis falla)
- ✅ **Singleton Redis** con `ConnectionPool` para reutilizar conexiones
- ✅ **Lifespan de FastAPI** para inicialización y cierre graceful de recursos
- ✅ **Inyección de dependencias** con FastAPI `Depends`

---

## 📋 Requisitos Previos

- Python 3.12+
- Redis server corriendo (puerto por defecto: 6379, configurable en `.env`)
- API Key de OpenWeatherMap ([obtener gratis aquí](https://openweathermap.org/api))

---

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repo-url>
cd weather-api
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate    # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:

```env
# ===========================================
# Weather API Configuration
# ===========================================
ACCESS_WEATHER_API_KEY=tu_api_key_aqui
ACCESS_URL_BASE_WEATHER_API=https://api.openweathermap.org
ACCESS_PATH_CITY_WEATHER=/data/2.5/weather
ACCESS_WEATHER_LANG=es
ACCESS_WEATHER_UNITS=metric

# ===========================================
# Redis Configuration
# ===========================================
ACCESS_REDIS_HOST=localhost
ACCESS_REDIS_PORT=6379
ACCESS_REDIS_DB=0

# ===========================================
# Cache Configuration
# ===========================================
ACCESS_CACHE_TTL_SECONDS=43200

# ===========================================
# Rate Limiting
# ===========================================
ACCESS_RATE_LIMIT=10/minute
```

### 5. Iniciar Redis
```bash
# Linux/Mac (puerto por defecto)
redis-server

# O con Docker
docker run -d -p 6379:6379 redis:latest

# Si usás un puerto distinto, actualizá ACCESS_REDIS_PORT en .env
```

---

## ▶️ Ejecución

### Modo desarrollo (con hot reload)
```bash
python run.py
```

### Modo producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

---

## 📚 Documentación Interactiva

FastAPI genera documentación automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🌐 Endpoints

### `GET /v1/weather/{city}`

Obtiene información meteorológica actual de una ciudad.

**Parámetros:**
- `city` (path, string, requerido): Nombre de la ciudad

**Respuestas:**

- `200 OK`: Datos meteorológicos exitosos
- `400 Bad Request`: Nombre de ciudad inválido
- `404 Not Found`: Ciudad no encontrada
- `429 Too Many Requests`: Rate limit excedido
- `503 Service Unavailable`: Servicio externo no disponible

**Ejemplos:**

```bash
# Consulta exitosa
curl http://localhost:8000/v1/weather/madrid

# Respuesta
{
  "name": "Madrid",
  "main": {
    "temp": 22.5,
    "feels_like": 21.8,
    "humidity": 65
  },
  "weather": [
    {
      "description": "cielo claro"
    }
  ],
  "wind": {
    "speed": 3.5
  }
}
```

```bash
# Ciudad no encontrada
curl http://localhost:8000/v1/weather/ciudadinventada123

# Respuesta (404)
{
  "Error": "City ciudadinventada123 not found. Please check the city name and try again.",
  "code": "CITY_NOT_FOUND"
}
```

```bash
# Nombre inválido
curl http://localhost:8000/v1/weather/Madrid123$$

# Respuesta (400)
{
  "Error": "Invalid city name: 'Madrid123$$'. City names should only contain letters.",
  "code": "INVALID_CITY_NAME"
}
```

---

## 🏗️ Arquitectura

### Capas

```
┌──────────────────────────────────────────┐
│          weather_router.py               │  ← Endpoints HTTP
│     (Validación, Rate Limiting)          │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│        weather_services.py               │  ← Lógica de negocio
│     (Orquestación, failover graceful)    │
└──────────┬──────────────────┬────────────┘
           │                  │
           ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│ weather_client.py│  │ cache_services.py│  ← Integraciones
│ (OpenWeatherMap) │  │     (Redis)      │
└──────────────────┘  └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │  redis_client.py  │  ← Singleton pool
                      │ (ConnectionPool)  │
                      └──────────────────┘

Manejo de errores centralizado:
  custom_exceptions.py ──► exceptions_handlers.py ──► add_exception_handler()
```

### Componentes Principales

- **Routers**: Definen endpoints y aplican decoradores (rate limit)
- **Services**: Lógica de negocio, orquestación de caché y API externa
- **Clients**: Comunicación con servicios externos (OpenWeatherMap)
- **Models**: Modelos Pydantic para validación de datos
- **Middlewares**: Logging, rate limiting
- **Utils**: Excepciones personalizadas, handlers, seguridad, dependency injection

---

## 📁 Estructura del Proyecto

```
weather-api/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app con lifespan
│   ├── clients/
│   │   ├── weather_client.py        # Cliente OpenWeatherMap
│   │   └── redis_client.py          # Singleton Redis (ConnectionPool)
│   ├── config/
│   │   └── setting_config.py        # Configuración con Pydantic Settings
│   ├── middlewares/
│   │   ├── logging_middleware.py     # Sistema de logs
│   │   └── rate_limit_middleware.py  # Rate limiting con slowapi
│   ├── mocks/
│   │   └── data_mocks.py            # Mock data para testing
│   ├── models/
│   │   └── weather_models.py        # Modelos Pydantic anidados
│   ├── routes/
│   │   └── weather_router.py        # Endpoint GET /v1/weather/{city}
│   ├── services/
│   │   ├── cache_services.py        # Servicio de caché Redis
│   │   └── weather_services.py      # Lógica de negocio
│   └── utils/
│       ├── __init__.py              # Exporta utilidades
│       ├── dependency_utils.py      # Inyección de dependencias (async)
│       ├── security_utils.py        # Enmascaramiento de datos sensibles
│       └── errors/
│           ├── __init__.py
│           ├── custom_exceptions.py    # Excepciones personalizadas
│           └── exceptions_handlers.py  # Handlers globales
├── .env                         # Variables de entorno (no versionar)
├── .env.example                 # Template de variables de entorno
├── .gitignore
├── requirements.txt
├── run.py                       # Script de ejecución (uvicorn)
└── README.md
```

---

## 🔒 Seguridad

- **API Key protegida**: Nunca se expone en logs ni en errores
- **Sanitización de URLs**: Las URLs con query parameters sensibles se enmascaran automáticamente
- **Validación de entrada**: Previene inyección y caracteres inválidos
- **Logging seguro**: Solo información necesaria, sin datos sensibles
- **Rate limiting**: Protección contra abuso (10 req/min por defecto)

---

## 🎯 Manejo de Errores

La API implementa un sistema robusto de manejo de errores con códigos HTTP apropiados:

| Código | Error | Descripción |
|--------|-------|-------------|
| `400` | `INVALID_CITY_NAME` | Nombre de ciudad inválido (vacío, muy largo, caracteres especiales) |
| `404` | `CITY_NOT_FOUND` | Ciudad no encontrada en OpenWeatherMap |
| `429` | Rate Limit | Demasiadas peticiones (esperar 1 minuto) |
| `500` | `CACHE_ERROR` | Error en Redis (la API continúa sin caché) |
| `503` | `EXTERNAL_API_ERROR` | Servicio externo caído o timeout |

---

## 🚀 Rendimiento

- **Sin caché**: ~600ms por request (OpenWeatherMap)
- **Con caché (Redis)**: ~11ms por request (mejora de ~98%)
- **TTL de caché**: 12 horas (configurable)
- **Conexiones Redis**: Singleton con `ConnectionPool` (reutiliza conexiones, sin overhead por request)
- **Rate limit**: 10 requests/minuto/IP (configurable)

---

## 📝 Notas Importantes

- Si Redis no está disponible, la API continúa funcionando **sin caché** (graceful degradation)
- Los logs nunca exponen el API key completo (se muestra como `731d...a14b`)
- Las conexiones a Redis se manejan con un **singleton** via `ConnectionPool` para eficiencia
- La inicialización y cierre de recursos se maneja con el **lifespan** de FastAPI (no hay fugas de conexiones)
- Todas las temperaturas están en **Celsius**
- Los textos meteorológicos están en **español**
- Las variables de entorno se cargan desde `.env` usando `pydantic-settings`

---

## 🤝 Autor

**Leandro Quiroga**

Proyecto desarrollado con Python, FastAPI y arquitecturas backend escalables.
