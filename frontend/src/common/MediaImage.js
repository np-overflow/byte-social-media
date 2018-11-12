import React from "react"
import invariant from "invariant"

import styles from "./mediaImage.css"

const MediaImage = props => {
    invariant(props.src, "MediaImage should have a src prop")

    return <img className={styles.image} src={props.src} />
}

export default MediaImage