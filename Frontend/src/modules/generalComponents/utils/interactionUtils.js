/**
 * @fileoverview Utilidades para manejar interacciones de usuarios como likes,
 * reposts y follows en canciones, playlists y usuarios.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import axios from 'axios';

/** URL base de la API */
const API_BASE_URL = 'http://127.0.0.1:8000/api';

/**
 * Alterna una interacción (like, repost, follow) del usuario
 * @async
 * @function
 * @param {Object} params - Parámetros de la interacción
 * @param {string} params.tipo - Tipo de interacción ('like', 'repost', 'follow')
 * @param {number} [params.cancion_id] - ID de la canción (para likes/reposts de canciones)
 * @param {number} [params.playlist_id] - ID de la playlist (para likes/reposts de playlists)
 * @param {number} [params.usuario_objetivo_id] - ID del usuario objetivo (para follows)
 * @param {number} [params.usuario_id] - ID del usuario que hace la acción (opcional, para testing)
 * @returns {Promise<Object>} Respuesta del servidor con el estado actualizado
 * @throws {Error} Error en la petición HTTP
 * 
 * @example
 * // Dar like a una canción
 * const result = await toggleInteraction({
 *   tipo: 'like',
 *   cancion_id: 123,
 *   usuario_id: 1
 * });
 * 
 * // Seguir a un usuario
 * const result = await toggleInteraction({
 *   tipo: 'follow',
 *   usuario_objetivo_id: 456,
 *   usuario_id: 1
 * });
 */
export const toggleInteraction = async (params) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/contenido/interacciones/toggle/`, params);
    return response.data;
  } catch (error) {
    console.error('Error toggling interaction:', error);
    throw error;
  }
};

/**
 * Obtiene el estado de las interacciones de un usuario para una canción específica
 * @async
 * @function
 * @param {number} cancionId - ID de la canción
 * @param {number} [usuarioId=1] - ID del usuario (opcional, para testing)
 * @returns {Promise<Object>} Estado de las interacciones del usuario
 * @returns {boolean} returns.liked - Si el usuario ha dado like a la canción
 * @returns {boolean} returns.reposted - Si el usuario ha reposteado la canción
 * 
 * @example
 * const status = await getTrackInteractionStatus(123, 1);
 * if (status.liked) {
 *   console.log('El usuario ya dio like a esta canción');
 * }
 */
export const getTrackInteractionStatus = async (cancionId, usuarioId = 1) => {
  // TODO: Implementar endpoint para verificar el estado de las interacciones
  // Por ahora retornamos false, pero podrías implementar un endpoint para verificar el estado
  console.log(`Getting interaction status for track ${cancionId} and user ${usuarioId}`);
  return {
    liked: false,
    reposted: false
  };
};

/**
 * Obtiene el estado de las interacciones de un usuario para una playlist específica
 * @async
 * @function
 * @param {number} playlistId - ID de la playlist
 * @param {number} [usuarioId=1] - ID del usuario (opcional, para testing)
 * @returns {Promise<Object>} Estado de las interacciones del usuario
 * @returns {boolean} returns.liked - Si el usuario ha dado like a la playlist
 * @returns {boolean} returns.reposted - Si el usuario ha reposteado la playlist
 * 
 * @example
 * const status = await getPlaylistInteractionStatus(456, 1);
 * if (status.reposted) {
 *   console.log('El usuario ya reposteó esta playlist');
 * }
 */
export const getPlaylistInteractionStatus = async (playlistId, usuarioId = 1) => {
  // TODO: Implementar endpoint para verificar el estado de las interacciones
  // Por ahora retornamos false, pero podrías implementar un endpoint para verificar el estado
  console.log(`Getting interaction status for playlist ${playlistId} and user ${usuarioId}`);
  return {
    liked: false,
    reposted: false
  };
};
