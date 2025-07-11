import styles from "../Styles/Artist.module.css";
import { PlaylistCard } from "../../generalComponents/components/PlaylistCard";

export function Artist({ playlists = [] }) {
    const handlePlay = (playlistId) => {
        console.log("Reproducir playlist:", playlistId);
    };

    return (
        <div className={styles.artistContainer}>
            <section className={styles.artistHeader}>
                <h1>Artista</h1>
                <p>Explora tu música y herramientas de artista.</p>
            </section>

            <section className={styles.artistContent}>
                {playlists.length === 0 && (
                    <p>No hay playlists disponibles.</p>
                )}
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
