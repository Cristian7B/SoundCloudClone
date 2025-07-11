import styles from "../Styles/Mixes.module.css";
import { PlaylistCard } from "../../generalComponents/components/PlaylistCard";

export function Mixes({ playlists = [] }) {
    const handlePlay = (playlistId) => {
        console.log("Reproducir playlist:", playlistId);
    };

    return (
        <div className={styles.mixesContainer}>
            <section className={styles.mixesHeader}>
                <h1>Mezclas</h1>
                <p>Descubre tus mezclas favoritas y crea nuevas.</p>
            </section>

            <section className={styles.mixesContent}>
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
