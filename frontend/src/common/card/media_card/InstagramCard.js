import React from "react"
import invariant from "invariant"

import { INSTAGRAM_SRC, INSTAGRAM_BG_COLOR } from "../../../settings"
import ResponsiveCard from "../ResponsiveCard"

const InstagramCard = props => {
    invariant(props.author, "InstagramCard should have an author")

    return (
        <ResponsiveCard iconSrc={INSTAGRAM_SRC} titleBgColor={INSTAGRAM_BG_COLOR}
              titleBright title={props.author}>
            {props.children}
        </ResponsiveCard>
    )
}

export default InstagramCard