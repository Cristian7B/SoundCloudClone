import styles from "../Styles/ListHistory.module.css";
export function ListHistory({ history }) {
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