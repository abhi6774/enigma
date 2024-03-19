import styles from '../page.module.scss'
import Image from 'next/image'

export default function Navbar(){
    return <nav className={styles.nav}>
      <Image
        className={styles.enigmaLogo}
        src="/img/enigmalogo.png"
        width={275}
        height={65} 
        alt="enigmaIcon"
        />
    {/* <h1 className={styles.enigma}>ENIGMA</h1>
    <h1 className={styles.enigma2}>ENIGMA</h1> */}
  </nav>
}