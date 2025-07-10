import { useEffect, useState } from "react";
import styles from "../Styles/Library.module.css";
import { AudioCard } from "./AudioCard";
import axios from "axios";

export function Library() {
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTracks = async () => {
            try {
                const response = await axios.get("/api/tracks");
                console.log("response.data:", response.data);
                const data = Array.isArray(response.data) ? response.data : response.data.tracks;
                setTracks(data || []);
            } catch (err) {
                console.error("Error fetching tracks:", err);
                setError("No se pudo cargar la biblioteca.");
            } finally {
                setLoading(false);
            }
        };

        fetchTracks();
    }, []);

    const handlePlayPause = (id) => console.log(`Play/Pause clicked for track ${id}`);
    const handleLike = (id) => console.log(`Like clicked for track ${id}`);
    const handleRepost = (id) => console.log(`Repost clicked for track ${id}`);
    const handleShare = (id) => console.log(`Share clicked for track ${id}`);
    const handleCopy = (id) => console.log(`Copy link clicked for track ${id}`);
    const handleMore = (id) => console.log(`More options clicked for track ${id}`);

    return (
        <div className={styles.libraryContainer}>
            <section className={styles.libraryHeader}>
                <h1>Escucha los últimos posts de la gente a la que sigues:</h1>
            </section>

            {loading && <p>Cargando...</p>}
            {error && <p>{error}</p>}

            {!loading && !error && Array.isArray(tracks) && tracks.length === 0 && (
                <p>No se encontraron pistas.</p>
            )}

            {!loading && !error && Array.isArray(tracks) && tracks.length > 0 && (
                tracks.map((track) => (
                    <AudioCard
                        key={track.id}
                        userAvatar={track.userAvatar}
                        userName={track.userName}
                        trackTitle={track.trackTitle}
                        albumCover={track.albumCover}
                        timeAgo={track.timeAgo}
                        likes={track.likes}
                        reposts={track.reposts}
                        plays={track.plays}
                        comments={track.comments}
                        tags={track.tags}
                        isPlaying={track.isPlaying}
                        onPlayPause={() => handlePlayPause(track.id)}
                        onLike={() => handleLike(track.id)}
                        onRepost={() => handleRepost(track.id)}
                        onShare={() => handleShare(track.id)}
                        onCopy={() => handleCopy(track.id)}
                        onMore={() => handleMore(track.id)}
                    />
                ))
            )}
        </div>
    );
}
