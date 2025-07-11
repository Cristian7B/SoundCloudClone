/**
 * @fileoverview Punto de entrada principal del módulo de usuario.
 * Exporta todos los componentes, contextos, hooks y servicios relacionados
 * con la autenticación y gestión de usuarios.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

// Componentes de autenticación y perfil de usuario
export { default as Login } from './components/Login';
export { default as Register } from './components/Register';
export { default as UserProfile } from './components/UserProfile';
export { default as AuthModal } from './components/AuthModal';
export { default as UserMenu } from './components/UserMenu';

// Contexto de autenticación global
export { AuthProvider, useAuth } from './context/AuthContext';

// Hooks personalizados para funcionalidades de usuario
export { useAuthModal } from './hooks/useAuthModal';

// Servicios para comunicación con APIs de autenticación
export { default as authService } from './services/authService';
