/**
 * @fileoverview Componente principal de la biblioteca que muestra las canciones
 * más recientes de los usuarios seguidos con información completa de cada track.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import { useEffect, useState } from "react";
import styles from "../Styles/Library.module.css";
import { AudioCard } from "./AudioCard";
import axios from "axios";

/**
 * Componente que renderiza la biblioteca de música con las últimas canciones
 * @component
 * @returns {JSX.Element} Página de biblioteca con lista de canciones
 * 
 * @example
 * <Library />
 */
export function Library() {
    /** Estado para almacenar las canciones obtenidas de la API */
    const [tracks, setTracks] = useState([]);
    
    /** Cache de información de usuarios para evitar llamadas repetidas */
    const [users, setUsers] = useState({});
    
    /** Estado para controlar el estado de carga */
    const [loading, setLoading] = useState(true);
    
    /** Estado para manejar errores en la carga de datos */
    const [error, setError] = useState(null);

    useEffect(() => {
        /**
         * Obtiene información de un usuario específico
         * @async
         * @function
         * @param {string|number} userId - ID del usuario
         * @returns {Promise<Object>} Información del usuario
         */
        const fetchUser = async (userId) => {
            try {
                if (users[userId]) {
                    return users[userId]; // Retornar del cache si ya existe
                }

                const response = await axios.get(`http://127.0.0.1:8000/api/auth/usuarios/${userId}/nombre/`);
                const userData = response.data;
                
                // Actualizar cache de usuarios
                setUsers(prev => ({
                    ...prev,
                    [userId]: userData
                }));
                
                return userData;
            } catch (err) {
                console.error(`Error fetching user ${userId}:`, err);
                return { nombre: `Usuario ${userId}`, username: `user${userId}` }; // Fallback
            }
        };

        /**
         * Obtiene todas las canciones desde la API
         * @async
         * @function
         */
        const fetchTracks = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/contenido/canciones/");
                console.log("response.data:", response.data);
                const data = Array.isArray(response.data) ? response.data : [];
                setTracks(data);

                // Obtener información de usuarios únicos
                const uniqueUserIds = [...new Set(data.map(track => track.usuario_id))];
                const userPromises = uniqueUserIds.map(fetchUser);
                await Promise.all(userPromises);
                
            } catch (err) {
                console.error("Error fetching tracks:", err);
                setError("No se pudo cargar la biblioteca.");
            } finally {
                setLoading(false);
            }
        };

        fetchTracks();
    }, [users]);

    // Handlers para las interacciones con las canciones
    const handlePlayPause = (id) => console.log(`Play/Pause clicked for track ${id}`);
    const handleLike = (id) => console.log(`Like clicked for track ${id}`);
    const handleRepost = (id) => console.log(`Repost clicked for track ${id}`);
    const handleShare = (id) => console.log(`Share clicked for track ${id}`);
    const handleCopy = (id) => console.log(`Copy link clicked for track ${id}`);
    const handleMore = (id) => console.log(`More options clicked for track ${id}`);

    return (
        <div className={styles.libraryContainer}>
            {/* Encabezado de la biblioteca */}
            <section className={styles.libraryHeader}>
                <h1>Escucha los últimos posts de la gente a la que sigues:</h1>
            </section>

            {/* Estados de carga y error */}
            {loading && <p>Cargando...</p>}
            {error && <p>{error}</p>}

            {/* Mensaje cuando no hay canciones */}
            {!loading && !error && Array.isArray(tracks) && tracks.length === 0 && (
                <p>No se encontraron pistas.</p>
            )}

            {/* Lista de canciones */}
            {!loading && !error && Array.isArray(tracks) && tracks.length > 0 && (
                tracks.map((track) => (
                    <section key={track.cancion_id} className={styles.trackSection}>
                        <AudioCard
                            cancionId={track.cancion_id}
                            userName={users[track.usuario_id]?.nombre || `Usuario ${track.usuario_id}`}
                            trackTitle={track.titulo}
                            albumCover={track.imagen_url}
                            timeAgo={new Date(track.created_at).toLocaleDateString()}
                            likes={track.likes_count}
                            url={track.archivo_url}
                            reposts={track.reposts_count}
                            plays={track.reproducciones}
                            comments={0} // Comments not provided in API
                            tags={[track.genero, track.album_titulo]}
                            isPlaying={false}
                            onPlayPause={() => handlePlayPause(track.cancion_id)}
                            onLike={() => handleLike(track.cancion_id)}
                            onRepost={() => handleRepost(track.cancion_id)}
                            onShare={() => handleShare(track.cancion_id)}
                            onCopy={() => handleCopy(track.cancion_id)}
                            onMore={() => handleMore(track.cancion_id)}
                        />
                        <hr className={styles.divider} />
                    </section>
                ))
            )}
        </div>
    );
}
