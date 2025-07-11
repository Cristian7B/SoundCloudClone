/**
 * @fileoverview Punto de entrada principal del módulo de enrutamiento.
 * Exporta todos los componentes, contextos y hooks relacionados con
 * la navegación y el manejo de rutas en la aplicación.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

// Componentes de enrutamiento y layout
export { default as AppRouter } from './components/AppRouter';
export { default as AppRoutes } from './components/AppRoutes';
export { default as Layout } from './components/Layout';

// Contexto de navegación global
export { NavigationProvider } from './context/NavigationContext';

// Hooks personalizados para navegación
export { useNavigation } from './hooks/useNavigation';
