import React, { useState } from 'react';
import styles from '../Styles/MusicCard.module.css';
import soundcloudIcon from '/public/logo.svg';
import playIcon from '../assets/play.svg';

/**
 * Componente de tarjeta de música para mostrar canciones o álbumes individuales.
 * 
 * Este componente proporciona una interfaz visual atractiva para mostrar contenido
 * musical con imagen de portada, título, subtítulo y controles de reproducción.
 * Incluye efectos hover interactivos y enlace directo a SoundCloud.
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {string} props.coverImage - URL de la imagen de portada
 * @param {string} props.title - Título principal de la música
 * @param {string} props.subtitle - Subtítulo o descripción adicional
 * @param {string} props.soundcloudUrl - URL del contenido en SoundCloud
 * @param {Function} props.onPlay - Función callback ejecutada al hacer clic en play
 * @param {string} [props.className] - Clases CSS adicionales opcionales
 * 
 * @example
 * // Uso básico para mostrar una canción
 * <MusicCard
 *   coverImage="https://example.com/cover.jpg"
 *   title="Mi Canción Favorita"
 *   subtitle="Artista Genial"
 *   soundcloudUrl="https://soundcloud.com/track/123"
 *   onPlay={() => console.log('Reproduciendo...')}
 * />
 * 
 * @example
 * // Uso en una lista de resultados de búsqueda
 * {searchResults.map(track => (
 *   <MusicCard
 *     key={track.id}
 *     coverImage={track.artwork_url}
 *     title={track.title}
 *     subtitle={track.user.username}
 *     soundcloudUrl={track.permalink_url}
 *     onPlay={() => playTrack(track.id)}
 *     className="search-result-card"
 *   />
 * ))}
 * 
 * @returns {JSX.Element} Elemento JSX de la tarjeta de música
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function MusicCard({
    coverImage,
    title,
    subtitle,
    soundcloudUrl,
    onPlay,
    className
}) {
    /**
     * Estado que controla la visibilidad de los elementos interactivos.
     * Se activa cuando el usuario hace hover sobre la tarjeta.
     * 
     * @type {boolean}
     */
    const [isHovered, setIsHovered] = useState(false);

    /**
     * Maneja el clic en el botón de reproducción.
     * 
     * Previene la propagación del evento para evitar que se active
     * el enlace de SoundCloud cuando solo se quiere reproducir.
     * 
     * @param {Event} e - Evento de clic del botón
     * 
     * @example
     * // Se ejecuta cuando el usuario hace clic en el botón play
     * // <button onClick={handlePlayClick}>
     */
    const handlePlayClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        onPlay && onPlay();
    };

    /**
     * Estructura JSX de la tarjeta de música.
     * 
     * Incluye:
     * - Enlace externo a SoundCloud
     * - Contenedor de imagen con overlay interactivo
     * - Icono de SoundCloud en la esquina
     * - Botón de play que aparece en hover
     * - Información textual (título y subtítulo)
     * - Efectos hover para mejorar la experiencia del usuario
     */
    return (
        <a className={styles.anchords} target='_blank' href={soundcloudUrl}>
            <div 
                className={`${styles.musicCard} ${className || ''}`}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                <div className={styles.imageContainer}>
                    <img 
                        src={coverImage} 
                        alt={title}
                        className={styles.coverImage}
                    />

                    {/* Icono de SoundCloud en la esquina superior derecha */}
                    <div className={styles.soundcloudIcon}>
                        <img src={soundcloudIcon} alt="SoundCloud" />
                    </div>

                    {/* Botón de play que aparece en hover */}
                    <button 
                        className={`${styles.playButton} ${isHovered ? styles.visible : ''}`}
                        onClick={handlePlayClick}
                        aria-label={`Reproducir ${title}`}
                    >
                        <img src={playIcon} alt="Play" />
                    </button>

                    {/* Overlay oscuro en hover para mejorar contraste */}
                    <div className={`${styles.overlay} ${isHovered ? styles.visible : ''}`} />
                </div>

                {/* Información textual de la tarjeta */}
                <div className={styles.content}>
                    <h3 className={styles.title}>{title}</h3>
                    <p className={styles.subtitle}>{subtitle}</p>
                </div>
            </div>
        </a>
    );
}