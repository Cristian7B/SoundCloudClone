/**
 * @fileoverview Componente que muestra la sección "BlockBuster" con playlists
 * destacadas y recomendaciones personalizadas en la página de inicio.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import styles from "../Styles/BlockBuster.module.css";
import { PlaylistCard } from "../../generalComponents/components/PlaylistCard";

/**
 * Componente que renderiza la sección BlockBuster con playlists destacadas
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Array} [props.playlists=[]] - Array de playlists para mostrar
 * @param {string} props.playlists[].playlist_id - ID único de la playlist
 * @param {string} props.playlists[].imagen_url - URL de la imagen de portada
 * @param {string} props.playlists[].titulo - Título de la playlist
 * @param {string} props.playlists[].descripcion - Descripción de la playlist
 * @param {number} props.playlists[].total_canciones - Número total de canciones
 * @returns {JSX.Element} Sección BlockBuster con grid de playlists
 * 
 * @example
 * const playlists = [
 *   {
 *     playlist_id: "1",
 *     imagen_url: "/imagen.jpg",
 *     titulo: "Top Hits",
 *     descripcion: "Lo más popular",
 *     total_canciones: 25
 *   }
 * ];
 * 
 * <BlockBuster playlists={playlists} />
 */
export function BlockBuster({ playlists = [] }) {
    /**
     * Maneja la reproducción de una playlist
     * @function
     * @param {string} playlistId - ID de la playlist a reproducir
     */
    const handlePlay = (playlistId) => {
        console.log("Reproducir playlist:", playlistId);
        // TODO: Implementar lógica de reproducción
    };

    return (
        <div className={styles.blockBusterContainer}>
            {/* Encabezado de la sección */}
            <section className={styles.blockBusterHeader}>
                <h1>BlockBuster</h1>
                <p>Explora las últimas novedades y recomendaciones personalizadas.</p>
            </section>

            {/* Grid de playlists */}
            <section className={styles.blockBusterContent}>
                {/* Mensaje cuando no hay playlists */}
                {playlists.length === 0 && (
                    <p>No hay playlists disponibles en este momento.</p>
                )}
                
                {/* Renderizado de las tarjetas de playlist */}
                {playlists.map((playlist) => (
                    <PlaylistCard
                        key={playlist.playlist_id}
                        playlistId={playlist.playlist_id}
                        coverImage={playlist.imagen_url}
                        title={playlist.titulo}
                        subtitle={playlist.descripcion}
                        trackCount={playlist.total_canciones}
                        onPlay={handlePlay}
                    />
                ))}
            </section>
        </div>
    );
}
