import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import styles from '../Styles/Register.module.css';

const Register = ({ onSwitchToLogin, onClose }) => {
  const { register, loading, error, clearError } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
  });

  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    if (error) {
      clearError();
    }
  };

  const validateForm = () => {
    const errors = {};

    if (!formData.username.trim()) {
      errors.username = 'El nombre de usuario es requerido';
    }

    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'El email no es válido';
    }

    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }

    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Confirma tu contraseña';
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden';
    }

    if (!formData.first_name.trim()) {
      errors.first_name = 'El nombre es requerido';
    }

    if (!formData.last_name.trim()) {
      errors.last_name = 'El apellido es requerido';
    }

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    try {
      const { confirmPassword, ...registerData } = formData;
      await register(registerData);
      
      if (onClose) {
        onClose();
      }
    } catch (err) {
      console.error('Error en registro:', err);
    }
  };

  return (
    <div className={styles.registerContainer}>
      <div className={styles.registerHeader}>
        <h2>Crear cuenta</h2>
        <p>Únete a la comunidad de música</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.registerForm}>
        <div className={styles.inputGroup}>
          <input
            type="text"
            name="first_name"
            placeholder="Nombre"
            value={formData.first_name}
            onChange={handleChange}
            className={formErrors.first_name ? styles.inputError : ''}
          />
          {formErrors.first_name && (
            <span className={styles.errorText}>{formErrors.first_name}</span>
          )}
        </div>

        <div className={styles.inputGroup}>
          <input
            type="text"
            name="last_name"
            placeholder="Apellido"
            value={formData.last_name}
            onChange={handleChange}
            className={formErrors.last_name ? styles.inputError : ''}
          />
          {formErrors.last_name && (
            <span className={styles.errorText}>{formErrors.last_name}</span>
          )}
        </div>

        <div className={styles.inputGroup}>
          <input
            type="text"
            name="username"
            placeholder="Nombre de usuario"
            value={formData.username}
            onChange={handleChange}
            className={formErrors.username ? styles.inputError : ''}
          />
          {formErrors.username && (
            <span className={styles.errorText}>{formErrors.username}</span>
          )}
        </div>

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

        <div className={styles.inputGroup}>
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirmar contraseña"
            value={formData.confirmPassword}
            onChange={handleChange}
            className={formErrors.confirmPassword ? styles.inputError : ''}
          />
          {formErrors.confirmPassword && (
            <span className={styles.errorText}>{formErrors.confirmPassword}</span>
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
          {loading ? 'Creando cuenta...' : 'Crear cuenta'}
        </button>
      </form>

      <div className={styles.switchAuth}>
        <p>
          ¿Ya tienes cuenta?{' '}
          <button 
            type="button"
            onClick={onSwitchToLogin}
            className={styles.switchButton}
          >
            Inicia sesión
          </button>
        </p>
      </div>
    </div>
  );
};

export default Register;
