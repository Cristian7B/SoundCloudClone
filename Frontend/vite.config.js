/**
 * @fileoverview Configuración de Vite para el proyecto SoundCloud Clone Frontend.
 * Define los plugins, optimizaciones y configuraciones de build para la aplicación React.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 * @see {@link https://vite.dev/config/} Documentación oficial de Vite
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

/**
 * Configuración principal de Vite
 * @type {import('vite').UserConfig}
 */
export default defineConfig({
  /** Plugins de Vite utilizados en el proyecto */
  plugins: [
    /** Plugin de React con SWC para compilación rápida */
    react()
  ],
});
