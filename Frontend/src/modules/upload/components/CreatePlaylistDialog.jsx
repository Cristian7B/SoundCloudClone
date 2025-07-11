import React, { useState } from 'react';
import styles from '../Styles/UploadDialog.module.css';
import axios from 'axios';

/**
 * Componente de diálogo modal para crear nuevas playlists.
 * 
 * Este componente proporciona una interfaz de usuario completa para que los usuarios
 * puedan crear playlists personalizadas con título, descripción, imagen de portada
 * y configuración de visibilidad pública/privada.
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {boolean} props.isOpen - Controla la visibilidad del diálogo modal
 * @param {Function} props.onClose - Función callback ejecutada al cerrar el diálogo
 * @param {Function} props.onSuccess - Función callback ejecutada cuando la playlist se crea exitosamente
 * 
 * @example
 * // Uso básico del componente
 * const [showDialog, setShowDialog] = useState(false);
 * 
 * const handleSuccess = (playlistData) => {
 *   console.log('Playlist creada:', playlistData);
 *   // Actualizar estado global, mostrar notificación, etc.
 * };
 * 
 * return (
 *   <CreatePlaylistDialog
 *     isOpen={showDialog}
 *     onClose={() => setShowDialog(false)}
 *     onSuccess={handleSuccess}
 *   />
 * );
 * 
 * @returns {JSX.Element|null} Elemento JSX del diálogo modal o null si no está abierto
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function CreatePlaylistDialog({ isOpen, onClose, onSuccess }) {
  /**
   * Estado local que maneja los datos del formulario de creación de playlist.
   * 
   * @type {Object}
   * @property {string} titulo - Título de la playlist (requerido)
   * @property {string} descripcion - Descripción opcional de la playlist
   * @property {string} imagen_url - URL de la imagen de portada (opcional)
   * @property {boolean} es_publica - Define si la playlist es pública (true) o privada (false)
   */
  const [formData, setFormData] = useState({
    titulo: '',
    descripcion: '',
    imagen_url: '',
    es_publica: true
  });

  /**
   * Estado que indica si el formulario está siendo enviado al servidor.
   * Se utiliza para deshabilitar el botón de envío y mostrar estado de carga.
   * 
   * @type {boolean}
   */
  const [loading, setLoading] = useState(false);

  /**
   * Estado que almacena mensajes de error para mostrar al usuario.
   * Se limpia automáticamente al cerrar el diálogo o enviar exitosamente.
   * 
   * @type {string}
   */
  const [error, setError] = useState('');

  /**
   * Maneja los cambios en los campos del formulario.
   * Actualiza el estado local formData con los nuevos valores introducidos por el usuario.
   * Maneja tanto inputs de texto como checkboxes de manera diferenciada.
   * 
   * @param {Event} e - Evento del input que disparó el cambio
   * @param {string} e.target.name - Nombre del campo modificado
   * @param {string} e.target.value - Nuevo valor del campo (para inputs de texto)
   * @param {string} e.target.type - Tipo del input (text, checkbox, etc.)
   * @param {boolean} e.target.checked - Estado del checkbox (solo para checkboxes)
   * 
   * @example
   * // Se ejecuta automáticamente cuando el usuario escribe en un input
   * // <input name="titulo" onChange={handleChange} />
   */
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  /**
   * Maneja el envío del formulario de creación de playlist.
   * 
   * Valida los datos del formulario, realiza la petición HTTP al backend
   * para crear la playlist y maneja los estados de éxito y error.
   * 
   * @async
   * @param {Event} e - Evento de envío del formulario
   * 
   * @throws {Error} Error de validación si el título está vacío
   * @throws {Error} Error de red o del servidor durante la creación
   * 
   * @example
   * // Se ejecuta cuando el usuario hace clic en "Crear Playlist"
   * // <form onSubmit={handleSubmit}>
   */

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validación básica del campo requerido
    if (!formData.titulo.trim()) {
      setError('El título es obligatorio');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Preparar payload para enviar al backend
      const payload = {
        ...formData,
        usuario_id: 1 // Para testing, luego usar usuario autenticado
      };

      // Limpiar campos vacíos excepto es_publica que debe mantener su valor boolean
      Object.keys(payload).forEach(key => {
        if (payload[key] === '' && key !== 'es_publica') {
          delete payload[key];
        }
      });

      // Realizar petición POST al endpoint de creación de playlists
      const response = await axios.post('http://127.0.0.1:8000/api/contenido/playlists/', payload);
      
      console.log('Playlist creada:', response.data);
      onSuccess && onSuccess(response.data);
      handleClose();
    } catch (err) {
      console.error('Error al crear playlist:', err);
      setError(err.response?.data?.message || 'Error al crear la playlist');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cierra el diálogo y reinicia todos los estados a sus valores iniciales.
   * 
   * Esta función se encarga de limpiar el formulario, eliminar mensajes de error
   * y ejecutar la función de cierre proporcionada por el componente padre.
   * 
   * @example
   * // Se ejecuta cuando el usuario hace clic en "Cancelar" o "X"
   * // <button onClick={handleClose}>Cancelar</button>
   */
  const handleClose = () => {
    // Reiniciar formulario a valores por defecto
    setFormData({
      titulo: '',
      descripcion: '',
      imagen_url: '',
      es_publica: true
    });
    setError('');
    onClose();
  };

  // Renderizado condicional: solo mostrar el diálogo si isOpen es true
  if (!isOpen) return null;

  /**
   * Estructura JSX del diálogo modal.
   * 
   * Incluye:
   * - Overlay de fondo con efecto blur
   * - Diálogo principal con header, formulario y acciones
   * - Formulario con campos validados
   * - Botones de acción (Cancelar/Crear)
   * - Manejo de estados de error y carga
   */

  return (
    <div className={styles.overlay}>
      <div className={styles.dialog}>
        <div className={styles.header}>
          <h2 className={styles.title}>Crear Nueva Playlist</h2>
          <button className={styles.closeButton} onClick={handleClose}>
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              Título <span className={styles.required}>*</span>
            </label>
            <input
              type="text"
              name="titulo"
              value={formData.titulo}
              onChange={handleChange}
              className={styles.input}
              placeholder="Ingresa el título de la playlist"
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>Descripción</label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              className={styles.textarea}
              placeholder="Describe tu playlist (opcional)"
              rows={4}
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>URL de la Imagen de Portada</label>
            <input
              type="url"
              name="imagen_url"
              value={formData.imagen_url}
              onChange={handleChange}
              className={styles.input}
              placeholder="https://ejemplo.com/portada-playlist.jpg"
            />
          </div>

          <div className={styles.formGroup}>
            <div className={styles.checkboxGroup}>
              <input
                type="checkbox"
                id="es_publica"
                name="es_publica"
                checked={formData.es_publica}
                onChange={handleChange}
                className={styles.checkbox}
              />
              <label htmlFor="es_publica" className={styles.checkboxLabel}>
                <span className={styles.checkboxCustom}></span>
                Hacer esta playlist pública
              </label>
            </div>
            <p className={styles.hint}>
              Las playlists públicas pueden ser vistas y seguidas por otros usuarios
            </p>
          </div>

          {error && (
            <div className={styles.error}>
              {error}
            </div>
          )}

          <div className={styles.actions}>
            <button
              type="button"
              onClick={handleClose}
              className={styles.cancelButton}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className={styles.submitButton}
            >
              {loading ? 'Creando...' : 'Crear Playlist'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
