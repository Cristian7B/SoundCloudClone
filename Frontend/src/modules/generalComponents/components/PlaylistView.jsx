import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styles from '../Styles/PlaylistView.module.css';
import likeIcon from '../assets/like.svg';
import repostIcon from '../assets/repost.svg';
import copyIcon from '../assets/copy.svg';
import verifiedIcon from '../assets/verificado.svg';
import playIcon from '../assets/play.svg';

export function PlaylistView() {
  const { playlistId } = useParams();
  const [playlist, setPlaylist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [following, setFollowing] = useState(false);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    fetchPlaylist();
  }, [playlistId]);

  const fetchPlaylist = async () => {
    try {
      setLoading(true);
      // Reemplaza con tu endpoint real
      const response = await fetch(`/api/playlists/${playlistId}`);
      const data = await response.json();
      setPlaylist(data);
    } catch (error) {
      console.error('Error fetching playlist:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFollow = () => {
    setFollowing(!following);
    // Aquí harías la petición al backend para seguir/dejar de seguir
  };

  const handlePlayTrack = (trackId) => {
    if (currentTrack === trackId && isPlaying) {
      setIsPlaying(false);
    } else {
      setCurrentTrack(trackId);
      setIsPlaying(true);
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

  if (!playlist) {
    return (
      <div className={styles.error}>
        <h2>Playlist no encontrada</h2>
        <p>La playlist que buscas no existe o ha sido eliminada.</p>
      </div>
    );
  }

  return (
    <div className={styles.playlistView}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.playlistInfo}>
          <img 
            src={playlist.coverImage} 
            alt={playlist.title}
            className={styles.playlistCover}
          />
          <div className={styles.playlistDetails}>
            <div className={styles.artistInfo}>
              <img 
                src={playlist.artist.avatar} 
                alt={playlist.artist.name}
                className={styles.artistAvatar}
              />
              <div>
                <h2 className={styles.playlistTitle}>{playlist.title}</h2>
                <div className={styles.artistName}>
                  {playlist.artist.name}
                  {playlist.artist.verified && (
                    <img src={verifiedIcon} alt="Verified" className={styles.verifiedIcon} />
                  )}
                </div>
                <p className={styles.followerCount}>
                  👥 {playlist.artist.followers?.toLocaleString() || '0'} seguidores
                </p>
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

        {/* Actions */}
        <div className={styles.actions}>
          <div className={styles.stats}>
            <span className={styles.stat}>
              <img src={likeIcon} alt="Likes" />
              {playlist.likes?.toLocaleString() || '0'}
            </span>
            <span className={styles.stat}>
              <img src={repostIcon} alt="Reposts" />
              {playlist.reposts || '0'}
            </span>
          </div>
          <div className={styles.actionButtons}>
            <button className={styles.actionButton}>
              <img src={likeIcon} alt="Like" />
            </button>
            <button className={styles.actionButton}>
              <img src={repostIcon} alt="Repost" />
            </button>
            <button className={styles.actionButton}>
              <img src={copyIcon} alt="Copy" />
            </button>
            <button className={styles.actionButton}>
            </button>
          </div>
        </div>
      </div>

      {/* Track List */}
      <div className={styles.trackList}>
        {playlist.tracks?.map((track, index) => (
          <div 
            key={track.id} 
            className={`${styles.trackItem} ${currentTrack === track.id ? styles.active : ''}`}
          >
            <div className={styles.trackNumber}>
              {index + 1}
            </div>
            
            <div className={styles.trackCover}>
              <img src={track.coverImage} alt={track.title} />
              <button 
                className={styles.trackPlayButton}
                onClick={() => handlePlayTrack(track.id)}
              >
                <img 
                    src={playIcon}
                  alt={currentTrack === track.id && isPlaying ? 'Pause' : 'Play'} 
                />
              </button>
            </div>

            <div className={styles.trackInfo}>
              <div className={styles.trackTitle}>{track.title}</div>
              <div className={styles.trackArtist}>
                {track.artists?.map(artist => artist.name).join(', ')}
              </div>
            </div>

            <div className={styles.trackActions}>
              {track.availability === 'available' ? (
                <div className={styles.trackPlays}>
                  ▶ {formatPlays(track.plays)}
                </div>
              ) : (
                <div className={styles.notAvailable}>
                  🌍 No disponible en tu país
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}