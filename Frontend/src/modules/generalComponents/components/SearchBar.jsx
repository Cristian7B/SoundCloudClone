import styles from "../Styles/SearchBar.module.css";
import iconoBuscar from "../assets/search.svg"; 
export function SearchBar() {
    return (
        <div className={styles.centerSection}>
            <input
                type="text"
                placeholder="Search"
                className={styles.searchInput}
            />
            <button className={styles.searchButton}>
                <img src={iconoBuscar} alt="Buscar logo" />
            </button>
        </div>
    );
}