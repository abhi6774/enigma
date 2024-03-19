'use client'
import { useState, useEffect, useRef } from "react";
import styles from '../page.module.scss';
import { useRouter } from "next/navigation";

// import setFileAvailibility from './setFileState'

const DragDropFiles = () => {
  const [files, setFiles] = useState(null);
  const [fileAvailibility, setFileAvailibility] = useState("file not available")
  const [fetchingPDF, setfetchingPDF] = useState(false)
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
      
      setfetchingPDF(true)
      console.log(fetchingPDF)

      try{
        const response = await fetch("http://192.168.200.169:8000/summarize/pdf", {
          method: "POST",
          body: formData
        })  

        if (!response.ok) {
          throw new Error(`Error uploading file `, error);
        }

        const result = await response.json();
        console.log(result["session_id"]);

        router.push(`/conversation/${result["session_id"]}`);

      }catch (error) {
        console.error('Error:', error);
      }finally {
        setFiles(null)
      }


      
    // try{
    //   const response = await fetch("http://13.48.136.54:8000/api/api-code/", {
    //     method: "POST",
    //     headers: {
    //       Authorization: "Bearer f25538be-ee8d-4cd0-bcfe-f76c0173487e"
    //     }
    //   })  

    //   if (!response.ok) {
    //     throw new Error(`Error fetching code `, error);
    //   }

    //   const result = await response.json();
    //   console.log(result);

    //   router.push(`/conversation/${result["session_id"]}`);

    // }catch (error) {
    //   console.error('Error:', error);
    // }finally {
    //   setFiles(null)
    // }

//       f25538be-ee8d-4cd0-bcfe-f76c0173487e

      // Each team must integrate the provided API into their project.
      // The above Access key must be passed in the Authorization header of the API request in the format "Bearer <access_key>".
      // Use the POST method for the specified API URL: http://13.48.136.54:8000/api/api-code/.

    }
  };

  useEffect(()=>{
    files == null ? setFileAvailibility(null) : setFileAvailibility(files[0].name)
  },[files])

  if (files)    
  return (
    <div className={styles.dragdropContainer}>
      <div className={styles.card}>
        <h4>{files[0].name}</h4>      
        <button className={styles.selectFileBtn} onClick={() => setFiles(null)}>Cancel</button>
      </div>

     {fetchingPDF ?  <button onClick={()=>Upload()} id={styles.analysisbutton} className={styles.analysisbutton2} >Analysis Results <div className={styles.loadingContainer}></div></button> : <button onClick={()=>Upload()} id={styles.analysisbutton}>Analysis Results</button>}
      
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
                  accept=".pdf"
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

