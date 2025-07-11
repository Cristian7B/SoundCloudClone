/**
 * @fileoverview Componente de tarjeta de audio que muestra información de una canción
 * con controles de reproducción e interacciones (like, repost, copy).
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { useState, useEffect } from 'react';
import styles from '../Styles/AudioCard.module.css';
import playIcon from '../assets/play.svg';
import pauseIcon from '../assets/pause.svg';
import likeIcon from '../assets/like.svg';
import repostIcon from '../assets/repost.svg';
import copyIcon from '../assets/copy.svg';
import { toggleInteraction, getTrackInteractionStatus } from '../../generalComponents/utils/interactionUtils';

/**
 * Componente que renderiza una tarjeta de audio con información de la canción
 * y controles de interacción
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {string|number} props.cancionId - ID único de la canción
 * @param {string} props.userName - Nombre del usuario/artista
 * @param {string} props.trackTitle - Título de la canción
 * @param {string} props.albumCover - URL de la imagen de portada
 * @param {string} props.timeAgo - Tiempo transcurrido desde la publicación
 * @param {number} [props.likes] - Número inicial de likes
 * @param {number} [props.reposts] - Número inicial de reposts
 * @param {number} props.plays - Número de reproducciones
 * @param {number} props.comments - Número de comentarios
 * @param {string[]} [props.tags=[]] - Array de etiquetas de la canción
 * @param {boolean} [props.isPlaying=false] - Estado de reproducción
 * @param {Function} props.onPlayPause - Callback para play/pause
 * @param {Function} [props.onLike] - Callback opcional para like
 * @param {Function} [props.onRepost] - Callback opcional para repost
 * @param {Function} [props.onCopy] - Callback opcional para copy
 * @param {string} props.url - URL de la canción
 * @returns {JSX.Element} Tarjeta de audio interactiva
 * 
 * @example
 * <AudioCard
 *   cancionId="123"
 *   userName="Artista"
 *   trackTitle="Mi Canción"
 *   albumCover="/imagen.jpg"
 *   timeAgo="hace 2 horas"
 *   likes={150}
 *   reposts={25}
 *   plays={1000}
 *   comments={10}
 *   tags={["rock", "alternativo"]}
 *   isPlaying={false}
 *   onPlayPause={() => {}}
 *   url="/audio.mp3"
 * />
 */
export function AudioCard({
  cancionId, // Agregar ID de la canción
  userName,
  trackTitle,
  albumCover,
  timeAgo,
  likes: initialLikes,
  reposts: initialReposts,
  plays,
  comments,
  tags = [],
  isPlaying = false,
  onPlayPause,
  onLike,
  onRepost,
  onCopy,
  url
}) {
  /** Estado para controlar si la canción está marcada como gustada */
  const [isLiked, setIsLiked] = useState(false);
  
  /** Estado para controlar si la canción está reposteada */
  const [isReposted, setIsReposted] = useState(false);
  
  /** Estado local para el conteo de likes */
  const [likes, setLikes] = useState(initialLikes || 0);
  
  /** Estado local para el conteo de reposts */
  const [reposts, setReposts] = useState(initialReposts || 0);
  
  /** Estado para controlar la carga de interacciones */
  const [loading, setLoading] = useState(false);

  // Cargar estado de interacciones al montar el componente
  useEffect(() => {
    /**
     * Carga el estado de interacciones del usuario para esta canción
     * @async
     * @function
     */
    const loadInteractionStatus = async () => {
      if (cancionId) {
        try {
          const status = await getTrackInteractionStatus(cancionId);
          setIsLiked(status.liked);
          setIsReposted(status.reposted);
        } catch (error) {
          console.error('Error loading interaction status:', error);
        }
      }
    };

    loadInteractionStatus();
  }, [cancionId]);

  /**
   * Maneja la acción de dar like/unlike a la canción
   * @async
   * @function
   */

  const handleLike = async () => {
    if (!cancionId || loading) return;
    
    try {
      setLoading(true);
      const response = await toggleInteraction({
        tipo: 'like',
        cancion_id: cancionId,
        usuario_id: 1 // Para testing, luego usar usuario autenticado
      });

      setIsLiked(response.activo);
      
      if (response.activo) {
        setLikes(prev => prev + 1);
      } else {
        setLikes(prev => Math.max(0, prev - 1));
      }

      // Ejecutar callback opcional
      onLike && onLike();
    } catch (error) {
      console.error('Error toggling like:', error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Maneja la acción de repost/unrepost de la canción
   * @async
   * @function
   */
  const handleRepost = async () => {
    if (!cancionId || loading) return;
    
    try {
      setLoading(true);
      const response = await toggleInteraction({
        tipo: 'repost',
        cancion_id: cancionId,
        usuario_id: 1 // Para testing, luego usar usuario autenticado
      });

      setIsReposted(response.activo);
      if (response.activo) {
        setReposts(prev => prev + 1);
      } else {
        setReposts(prev => Math.max(0, prev - 1));
      }

      // Ejecutar callback opcional
      onRepost && onRepost();
    } catch (error) {
      console.error('Error toggling repost:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!url) {
      console.warn('No URL provided to copy');
      return;
    }

    try {
      await navigator.clipboard.writeText(url);
      console.log('URL copied to clipboard:', url);
      onCopy && onCopy();
    } catch (error) {
      try {
        const textArea = document.createElement('textarea');
        textArea.value = url;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        console.log('URL copied to clipboard (fallback):', url);
        onCopy && onCopy();
      } catch (fallbackError) {
        console.error('Error copying URL to clipboard:', error, fallbackError);
      }
    }
  };

  return (
    <div className={styles.audioCard}>
      <div className={styles.header}>
        <div className={styles.userAvatar}>
          U
        </div>
        <div className={styles.userInfo}>
          <span className={styles.userName}>{userName}</span>
          <span className={styles.timeAgo}>posteó una pista hace {timeAgo}</span>
        </div>
        {tags.length > 0 && (
          <div className={styles.tags}>
            {tags.map((tag, index) => (
              <span key={index} className={styles.tag}>
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className={styles.mainContent}>
        <div className={styles.albumCover}>
          <img src={albumCover} alt={trackTitle} />
        </div>
        
        <div className={styles.trackInfo}>
          <div className={styles.playSection}>
            <button 
              className={styles.playButton}
              onClick={onPlayPause}
            >
              <img 
                src={isPlaying ? pauseIcon : playIcon} 
                alt={isPlaying ? 'Pause' : 'Play'} 
              />
            </button>
            <div className={styles.trackDetails}>
              <h3 className={styles.artistName}>{userName}</h3>
              <h4 className={styles.trackTitle}>{trackTitle}</h4>
            </div>
          </div>
          
          <div className={styles.waveformPlaceholder}>
            <div className={styles.waveformBars}>
              {Array.from({ length: 100 }).map((_, index) => (
                <div 
                  key={index} 
                  className={styles.waveformBar}
                  style={{
                    height: `${Math.random() * 40 + 10}px`,
                    backgroundColor: index < 30 ? '#ff5500' : '#555555'
                  }}
                />
              ))}
            </div>
            <div className={styles.timeStamps}>
              <span>0:00</span>
              <span>3:45</span>
            </div>
          </div>
        </div>
      </div>


      <div className={styles.actions}>
        <button 
          className={`${styles.actionButton} ${isLiked ? styles.liked : ''}`}
          onClick={handleLike}
        >
          <img src={likeIcon} alt="Like" />
          <span>{likes}</span>
        </button>
        
        <button 
          className={`${styles.actionButton} ${isReposted ? styles.reposted : ''}`}
          onClick={handleRepost}
        >
          <img src={repostIcon} alt="Repost" />
          <span>{reposts}</span>
        </button>
        
        <button className={styles.actionButton} onClick={handleCopy}>
          <img src={copyIcon} alt="Copy link" />
        </button>
        
        <div className={styles.stats}>
          <span className={styles.plays}>
            <span className={styles.playIcon}>▶</span>
            {plays}
          </span>
          <span className={styles.comments}>
            <span className={styles.commentIcon}>💬</span>
            {comments}
          </span>
        </div>
      </div>
    </div>
  );
}