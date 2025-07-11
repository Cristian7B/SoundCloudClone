/**
 * @fileoverview Configuración de ESLint para el proyecto SoundCloud Clone Frontend.
 * Define las reglas de linting, plugins y configuraciones para mantener
 * la calidad del código React/JavaScript.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 * @see {@link https://eslint.org/docs/latest/} Documentación oficial de ESLint
 */

import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

/**
 * Configuración principal de ESLint para el proyecto
 * @type {import('eslint').Linter.Config[]}
 */
export default defineConfig([
  // Ignorar carpeta de distribución
  globalIgnores(['dist']),
  {
    // Archivos objetivo para linting
    files: ['**/*.{js,jsx}'],
    
    // Extensiones de configuraciones base
    extends: [
      js.configs.recommended,
      reactHooks.configs['recommended-latest'],
      reactRefresh.configs.vite,
    ],
    
    // Configuración del lenguaje y entorno
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    
    // Reglas personalizadas
    rules: {
      // Permitir variables no usadas que empiecen con mayúscula o guión bajo
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
    },
  },
])
