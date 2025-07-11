/**
 * @fileoverview Componente de formulario de inicio de sesión con validación
 * de campos y manejo de errores integrado con el contexto de autenticación.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import styles from '../Styles/Login.module.css';

/**
 * Componente de formulario de login para autenticación de usuarios
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Function} [props.onSwitchToRegister] - Callback para cambiar al modo registro
 * @param {Function} [props.onClose] - Callback para cerrar el modal/formulario
 * @returns {JSX.Element} Formulario de inicio de sesión
 * 
 * @example
 * <Login
 *   onSwitchToRegister={() => setMode('register')}
 *   onClose={() => setIsModalOpen(false)}
 * />
 */
const Login = ({ onSwitchToRegister, onClose }) => {
  /** Contexto de autenticación con funciones y estados */
  const { login, loading, error, clearError } = useAuth();
  
  /** Estado del formulario con datos de login */
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  /** Estado para errores de validación del formulario */
  const [formErrors, setFormErrors] = useState({});

  /**
   * Maneja los cambios en los campos del formulario
   * @function
   * @param {Event} e - Evento de cambio del input
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo específico al empezar a escribir
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    // Limpiar error general si existe
    if (error) {
      clearError();
    }
  };

  /**
   * Valida los campos del formulario
   * @function
   * @returns {Object} Objeto con los errores encontrados
   */
  const validateForm = () => {
    const errors = {};

    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'El email no es válido';
    }

    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    }

    return errors;
  };

  /**
   * Maneja el envío del formulario de login
   * @async
   * @function
   * @param {Event} e - Evento de envío del formulario
   */

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    try {
      await login(formData);
      
      if (onClose) {
        onClose();
      }
    } catch (err) {
      console.error('Error en login:', err);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <div className={styles.loginHeader}>
        <h2>Iniciar sesión</h2>
        <p>Bienvenido de vuelta</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.loginForm}>
        <div className={styles.inputGroup}>
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className={formErrors.email ? styles.inputError : ''}
          />
          {formErrors.email && (
            <span className={styles.errorText}>{formErrors.email}</span>
          )}
        </div>

        <div className={styles.inputGroup}>
          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            className={formErrors.password ? styles.inputError : ''}
          />
          {formErrors.password && (
            <span className={styles.errorText}>{formErrors.password}</span>
          )}
        </div>

        {error && (
          <div className={styles.errorMessage}>
            {error}
          </div>
        )}

        <button 
          type="submit" 
          className={styles.submitButton}
          disabled={loading}
        >
          {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
        </button>
      </form>

      <div className={styles.forgotPassword}>
        <a href="#" className={styles.forgotLink}>
          ¿Olvidaste tu contraseña?
        </a>
      </div>

      <div className={styles.switchAuth}>
        <p>
          ¿No tienes cuenta?{' '}
          <button 
            type="button"
            onClick={onSwitchToRegister}
            className={styles.switchButton}
          >
            Regístrate
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;
