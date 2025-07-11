/**
 * @fileoverview Archivo de constantes que centraliza la configuración de iconos
 * y recursos SVG utilizados en toda la aplicación SoundCloud Clone.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import amplificar from '../assets/amplificar.svg';
import sustituir from '../assets/sustituir.svg';
import distribuir from '../assets/distribuir.svg';
import masterizar from '../assets/masterizar.svg';
import monetizar from '../assets/monetizar.svg';
import destacados from '../assets/destacados.svg';
import fansDestacados from '../assets/fansDestacados.svg';
import comentarios from '../assets/comentarios.svg';
import before from '../assets/before.svg';
import comment from '../assets/comment.svg';
import like from '../assets/like.svg';
import mas from '../assets/mas.svg';
import menu from '../assets/menu.svg';
import message from '../assets/message.svg';
import next from '../assets/next.svg';
import notifications from '../assets/notifications.svg';
import play from '../assets/play.svg';
import repost from '../assets/repost.svg';
import search from '../assets/search.svg';

/**
 * Array de iconos disponibles para herramientas de artistas
 * @constant {Array<Object>}
 * @property {string} icon - Ruta al archivo SVG del icono
 * @property {string} title - Título descriptivo del icono
 * @example
 * iconosArtistas.forEach(({ icon, title }) => {
 *   console.log(`${title}: ${icon}`);
 * });
 */
export const iconosArtistas = [
  { icon: amplificar, title: 'Amplificar' },
  { icon: sustituir, title: 'Sustituir' },
  { icon: distribuir, title: 'Distribuir' },
  { icon: masterizar, title: 'Masterizar' },
  { icon: monetizar, title: 'Monetizar' },
  { icon: destacados, title: 'Destacados' },
  { icon: fansDestacados, title: 'Fans dest.' },
  { icon: comentarios, title: 'Comentarios' },
];

/**
 * Objeto que mapea nombres de iconos a sus respectivas rutas SVG
 * para facilitar el acceso programático a los recursos gráficos
 * @constant {Object<string, string>}
 * @example
 * // Usar un icono específico
 * const playIcon = rutasSvgs.play;
 * 
 * // Iterar sobre todos los iconos disponibles
 * Object.entries(rutasSvgs).forEach(([name, path]) => {
 *   console.log(`${name}: ${path}`);
 * });
 */
export const rutasSvgs = {
  /** Icono de flecha hacia atrás */
  before,
  /** Icono de comentario */
  comment,
  /** Icono de me gusta */
  like,
  /** Icono de más opciones */
  mas,
  /** Icono de menú */
  menu,
  /** Icono de mensaje */
  message,
  /** Icono de siguiente */
  next,
  /** Icono de notificaciones */
  notifications,
  /** Icono de reproducir */
  play,
  /** Icono de repost */
  repost,
  /** Icono de búsqueda */
  search,
};


