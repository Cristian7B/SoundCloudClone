import styles from '../Styles/ArtistTools.module.css';
import { iconosArtistas } from '../utils/const';
import { SquareTool } from './SquareTool';
import mas from '../assets/mas.svg';
export function ArtistTools() {
    return (
        <article className={styles.artistTools}>
            <div className={styles.artistToolsContainerTop}>
                <h3>HERRAMIENTAS DE ARTISTAS</h3>
                <hr />
            </div>
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
            <div className={styles.artistToolsContainerBottom}>
                <img src={mas} alt="Mas ícono" />
                <p>Obtén herramientas de Artist de 6800 COP/mes</p>
            </div>
        </article>
    );
}