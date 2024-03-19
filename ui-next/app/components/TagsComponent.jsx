import styles from '../../convostyles.module.scss'


function TagsComponent ({keys}) {
    return <div className={styles.tagsComponentDiv}> 
        {keys.map((input, index)=>{
            return <div key={index} className={styles.tags}>
                  <input style={{display:"none"}} className={styles.qw} id={`${"checkTag"}` + index } type="checkbox"/>
                  <label onClick={(e)=>updateCheckBoxes(e)} htmlFor={`${"checkTag"}` + index } key ={index}>{input}</label>
            </div> 
        })}
     </div>
}

export default TagsComponent;