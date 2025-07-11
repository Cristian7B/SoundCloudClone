/**
 * @fileoverview Punto de entrada principal de la aplicación React.
 * Renderiza el componente App en el DOM usando React 18 con StrictMode.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

// Renderizar la aplicación en el elemento con id 'root'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
