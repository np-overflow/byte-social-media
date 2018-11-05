import React from "react"

import styles from "./mediaImage.css"

const MediaImage = props => (
    <img className={styles.image} src={props.src} />
)

export default MediaImage