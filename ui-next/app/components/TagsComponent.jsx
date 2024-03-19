import styles from '../../convostyles.module.scss'

function TagsComponent ({keys}) {

    function runyhiig(){
        console.log("this is from child function")
    }

    return <div className={styles.tagsComponentDiv}> 
        {keys.map((input, index)=>{
            return <div key={index} className={styles.tags}>
                  <span onClick={runyhiig} htmlFor={`${"checkTag"}` + index } key ={index}>{input}</span>
            </div> 
        })}
     </div>
}

export default TagsComponent;