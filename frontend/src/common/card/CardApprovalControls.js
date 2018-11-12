import React from "react"

import styles from "./cardApprovalControls.css"

const CardApprovalControls = props => (
    <div className={styles.container}>
        <button className={`${styles.button} ${styles.tick}`} onClick={props.approveHandler}>✓</button>
        <button className={`${styles.button} ${styles.cross}`} onClick={props.rejectHandler}>✖</button>
    </div>
)

export default CardApprovalControls