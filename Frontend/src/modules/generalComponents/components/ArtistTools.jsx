/**
 * @fileoverview Componente que muestra las herramientas disponibles para artistas
 * con información de precios y funcionalidades.
 * 
 * @author SoundCloud Clone Team
 * @since 1.0.0
 */

import styles from '../Styles/ArtistTools.module.css';
import { iconosArtistas } from '../utils/const';
import { SquareTool } from './SquareTool';
import mas from '../assets/mas.svg';

/**
 * Componente que renderiza un panel con las herramientas disponibles para artistas
 * @component
 * @returns {JSX.Element} Panel de herramientas para artistas
 * 
 * @example
 * <ArtistTools />
 */
export function ArtistTools() {
    return (
        <article className={styles.artistTools}>
            {/* Encabezado del panel */}
            <div className={styles.artistToolsContainerTop}>
                <h3>HERRAMIENTAS DE ARTISTAS</h3>
                <hr />
            </div>
            
            {/* Grid de herramientas disponibles */}
            <div className={styles.artistToolsContainerCenter}>
                {
                    iconosArtistas.map(({ icon, title }) => (
                        <SquareTool
                            key={title}
                            icon={icon}
                            title={title}
                        />
                    ))
                }
            </div>
            
            {/* Información de precios y call-to-action */}
            <div className={styles.artistToolsContainerBottom}>
                <img src={mas} alt="Mas ícono" />
                <p>Obtén herramientas de Artist de 6800 COP/mes</p>
            </div>
        </article>
    );
}