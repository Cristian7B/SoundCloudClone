import { useEffect, useState } from "react";
import styles from "../Styles/Mixes.module.css";
import { MusicCard } from "./MusicCard";

export function Mixes() {
    const [mixes, setMixes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMixes = async () => {
            try {
                const response = await fetch("/api/mixes");
                const data = await response.json();
                setMixes(Array.isArray(data) ? data : data.mixes || []);
            } catch (err) {
                console.error("Error al obtener mixes:", err);
                setError("No se pudieron cargar las mezclas.");
            } finally {
                setLoading(false);
            }
        };

        fetchMixes();
    }, []);

    const handlePlay = (mixId) => {
        console.log(`Reproducir mezcla ${mixId}`);
    };

    return (
        <div className={styles.mixesContainer}>
            <section className={styles.mixesHeader}>
                <h1>Mezclas</h1>
                <p>Descubre tus mezclas favoritas y crea nuevas.</p>
            </section>

            <section className={styles.mixesContent}>
                {loading && <p>Cargando mezclas...</p>}
                {error && <p>{error}</p>}
                {!loading && !error && mixes.length === 0 && (
                    <p>No hay mezclas disponibles.</p>
                )}
                {!loading && !error && mixes.map((mix) => (
                    <MusicCard
                        key={mix.id}
                        coverImage={mix.coverImage}
                        title={mix.title}
                        subtitle={mix.subtitle}
                        soundcloudUrl={mix.soundcloudUrl}
                        onPlay={() => handlePlay(mix.id)}
                    />
                ))}
            </section>
        </div>
    );
}
