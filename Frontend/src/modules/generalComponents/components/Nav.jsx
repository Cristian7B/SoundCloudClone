import styles from '../Styles/Nav.module.css';
import notification from "../assets/notifications.svg";
import messages from "../assets/message.svg";
import menu from "../assets/menu.svg";
import { SearchBar } from './SearchBar';
import { UserMenu } from '../../user';
import { useNavigation } from '../../Routes/hooks/useNavigation';
import { UploadButtons } from '../../upload';

/**
 * Componente de navegación principal de la aplicación.
 * 
 * Este componente proporciona la barra de navegación superior que incluye:
 * - Logo y navegación principal
 * - Barra de búsqueda integrada
 * - Menú de usuario y autenticación
 * - Botones de upload y acciones
 * - Navegación responsive
 * 
 * @component
 * 
 * @example
 * // Uso en el layout principal de la aplicación
 * function Layout({ children }) {
 *   return (
 *     <div>
 *       <Nav />
 *       <main>{children}</main>
 *       <Footer />
 *     </div>
 *   );
 * }
 * 
 * @example
 * // Uso con contexto de navegación
 * function App() {
 *   return (
 *     <NavigationProvider>
 *       <Nav />
 *       <AppRoutes />
 *     </NavigationProvider>
 *   );
 * }
 * 
 * @returns {JSX.Element} Elemento JSX de la barra de navegación
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function Nav() {
    /**
     * Hook de navegación que proporciona funciones para navegar
     * entre diferentes rutas y verificar la ruta activa.
     * 
     * @type {Object}
     * @property {Function} navigateToHome - Navega a la página principal
     * @property {Function} navigateToLibrary - Navega a la biblioteca
     * @property {Function} isActiveRoute - Verifica si una ruta está activa
     */
    const { navigateToHome, navigateToLibrary, isActiveRoute } = useNavigation();

    /**
     * Estructura JSX de la barra de navegación.
     * 
     * Organizada en tres secciones principales:
     * 1. Sección izquierda - Logo y menú principal
     * 2. Sección central - Barra de búsqueda
     * 3. Sección derecha - Enlaces, usuario y botones de acción
     */
    return (
        <nav className={styles.nav}>
            {/* Sección izquierda: Logo y navegación principal */}
            <div className={styles.leftSection}>
                <div 
                    className={styles.logo} 
                    onClick={navigateToHome}
                    role="button"
                    tabIndex={0}
                    aria-label="Ir a página principal"
                >
                    <img 
                        className={styles.img} 
                        src="/public/logo.svg" 
                        alt="Icono de SoundCloud" 
                    />
                </div>
                <ul className={styles.menu}>
                    <li 
                        className={isActiveRoute('/home') ? styles.active : ''}
                        onClick={navigateToHome}
                        role="button"
                        tabIndex={0}
                        aria-label="Navegar a Home"
                    >
                        Home
                    </li>
                    <li 
                        className={isActiveRoute('/library') ? styles.active : ''}
                        onClick={navigateToLibrary}
                        role="button"
                        tabIndex={0}
                        aria-label="Navegar a Library"
                    >
                        Library
                    </li>
                </ul>
            </div>

            {/* Sección central: Barra de búsqueda */}
            <SearchBar />

            {/* Sección derecha: Enlaces, usuario y acciones */}
            <div className={styles.rightSection}>
                <a href="#" className={styles.proLink}>Try Artist Pro</a>
                
                {/* Componente de autenticación y menú de usuario */}
                <UserMenu />
                
                {/* Botones de upload integrados */}
                <section className={styles.buttonsSection}>
                    <UploadButtons/>
                </section>
            </div>
        </nav>
    );
}
