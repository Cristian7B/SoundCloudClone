/**
 * @fileoverview Componente principal de la aplicación SoundCloud Clone.
 * Configura el enrutamiento principal y los proveedores de contexto globales.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import './App.css'
import { ArtistTools } from './modules/generalComponents/components/ArtistTools'
import { Nav } from './modules/generalComponents/components/Nav'
import { Library } from './modules/library/components/Library'
import { AppRouter } from './modules/Routes'
import { AuthProvider } from './modules/user'

/**
 * Componente raíz de la aplicación que configura el enrutamiento
 * y los proveedores de contexto necesarios
 * @component
 * @returns {JSX.Element} Aplicación principal con enrutamiento configurado
 * 
 * @example
 * // Uso típico en main.jsx
 * import App from './App.jsx'
 * 
 * ReactDOM.createRoot(document.getElementById('root')).render(
 *   <React.StrictMode>
 *     <App />
 *   </React.StrictMode>,
 * )
 */
function App() {
  return (
    <>
      {/* Router principal que maneja todas las rutas de la aplicación */}
      <AppRouter/>
    </>
  )
}

export default App;
