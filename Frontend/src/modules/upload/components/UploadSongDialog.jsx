import React, { useState } from 'react';
import styles from '../Styles/UploadDialog.module.css';
import axios from 'axios';

/**
 * Componente de diálogo modal para subir nuevas canciones.
 * 
 * Este componente proporciona una interfaz completa para que los usuarios puedan
 * subir canciones con metadatos detallados incluyendo título, descripción, archivos
 * de audio e imagen, duración, género y álbum asociado.
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {boolean} props.isOpen - Controla la visibilidad del diálogo modal
 * @param {Function} props.onClose - Función callback ejecutada al cerrar el diálogo
 * @param {Function} props.onSuccess - Función callback ejecutada cuando la canción se sube exitosamente
 * 
 * @example
 * // Uso básico del componente
 * const [showDialog, setShowDialog] = useState(false);
 * 
 * const handleSuccess = (songData) => {
 *   console.log('Canción subida:', songData);
 *   // Actualizar biblioteca, mostrar notificación, etc.
 * };
 * 
 * return (
 *   <UploadSongDialog
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
export function UploadSongDialog({ isOpen, onClose, onSuccess }) {
  /**
   * Estado local que maneja los datos del formulario de subida de canción.
   * 
   * @type {Object}
   * @property {string} titulo - Título de la canción (requerido)
   * @property {string} descripcion - Descripción opcional de la canción
   * @property {string} archivo_url - URL del archivo de audio (requerido)
   * @property {string} imagen_url - URL de la imagen de portada (opcional)
   * @property {string} duracion - Duración de la canción en formato MM:SS (opcional)
   * @property {string} genero - Género musical seleccionado (opcional)
   * @property {string} album - Nombre del álbum al que pertenece (opcional)
   */
  const [formData, setFormData] = useState({
    titulo: '',
    descripcion: '',
    archivo_url: '',
    imagen_url: '',
    duracion: '',
    genero: '',
    album: ''
  });

  /**
   * Estado que indica si el formulario está siendo enviado al servidor.
   * Se utiliza para deshabilitar controles y mostrar estado de carga.
   * 
   * @type {boolean}
   */
  const [loading, setLoading] = useState(false);

  /**
   * Estado que almacena mensajes de error para mostrar al usuario.
   * Se actualiza durante la validación y peticiones al servidor.
   * 
   * @type {string}
   */
  const [error, setError] = useState('');

  /**
   * Maneja los cambios en todos los campos del formulario.
   * Actualiza el estado local formData con los nuevos valores introducidos.
   * 
   * @param {Event} e - Evento del input que disparó el cambio
   * @param {string} e.target.name - Nombre del campo modificado
   * @param {string} e.target.value - Nuevo valor del campo
   * 
   * @example
   * // Se ejecuta automáticamente en cada cambio de input
   * // <input name="titulo" onChange={handleChange} />
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  /**
   * Maneja el envío del formulario de subida de canción.
   * 
   * Valida campos requeridos, prepara el payload y realiza la petición
   * HTTP al backend para crear la nueva canción en la base de datos.
   * 
   * @async
   * @param {Event} e - Evento de envío del formulario
   * 
   * @throws {Error} Error de validación si faltan campos requeridos
   * @throws {Error} Error de red o del servidor durante la subida
   * 
   * @example
   * // Se ejecuta cuando el usuario hace clic en "Subir Canción"
   * // <form onSubmit={handleSubmit}>
   */

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validación de campos requeridos
    if (!formData.titulo.trim() || !formData.archivo_url.trim()) {
      setError('El título y la URL del archivo son obligatorios');
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

      // Limpiar campos vacíos para evitar enviar strings vacías
      Object.keys(payload).forEach(key => {
        if (payload[key] === '') {
          delete payload[key];
        }
      });

      // Realizar petición POST al endpoint de creación de canciones
      const response = await axios.post('http://127.0.0.1:8000/api/contenido/canciones/', payload);
      
      console.log('Canción creada:', response.data);
      onSuccess && onSuccess(response.data);
      handleClose();
    } catch (err) {
      console.error('Error al crear canción:', err);
      setError(err.response?.data?.message || 'Error al crear la canción');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cierra el diálogo y reinicia todos los estados a sus valores iniciales.
   * 
   * Esta función se encarga de limpiar completamente el formulario, eliminar
   * mensajes de error y ejecutar la función de cierre del componente padre.
   * 
   * @example
   * // Se ejecuta cuando el usuario hace clic en "Cancelar" o "X"
   * // <button onClick={handleClose}>Cancelar</button>
   */

  const handleClose = () => {
    setFormData({
      titulo: '',
      descripcion: '',
      archivo_url: '',
      imagen_url: '',
      duracion: '',
      genero: '',
      album: ''
    });
    setError('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.dialog}>
        <div className={styles.header}>
          <h2 className={styles.title}>Subir Nueva Canción</h2>
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
              placeholder="Ingresa el título de la canción"
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
              placeholder="Describe tu canción (opcional)"
              rows={3}
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>
              URL del Archivo de Audio <span className={styles.required}>*</span>
            </label>
            <input
              type="url"
              name="archivo_url"
              value={formData.archivo_url}
              onChange={handleChange}
              className={styles.input}
              placeholder="https://ejemplo.com/mi-cancion.mp3"
              required
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
              placeholder="https://ejemplo.com/portada.jpg"
            />
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label className={styles.label}>Duración</label>
              <input
                type="text"
                name="duracion"
                value={formData.duracion}
                onChange={handleChange}
                className={styles.input}
                placeholder="00:03:45"
              />
            </div>

            <div className={styles.formGroup}>
              <label className={styles.label}>Género</label>
              <select
                name="genero"
                value={formData.genero}
                onChange={handleChange}
                className={styles.select}
              >
                <option value="">Seleccionar género</option>
                <option value="Rock">Rock</option>
                <option value="Pop">Pop</option>
                <option value="Hip Hop">Hip Hop</option>
                <option value="Electronic">Electronic</option>
                <option value="Jazz">Jazz</option>
                <option value="Classical">Classical</option>
                <option value="Reggaeton">Reggaeton</option>
                <option value="Salsa">Salsa</option>
                <option value="Blues">Blues</option>
                <option value="Country">Country</option>
                <option value="R&B">R&B</option>
                <option value="Indie">Indie</option>
                <option value="Folk">Folk</option>
                <option value="Punk">Punk</option>
                <option value="Metal">Metal</option>
                <option value="Otro">Otro</option>
              </select>
            </div>
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>Álbum</label>
            <input
              type="text"
              name="album"
              value={formData.album}
              onChange={handleChange}
              className={styles.input}
              placeholder="Nombre del álbum (opcional)"
            />
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
              {loading ? 'Subiendo...' : 'Subir Canción'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
