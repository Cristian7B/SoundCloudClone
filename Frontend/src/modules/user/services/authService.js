/**
 * @fileoverview Servicio de autenticación que maneja todas las operaciones
 * relacionadas con la autenticación de usuarios incluyendo login, registro,
 * logout, gestión de tokens y perfil de usuario.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

/** URL base para las APIs de autenticación */
const API_BASE_URL = 'http://127.0.0.1:8000/api/auth'; 

/**
 * Servicio para manejar operaciones de autenticación
 * @class AuthService
 */
class AuthService {
  /**
   * Registra un nuevo usuario en el sistema
   * @async
   * @param {Object} userData - Datos del usuario para el registro
   * @param {string} userData.username - Nombre de usuario
   * @param {string} userData.email - Correo electrónico
   * @param {string} userData.password - Contraseña
   * @param {string} userData.password_confirm - Confirmación de contraseña
   * @returns {Promise<Object>} Datos del usuario registrado y tokens
   * @throws {Error} Error específico según el tipo de validación fallida
   * @example
   * const userData = {
   *   username: 'usuario123',
   *   email: 'usuario@email.com',
   *   password: 'password123',
   *   password_confirm: 'password123'
   * };
   * const result = await authService.register(userData);
   */
  async register(userData) {
    // eslint-disable-next-line no-useless-catch
    try {
      const response = await fetch(`${API_BASE_URL}/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        // Manejo específico de errores de validación
        if (data.username) {
          throw new Error(`Username: ${data.username[0]}`);
        } else if (data.email) {
          throw new Error(`Email: ${data.email[0]}`);
        } else if (data.password) {
          throw new Error(`Password: ${data.password[0]}`);
        } else if (data.non_field_errors) {
          throw new Error(data.non_field_errors[0]);
        } else if (data.detail) {
          throw new Error(data.detail);
        } else {
          throw new Error(data.message || 'Error en el registro');
        }
      }

      // Almacenar tokens en localStorage
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Inicia sesión de un usuario existente
   * @async
   * @param {Object} credentials - Credenciales de acceso
   * @param {string} credentials.email - Email o username del usuario
   * @param {string} credentials.password - Contraseña del usuario
   * @returns {Promise<Object>} Datos del usuario y tokens de acceso
   * @throws {Error} Error de autenticación o validación
   * @example
   * const credentials = {
   *   email: 'usuario@email.com',
   *   password: 'password123'
   * };
   * const result = await authService.login(credentials);
   */
  async login(credentials) {
    try {
      const loginData = {
        email: credentials.email || credentials.username, // El backend espera email
        password: credentials.password
      };

      console.log('Sending login data:', loginData); // Debug log

      const response = await fetch(`${API_BASE_URL}/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });

      const data = await response.json();
      console.log('Login response:', { status: response.status, data }); // Debug log

      if (!response.ok) {
        // Manejo específico de errores de login
        if (data.non_field_errors) {
          throw new Error(data.non_field_errors[0]);
        } else if (data.email) {
          throw new Error(data.email[0]);
        } else if (data.password) {
          throw new Error(data.password[0]);
        } else if (data.detail) {
          throw new Error(data.detail);
        } else {
          throw new Error(data.message || 'Error en el login');
        }
      }

      // Almacenar tokens en localStorage
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      return data;
    } catch (error) {
      console.error('Login error:', error); // Debug log
      throw error;
    }
  }

  /**
   * Cierra la sesión del usuario actual
   * @async
   * @returns {Promise<Object>} Mensaje de confirmación de logout
   * @throws {Error} Error durante el proceso de logout
   * @example
   * await authService.logout();
   */
  async logout() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        // Invalidar el refresh token en el servidor
        await fetch(`${API_BASE_URL}/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: refreshToken }),
        });
      }

      // Limpiar tokens del localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      return { message: 'Logout exitoso' };
    } catch (error) {
      // Limpiar tokens localmente incluso si hay error
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw error;
    }
  }

  /**
   * Obtiene el perfil del usuario autenticado
   * @async
   * @returns {Promise<Object>} Datos del perfil del usuario
   * @throws {Error} Error si no hay token o falló la petición
   * @example
   * const profile = await authService.getProfile();
   * console.log(profile.username, profile.email);
   */
  async getProfile() {
    // eslint-disable-next-line no-useless-catch
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        throw new Error('No hay token de acceso');
      }

      const response = await fetch(`${API_BASE_URL}/profile/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        // Si el token expiró, intentar renovarlo
        if (response.status === 401) {
          await this.refreshToken();
          return this.getProfile();
        }
        throw new Error(data.message || 'Error al obtener perfil');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Actualiza la información del perfil del usuario
   * @async
   * @param {Object} userData - Nuevos datos del usuario
   * @param {string} [userData.username] - Nuevo nombre de usuario
   * @param {string} [userData.email] - Nuevo email
   * @param {string} [userData.first_name] - Nuevo nombre
   * @param {string} [userData.last_name] - Nuevo apellido
   * @returns {Promise<Object>} Datos actualizados del usuario
   * @throws {Error} Error de validación o autenticación
   * @example
   * const updatedData = {
   *   username: 'nuevo_username',
   *   first_name: 'Juan'
   * };
   * const result = await authService.updateProfile(updatedData);
   */
  async updateProfile(userData) {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        throw new Error('No hay token de acceso');
      }

      const response = await fetch(`${API_BASE_URL}/update-info/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        // Si el token expiró, intentar renovarlo
        if (response.status === 401) {
          await this.refreshToken();
          return this.updateProfile(userData);
        }
        throw new Error(data.message || 'Error al actualizar perfil');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Renueva el token de acceso usando el refresh token
   * @async
   * @returns {Promise<Object>} Nuevo token de acceso
   * @throws {Error} Error si el refresh token es inválido o expiró
   * @private
   */
  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!refreshToken) {
        throw new Error('No hay refresh token');
      }

      const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Si el refresh token expiró, cerrar sesión
        this.logout();
        throw new Error('Sesión expirada');
      }

      // Actualizar el access token
      localStorage.setItem('access_token', data.access);
      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Verifica si el usuario está autenticado
   * @returns {boolean} True si hay un token de acceso válido
   * @example
   * if (authService.isAuthenticated()) {
   *   // Usuario autenticado
   * }
   */
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }

  /**
   * Obtiene el token de acceso actual
   * @returns {string|null} Token de acceso o null si no existe
   * @example
   * const token = authService.getToken();
   */
  getToken() {
    return localStorage.getItem('access_token');
  }
}

/** Instancia única del servicio de autenticación */
export default new AuthService();
