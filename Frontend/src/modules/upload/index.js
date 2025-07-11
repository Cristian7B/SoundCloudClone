/**
 * Módulo de Upload para SoundCloud Clone
 * 
 * Este módulo proporciona todas las funcionalidades relacionadas con la carga
 * y creación de contenido musical en la plataforma. Incluye componentes para
 * subir canciones, crear playlists y gestionar el contenido del usuario.
 * 
 * @module Upload
 * @version 1.0.0
 * @author Tu Nombre
 * 
 * @description
 * El módulo Upload está diseñado para ser completamente autocontenido y reutilizable.
 * Proporciona interfaces de usuario modernas con tema dark, validación de formularios,
 * manejo de errores y integración completa con el backend Django.
 * 
 * @features
 * - Subida de canciones con metadatos completos
 * - Creación de playlists públicas y privadas
 * - Diálogos modales responsivos y accesibles
 * - Validación de formularios en tiempo real
 * - Integración con APIs REST del backend
 * - Tema dark consistente
 * - Efectos visuales modernos
 * 
 * @dependencies
 * - React (hooks: useState)
 * - Axios (peticiones HTTP)
 * - CSS Modules (estilos encapsulados)
 * 
 * @apiEndpoints
 * - POST /api/contenido/canciones/ - Crear nueva canción
 * - POST /api/contenido/playlists/ - Crear nueva playlist
 * 
 * @examples
 * // Importar componentes individuales
 * import { UploadSongDialog, CreatePlaylistDialog } from '../modules/upload';
 * 
 * // Importar página completa
 * import { UploadPage } from '../modules/upload';
 * 
 * // Importar botones integrados
 * import { UploadButtons } from '../modules/upload';
 */

/**
 * Componente de diálogo modal para subir nuevas canciones.
 * Proporciona formulario completo con validación para metadatos musicales.
 * 
 * @see {@link ./components/UploadSongDialog.jsx} Para implementación completa
 */
export { UploadSongDialog } from './components/UploadSongDialog';

/**
 * Componente de diálogo modal para crear nuevas playlists.
 * Permite configurar título, descripción, portada y visibilidad.
 * 
 * @see {@link ./components/CreatePlaylistDialog.jsx} Para implementación completa
 */
export { CreatePlaylistDialog } from './components/CreatePlaylistDialog';

/**
 * Componente de botones integrados para acceso rápido a funcionalidades de upload.
 * Incluye gestión de estado y apertura de diálogos modales.
 * 
 * @see {@link ./components/UploadButtons.jsx} Para implementación completa
 */
export { UploadButtons } from './components/UploadButtons';

/**
 * Página completa de upload con presentación visual y características.
 * Incluye header, botones de acción y sección explicativa de funcionalidades.
 * 
 * @see {@link ./components/UploadPage.jsx} Para implementación completa
 */
export { UploadPage } from './components/UploadPage';
