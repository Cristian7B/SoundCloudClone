import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../Styles/PlaylistCard.module.css';
import soundcloudIcon from '/public/logo.svg';
import playIcon from '../assets/play.svg';

export function PlaylistCard({
    playlistId,
    coverImage,
    title,
    subtitle,
    trackCount,
    onPlay,
    className
}) {
    const [isHovered, setIsHovered] = useState(false);
    const navigate = useNavigate();

    const handleCardClick = () => {
        navigate(`/playlist/${playlistId}`);
    };

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
            <div className={styles.imageContainer}>
                <img 
                    src={coverImage} 
                    alt={title}
                    className={styles.coverImage}
                />

                {/* SoundCloud Icon */}
                <div className={styles.soundcloudIcon}>
                    <img src={soundcloudIcon} alt="SoundCloud" />
                </div>

                {/* Play Button - Solo visible en hover */}
                <button 
                    className={`${styles.playButton} ${isHovered ? styles.visible : ''}`}
                    onClick={handlePlayClick}
                >
                <img src={playIcon} alt="Play Playlist" />
                </button>

                {/* Track Count Badge */}
                {
                    trackCount && (
                    <div className={styles.trackCountBadge}>
                        <span>{trackCount} tracks</span>
                    </div>
                )}

                {/* Overlay en hover */}
                <div className={`${styles.overlay} ${isHovered ? styles.visible : ''}`} />
            </div>

            <div className={styles.content}>
                <h3 className={styles.title}>{title}</h3>
                <p className={styles.subtitle}>{subtitle}</p>
            </div>
        </div>
    );
}