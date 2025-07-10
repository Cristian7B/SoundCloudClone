import styles from "../Styles/Home.module.css";
import { Artist } from "./Artist";
import { BlockBuster } from "./BlockBuster";
import { Mixes } from "./Mixes";
export function Home() {
    return (
        <div className={styles.homeContainer}>
            <BlockBuster />
            <Artist />
            <Mixes />
        </div>
    );
}