import React from "react"
import invariant from "invariant"

import { TWITTER_SRC, TWITTER_BG_COLOR } from "../../../settings"
import ResponsiveCard from "../ResponsiveCard"

const TwitterCard = props => {
    invariant(props.author, "TwitterCard should have an author")

    return (
        <ResponsiveCard iconSrc={TWITTER_SRC} titleBgColor={TWITTER_BG_COLOR}
              titleBright title={props.author}>
            {props.children}
        </ResponsiveCard>
    )
}

export default TwitterCard