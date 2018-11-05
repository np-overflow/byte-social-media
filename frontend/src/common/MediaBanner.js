import React from "react"
import invariant from "invariant"

import styles from "./mediaBanner.css"
import SmallName from "./SmallName"

const MediaBanner = props => {
    invariant(props.iconSrc, "MediaBanner should have an iconSrc prop")
    invariant(props.bgColor, "MediaBanner should have a bgColor prop")

    let smallNameProps = {
        bright: props.bright,
        dark: props.dark
    }

    return (
        <div style={{ backgroundColor: props.bgColor }}
            className="container-fluid p-1 d-flex flex-row align-items-center">
            <img className={styles.icon + " p-1 pr-2"}
                 srcSet={props.iconSrcSet}
                 src={props.iconSrc}
                 sizes={props.iconSizes} />
            <SmallName {...smallNameProps}>{props.children}</SmallName>
        </div>
    )
}

export default MediaBanner