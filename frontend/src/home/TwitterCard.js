import React from "react"
import invariant from "invariant"

import { TWITTER_SRC, TWITTER_BG_COLOR } from "../settings"
import Card from "../common/Card"

const TwitterCard = props => {
    invariant(props.author, "TwitterCard should have an author")

    return (
        <Card iconSrc={TWITTER_SRC} titleBgColor={TWITTER_BG_COLOR}
              titleBright title={props.author}>
            {props.children}
        </Card>
    )
}

export default TwitterCard