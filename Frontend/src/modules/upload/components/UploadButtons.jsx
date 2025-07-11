import React, { useState } from 'react';
import { UploadSongDialog } from './UploadSongDialog';
import { CreatePlaylistDialog } from './CreatePlaylistDialog';
import styles from '../Styles/UploadButtons.module.css';

/**
 * Componente de botones de carga que proporciona acceso rápido a las funcionalidades de upload.
 * 
 * Este componente actúa como un punto de entrada centralizado para las acciones de subida
 * de contenido, incluyendo canciones y playlists. Maneja la apertura y cierre de los
 * diálogos modales correspondientes y gestiona los callbacks de éxito.
 * 
 * @component
 * 
 * @example
 * // Uso básico del componente
 * return (
 *   <div>
 *     <h1>Panel de Usuario</h1>
 *     <UploadButtons />
 *   </div>
 * );
 * 
 * @example
 * // Integración en una página de perfil
 * function UserProfile() {
 *   return (
 *     <div className="profile-page">
 *       <UserInfo />
 *       <UploadButtons />
 *       <UserContent />
 *     </div>
 *   );
 * }
 * 
 * @returns {JSX.Element} Elemento JSX con los botones y diálogos integrados
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function UploadButtons() {
  /**
   * Estado que controla la visibilidad del diálogo de subida de canciones.
   * 
   * @type {boolean}
   */
  const [showSongDialog, setShowSongDialog] = useState(false);

  /**
   * Estado que controla la visibilidad del diálogo de creación de playlists.
   * 
   * @type {boolean}
   */
  const [showPlaylistDialog, setShowPlaylistDialog] = useState(false);

  /**
   * Maneja el éxito en la creación de una nueva canción.
   * 
   * Esta función se ejecuta cuando una canción se sube exitosamente al servidor.
   * Puede ser extendida para actualizar el estado global, mostrar notificaciones,
   * redirigir al usuario o actualizar listas de contenido.
   * 
   * @param {Object} songData - Datos de la canción creada devueltos por el servidor
   * @param {number} songData.cancion_id - ID único de la canción creada
   * @param {string} songData.titulo - Título de la canción
   * @param {string} songData.archivo_url - URL del archivo de audio
   * @param {number} songData.usuario_id - ID del usuario propietario
   * 
   * @example
   * // Datos típicos recibidos del servidor
   * const songData = {
   *   cancion_id: 123,
   *   titulo: "Mi Nueva Canción",
   *   archivo_url: "https://example.com/song.mp3",
   *   usuario_id: 1
   * };
   */
  const handleSongSuccess = (songData) => {
    console.log('Canción creada exitosamente:', songData);
    // TODO: Implementar lógica adicional como:
    // - Mostrar notificación de éxito
    // - Actualizar estado global de canciones
    // - Redirigir a la página de la canción
    // - Actualizar estadísticas del usuario
  };

  /**
   * Maneja el éxito en la creación de una nueva playlist.
   * 
   * Esta función se ejecuta cuando una playlist se crea exitosamente en el servidor.
   * Puede ser extendida para actualizar el estado global, mostrar notificaciones
   * o redirigir al usuario a la nueva playlist.
   * 
   * @param {Object} playlistData - Datos de la playlist creada devueltos por el servidor
   * @param {number} playlistData.playlist_id - ID único de la playlist creada
   * @param {string} playlistData.titulo - Título de la playlist
   * @param {boolean} playlistData.es_publica - Si la playlist es pública
   * @param {number} playlistData.usuario_id - ID del usuario propietario
   * 
   * @example
   * // Datos típicos recibidos del servidor
   * const playlistData = {
   *   playlist_id: 456,
   *   titulo: "Mi Nueva Playlist",
   *   es_publica: true,
   *   usuario_id: 1
   * };
   */
  const handlePlaylistSuccess = (playlistData) => {
    console.log('Playlist creada exitosamente:', playlistData);
    // TODO: Implementar lógica adicional como:
    // - Mostrar notificación de éxito
    // - Actualizar estado global de playlists
    // - Redirigir a la página de la playlist
    // - Actualizar estadísticas del usuario
  };

  /**
   * Estructura JSX del componente.
   * 
   * Incluye:
   * - Container principal con estilos responsivos
   * - Grupo de botones para acciones de upload
   * - Diálogos modales conditionally renderizados
   * - Gestión de eventos onClick para apertura de diálogos
   */
  return (
    <div className={styles.container}>
      <div className={styles.buttonGroup}>
        {/* Botón para abrir diálogo de subida de canciones */}
        <button
          className={styles.uploadButton}
          onClick={() => setShowSongDialog(true)}
          aria-label="Abrir diálogo para subir una nueva canción"
        >
          <span className={styles.icon}>🎵</span>
          Subir Canción
        </button>

        {/* Botón para abrir diálogo de creación de playlists */}
        <button
          className={styles.uploadButton}
          onClick={() => setShowPlaylistDialog(true)}
          aria-label="Abrir diálogo para crear una nueva playlist"
        >
          <span className={styles.icon}>📝</span>
          Crear Playlist
        </button>
      </div>

      {/* Diálogo modal para subir canciones */}
      <UploadSongDialog
        isOpen={showSongDialog}
        onClose={() => setShowSongDialog(false)}
        onSuccess={handleSongSuccess}
      />

      {/* Diálogo modal para crear playlists */}
      <CreatePlaylistDialog
        isOpen={showPlaylistDialog}
        onClose={() => setShowPlaylistDialog(false)}
        onSuccess={handlePlaylistSuccess}
      />
    </div>
  );
}
