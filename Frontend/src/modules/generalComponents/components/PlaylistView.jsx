import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useNavigation } from '../../Routes/hooks/useNavigation';
import styles from '../Styles/PlaylistView.module.css';
import likeIcon from '../assets/like.svg';
import repostIcon from '../assets/repost.svg';
import copyIcon from '../assets/copy.svg';
import playIcon from '../assets/play.svg';
import axios from 'axios';
import { toggleInteraction } from '../utils/interactionUtils';

export function PlaylistView() {
  const { playlistId } = useParams();
  const { goBack } = useNavigation();
  const [playlist, setPlaylist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [following, setFollowing] = useState(false);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const [trackInteractions, setTrackInteractions] = useState({}); // {trackId: {liked: bool, reposted: bool}}
  const [trackCounts, setTrackCounts] = useState({}); // {trackId: {likes: number, reposts: number}}

  useEffect(() => {
    const fetchPlaylist = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await axios.get(`http://127.0.0.1:8000/api/contenido/playlists/${playlistId}/`);
        setPlaylist(response.data);
        
        const initialCounts = {};
        const initialInteractions = {};
        
        response.data.canciones?.forEach(track => {
          initialCounts[track.cancion_id] = {
            likes: track.likes_count || 0,
            reposts: track.reposts_count || 0
          };
          initialInteractions[track.cancion_id] = {
            liked: false, // TODO: Obtener del servidor
            reposted: false // TODO: Obtener del servidor
          };
        });
        
        setTrackCounts(initialCounts);
        setTrackInteractions(initialInteractions);
      } catch (error) {
        console.error('Error fetching playlist:', error);
        setError('No se pudo cargar la playlist');
      } finally {
        setLoading(false);
      }
    };

    if (playlistId) {
      fetchPlaylist();
    }
  }, [playlistId]);

  const handleFollow = () => {
    setFollowing(!following);
  };

  const handlePlayTrack = (trackId) => {
    if (currentTrack === trackId && isPlaying) {
      setIsPlaying(false);
    } else {
      setCurrentTrack(trackId);
      setIsPlaying(true);
    }
  };

  const handleBackClick = () => {
    goBack();
  };

  const handleTrackLike = async (trackId) => {
    try {
      const response = await toggleInteraction({
        tipo: 'like',
        cancion_id: trackId,
        usuario_id: 1 // Para testing
      });

      setTrackInteractions(prev => ({
        ...prev,
        [trackId]: {
          ...prev[trackId],
          liked: response.activo
        }
      }));

      setTrackCounts(prev => ({
        ...prev,
        [trackId]: {
          ...prev[trackId],
          likes: response.activo 
            ? prev[trackId].likes + 1 
            : Math.max(0, prev[trackId].likes - 1)
        }
      }));
    } catch (error) {
      console.error('Error toggling track like:', error);
    }
  };

  const handleTrackRepost = async (trackId) => {
    try {
      const response = await toggleInteraction({
        tipo: 'repost',
        cancion_id: trackId,
        usuario_id: 1 // Para testing
      });

      setTrackInteractions(prev => ({
        ...prev,
        [trackId]: {
          ...prev[trackId],
          reposted: response.activo
        }
      }));

      setTrackCounts(prev => ({
        ...prev,
        [trackId]: {
          ...prev[trackId],
          reposts: response.activo 
            ? prev[trackId].reposts + 1 
            : Math.max(0, prev[trackId].reposts - 1)
        }
      }));
    } catch (error) {
      console.error('Error toggling track repost:', error);
    }
  };

  const formatPlays = (plays) => {
    if (plays >= 1000000) {
      return (plays / 1000000).toFixed(1) + 'M';
    } else if (plays >= 1000) {
      return (plays / 1000).toFixed(0) + 'K';
    }
    return plays.toString();
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Cargando playlist...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.error}>
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={handleBackClick} className={styles.backButton}>
          ← Volver
        </button>
      </div>
    );
  }

  if (!playlist) {
    return (
      <div className={styles.error}>
        <h2>Playlist no encontrada</h2>
        <p>La playlist que buscas no existe o ha sido eliminada.</p>
        <button onClick={handleBackClick} className={styles.backButton}>
          ← Volver
        </button>
      </div>
    );
  }

  return (
    <div className={styles.playlistView}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.headerTop}>
          <button className={styles.backButton} onClick={handleBackClick}>
            ← Volver
          </button>
        </div>
        
        <div className={styles.playlistContainer}>
          <div className={styles.playlistInfo}>
            <img 
              src={playlist.imagen_url} 
              alt={playlist.titulo}
              className={styles.playlistCover}
            />
            <div className={styles.playlistDetails}>
              <div className={styles.artistInfo}>
                <div>
                  <h2 className={styles.playlistTitle}>{playlist.titulo}</h2>
                  <p className={styles.playlistDescription}>{playlist.descripcion}</p>
                  <div className={styles.playlistMeta}>
                    <span className={styles.trackCount}>
                      {playlist.total_canciones} cancion{playlist.total_canciones !== 1 ? 'es' : ''}
                    </span>
                    <span className={styles.visibility}>
                      {playlist.es_publica ? '🌍 Pública' : '🔒 Privada'}
                    </span>
                  </div>
                </div>
              </div>
              <button 
                className={`${styles.followButton} ${following ? styles.following : ''}`}
                onClick={handleFollow}
              >
                {following ? 'Siguiendo' : 'Seguir'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.playControls}>
        <button className={styles.playAllButton}>
          <img src={playIcon} alt="Play" />
          Reproducir
        </button>
        <div className={styles.playlistActions}>
          <button className={styles.actionButton}>
            <img src={likeIcon} alt="Like" />
          </button>
          <button className={styles.actionButton}>
            <img src={repostIcon} alt="Repost" />
          </button>
          <button className={styles.actionButton}>
            <img src={copyIcon} alt="Copy" />
          </button>
        </div>
      </div>

      <div className={styles.trackList}>
        {playlist.canciones?.map((track, index) => (
          <div 
            key={track.cancion_id} 
            className={`${styles.trackItem} ${currentTrack === track.cancion_id ? styles.active : ''}`}
          >
            <div className={styles.trackNumber}>
              {index + 1}
            </div>
            
            <div className={styles.trackCover}>
              <img src={track.imagen_url} alt={track.titulo} />
              <button 
                className={styles.trackPlayButton}
                onClick={() => handlePlayTrack(track.cancion_id)}
              >
                <img 
                    src={playIcon}
                  alt={currentTrack === track.cancion_id && isPlaying ? 'Pause' : 'Play'} 
                />
              </button>
            </div>

            <div className={styles.trackInfo}>
              <div className={styles.trackTitle}>{track.titulo}</div>
              <div className={styles.trackArtist}>
                {track.genero} • {track.duracion}
              </div>
            </div>

            <div className={styles.trackActions}>
              <div className={styles.trackPlays}>
                ▶ {formatPlays(track.reproducciones)}
              </div>
              <div className={styles.trackStats}>
                <span>❤️ {trackCounts[track.cancion_id]?.likes || track.likes_count}</span>
                <span>🔄 {trackCounts[track.cancion_id]?.reposts || track.reposts_count}</span>
              </div>
              <div className={styles.trackButtons}>
                <button 
                  className={`${styles.trackActionButton} ${trackInteractions[track.cancion_id]?.liked ? styles.liked : ''}`}
                  onClick={() => handleTrackLike(track.cancion_id)}
                >
                  <img src={likeIcon} alt="Like" />
                </button>
                <button 
                  className={`${styles.trackActionButton} ${trackInteractions[track.cancion_id]?.reposted ? styles.reposted : ''}`}
                  onClick={() => handleTrackRepost(track.cancion_id)}
                >
                  <img src={repostIcon} alt="Repost" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}