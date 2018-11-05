import React from "react"
import invariant from "invariant"

import styles from "./card.css"
import MediaBanner from "./MediaBanner";

const Card = props => {
    invariant(props.children.length === 2, "Card should have 2 children elements")
    invariant(props.iconSrc, "Card should have an iconSrc prop")

    const mediaBannerProps = {
        bright: props.titleBright,
        dark: props.titleDark,
        bgColor: props.titleBgColor,
        iconSrc: props.iconSrc,
        iconSizes: props.iconSizes,
        iconSrcSet: props.iconSrcSet
    }

    return (
        <div className={styles['card-container'] + " pb-2"}>
            <MediaBanner {...mediaBannerProps}>
                {props.title}
            </MediaBanner>
            {props.children}
        </div>
    )
}

export default Card