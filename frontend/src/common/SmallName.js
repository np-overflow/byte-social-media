import React from "react"

import styles from "./smallName.css"

const SmallName = props => {
    let textStyle;
    if (props.bright) {
        textStyle = styles.bright
    } else if (props.dark) {
        textStyle = styles.dark
    } else {
        textStyle = ""
    }

    return <p className={textStyle}>{props.children}</p>
}

export default SmallName