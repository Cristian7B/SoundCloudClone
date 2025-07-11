/**
 * @fileoverview Componente de tarjeta de playlist que muestra información básica
 * de una playlist con interacciones de hover y navegación.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { useState } from 'react';
import { useNavigation } from '../../Routes/hooks/useNavigation';
import styles from '../Styles/PlaylistCard.module.css';
import soundcloudIcon from '/public/logo.svg';
import playIcon from '../assets/play.svg';

/**
 * Componente que renderiza una tarjeta de playlist con información básica
 * y controles de reproducción
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {string|number} props.playlistId - ID único de la playlist
 * @param {string} props.coverImage - URL de la imagen de portada
 * @param {string} props.title - Título de la playlist
 * @param {string} props.subtitle - Subtítulo o descripción
 * @param {number} [props.trackCount] - Número de pistas en la playlist
 * @param {Function} [props.onPlay] - Callback para reproducir la playlist
 * @param {string} [props.className] - Clases CSS adicionales
 * @returns {JSX.Element} Tarjeta de playlist interactiva
 * 
 * @example
 * <PlaylistCard
 *   playlistId="123"
 *   coverImage="/imagen.jpg"
 *   title="Mi Playlist"
 *   subtitle="Por Usuario"
 *   trackCount={15}
 *   onPlay={(id) => console.log('Playing:', id)}
 *   className="custom-class"
 * />
 */
export function PlaylistCard({
    playlistId,
    coverImage,
    title,
    subtitle,
    trackCount,
    onPlay,
    className
}) {
    /** Estado para controlar efectos de hover */
    const [isHovered, setIsHovered] = useState(false);
    
    /** Hook de navegación para ir a la página de la playlist */
    const { navigateToPlaylist } = useNavigation();

    /**
     * Maneja el clic en la tarjeta para navegar a la playlist
     * @function
     */
    const handleCardClick = () => {
        navigateToPlaylist(playlistId);
    };

    /**
     * Maneja el clic en el botón de reproducción
     * @function
     * @param {Event} e - Evento del clic
     */
    const handlePlayClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        onPlay && onPlay(playlistId);
    };

    return (
        <div 
            className={`${styles.playlistCard} ${className || ''}`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onClick={handleCardClick}
        >
            {/* Contenedor de la imagen con overlays y controles */}
            <div className={styles.imageContainer}>
                <img 
                    src={coverImage} 
                    alt={title}
                    className={styles.coverImage}
                />

                {/* Icono de SoundCloud */}
                <div className={styles.soundcloudIcon}>
                    <img src={soundcloudIcon} alt="SoundCloud" />
                </div>

                {/* Botón de reproducción que aparece en hover */}
                <button 
                    className={`${styles.playButton} ${isHovered ? styles.visible : ''}`}
                    onClick={handlePlayClick}
                    aria-label={`Reproducir playlist ${title}`}
                >
                    <img src={playIcon} alt="Play Playlist" />
                </button>

                {/* Badge con el número de pistas */}
                {
                    trackCount && (
                    <div className={styles.trackCountBadge}>
                        <span>{trackCount} tracks</span>
                    </div>
                )}

                {/* Overlay que aparece en hover */}
                <div className={`${styles.overlay} ${isHovered ? styles.visible : ''}`} />
            </div>

            {/* Contenido de texto de la tarjeta */}
            <div className={styles.content}>
                <h3 className={styles.title}>{title}</h3>
                <p className={styles.subtitle}>{subtitle}</p>
            </div>
        </div>
    );
}