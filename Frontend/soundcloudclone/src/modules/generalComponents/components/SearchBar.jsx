import styles from "../Styles/SearchBar.module.css";
export function SearchBar() {
    return (
        <div className={styles.searchBar}>
            <input
                type="text"
                placeholder="Search..."
                className={styles.searchInput}
            />
            <button className={styles.searchButton}>Search</button>
        </div>
    );
}