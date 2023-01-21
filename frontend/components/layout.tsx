import styles from './layout.module.css';

type LayourProps = React.PropsWithChildren<{}>;

export default function Layout({ children }: LayourProps) {
  return <div className={styles.container}>{children}</div>;
}
