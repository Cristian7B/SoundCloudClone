/**
 * @fileoverview Modal de autenticación que permite alternar entre
 * los formularios de login y registro de usuarios.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { useState } from 'react';
import Login from './Login';
import Register from './Register';
import styles from '../Styles/AuthModal.module.css';

/**
 * Componente modal que contiene los formularios de autenticación
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {boolean} props.isOpen - Controla la visibilidad del modal
 * @param {Function} props.onClose - Función para cerrar el modal
 * @param {string} [props.initialMode='login'] - Modo inicial del modal ('login' | 'register')
 * @returns {JSX.Element|null} Modal de autenticación o null si está cerrado
 * 
 * @example
 * <AuthModal
 *   isOpen={isModalOpen}
 *   onClose={() => setIsModalOpen(false)}
 *   initialMode="login"
 * />
 */
const AuthModal = ({ isOpen, onClose, initialMode = 'login' }) => {
  /** Estado para controlar el modo actual del modal */
  const [mode, setMode] = useState(initialMode);

  // No renderizar el modal si no está abierto
  if (!isOpen) return null;

  /**
   * Cambia el modal al modo de login
   * @function
   */
  const handleSwitchToLogin = () => {
    setMode('login');
  };

  /**
   * Cambia el modal al modo de registro
   * @function
   */
  const handleSwitchToRegister = () => {
    setMode('register');
  };

  /**
   * Cierra el modal y resetea al modo login
   * @function
   */
  const handleClose = () => {
    setMode('login'); // Reset to login when closing
    onClose();
  };

  return (
    <div className={styles.modalOverlay} onClick={handleClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        {/* Botón para cerrar el modal */}
        <button 
          className={styles.closeButton}
          onClick={handleClose}
          aria-label="Cerrar modal"
        >
          ×
        </button>
        
        {/* Renderizado condicional del formulario según el modo */}
        {mode === 'login' ? (
          <Login 
            onSwitchToRegister={handleSwitchToRegister}
            onClose={handleClose}
          />
        ) : (
          <Register 
            onSwitchToLogin={handleSwitchToLogin}
            onClose={handleClose}
          />
        )}
      </div>
    </div>
  );
};

export default AuthModal;
