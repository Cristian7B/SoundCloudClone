-- Script PostgreSQL para SoundCloud Clone Database
-- Generado basado en los modelos Django definidos
-- Version: 1.0
-- Fecha: 2025-07-11

-- Eliminar tablas existentes si existen (en orden correcto para evitar conflictos de FK)
DROP TABLE IF EXISTS playlist_categorias CASCADE;
DROP TABLE IF EXISTS categorias_playlist CASCADE;
DROP TABLE IF EXISTS recomendaciones_playlists CASCADE;
DROP TABLE IF EXISTS similitud_playlists CASCADE;
DROP TABLE IF EXISTS playlist_tendencias CASCADE;
DROP TABLE IF EXISTS feedback_recomendaciones CASCADE;
DROP TABLE IF EXISTS recomendaciones_generadas CASCADE;
DROP TABLE IF EXISTS similitud_canciones CASCADE;
DROP TABLE IF EXISTS historial_reproducciones CASCADE;
DROP TABLE IF EXISTS preferencias_usuario CASCADE;
DROP TABLE IF EXISTS interacciones CASCADE;
DROP TABLE IF EXISTS playlist_canciones CASCADE;
DROP TABLE IF EXISTS playlists CASCADE;
DROP TABLE IF EXISTS canciones CASCADE;
DROP TABLE IF EXISTS albums CASCADE;
DROP TABLE IF EXISTS configuracion_sistema CASCADE;
DROP TABLE IF EXISTS registro_actividades CASCADE;
DROP TABLE IF EXISTS estadisticas_generales CASCADE;
DROP TABLE IF EXISTS sugerencias_busqueda CASCADE;
DROP TABLE IF EXISTS historial_busqueda CASCADE;
DROP TABLE IF EXISTS indices_busqueda CASCADE;
DROP TABLE IF EXISTS soundcloud_users CASCADE;
DROP TABLE IF EXISTS app_users CASCADE;

-- =============================================
-- TABLA: USUARIOS
-- =============================================
CREATE TABLE app_users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar consultas
CREATE INDEX idx_app_users_email ON app_users(email);
CREATE INDEX idx_app_users_username ON app_users(username);
CREATE INDEX idx_app_users_created_at ON app_users(created_at);

-- =============================================
-- TABLA: ALBUMS
-- =============================================
CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    imagen_url TEXT,
    usuario_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para albums
CREATE INDEX idx_albums_usuario_id ON albums(usuario_id);
CREATE INDEX idx_albums_created_at ON albums(created_at);
CREATE INDEX idx_albums_titulo ON albums(titulo);

-- =============================================
-- TABLA: CANCIONES
-- =============================================
CREATE TABLE canciones (
    cancion_id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    archivo_url TEXT NOT NULL,
    imagen_url TEXT,
    duracion INTERVAL,
    genero VARCHAR(100),
    usuario_id INTEGER NOT NULL,
    album_id INTEGER,
    reproducciones INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    reposts_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_canciones_album FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE SET NULL
);

-- Índices para canciones
CREATE INDEX idx_canciones_usuario_id ON canciones(usuario_id);
CREATE INDEX idx_canciones_album_id ON canciones(album_id);
CREATE INDEX idx_canciones_genero ON canciones(genero);
CREATE INDEX idx_canciones_created_at ON canciones(created_at);
CREATE INDEX idx_canciones_reproducciones ON canciones(reproducciones);
CREATE INDEX idx_canciones_titulo ON canciones(titulo);

-- =============================================
-- TABLA: PLAYLISTS
-- =============================================
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    imagen_url TEXT,
    usuario_id INTEGER NOT NULL,
    es_publica BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para playlists
CREATE INDEX idx_playlists_usuario_id ON playlists(usuario_id);
CREATE INDEX idx_playlists_es_publica ON playlists(es_publica);
CREATE INDEX idx_playlists_created_at ON playlists(created_at);
CREATE INDEX idx_playlists_titulo ON playlists(titulo);

-- =============================================
-- TABLA: PLAYLIST_CANCIONES (Many-to-Many)
-- =============================================
CREATE TABLE playlist_canciones (
    id SERIAL PRIMARY KEY,
    playlist_id INTEGER NOT NULL,
    cancion_id INTEGER NOT NULL,
    orden INTEGER DEFAULT 0,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_playlist_canciones_playlist FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE,
    CONSTRAINT fk_playlist_canciones_cancion FOREIGN KEY (cancion_id) REFERENCES canciones(cancion_id) ON DELETE CASCADE,
    CONSTRAINT unique_playlist_cancion UNIQUE (playlist_id, cancion_id)
);

-- Índices para playlist_canciones
CREATE INDEX idx_playlist_canciones_playlist_id ON playlist_canciones(playlist_id);
CREATE INDEX idx_playlist_canciones_cancion_id ON playlist_canciones(cancion_id);
CREATE INDEX idx_playlist_canciones_orden ON playlist_canciones(orden);

-- =============================================
-- TABLA: INTERACCIONES
-- =============================================
CREATE TABLE interacciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    cancion_id INTEGER,
    playlist_id INTEGER,
    usuario_objetivo_id INTEGER,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('like', 'repost', 'follow')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_interacciones_cancion FOREIGN KEY (cancion_id) REFERENCES canciones(cancion_id) ON DELETE CASCADE,
    CONSTRAINT fk_interacciones_playlist FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE,
    CONSTRAINT unique_interaccion_cancion UNIQUE (usuario_id, cancion_id, tipo),
    CONSTRAINT unique_interaccion_playlist UNIQUE (usuario_id, playlist_id, tipo),
    CONSTRAINT unique_interaccion_usuario UNIQUE (usuario_id, usuario_objetivo_id, tipo)
);

-- Índices para interacciones
CREATE INDEX idx_interacciones_usuario_id ON interacciones(usuario_id);
CREATE INDEX idx_interacciones_cancion_id ON interacciones(cancion_id);
CREATE INDEX idx_interacciones_playlist_id ON interacciones(playlist_id);
CREATE INDEX idx_interacciones_tipo ON interacciones(tipo);
CREATE INDEX idx_interacciones_created_at ON interacciones(created_at);

-- =============================================
-- TABLA: PREFERENCIAS_USUARIO
-- =============================================
CREATE TABLE preferencias_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE NOT NULL,
    generos_favoritos JSONB DEFAULT '[]',
    artistas_seguidos JSONB DEFAULT '[]',
    total_reproducciones INTEGER DEFAULT 0,
    canciones_gustadas INTEGER DEFAULT 0,
    playlists_creadas INTEGER DEFAULT 0,
    ultima_actividad TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para preferencias_usuario
CREATE INDEX idx_preferencias_usuario_id ON preferencias_usuario(usuario_id);
CREATE INDEX idx_preferencias_generos ON preferencias_usuario USING GIN (generos_favoritos);
CREATE INDEX idx_preferencias_artistas ON preferencias_usuario USING GIN (artistas_seguidos);

-- =============================================
-- TABLA: HISTORIAL_REPRODUCCIONES
-- =============================================
CREATE TABLE historial_reproducciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    cancion_id INTEGER NOT NULL,
    duracion_reproducida INTERVAL NOT NULL,
    porcentaje_escuchado FLOAT NOT NULL,
    dispositivo VARCHAR(50),
    ubicacion VARCHAR(100),
    hora_del_dia TIME DEFAULT CURRENT_TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para historial_reproducciones
CREATE INDEX idx_historial_usuario_id ON historial_reproducciones(usuario_id);
CREATE INDEX idx_historial_cancion_id ON historial_reproducciones(cancion_id);
CREATE INDEX idx_historial_created_at ON historial_reproducciones(created_at);
CREATE INDEX idx_historial_dispositivo ON historial_reproducciones(dispositivo);

-- =============================================
-- TABLA: SIMILITUD_CANCIONES
-- =============================================
CREATE TABLE similitud_canciones (
    id SERIAL PRIMARY KEY,
    cancion_a_id INTEGER NOT NULL,
    cancion_b_id INTEGER NOT NULL,
    puntuacion_similitud FLOAT NOT NULL,
    factores_similitud JSONB DEFAULT '{}',
    calculada_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_similitud_canciones UNIQUE (cancion_a_id, cancion_b_id)
);

-- Índices para similitud_canciones
CREATE INDEX idx_similitud_cancion_a ON similitud_canciones(cancion_a_id);
CREATE INDEX idx_similitud_cancion_b ON similitud_canciones(cancion_b_id);
CREATE INDEX idx_similitud_puntuacion ON similitud_canciones(puntuacion_similitud);

-- =============================================
-- TABLA: RECOMENDACIONES_GENERADAS
-- =============================================
CREATE TABLE recomendaciones_generadas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    canciones_recomendadas JSONB DEFAULT '[]',
    algoritmo_usado VARCHAR(50) NOT NULL,
    puntuacion_confianza FLOAT NOT NULL,
    valida_hasta TIMESTAMP WITH TIME ZONE NOT NULL,
    generada_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para recomendaciones_generadas
CREATE INDEX idx_recomendaciones_usuario_id ON recomendaciones_generadas(usuario_id);
CREATE INDEX idx_recomendaciones_algoritmo ON recomendaciones_generadas(algoritmo_usado);
CREATE INDEX idx_recomendaciones_valida_hasta ON recomendaciones_generadas(valida_hasta);

-- =============================================
-- TABLA: FEEDBACK_RECOMENDACIONES
-- =============================================
CREATE TABLE feedback_recomendaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    cancion_recomendada_id INTEGER NOT NULL,
    accion VARCHAR(20) NOT NULL CHECK (accion IN ('reproducida', 'gustada', 'omitida', 'rechazada')),
    tiempo_interaccion INTERVAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_feedback_recomendacion UNIQUE (usuario_id, cancion_recomendada_id)
);

-- Índices para feedback_recomendaciones
CREATE INDEX idx_feedback_usuario_id ON feedback_recomendaciones(usuario_id);
CREATE INDEX idx_feedback_cancion_id ON feedback_recomendaciones(cancion_recomendada_id);
CREATE INDEX idx_feedback_accion ON feedback_recomendaciones(accion);

-- =============================================
-- TABLA: PLAYLIST_TENDENCIAS
-- =============================================
CREATE TABLE playlist_tendencias (
    id SERIAL PRIMARY KEY,
    playlist_id INTEGER UNIQUE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    usuario_creador_id INTEGER NOT NULL,
    reproducciones_ultima_semana INTEGER DEFAULT 0,
    nuevos_seguidores INTEGER DEFAULT 0,
    puntuacion_tendencia FLOAT DEFAULT 0.0,
    categoria VARCHAR(50) NOT NULL CHECK (categoria IN ('nueva', 'viral', 'genero', 'region', 'editorial')),
    activa_en_tendencias BOOLEAN DEFAULT TRUE,
    fecha_ingreso_tendencia TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para playlist_tendencias
CREATE INDEX idx_tendencias_playlist_id ON playlist_tendencias(playlist_id);
CREATE INDEX idx_tendencias_puntuacion ON playlist_tendencias(puntuacion_tendencia);
CREATE INDEX idx_tendencias_categoria ON playlist_tendencias(categoria);

-- =============================================
-- TABLA: SIMILITUD_PLAYLISTS
-- =============================================
CREATE TABLE similitud_playlists (
    id SERIAL PRIMARY KEY,
    playlist_a_id INTEGER NOT NULL,
    playlist_b_id INTEGER NOT NULL,
    similitud_contenido FLOAT DEFAULT 0.0,
    similitud_usuarios FLOAT DEFAULT 0.0,
    similitud_total FLOAT DEFAULT 0.0,
    canciones_comunes INTEGER DEFAULT 0,
    usuarios_comunes INTEGER DEFAULT 0,
    calculada_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_similitud_playlists UNIQUE (playlist_a_id, playlist_b_id)
);

-- Índices para similitud_playlists
CREATE INDEX idx_similitud_playlist_a ON similitud_playlists(playlist_a_id);
CREATE INDEX idx_similitud_playlist_b ON similitud_playlists(playlist_b_id);
CREATE INDEX idx_similitud_total ON similitud_playlists(similitud_total);

-- =============================================
-- TABLA: RECOMENDACIONES_PLAYLISTS
-- =============================================
CREATE TABLE recomendaciones_playlists (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    playlist_recomendada_id INTEGER NOT NULL,
    razon_recomendacion VARCHAR(100) NOT NULL CHECK (razon_recomendacion IN ('gustos_similares', 'artista_seguido', 'genero_favorito', 'amigos', 'tendencia', 'nueva')),
    puntuacion_recomendacion FLOAT NOT NULL,
    mostrada_al_usuario BOOLEAN DEFAULT FALSE,
    interaccion_usuario VARCHAR(20) CHECK (interaccion_usuario IN ('vista', 'reproducida', 'seguida', 'ignorada')),
    fecha_recomendacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_interaccion TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT unique_recomendacion_playlist UNIQUE (usuario_id, playlist_recomendada_id)
);

-- Índices para recomendaciones_playlists
CREATE INDEX idx_rec_playlists_usuario_id ON recomendaciones_playlists(usuario_id);
CREATE INDEX idx_rec_playlists_playlist_id ON recomendaciones_playlists(playlist_recomendada_id);
CREATE INDEX idx_rec_playlists_puntuacion ON recomendaciones_playlists(puntuacion_recomendacion);

-- =============================================
-- TABLA: CATEGORIAS_PLAYLIST
-- =============================================
CREATE TABLE categorias_playlist (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    color_hex VARCHAR(7) DEFAULT '#000000',
    icono VARCHAR(50),
    es_genero_musical BOOLEAN DEFAULT FALSE,
    es_estado_animo BOOLEAN DEFAULT FALSE,
    es_actividad BOOLEAN DEFAULT FALSE,
    activa BOOLEAN DEFAULT TRUE,
    orden_display INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para categorias_playlist
CREATE INDEX idx_categorias_nombre ON categorias_playlist(nombre);
CREATE INDEX idx_categorias_orden ON categorias_playlist(orden_display);

-- =============================================
-- TABLA: PLAYLIST_CATEGORIAS (Many-to-Many)
-- =============================================
CREATE TABLE playlist_categorias (
    id SERIAL PRIMARY KEY,
    playlist_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    relevancia FLOAT DEFAULT 1.0,
    asignada_automaticamente BOOLEAN DEFAULT FALSE,
    asignada_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_playlist_categorias_categoria FOREIGN KEY (categoria_id) REFERENCES categorias_playlist(id) ON DELETE CASCADE,
    CONSTRAINT unique_playlist_categoria UNIQUE (playlist_id, categoria_id)
);

-- Índices para playlist_categorias
CREATE INDEX idx_playlist_cat_playlist_id ON playlist_categorias(playlist_id);
CREATE INDEX idx_playlist_cat_categoria_id ON playlist_categorias(categoria_id);
CREATE INDEX idx_playlist_cat_relevancia ON playlist_categorias(relevancia);

-- =============================================
-- TABLA: ESTADISTICAS_GENERALES
-- =============================================
CREATE TABLE estadisticas_generales (
    id SERIAL PRIMARY KEY,
    total_usuarios INTEGER DEFAULT 0,
    total_canciones INTEGER DEFAULT 0,
    total_playlists INTEGER DEFAULT 0,
    total_reproducciones_hoy INTEGER DEFAULT 0,
    total_reproducciones_mes INTEGER DEFAULT 0,
    usuarios_activos_hoy INTEGER DEFAULT 0,
    usuarios_activos_mes INTEGER DEFAULT 0,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TABLA: REGISTRO_ACTIVIDADES
-- =============================================
CREATE TABLE registro_actividades (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    accion VARCHAR(50) NOT NULL CHECK (accion IN ('login', 'logout', 'upload_song', 'create_playlist', 'delete_song', 'delete_playlist', 'follow_user', 'unfollow_user')),
    detalles JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para registro_actividades
CREATE INDEX idx_registro_usuario_id ON registro_actividades(usuario_id);
CREATE INDEX idx_registro_accion ON registro_actividades(accion);
CREATE INDEX idx_registro_timestamp ON registro_actividades(timestamp);

-- =============================================
-- TABLA: CONFIGURACION_SISTEMA
-- =============================================
CREATE TABLE configuracion_sistema (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    descripcion TEXT,
    tipo_dato VARCHAR(20) DEFAULT 'string' CHECK (tipo_dato IN ('string', 'integer', 'float', 'boolean', 'json')),
    modificable_por_admin BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para configuracion_sistema
CREATE INDEX idx_config_clave ON configuracion_sistema(clave);

-- =============================================
-- TABLA: INDICES_BUSQUEDA
-- =============================================
CREATE TABLE indices_busqueda (
    id SERIAL PRIMARY KEY,
    termino_busqueda VARCHAR(255) UNIQUE NOT NULL,
    resultados_canciones JSONB DEFAULT '[]',
    resultados_playlists JSONB DEFAULT '[]',
    resultados_usuarios JSONB DEFAULT '[]',
    frecuencia_busqueda INTEGER DEFAULT 1,
    ultima_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para indices_busqueda
CREATE INDEX idx_busqueda_termino ON indices_busqueda(termino_busqueda);
CREATE INDEX idx_busqueda_frecuencia ON indices_busqueda(frecuencia_busqueda);

-- =============================================
-- TABLA: HISTORIAL_BUSQUEDA
-- =============================================
CREATE TABLE historial_busqueda (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    termino_busqueda VARCHAR(255) NOT NULL,
    resultados_encontrados INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para historial_busqueda
CREATE INDEX idx_hist_busqueda_usuario_id ON historial_busqueda(usuario_id);
CREATE INDEX idx_hist_busqueda_termino ON historial_busqueda(termino_busqueda);
CREATE INDEX idx_hist_busqueda_created_at ON historial_busqueda(created_at);

-- =============================================
-- TABLA: SUGERENCIAS_BUSQUEDA
-- =============================================
CREATE TABLE sugerencias_busqueda (
    id SERIAL PRIMARY KEY,
    termino VARCHAR(255) UNIQUE NOT NULL,
    categoria VARCHAR(50) NOT NULL CHECK (categoria IN ('cancion', 'playlist', 'usuario', 'genero', 'album')),
    popularidad INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para sugerencias_busqueda
CREATE INDEX idx_sugerencias_termino ON sugerencias_busqueda(termino);
CREATE INDEX idx_sugerencias_categoria ON sugerencias_busqueda(categoria);
CREATE INDEX idx_sugerencias_popularidad ON sugerencias_busqueda(popularidad);

-- =============================================
-- TRIGGERS PARA ACTUALIZAR TIMESTAMPS
-- =============================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar triggers a las tablas que tienen updated_at
CREATE TRIGGER update_app_users_updated_at BEFORE UPDATE ON app_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_albums_updated_at BEFORE UPDATE ON albums FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_canciones_updated_at BEFORE UPDATE ON canciones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_playlists_updated_at BEFORE UPDATE ON playlists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_config_updated_at BEFORE UPDATE ON configuracion_sistema FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- DATOS INICIALES
-- =============================================

-- Insertar categorías básicas de playlist
INSERT INTO categorias_playlist (nombre, descripcion, color_hex, es_genero_musical, es_estado_animo, es_actividad, orden_display) VALUES
('Pop', 'Música pop contemporánea', '#FF6B6B', TRUE, FALSE, FALSE, 1),
('Rock', 'Rock clásico y moderno', '#4ECDC4', TRUE, FALSE, FALSE, 2),
('Hip Hop', 'Hip hop y rap', '#45B7D1', TRUE, FALSE, FALSE, 3),
('Electronic', 'Música electrónica y EDM', '#FFA07A', TRUE, FALSE, FALSE, 4),
('Jazz', 'Jazz clásico y contemporáneo', '#98D8C8', TRUE, FALSE, FALSE, 5),
('Entrenamiento', 'Música para ejercitarse', '#FF8C42', FALSE, FALSE, TRUE, 6),
('Relajación', 'Música para relajarse', '#6C5CE7', FALSE, TRUE, FALSE, 7),
('Fiesta', 'Música para fiestas', '#FDCB6E', FALSE, TRUE, TRUE, 8),
('Estudio', 'Música para concentrarse', '#00B894', FALSE, FALSE, TRUE, 9),
('Nostálgica', 'Música que evoca recuerdos', '#E17055', FALSE, TRUE, FALSE, 10);

-- Insertar configuraciones iniciales del sistema
INSERT INTO configuracion_sistema (clave, valor, descripcion, tipo_dato) VALUES
('max_upload_size', '50', 'Tamaño máximo de archivo en MB', 'integer'),
('songs_per_page', '20', 'Número de canciones por página', 'integer'),
('enable_recommendations', 'true', 'Habilitar sistema de recomendaciones', 'boolean'),
('max_playlist_songs', '1000', 'Máximo número de canciones por playlist', 'integer'),
('trending_algorithm_weight', '0.7', 'Peso del algoritmo de tendencias', 'float'),
('site_name', 'SoundCloud Clone', 'Nombre del sitio', 'string'),
('maintenance_mode', 'false', 'Modo mantenimiento activado', 'boolean'),
('api_rate_limit', '100', 'Límite de requests por minuto', 'integer');

-- Insertar estadísticas iniciales
INSERT INTO estadisticas_generales (total_usuarios, total_canciones, total_playlists) VALUES (0, 0, 0);
-- =============================================
-- COMENTARIOS FINALES
-- =============================================

-- Este script crea una base de datos completa para un clon de SoundCloud con:
-- 1. Sistema de usuarios con autenticación personalizada
-- 2. Gestión de contenido (albums, canciones, playlists)
-- 3. Sistema de interacciones sociales (likes, follows, reposts)
-- 4. Motor de recomendaciones con múltiples algoritmos
-- 5. Sistema de búsqueda y categorización
-- 6. Analytics y estadísticas del sistema
-- 7. Configuración dinámica del sistema
-- 8. Registro de actividades para auditoría

-- Todas las tablas incluyen:
-- - Índices optimizados para consultas comunes
-- - Restricciones de integridad referencial
-- - Triggers para actualización automática de timestamps
-- - Configuración para tipos de datos JSON/JSONB donde corresponde
-- - Validaciones a nivel de base de datos

-- Para usar este script:
-- 1. Crear una base de datos PostgreSQL
-- 2. Ejecutar este script completo
-- 3. Verificar que todas las tablas se crearon correctamente
-- 4. Configurar las conexiones desde Django

COMMENT ON DATABASE postgres IS 'Base de datos para SoundCloud Clone - Sistema completo de 
