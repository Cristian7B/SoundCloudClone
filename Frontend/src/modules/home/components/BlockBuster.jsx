import { useEffect, useState } from "react";
import styles from "../Styles/BlockBuster.module.css";
import { PlaylistCard } from "./PlaylistCard";

export function BlockBuster() {
    const [playlists, setPlaylists] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const response = await fetch("/api/playlists");
                const data = await response.json();
                setPlaylists(Array.isArray(data) ? data : data.playlists || []);
            } catch (err) {
                console.error("Error fetching playlists:", err);
                setError("No se pudieron cargar las playlists.");
            } finally {
                setLoading(false);
            }
        };

        fetchPlaylists();
    }, []);

    const handlePlay = (playlistId) => {
        console.log("Reproducir playlist:", playlistId);
    };

    return (
        <div className={styles.blockBusterContainer}>
            <section className={styles.blockBusterHeader}>
                <h1>BlockBuster</h1>
                <p>Explora las últimas novedades y recomendaciones personalizadas.</p>
            </section>

            <section className={styles.blockBusterContent}>
                {loading && <p>Cargando playlists...</p>}
                {error && <p>{error}</p>}
                {!loading && !error && playlists.length === 0 && (
                    <p>No hay playlists disponibles en este momento.</p>
                )}
                {!loading && !error && playlists.map((playlist) => (
                    <PlaylistCard
                        key={playlist.playlistId}
                        playlistId={playlist.playlistId}
                        coverImage={playlist.coverImage}
                        title={playlist.title}
                        subtitle={playlist.subtitle}
                        trackCount={playlist.trackCount}
                        onPlay={handlePlay}
                    />
                ))}
            </section>
        </div>
    );
}
