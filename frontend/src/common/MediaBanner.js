import React from "react"

import styles from "./mediaBanner.css"
import SmallName from "./SmallName"

const MediaBanner = props => {
    let smallNameProps = {
        bright: props.bright,
        dark: props.dark
    }

    return (
        <div style={{ backgroundColor: props.bgColor }}
            className="container-fluid p-1 d-flex flex-row align-items-center">
            <img className={styles.icon + " p-1 pr-2"} src={props.iconSrc} />
            <SmallName {...smallNameProps}>{props.children}</SmallName>
        </div>
    )
}

export default MediaBanner