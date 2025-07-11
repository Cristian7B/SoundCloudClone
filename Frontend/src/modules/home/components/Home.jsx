/**
 * @fileoverview Componente principal de la página de inicio que muestra
 * diferentes secciones de contenido musical organizadas por categorías.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import { useEffect, useState } from "react";
import styles from "../Styles/Home.module.css";
import { Artist } from "./Artist";
import { BlockBuster } from "./BlockBuster";
import { Mixes } from "./Mixes";
import axios from "axios";

/**
 * Componente que renderiza la página principal con secciones de música
 * organizadas en diferentes categorías (BlockBuster, Artist, Mixes)
 * @component
 * @returns {JSX.Element} Página de inicio con secciones de música
 * 
 * @example
 * <Home />
 */
export function Home() {
    /** Estado para almacenar las playlists obtenidas de la API */
    const [playlists, setPlaylists] = useState([]);
    
    /** Estado para controlar el estado de carga */
    const [loading, setLoading] = useState(true);
    
    /** Estado para manejar errores en la carga de datos */
    const [error, setError] = useState(null);

    // Efecto para cargar las playlists al montar el componente
    useEffect(() => {
        /**
         * Obtiene las playlists desde la API
         * @async
         * @function
         */
        const fetchPlaylists = async () => {
            try {
                setLoading(true);
                const response = await axios.get("http://127.0.0.1:8000/api/contenido/playlists/");
                const data = response.data;
                
                // Asegurar que data es un array
                const playlistArray = Array.isArray(data) ? data : [];
                setPlaylists(playlistArray);
            } catch (err) {
                console.error("Error fetching playlists:", err);
                setError("No se pudieron cargar las playlists.");
            } finally {
                setLoading(false);
            }
        };

        fetchPlaylists();
    }, []);

    // Calcular distribución de playlists entre componentes
    const totalPlaylists = playlists.length;
    const playlistsPerComponent = Math.ceil(totalPlaylists / 3);
    
    /** Playlists para la sección BlockBuster */
    const blockBusterPlaylists = playlists.slice(0, playlistsPerComponent);
    
    /** Playlists para la sección Artist */
    const artistPlaylists = playlists.slice(playlistsPerComponent, playlistsPerComponent * 2);
    
    /** Playlists para la sección Mixes */
    const mixesPlaylists = playlists.slice(playlistsPerComponent * 2);

    // Estado de carga
    if (loading) {
        return (
            <div className={styles.homeContainer}>
                <div className={styles.loading}>
                    <p>Cargando playlists...</p>
                </div>
            </div>
        );
    }

    // Estado de error
    if (error) {
        return (
            <div className={styles.homeContainer}>
                <div className={styles.error}>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    // Renderizado principal con las tres secciones
    return (
        <div className={styles.homeContainer}>
            <BlockBuster playlists={blockBusterPlaylists} />
            <Artist playlists={artistPlaylists} />
            <Mixes playlists={mixesPlaylists} />
        </div>
    );
}