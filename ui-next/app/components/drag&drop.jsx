'use client'
import { useState, useEffect, useRef } from "react";
import styles from '../page.module.scss';
import { useRouter } from "next/navigation";

// import setFileAvailibility from './setFileState'

const DragDropFiles = () => {
  const [files, setFiles] = useState(null);
  const [fileAvailibility, setFileAvailibility] = useState("file not available")
  const router = useRouter();
  const inputRef = useRef();

  const DragOver = (event) => {
    event.preventDefault();
  };

  const Drop = (event) => {
    event.preventDefault();
    setFiles(event.dataTransfer.files)
  };
  
  const Upload = async () => {
    if(fileAvailibility == null){
      alert("Please select a file...")
    }else{

      const formData = new FormData();
      formData.append("file", files[0]);
  
      try{
        const response = await fetch("http://localhost:8000/summarize/pdf", {
          method: "POST",
          body: formData
        })  

        if (!response.ok) {
          throw new Error(`Error uploading file `, error);
        }

        const result = await response.json();
        window.sessionStorage.setItem("summary_response", JSON.stringify(result));
        router.push("/conversation");

      }catch (error) {
        console.error('Error:', error);
      }finally {
        setFiles(null)
      }
    }
  };

  useEffect(()=>{
    files == null ? setFileAvailibility(null) : setFileAvailibility(files[0].name)
  },[files])

  if (files) return (
    <div className={styles.dragdropContainer}>
      <div className={styles.card}>
        <h4>{files[0].name}</h4>      
        <button className={styles.selectFileBtn} onClick={() => setFiles(null)}>Cancel</button>
      </div>

      {/* <Link className={styles.link} href="/conversation"> */}
        <button onClick={()=>Upload()} id={styles.analysisbutton}>Analysis Results</button>
      {/* </Link> */}


    </div>
            
  )

  return (
    <div className={styles.dragdropContainer}>
        <div 
          className={styles.card}
          onDragOver={DragOver}
          onDrop={Drop}
        >
          <div className={styles.dragAndDrop}>
            <img className={styles.uploadLogo} src="/img/uploadLogo.png" alt="uploadLogo" />
            <h1>Drag & Drop document</h1>
          </div>

          <div className={styles.or}>
            <p style={{color:"#999", fontSize:"27px", fontWeight:"200"}}>--------------<span style={{fontWeight:"500"}}>&nbsp; or &nbsp; </span>--------------</p> 
          </div>

          <div className={styles.selectFileContainer}>
            <label htmlFor="upload-file">
                <button className={styles.selectFileBtn} onClick={() => inputRef.current.click()}>Select file</button>
                <input 
                  onChange={(event) => setFiles(event.target.files)}
                  hidden   
                  ref={inputRef}
                  type="file" 
                  id="upload-file"
                  accept=".pdf,.doc,.docx"
                  style={{display:"none"}}/>
            </label>
          </div> 

        </div>

        {/* <Link className={styles.link} href="/conversation"> */}
          <button onClick={()=>Upload()} id={styles.analysisbutton}>Analysis Results</button>
        {/* </Link> */}

    </div>
  );
};

export default DragDropFiles;

