import React, { useState } from 'react';
import styles from '../Styles/MusicCard.module.css';
import soundcloudIcon from '/public/logo.svg';
import playIcon from '../assets/play.svg'   ;

export function MusicCard({
    coverImage,
    title,
    subtitle,
    soundcloudUrl,
    onPlay,
    className
}) {
    const [isHovered, setIsHovered] = useState(false);

    const handlePlayClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        onPlay && onPlay();
    };

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

                    <div className={styles.soundcloudIcon}>
                        <img src={soundcloudIcon} alt="SoundCloud" />
                    </div>

                    <button 
                    className={`${styles.playButton} ${isHovered ? styles.visible : ''}`}
                    onClick={handlePlayClick}
                    >
                        <img src={playIcon} alt="Play" />
                    </button>

                    <div className={`${styles.overlay} ${isHovered ? styles.visible : ''}`} />
                    </div>

                    <div className={styles.content}>
                    <h3 className={styles.title}>{title}</h3>
                    <p className={styles.subtitle}>{subtitle}</p>
                </div>
            </div>
        </a>
    );
}