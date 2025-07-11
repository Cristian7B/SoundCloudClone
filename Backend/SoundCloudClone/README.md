# SoundCloud Clone - Backend API

Un clon completo de SoundCloud desarrollado con Django y Django REST Framework, que proporciona una API robusta para una plataforma de streaming de música con características sociales.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [API Endpoints](#api-endpoints)
- [Modelos de Datos](#modelos-de-datos)
- [Autenticación](#autenticación)
- [Funcionalidades](#funcionalidades)
- [Desarrollo](#desarrollo)
- [Deployment](#deployment)
- [Contribuir](#contribuir)

## 🚀 Características

### Gestión de Usuarios
- ✅ Registro de usuarios con verificación por email
- ✅ Autenticación basada en JWT
- ✅ Gestión completa de perfiles de usuario
- ✅ Sistema de notificaciones por email

### Gestión de Contenido Musical
- ✅ Subida y gestión de canciones
- ✅ Creación y gestión de álbumes
- ✅ Playlists personalizadas con ordenamiento manual
- ✅ Metadatos completos (género, duración, descripciones)

### Características Sociales
- ✅ Sistema de likes para canciones y playlists
- ✅ Reposts de contenido
- ✅ Sistema de seguimiento entre usuarios
- ✅ Estadísticas de engagement en tiempo real

### Búsqueda y Descubrimiento
- ✅ Búsqueda en tiempo real de canciones y playlists
- ✅ Historial de búsquedas
- ✅ Sugerencias de búsqueda
- ✅ Indexación inteligente de términos

### Recomendaciones
- ✅ Sistema de recomendaciones de canciones
- ✅ Sugerencias de playlists personalizadas
- ✅ Algoritmos de descubrimiento de contenido

## 🏗️ Arquitectura

El proyecto está organizado en módulos Django especializados:

```
SoundCloudClone/
├── apiAutenticacion/        # Autenticación y gestión de usuarios
├── apiPersistencia/         # Gestión de contenido musical
├── apiBuscar/              # Funcionalidad de búsqueda
├── apiDatabase/            # Utilidades de base de datos
├── apiSugerenciaCanciones/ # Recomendaciones de canciones
├── apiSugerenciaPlaylists/ # Recomendaciones de playlists
└── SoundCloudClone/        # Configuración principal del proyecto
```

### Tecnologías Utilizadas

- **Backend Framework**: Django 5.2.3
- **API Framework**: Django REST Framework
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (django-rest-framework-simplejwt)
- **Email**: Gmail SMTP / Console Backend
- **CORS**: django-cors-headers

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL 12+
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd SoundCloudClone/Backend/SoundCloudClone
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

## ⚙️ Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DB_NAME=soundcloudclone_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Email (Gmail)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Para desarrollo, usar console backend:
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Configuración de Email

Para Gmail SMTP:
1. Habilitar verificación en 2 pasos
2. Generar contraseña de aplicación
3. Usar la contraseña de aplicación en `EMAIL_HOST_PASSWORD`

Para desarrollo:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 🔌 API Endpoints

### Autenticación (`/api/auth/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/register/` | Registro de usuario | No |
| POST | `/login/` | Inicio de sesión | No |
| GET | `/profile/` | Perfil del usuario | Sí |
| PUT/PATCH | `/update-info/` | Actualizar perfil | Sí |
| POST | `/logout/` | Cerrar sesión | No |
| POST | `/token/refresh/` | Renovar token | No |
| GET | `/usuarios/{id}/nombre/` | Info básica de usuario | No |

### Contenido Musical (`/api/contenido/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET/POST | `/canciones/` | Listar/crear canciones | GET: No, POST: Sí |
| GET | `/canciones/{id}/` | Detalle de canción | No |
| GET | `/albums/` | Listar álbumes | No |
| POST | `/albums/` | Crear álbum | Sí |
| GET/POST | `/playlists/` | Listar/crear playlists | GET: No, POST: Sí |
| POST | `/playlists/{id}/agregar-cancion/` | Agregar canción | Sí |
| DELETE | `/playlists/{id}/quitar-cancion/` | Quitar canción | Sí |
| POST | `/playlists/{id}/reordenar/` | Reordenar canciones | Sí |

### Interacciones Sociales (`/api/contenido/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/interacciones/` | Crear interacción | Sí |
| POST | `/interacciones/toggle/` | Toggle like/repost/follow | Sí |
| GET | `/usuarios/{id}/canciones/` | Canciones de usuario | No |
| GET | `/usuarios/{id}/playlists/` | Playlists de usuario | No |
| GET | `/usuarios/{id}/stats/` | Estadísticas de usuario | No |

### Búsqueda (`/api/buscar/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/?q=termino` | Buscar contenido | No |
| GET | `/sugerencias/` | Sugerencias de búsqueda | No |

## 📊 Modelos de Datos

### Usuario (AppUser)
- Extiende el modelo de usuario de Django
- Campos adicionales: `nombre`, `user_id`, timestamps
- Autenticación por email

### Contenido Musical
- **Album**: Contenedor de canciones con metadatos
- **Cancion**: Contenido musical principal con estadísticas
- **Playlist**: Listas personalizadas de canciones
- **PlaylistCancion**: Relación muchos-a-muchos con ordenamiento

### Interacciones Sociales
- **Interaccion**: Modelo unificado para likes, reposts y follows
- Constraints únicos para prevenir duplicados
- Contadores desnormalizados para rendimiento

### Búsqueda y Analytics
- **IndicesBusqueda**: Indexación de términos de búsqueda
- **HistorialBusqueda**: Historial de búsquedas por usuario
- **SugerenciasBusqueda**: Sugerencias curadas

## 🔐 Autenticación

### JWT (JSON Web Tokens)

El sistema utiliza JWT para autenticación stateless:

- **Access Token**: 60 minutos de vida
- **Refresh Token**: 1 día de vida
- **Rotación**: Los refresh tokens se rotan en cada uso
- **Blacklisting**: Tokens invalidados en logout

### Flujo de Autenticación

1. Usuario se registra/logea → Recibe access + refresh token
2. Requests autenticados usan: `Authorization: Bearer <access_token>`
3. Al expirar access token → Usar refresh token para obtener nuevos tokens
4. Al hacer logout → Refresh token se añade a blacklist

## 🎵 Funcionalidades

### Gestión de Playlists
- Creación de playlists públicas/privadas
- Adición/eliminación de canciones
- Reordenamiento manual de canciones
- Estadísticas de reproducción

### Sistema Social
- Likes y reposts con toggle automático
- Sistema de seguimiento entre usuarios
- Estadísticas en tiempo real
- Feed de actividad social

### Búsqueda Inteligente
- Búsqueda en tiempo real con debouncing
- Indexación de términos populares
- Historial personal de búsquedas
- Sugerencias categorizadas

### Email Notifications
- Email de bienvenida al registrarse
- Manejo robusto de encoding internacional
- Fallback para sistemas con limitaciones ASCII
- Configuración flexible (SMTP/Console)

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Limpiar base de datos (desarrollo)
python manage.py flush
```

### Estructura de Archivos

```
app/
├── models.py          # Modelos de datos
├── serializers.py     # Serializers DRF
├── views.py          # Vistas de API
├── urls.py           # Configuración de URLs
├── admin.py          # Configuración del admin
├── apps.py           # Configuración de la app
└── migrations/       # Migraciones de base de datos
```

### Estilo de Código

- Documentación estilo Javadoc en todos los módulos
- Naming conventions consistentes
- Separación clara de responsabilidades
- Manejo robusto de errores

## 🚀 Deployment

### Configuración de Producción

1. **Variables de entorno**
```bash
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
SECRET_KEY=tu-secret-key-segura
```

2. **Base de datos**
```bash
# Configurar PostgreSQL en producción
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

3. **Archivos estáticos**
```bash
python manage.py collectstatic
```

4. **CORS para frontend**
```python
CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend.com",
]
```

### Opciones de Deployment

- **ASGI**: Para aplicaciones con alta concurrencia
- **WSGI**: Para deployment tradicional
- **Docker**: Containerización disponible
- **Cloud**: Compatible con AWS, GCP, Azure

## 🤝 Contribuir

### Flujo de Contribución

1. Fork del repositorio
2. Crear branch para feature: `git checkout -b feature/nueva-caracteristica`
3. Commit cambios: `git commit -m 'Agregar nueva característica'`
4. Push al branch: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

### Estándares

- Documentar todas las funciones y clases
- Incluir tests para nuevas funcionalidades
- Seguir convenciones de naming del proyecto
- Actualizar documentación cuando sea necesario

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Development Team** - Desarrollo inicial

## 🙏 Agradecimientos

- Django y Django REST Framework communities
- Contributors del proyecto
- Inspiración del diseño original de SoundCloud

---

**Versión**: 1.0  
**Estado**: En desarrollo activo  
**Última actualización**: Julio 2025
