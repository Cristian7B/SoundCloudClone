import React from 'react';
import { UploadButtons } from './UploadButtons';
import styles from '../Styles/UploadPage.module.css';

/**
 * Página principal de carga de contenido para la aplicación SoundCloud Clone.
 * 
 * Esta página proporciona una interfaz completa y atractiva para que los usuarios
 * puedan acceder a todas las funcionalidades de upload de contenido. Incluye
 * una presentación visual de las características, botones de acción principales
 * y una descripción detallada de las capacidades de la plataforma.
 * 
 * @component
 * 
 * @example
 * // Uso como página principal de upload
 * import { UploadPage } from '../modules/upload';
 * 
 * function App() {
 *   return (
 *     <Router>
 *       <Route path="/upload" component={UploadPage} />
 *     </Router>
 *   );
 * }
 * 
 * @example
 * // Uso en un dashboard de usuario
 * function UserDashboard() {
 *   return (
 *     <div>
 *       <Navigation />
 *       <UploadPage />
 *       <Footer />
 *     </div>
 *   );
 * }
 * 
 * @returns {JSX.Element} Elemento JSX de la página completa de upload
 * 
 * @features
 * - Header atractivo con título y descripción
 * - Botones integrados para subir canciones y crear playlists
 * - Sección de características explicativas
 * - Diseño responsivo y accesible
 * - Tema dark consistente con la aplicación
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function UploadPage() {
  /**
   * Estructura JSX de la página completa.
   * 
   * La página está organizada en las siguientes secciones:
   * 1. Header - Título principal y descripción de la funcionalidad
   * 2. Content - Botones de acción principales (UploadButtons)
   * 3. Features - Grid de características explicativas con iconos
   * 
   * Cada sección utiliza CSS Modules para estilos encapsulados y
   * mantiene la consistencia visual con el resto de la aplicación.
   */
  return (
    <div className={styles.uploadPage}>
      <div className={styles.container}>
        {/* Header principal con título y descripción */}
        <header className={styles.header}>
          <h1 className={styles.title}>Sube tu Música</h1>
          <p className={styles.subtitle}>
            Comparte tus creaciones con el mundo. Sube canciones individuales o crea playlists personalizadas.
          </p>
        </header>

        {/* Sección principal con botones de acción */}
        <section className={styles.content}>
          <UploadButtons />
        </section>

        {/* Grid de características y beneficios */}
        <section className={styles.features}>
          {/* Característica 1: Subida de canciones */}
          <div className={styles.feature}>
            <div className={styles.featureIcon}>🎵</div>
            <h3 className={styles.featureTitle}>Sube Canciones</h3>
            <p className={styles.featureDescription}>
              Comparte tu música favorita con título, descripción, portada y más detalles
            </p>
          </div>

          {/* Característica 2: Creación de playlists */}
          <div className={styles.feature}>
            <div className={styles.featureIcon}>📝</div>
            <h3 className={styles.featureTitle}>Crea Playlists</h3>
            <p className={styles.featureDescription}>
              Organiza tu música en colecciones temáticas y compártelas con otros usuarios
            </p>
          </div>

          {/* Característica 3: Compartir globalmente */}
          <div className={styles.feature}>
            <div className={styles.featureIcon}>🌍</div>
            <h3 className={styles.featureTitle}>Comparte Globalmente</h3>
            <p className={styles.featureDescription}>
              Haz que tu contenido sea público para que otros puedan descubrir tu música
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
