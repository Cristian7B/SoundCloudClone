/**
 * @fileoverview Componente de herramienta cuadrada que muestra un icono y título
 * para las herramientas de artistas disponibles.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import styles from "../Styles/SquareTool.module.css";
import mas from "../assets/masSquare.svg";

/**
 * Componente que renderiza una herramienta individual en formato cuadrado
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {string} props.icon - URL del icono de la herramienta
 * @param {string} props.title - Título descriptivo de la herramienta
 * @returns {JSX.Element} Tarjeta cuadrada de herramienta
 * 
 * @example
 * <SquareTool
 *   icon="/icono-amplificar.svg"
 *   title="Amplificar"
 * />
 */
export function SquareTool({icon, title}) {
    return (
        <div className={styles.squareTool}>
            {/* Icono principal de la herramienta */}
            <img src={icon} alt={title} className={styles.icon} />
            
            {/* Icono "más" para indicar funcionalidad adicional */}
            <img src={mas} alt={`Más sobre ${title}`} className={styles.iconMas} />
            
            {/* Título de la herramienta */}
            <h5>{title}</h5>
        </div>
    );
}   