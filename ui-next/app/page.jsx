import styles from "./page.module.scss";
import DragDropAnalysis from "./components/Drag&Drop";
// import Card, { DraggableCardWrapper } from './components/Drag&Drop'
import Navbar from "./components/navbar";

export default function Home() {
  return (
    <div className={styles.parentContainer}>

      <Navbar/>

      <main className={styles.main}>

        <div>
          <h1>Are you exhausted with lengthy documents?</h1>
          <h1>ENIGMA can help you!</h1>
        </div>

        <DragDropAnalysis/> {/* componenet containing drag & drop functionality */}

        {/* <Link className={styles.link} href="/conversation">
          <button id={styles.analysisbutton}>Analysis Results</button>
        </Link> */}

      </main>

    </div>
  );
}