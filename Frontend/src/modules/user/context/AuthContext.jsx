/**
 * @fileoverview Contexto de autenticación para la aplicación SoundCloud Clone.
 * Proporciona un estado global para la autenticación de usuarios y funciones
 * relacionadas como login, registro, logout y gestión de errores.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import authService from '../services/authService';

/**
 * Estado inicial del contexto de autenticación
 * @constant {Object}
 */
const initialState = {
  /** @type {Object|null} - Datos del usuario autenticado */
  user: null,
  /** @type {boolean} - Indica si el usuario está autenticado */
  isAuthenticated: false,
  /** @type {boolean} - Indica si se está cargando información */
  loading: true,
  /** @type {string|null} - Mensaje de error actual */
  error: null,
};

/**
 * Acciones disponibles para el reducer de autenticación
 * @constant {Object}
 */
const AUTH_ACTIONS = {
  /** Acción para establecer el estado de carga */
  SET_LOADING: 'SET_LOADING',
  /** Acción para establecer los datos del usuario */
  SET_USER: 'SET_USER',
  /** Acción para establecer un error */
  SET_ERROR: 'SET_ERROR',
  /** Acción para cerrar sesión */
  LOGOUT: 'LOGOUT',
  /** Acción para limpiar errores */
  CLEAR_ERROR: 'CLEAR_ERROR',
};

/**
 * Reducer para manejar las acciones del estado de autenticación
 * @param {Object} state - Estado actual
 * @param {Object} action - Acción a ejecutar
 * @param {string} action.type - Tipo de acción
 * @param {*} action.payload - Datos de la acción
 * @returns {Object} Nuevo estado
 */
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      };
    case AUTH_ACTIONS.SET_USER:
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        loading: false,
        error: null,
      };
    case AUTH_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
      };
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      };
    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

/** Contexto de autenticación */
const AuthContext = createContext();

/**
 * Hook personalizado para acceder al contexto de autenticación
 * @returns {Object} Contexto de autenticación con estado y funciones
 * @throws {Error} Si se usa fuera del AuthProvider
 * @example
 * const { user, isAuthenticated, login, logout } = useAuth();
 */

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

/**
 * Proveedor del contexto de autenticación que maneja el estado global de autenticación
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {React.ReactNode} props.children - Componentes hijos
 * @returns {JSX.Element} Proveedor del contexto envolviendo los componentes hijos
 * @example
 * <AuthProvider>
 *   <App />
 * </AuthProvider>
 */
export const AuthProvider = ({ children }) => {
  /** Estado del contexto manejado por useReducer */
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Verificar autenticación al montar el componente
  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Verifica si el usuario está autenticado al cargar la aplicación
   * @async
   * @function
   */
  const checkAuth = async () => {
    try {
      if (authService.isAuthenticated()) {
        const userData = await authService.getProfile();
        dispatch({ type: AUTH_ACTIONS.SET_USER, payload: userData });
      } else {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
      }
    } catch (error) {
      console.error('Error checking auth:', error);
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
    }
  };

  /**
   * Registra un nuevo usuario en la aplicación
   * @async
   * @param {Object} userData - Datos del usuario a registrar
   * @param {string} userData.email - Email del usuario
   * @param {string} userData.password - Contraseña del usuario
   * @param {string} userData.username - Nombre de usuario
   * @returns {Promise<Object>} Respuesta del servicio de registro
   * @throws {Error} Error de validación o servidor
   */
  const register = async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
      
      const response = await authService.register(userData);
      dispatch({ type: AUTH_ACTIONS.SET_USER, payload: response.user });
      
      return response;
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  /**
   * Inicia sesión de un usuario existente
   * @async
   * @param {Object} credentials - Credenciales de login
   * @param {string} credentials.email - Email del usuario
   * @param {string} credentials.password - Contraseña del usuario
   * @returns {Promise<Object>} Respuesta del servicio de login
   * @throws {Error} Error de autenticación
   */
  const login = async (credentials) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
      
      const response = await authService.login(credentials);
      dispatch({ type: AUTH_ACTIONS.SET_USER, payload: response.user });
      
      return response;
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  /**
   * Cierra la sesión del usuario actual
   * @async
   * @function
   */
  const logout = async () => {
    try {
      await authService.logout();
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    } catch (error) {
      console.error('Error during logout:', error);
      // Forzar logout local incluso si hay error
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  };

  /**
   * Actualiza el perfil del usuario autenticado
   * @async
   * @param {Object} userData - Nuevos datos del usuario
   * @returns {Promise<Object>} Respuesta del servicio de actualización
   * @throws {Error} Error de validación o servidor
   */
  const updateProfile = async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
      
      const response = await authService.updateProfile(userData);
      dispatch({ type: AUTH_ACTIONS.SET_USER, payload: response.user });
      
      return response;
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  /**
   * Limpia el mensaje de error actual
   * @function
   */
  const clearError = () => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  };

  /** Valor del contexto con estado y funciones disponibles */
  const value = {
    ...state,
    register,
    login,
    logout,
    updateProfile,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
