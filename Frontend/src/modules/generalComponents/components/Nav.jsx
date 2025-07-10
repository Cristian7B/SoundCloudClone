import styles from '../Styles/Nav.module.css';
import drop from "../assets/dropdown.svg"
import notification from "../assets/notifications.svg"
import messages from "../assets/message.svg"
import menu from "../assets/menu.svg";
import { SearchBar } from './SearchBar';
export function Nav() {
    return (
        <nav className={styles.nav}>
            <div className={styles.leftSection}>
                <div className={styles.logo}>
                    <img className={styles.img} src="/public/logo.svg" alt="Icono de SoundCloud" />
                </div>
                <ul className={styles.menu}>
                    <li>Home</li>
                    <li>Feed</li>
                    <li>Library</li>
                </ul>
            </div>

            <SearchBar />

            <div className={styles.rightSection}>
                <a href="#" className={styles.proLink}>Try Artist Pro</a>
                <a href="#">Upload</a>
                <div className={styles.profileCircle}>
                    <img className={styles.img} src="" alt="" />
                    <img className={styles.img} src={drop} alt="Dropdown icon" />
                </div>
                <section className={styles.buttonsSection}>
                    <button className={styles.notificationButton}>
                        <img className={styles.img}  src={notification} alt="Notification icon" />
                    </button>
                    <button className={styles.messagesButton}>
                        <img className={styles.img} src={messages} alt="Dropdown icon" />
                    </button>
                    <button className={styles.menuButton}>
                        <img className={styles.img} src={menu} alt="Menu icon" />
                    </button>
                </section>
            </div>
        </nav>
    );
}
