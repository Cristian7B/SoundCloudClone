import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { MusicCard } from '../../generalComponents/components/MusicCard';
import { PlaylistCard } from '../../generalComponents/components/PlaylistCard';
import styles from '../Styles/UserProfile.module.css';
import axios from 'axios';

const UserProfile = ({ onClose }) => {
  const { user, updateProfile, logout, loading, error, clearError } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [userTracks, setUserTracks] = useState([]);
  const [userPlaylists, setUserPlaylists] = useState([]);
  const [tracksLoading, setTracksLoading] = useState(false);
  const [playlistsLoading, setPlaylistsLoading] = useState(false);
  const [tracksStats, setTracksStats] = useState(null);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    username: '',
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        username: user.username || '',
      });
    }
  }, [user]);

  useEffect(() => {
    if (user?.user_id) {
      fetchUserTracks();
      fetchUserPlaylists();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.user_id]);

  // Función para obtener las canciones del usuario
  const fetchUserTracks = async () => {
    if (!user?.user_id) return;
    
    setTracksLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/contenido/usuarios/${user.user_id}/canciones/`);
      setUserTracks(response.data.canciones || []);
      setTracksStats(response.data.estadisticas || null);
    } catch (err) {
      console.error('Error fetching user tracks:', err);
    } finally {
      setTracksLoading(false);
    }
  };

  // Función para obtener las playlists del usuario
  const fetchUserPlaylists = async () => {
    if (!user?.user_id) return;
    
    setPlaylistsLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/contenido/usuarios/${user.user_id}/playlists/`);
      const allPlaylists = [
        ...(response.data.playlists_publicas?.playlists || []),
        ...(response.data.playlists_privadas?.playlists || [])
      ];
      setUserPlaylists(allPlaylists);
    } catch (err) {
      console.error('Error fetching user playlists:', err);
    } finally {
      setPlaylistsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar errores cuando el usuario empiece a escribir
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    if (error) {
      clearError();
    }
  };

  const validateForm = () => {
    const errors = {};

    if (!formData.first_name.trim()) {
      errors.first_name = 'El nombre es requerido';
    }

    if (!formData.last_name.trim()) {
      errors.last_name = 'El apellido es requerido';
    }

    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'El email no es válido';
    }

    if (!formData.username.trim()) {
      errors.username = 'El nombre de usuario es requerido';
    }

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    try {
      await updateProfile(formData);
      setIsEditing(false);
    } catch (err) {
      console.error('Error actualizando perfil:', err);
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      email: user.email || '',
      username: user.username || '',
    });
    setFormErrors({});
    setIsEditing(false);
    clearError();
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Error durante logout:', err);
    }
  };

  // Handlers para los componentes
  const handleTrackPlay = (track) => {
    console.log('Playing track:', track);
    // Aquí puedes integrar con el reproductor de audio
  };

  const handlePlaylistPlay = (playlistId) => {
    console.log('Playing playlist:', playlistId);
    // Aquí puedes integrar con el reproductor de audio
  };

  if (!user) {
    return (
      <div className={styles.profileContainer}>
        <div className={styles.loadingMessage}>
          Cargando perfil...
        </div>
      </div>
    );
  }

  return (
    <div className={styles.profileContainer}>
      <div className={styles.profileTopBar}>
        <h2 className={styles.profileTitle}>Mi Perfil</h2>
        <button 
          className={styles.closeButton}
          onClick={onClose}
          title="Cerrar perfil"
        >
          ×
        </button>
      </div>
      
      <div className={styles.profileContent}>
        <div className={styles.profileHeader}>
          <div className={styles.avatarSection}>
            <div className={styles.avatar}>
              {user.first_name?.[0]?.toUpperCase() || 'U'}
            </div>
            <button className={styles.changeAvatarBtn}>
              Cambiar foto
            </button>
          </div>
          <div className={styles.headerInfo}>
            <h1>{user.nombre}</h1>
            <p className={styles.username}>@{user.username}</p>
            <p className={styles.email}>{user.email}</p>
          </div>
        </div>

      <div className={styles.profileActions}>
        {!isEditing ? (
          <button 
            onClick={() => setIsEditing(true)}
            className={styles.editButton}
          >
            Editar perfil
          </button>
        ) : (
          <div className={styles.actionButtons}>
            <button 
              onClick={handleCancel}
              className={styles.cancelButton}
            >
              Cancelar
            </button>
            <button 
              onClick={handleSubmit}
              className={styles.saveButton}
              disabled={loading}
            >
              {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        )}
      </div>

      {isEditing && (
        <div className={styles.editForm}>
          <h3>Editar información</h3>
          
          <form onSubmit={handleSubmit}>
            <div className={styles.inputRow}>
              <div className={styles.inputGroup}>
                <label>Nombre</label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className={formErrors.first_name ? styles.inputError : ''}
                />
                {formErrors.first_name && (
                  <span className={styles.errorText}>{formErrors.first_name}</span>
                )}
              </div>

              <div className={styles.inputGroup}>
                <label>Apellido</label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className={formErrors.last_name ? styles.inputError : ''}
                />
                {formErrors.last_name && (
                  <span className={styles.errorText}>{formErrors.last_name}</span>
                )}
              </div>
            </div>

            <div className={styles.inputGroup}>
              <label>Nombre de usuario</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                className={formErrors.username ? styles.inputError : ''}
              />
              {formErrors.username && (
                <span className={styles.errorText}>{formErrors.username}</span>
              )}
            </div>

            <div className={styles.inputGroup}>
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={formErrors.email ? styles.inputError : ''}
              />
              {formErrors.email && (
                <span className={styles.errorText}>{formErrors.email}</span>
              )}
            </div>

            {error && (
              <div className={styles.errorMessage}>
                {error}
              </div>
            )}
          </form>
        </div>
      )}

      <div className={styles.profileStats}>
        <div className={styles.statItem}>
          <span className={styles.statNumber}>0</span>
          <span className={styles.statLabel}>Seguidores</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statNumber}>0</span>
          <span className={styles.statLabel}>Siguiendo</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statNumber}>{userTracks.length}</span>
          <span className={styles.statLabel}>Tracks</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statNumber}>{userPlaylists.length}</span>
          <span className={styles.statLabel}>Playlists</span>
        </div>
        {tracksStats && (
          <div className={styles.statItem}>
            <span className={styles.statNumber}>{tracksStats.total_reproducciones}</span>
            <span className={styles.statLabel}>Reproducciones</span>
          </div>
        )}
      </div>

        <div className={styles.profileSections}>
          <div className={styles.section}>
            <h3>Tus tracks ({userTracks.length})</h3>
            {tracksLoading ? (
              <p>Cargando tracks...</p>
            ) : userTracks.length > 0 ? (
              <div className={styles.tracksGrid}>
                {userTracks.map((track) => (
                  <MusicCard
                    key={track.cancion_id}
                    coverImage={track.imagen_url || '/default-cover.jpg'}
                    title={track.titulo}
                    subtitle={`${track.genero || 'Sin género'} • ${track.reproducciones} reproducciones`}
                    soundcloudUrl={track.archivo_url}
                    onPlay={() => handleTrackPlay(track)}
                  />
                ))}
              </div>
            ) : (
              <p className={styles.emptyMessage}>No has subido ningún track aún</p>
            )}
          </div>

          <div className={styles.section}>
            <h3>Playlists ({userPlaylists.length})</h3>
            {playlistsLoading ? (
              <p>Cargando playlists...</p>
            ) : userPlaylists.length > 0 ? (
              <div className={styles.playlistsGrid}>
                {userPlaylists.map((playlist) => (
                  <PlaylistCard
                    key={playlist.playlist_id}
                    playlistId={playlist.playlist_id}
                    coverImage={playlist.imagen_url || '/default-playlist.jpg'}
                    title={playlist.titulo}
                    subtitle={playlist.descripcion || 'Sin descripción'}
                    trackCount={playlist.total_canciones}
                    onPlay={handlePlaylistPlay}
                  />
                ))}
              </div>
            ) : (
              <p className={styles.emptyMessage}>No tienes playlists creadas</p>
            )}
          </div>
        </div>

        <div className={styles.dangerZone}>
          <button 
            onClick={handleLogout}
            className={styles.logoutButton}
          >
            Cerrar sesión
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
