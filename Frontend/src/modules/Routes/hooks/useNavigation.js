/**
 * @fileoverview Hook personalizado para acceder al contexto de navegación
 * y utilizar las funciones de navegación en toda la aplicación.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import { useContext } from 'react';
import NavigationContext from '../context/NavigationContext';

/**
 * Hook personalizado para acceder al contexto de navegación
 * @hook
 * @returns {Object} Objeto con todas las funciones de navegación disponibles
 * @returns {Function} returns.navigateToHome - Navegar a la página principal
 * @returns {Function} returns.navigateToLibrary - Navegar a la biblioteca
 * @returns {Function} returns.navigateToFeed - Navegar al feed
 * @returns {Function} returns.navigateTo - Navegar a una ruta específica
 * @returns {Function} returns.navigateToPlaylist - Navegar a una playlist
 * @returns {Function} returns.goBack - Navegar hacia atrás
 * @returns {Function} returns.getCurrentRoute - Obtener la ruta actual
 * @returns {Function} returns.isActiveRoute - Verificar si una ruta está activa
 * @returns {string} returns.currentPath - Ruta actual
 * @throws {Error} Si se usa fuera del NavigationProvider
 * 
 * @example
 * const { navigateToHome, isActiveRoute, currentPath } = useNavigation();
 * 
 * // Navegar a home
 * navigateToHome();
 * 
 * // Verificar si estamos en home
 * const isHome = isActiveRoute('/home');
 * 
 * // Obtener ruta actual
 * console.log('Ruta actual:', currentPath);
 */
export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation debe ser usado dentro de un NavigationProvider');
  }
  return context;
};
