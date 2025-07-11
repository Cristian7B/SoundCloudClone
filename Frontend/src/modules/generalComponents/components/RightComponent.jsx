/**
 * @fileoverview Componente lateral derecho que proporciona información adicional
 * o funcionalidades secundarias en el layout de la aplicación.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import styles from "../Styles/RightComponent.module.css";

/**
 * Componente que renderiza el panel lateral derecho de la aplicación
 * @component
 * @returns {JSX.Element} Panel lateral derecho
 * 
 * @example
 * <RightComponent />
 */
export function RightComponent() {
    return (
        <div className={styles.rightComponent}>
            <h2>Right Component</h2>
        </div>
    );
}
