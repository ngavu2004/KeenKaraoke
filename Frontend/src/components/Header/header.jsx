import styles from './header.module.css'

export const Header = () => {
    return (
        <div>
            <nav className={styles.header}>
                <h1 className={styles.title}>KeenKaroke</h1>
            </nav>
        </div>
    );
}