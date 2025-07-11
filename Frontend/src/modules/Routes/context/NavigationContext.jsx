/**
 * @fileoverview Contexto de navegación que proporciona funciones centralizadas
 * para el manejo de rutas y navegación en la aplicación SoundCloud Clone.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { createContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

/** Contexto para compartir funciones de navegación */
const NavigationContext = createContext();

/**
 * Proveedor del contexto de navegación que centraliza todas las funciones
 * de navegación de la aplicación
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {React.ReactNode} props.children - Componentes hijos
 * @returns {JSX.Element} Proveedor del contexto de navegación
 * 
 * @example
 * <NavigationProvider>
 *   <App />
 * </NavigationProvider>
 */
export const NavigationProvider = ({ children }) => {
  /** Hook de React Router para navegación programática */
  const navigate = useNavigate();
  
  /** Hook de React Router para obtener la ubicación actual */
  const location = useLocation();

  /**
   * Navega a la página principal
   * @function
   */
  const navigateToHome = () => {
    navigate('/home');
  };

  /**
   * Navega a la biblioteca de música
   * @function
   */
  const navigateToLibrary = () => {
    navigate('/library');
  };

  /**
   * Navega al feed de actividades
   * @function
   */
  const navigateToFeed = () => {
    navigate('/feed');
  };

  /**
   * Navega a una ruta específica
   * @function
   * @param {string} path - Ruta de destino
   * @example
   * navigateTo('/profile/123');
   */
  const navigateTo = (path) => {
    navigate(path);
  };

  /**
   * Navega a una playlist específica
   * @function
   * @param {string|number} playlistId - ID de la playlist
   * @example
   * navigateToPlaylist('abc123');
   */
  const navigateToPlaylist = (playlistId) => {
    navigate(`/playlist/${playlistId}`);
  };

  /**
   * Navega hacia atrás en el historial
   * @function
   */
  const goBack = () => {
    navigate(-1);
  };

  /**
   * Obtiene la ruta actual
   * @function
   * @returns {string} Ruta actual del pathname
   */
  const getCurrentRoute = () => {
    return location.pathname;
  };

  /**
   * Verifica si una ruta está activa
   * @function
   * @param {string} route - Ruta a verificar
   * @returns {boolean} True si la ruta está activa
   * @example
   * const isHome = isActiveRoute('/home');
   */
  const isActiveRoute = (route) => {
    return location.pathname === route;
  };

  /** Valor del contexto con todas las funciones de navegación */
  const value = {
    navigateToHome,
    navigateToLibrary,
    navigateToFeed,
    navigateTo,
    navigateToPlaylist,
    goBack,
    getCurrentRoute,
    isActiveRoute,
    currentPath: location.pathname,
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};

export default NavigationContext;
