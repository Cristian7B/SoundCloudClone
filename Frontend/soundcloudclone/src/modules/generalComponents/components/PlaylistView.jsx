import styles from "../Styles/PlaylistView.module.css";
export function PlaylistView({ playlist }) {
    return (
        <div className={styles.playlistView}>
            <h2>{playlist.name}</h2>
            <ul>
                {playlist.tracks.map((track, index) => (
                    <li key={index} className={styles.trackItem}>
                        <span className={styles.trackTitle}>{track.title}</span>
                        <span className={styles.trackArtist}>{track.artist}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}