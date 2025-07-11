/**
 * @fileoverview Hook personalizado para manejar el estado y las acciones
 * del modal de autenticación (login/registro).
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

/**
 * Hook personalizado para gestionar el modal de autenticación
 * @hook
 * @returns {Object} Estado y funciones para controlar el modal de autenticación
 * @returns {boolean} returns.isAuthModalOpen - Estado de apertura del modal
 * @returns {string} returns.authMode - Modo actual del modal ('login' | 'register')
 * @returns {Function} returns.openLoginModal - Función para abrir el modal en modo login
 * @returns {Function} returns.openRegisterModal - Función para abrir el modal en modo registro
 * @returns {Function} returns.closeAuthModal - Función para cerrar el modal
 * 
 * @example
 * const {
 *   isAuthModalOpen,
 *   authMode,
 *   openLoginModal,
 *   openRegisterModal,
 *   closeAuthModal
 * } = useAuthModal();
 * 
 * // Abrir modal de login
 * openLoginModal();
 * 
 * // Abrir modal de registro
 * openRegisterModal();
 */
export const useAuthModal = () => {
  /** Estado para controlar la apertura/cierre del modal */
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  
  /** Estado para controlar el modo del modal ('login' | 'register') */
  const [authMode, setAuthMode] = useState('login');
  
  /** Contexto de autenticación para verificar si el usuario está autenticado */
  const { isAuthenticated } = useAuth();

  // Cerrar modal automáticamente cuando el usuario se autentica
  useEffect(() => {
    if (isAuthenticated) {
      setIsAuthModalOpen(false);
    }
  }, [isAuthenticated]);

  /**
   * Abre el modal de autenticación en modo login
   * @function
   */
  const openLoginModal = () => {
    setAuthMode('login');
    setIsAuthModalOpen(true);
  };

  /**
   * Abre el modal de autenticación en modo registro
   * @function
   */
  const openRegisterModal = () => {
    setAuthMode('register');
    setIsAuthModalOpen(true);
  };

  /**
   * Cierra el modal de autenticación
   * @function
   */
  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
  };

  return {
    isAuthModalOpen,
    authMode,
    openLoginModal,
    openRegisterModal,
    closeAuthModal,
  };
};
