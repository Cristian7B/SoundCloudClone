import styles from "../Styles/SquareTool.module.css";
import mas from "../assets/masSquare.svg";
export function SquareTool({icon, title}) {
    return (
        <div className={styles.squareTool}>
            <img src={icon} alt={title} className={styles.icon} />
            <img src={mas} alt={title} className={styles.iconMas} />
            <h5>{title}</h5>
        </div>
    );
}   