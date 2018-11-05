import React from "react"
import invariant from "invariant"

import { FACEBOOK_SRC, FACEBOOK_BG_COLOR } from "../settings"
import Card from "../common/Card";

const FacebookCard = props => {
    invariant(props.author, "FacebookCard should have an author prop")

    return (
        <Card iconSrc={FACEBOOK_SRC} titleBgColor={FACEBOOK_BG_COLOR}
              titleBright title={props.author}>
            {props.children}
        </Card>
    )
}

export default FacebookCard