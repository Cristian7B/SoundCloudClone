import styles from "../Styles/ListHistory.module.css";

/**
 * Componente para mostrar el historial de reproducción del usuario.
 * 
 * Este componente renderiza una lista cronológica de elementos del historial,
 * mostrando el título y la fecha de cada elemento reproducido. Es útil para
 * que los usuarios puedan revisar su actividad musical reciente.
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Array<Object>} props.history - Array de elementos del historial
 * @param {string} props.history[].title - Título del elemento reproducido
 * @param {string} props.history[].date - Fecha de reproducción
 * 
 * @example
 * // Uso básico del componente
 * const historyData = [
 *   { title: "Canción 1", date: "2025-01-10" },
 *   { title: "Playlist Mix", date: "2025-01-09" }
 * ];
 * 
 * return (
 *   <ListHistory history={historyData} />
 * );
 * 
 * @example
 * // Integración en sidebar o panel lateral
 * function UserSidebar({ userHistory }) {
 *   return (
 *     <aside>
 *       <UserProfile />
 *       <ListHistory history={userHistory} />
 *       <RecentPlaylists />
 *     </aside>
 *   );
 * }
 * 
 * @returns {JSX.Element} Elemento JSX con la lista del historial
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function ListHistory({ history }) {
    /**
     * Renderiza la estructura del historial.
     * 
     * Incluye:
     * - Título de la sección
     * - Lista de elementos del historial con título y fecha
     * - Manejo de arrays vacíos
     */
    return (
        <div className={styles.listHistory}>
            <h2>History</h2>
            <ul>
                {history.map((item, index) => (
                    <li key={index} className={styles.historyItem}>
                        <span className={styles.historyTitle}>{item.title}</span>
                        <span className={styles.historyDate}>{item.date}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}